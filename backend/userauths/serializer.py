from rest_framework import serializers
from userauths.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta:
        """
        Meta class specifying the model and fields for serialization
        """
        model = User
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model
    """   
    class Meta:
        """
        Meta class specifying the model and field for serialization
        """
        model = Profile
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        Custom the serialized representation of a profile object to 
        include nested User data
        """
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response