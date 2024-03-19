from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from userauths.models import User, Profile
from userauths.serializer import (
    MyTokenObtainPairSerializer, RegisterSerializer)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining token pairs(access and refresh token)

    This view extends the TokenObtainPairView provided by
    rest_framework_simplejwt to use my custom serializer,
    MyTokenObtainPairSerialize, for generating the tokens

    The serializer_class attribure is set to MyTokenObtainPairSerializer
    to override the default class used by TokenObtainPairView
    """

    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    View for user registeration
    It extends the generic.CreateAPIView class from Django rest framework

    - queryset is set  to specify the model queryset for the view,which is the
    User model

    - Permission class is set to allow unrestricted acess to the registeration
    endpoint(can be acessed by both authenticated and unauthenticated users)

    - Serializer class is set to the custom RegisterSerializer class to be
    able to validate and handle registration data
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
