from django.shortcuts import render
from rest_framework.views import APIView
from .serializers.common import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

import jwt

User = get_user_model()

class AllUsers(APIView):
  


  def get(self, request):
    
    users = User.objects.all()
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
class OneUser(APIView):
  
  http_method_names = ['get']

  permission_classes = (IsAuthenticated,)

  def get_user(self, id):
    try:
      return User.objects.get(id=id)
    except User.DoesNotExist:
      raise PermissionDenied(detail='Invalid credentials.')
      
  def get(self, request):
    
    user = self.get_user(request.user.id)
    
    return Response({
      'success': True,
      'user': model_to_dict(user)
    }, status=status.HTTP_200_OK)
    
class Register(APIView):

  def post(self, request):
    user = UserSerializer(data=request.data)
    if user.is_valid():
      user.save()
      return Response({
        'message': 'Register successful.'
      }, status=status.HTTP_201_CREATED)

    return Response(user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class Update(APIView):
  http_method_names = ['put']

  permission_classes = (IsAuthenticated,)


  def get_user(self, id):
    try:
      return User.objects.get(id=id)
    except User.DoesNotExist:
      raise PermissionDenied(detail='Invalid credentials.')

  def put(self, request):
    
    serializer = UserSerializer(request.user, data=request.data)
    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class Login(APIView):
  http_method_names = ['post']

  def get_user(self, email):
    try:
      
      return User.objects.get(email=email)
    except User.DoesNotExist:
      raise PermissionDenied(detail='Invalid credentials.')


  def post(self, request):
    email = request.data.get('email')
    
    password = request.data.get('password')
    user = self.get_user(email=email)
    
    if not user.check_password(password):
      raise PermissionDenied(detail='Invalid credentials.')
    
    dt = datetime.now() + timedelta(days=7)
    token = jwt.encode(
      {'sub': user.id, 'exp': dt},
      settings.SECRET_KEY,
      algorithm='HS256'
    )
    
    return Response({
      'success': True,
      'token': token, 
      'message': f'Welcome back {user.username}'
    })

  