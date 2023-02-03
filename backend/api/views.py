import io
import os

from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    MiniRecipeSerializer,
    RecipeSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)

    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe)
            if not created:
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепта нет в избранном'},
                status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            cart, created = Cart.objects.get_or_create(
                user=user, recipe=recipe)
            if not created:
                return Response(
                    {'errors': 'Рецепт уже добавлен в корзину'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            cart = Cart.objects.filter(user=user, recipe=recipe)
            if cart.exists():
                cart.delete()
                return Response(status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепта нет в корзине'},
                status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount')
        buy_list = dict()
        for ingredient in ingredients:
            if ingredient[0] not in buy_list:
                buy_list[ingredient[0]] = {
                    'measurement_unit': ingredient[1],
                    'amount': ingredient[2]
                }
            else:
                buy_list[ingredient[0]]['amount'] += ingredient[2]
        
        pdfmetrics.registerFont(
            TTFont(
                'DejaVuSerif',
                os.path.dirname(os.path.abspath(__file__))+'/DejaVuSerif.ttf',
                'UTF-8'
                )
            )
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, bottomup=0)
        p.setFont('DejaVuSerif', 14)
        p.drawString(100, 100, "Список покупок:")
        p.setFont('DejaVuSerif', 12)
        height = 115
        width = 100
        print(buy_list)
        for name, data in buy_list.items():
            p.drawString(
                x=width,
                y=height,
                text=f'{name} ({data["measurement_unit"]}) - {data["amount"]}'
            )
            height += 15                 
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='list.pdf')
