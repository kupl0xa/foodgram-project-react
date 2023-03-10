from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель для тэгов"""
    name = models.CharField(max_length=150, blank=False)
    color = ColorField(blank=False)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингредиентов"""
    name = models.CharField(max_length=150, blank=False)
    measurement_unit = models.CharField(max_length=15, blank=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def favorite(self, user, id=None):
        if id:
            return self.filter(favorites__user=user, id=id)
        return self.filter(favorites__user=user)

    def cart(self, user, id=None):
        if id:
            return self.filter(cart__user=user, id=id)
        return self.filter(cart__user=user)


class Recipe(models.Model):
    """Модель для рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=150, blank=False)
    image = models.ImageField(
        upload_to='recipes/images',
        null=False
    )
    text = models.CharField(max_length=150, blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        blank=False
    )
    tags = models.ManyToManyField(Tag, blank=False)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Время должно быть больше нуля'
            )]
    )

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель для связи ингредиентов и рецептов"""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Количество должно быть больше нуля'
            )]
    )

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient-recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount} в {self.recipe}'


class Favorite(models.Model):
    """Модель для хранения избранных рецептов пользователя"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Изранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorites-recipe'
            )
        ]


class Cart(models.Model):
    """Модель для хранения избранных рецептов пользователя"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart-recipe'
            )
        ]
