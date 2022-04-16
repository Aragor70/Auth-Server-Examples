from django.urls import path
from.views import Register, Login, AllUsers, Update, OneUser

urlpatterns = [
  path('', AllUsers.as_view()),
  path('users/', OneUser.as_view()),
  path('register/', Register.as_view()),
  path('login/', Login.as_view()),
  path('update/', Update.as_view())
]