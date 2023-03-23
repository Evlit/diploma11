from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField()
    password_repeat = PasswordField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attr):
        if attr['password'] != attr['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords'})
        return attr

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginUserSerializer(serializers.ModelSerializer):
    password = PasswordField()
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed
        return user


class ProfileUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password):
        if not isinstance(self.instance, User):
            raise NotImplementedError
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is incorrect')
        return old_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance
