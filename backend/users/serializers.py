from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Follow, User


class CustomUserSerializer(UserSerializer):
    """Просмотр и правка данных пользователем."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def create(self, validated_data):
        password = self.initial_data['password']
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()
