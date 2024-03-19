from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from userauths.models import User, Profile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    A custom serializer that inherits from TokenObtainPairSerializer(provided
    by rest_framework_simplejwt) for generating JWT tokens.

    This serializer extends the defualt behaviour by including additional user
    information within the generatred token response.
    """

    @classmethod
    def get_token(cls, user):
        """
        Overrides the default get_token method to customize the token payload

        This method retrieves a token using the parent class's implementation
        (super().get_token(user)) and then adds additiional user data to the
        token payload.
        - full_name
        - email
        - username

        It inculdes user's brand_id if it is assciated with a brand,else
        brand id is set to 0
        Reaturns the enhanced token with additional information
        """
        token = super().get_token(user)

        token["full_name"] = user.full_name
        token["email"] = user.email
        token["username"] = user.username
        try:
            token["brand_id"] = user.brand.id
        except AttributeError:
            token["brand_id"] = 0

        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registeration
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Meta options for RegisterSerializer
        """

        model = User
        fields = ["full_name", "email", "password", "password2"]

    def validate(self, attrs):
        """
        Validates the password fields to ensure they match
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": "Password do not match"})
        return attrs

    def create(self, validated_data):
        """
        Creates a new user with the provided validated data
        """
        user = User.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
        )
        email_user, mobile = user.email.split("@")
        user.set_password(validate_password["password"])

        user.set_password(validate_password["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """

    class Meta:
        """
        Meta class specifying the model and fields for serialization
        """

        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model
    """

    class Meta:
        """
        Meta class specifying the model and field for serialization
        """

        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        """
        Custom the serialized representation of a profile object to
        include nested User data
        """
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response
