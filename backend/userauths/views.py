from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from userauths.models import User, Profile
from userauths.serializer import MyTokenObtainPairSerializer, RegisterSerializer

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

