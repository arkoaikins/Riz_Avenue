from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from userauths.models import User, Profile
from userauths.serializer import (
    MyTokenObtainPairSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)
import shortuuid
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @swagger_auto_schema(
        operation_id="token_obtain_pair",
        operation_summary="Obtain Token Pair",
        operation_description="Endpoint for obtaining access and refresh"
        "tokens for user authentication Successfully authenticated "
        "users will receive a JSON response containing both tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="Email of the  user.",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password of the user."
                ),
            },
            required=["email", "password"],
        ),
        responses={
            200: "OK - Returns the access and refresh tokens.",
            400: "Bad Request - Invalid authentication credentials.",
            401: "Unauthorized - Permission denied.",
            500: "Server Error - Internal server error.",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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

    @swagger_auto_schema(
        operation_summary="Register View",
        operation_description="Endpoint for user registration.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "full_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Full name for the new user."
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Phone number for the new user.",
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="Email address for the new user.",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password for the new user."
                ),
                "password2": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password for the new user."
                ),
            },
            required=["email", "password", "password2"],
        ),
        responses={
            201: "Created - Returns the details of the newly registered user.",
            400: "Bad Request - Invalid registration data.",
            401: "Unauthorized - Permission denied.",
            500: "Server Error - Internal server error.",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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

            link = f"http://localhost:5173/create-new-password?otp={otp}&uidb64={uidb64}"  # nopep8
            print("link =====", link)

            # Send it as an emial to user(to be completed)
        return user


class PasswordChangeApi(generics.CreateAPIView):
    """
    API view for changing the user's password

    - permission_classes is set to allow unrestricted access(for password change)   # nopep8
    - serializer_class is set to custom UserSerializer class
    """

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new password
        - Retrieves the payload from the request data
        - Extracts the 'otp', 'uidb64', and 'password' from the payload
        - Attempts to retrieve the user with the provided 'uidb64' and 'otp'
        - If the user is found, sets the new password, clears the 'otp' field, and saves the user
        -  Returns a response indicating the success or failure of the password reset   # nopep8
        """
        payload = request.data
        otp = payload["otp"]
        uidb64 = payload["uidb64"]
        password = payload["password"]

        user = User.objects.get(id=uidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response(
                {"message": "Password Reset Sucessfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "Error occured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Profile(get)
    Profile Update(put)-- updates whole filed
    Profile(patch)--- updates cetain fields
    """

    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Profile (GET)",
        operation_description="Retrieve user profile.",
        responses={
            200: openapi.Response(description="OK - Returns the user profile."),   # nopep8
            401: openapi.Response(description="Unauthorized - Permission denied."),   # nopep8
            404: openapi.Response(description="Not Found - User or profile not found."),   # nopep8
            500: openapi.Response(description="Server Error - Internal server error."),   # nopep8
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve user profile.
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Profile Update (PUT)",
        operation_description="Update user profile with complete fields.",
        responses={
            200: openapi.Response(description="OK - Returns the updated user profile."),   # nopep8
            400: openapi.Response(description="Bad Request - Invalid request body."),   # nopep8
            401: openapi.Response(description="Unauthorized - Permission denied."),   # nopep8
            404: openapi.Response(description="Not Found - User or profile not found."),   # nopep8
            500: openapi.Response(description="Server Error - Internal server error."),   # nopep8
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Update user profile with complete fields.
        """
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Profile Update (PATCH)",
        operation_description="Update user profile with specific fields.",
        responses={
            200: openapi.Response(description="OK - Returns the updated user profile."),  # nopep8
            400: openapi.Response(description="Bad Request - Invalid request body."),  # nopep8
            401: openapi.Response(description="Unauthorized - Permission denied."),  # nopep8
            404: openapi.Response(description="Not Found - User or profile not found."),  # nopep8
            500: openapi.Response(description="Server Error - Internal server error."),  # nopep8
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        Update user profile with specific fields.
        """
        return self.partial_update(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        """
        Retrieves a user's profile based on the provided user ID.

        This method is used by Django's generic views to fetch the specific
        object (profile) associated with a request. It takes advantage of
        URLconf routing where the user ID is typically captured as a keyword
        argument named 'user_id'.

        Args:
            *args: Additional positional arguments passed to the view.
            **kwargs: Keyword arguments passed to the view,including 'user_id'.

        Returns:
            The Profile object of the user specified by the 'user_id'.

        Raises:
            NotFound: If either the User or Profile object is not found.
        """
        user_id = self.kwargs["user_id"]
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            return profile
        except User.DoesNotExist:
            raise NotFound("User does not exist")
        except Profile.DoesNotExist:
            raise NotFound("Profile does not exist")
