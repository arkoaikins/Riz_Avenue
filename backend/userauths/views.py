from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from userauths.models import User, Profile
from userauths.serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)
import shortuuid


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


def generate_otp():
    """
    Generates a unique 8-character OTP
    for password reset using shortuuid
    """
    uuid_key = shortuuid.uuid()
    unique_otp = uuid_key[:8]
    return unique_otp


class PasswordResetAPI(generics.RetrieveAPIView):
    """
    API view for initiating password reset

    It generatates reset otp which is sent to user to use
    to reset password

    - permission class is set to allow unrestricted acess(for password reset)
    - Serializer is set to custom UserSerializer class
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_object(self):
        """
        Fetches user object from provided email

        - It first gets the email from the URL parameters (self.kwargs).
        - Then, it tries to fetch a user with the given email.
        - If a user with the email is found, it generates a new OTP
        - The URL is then sent to the user via email.
        """
        email = self.kwargs["email"]
        user = User.objects.get(email=email)

        if user:
            user.otp = generate_otp()
            user.save()

            uidb64 = user.pk
            otp = user.otp

            link = f"http://localhost:5173/forgot-password?otp={otp}&uidb64={uidb64}"  # nopep8
            print("link =====", link)

            # Send it as an emial to user(to be done)
        return user
