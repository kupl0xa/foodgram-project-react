from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.pagination import CustomPageNumberPagination
from api.serializers import FollowSerializer

from .models import Follow, User


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        print(id)
        user = request.user
        following = get_object_or_404(User, id=id)

        if request.method == 'POST':
            follow, created = Follow.objects.get_or_create(
                user=user, following=following)
            if not created:
                return Response(
                    {'errors': 'Автор уже добавлен в подписки'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = Follow.objects.filter(user=user, following=following)
            if follow.exists():
                follow.delete()
                return Response(status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Автора нет в подписках'},
                status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        paginate = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            paginate,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
