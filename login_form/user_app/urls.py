from django.urls import path
from .views import users,login
urlpatterns = [
     path('users/',users),
     path('login/',login),
]