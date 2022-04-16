from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  passwordConfirmation = serializers.CharField(write_only=True)

  def validate(self, data):
    password = data.pop('password')
    password_confirmation = data.pop('passwordConfirmation')

    if password != password_confirmation:
      raise ValidationError(message='Passwords are not equal.')

    data['password'] = make_password(password)
    return data

  class Meta:
    model = User
    fields = '__all__'
