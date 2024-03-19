from rest_framework import serializers
from userauths.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
