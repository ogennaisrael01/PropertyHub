from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile, Avater
from django.contrib.auth.password_validation import validate_password as _validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=250)

    def validate_password(self, data):
        _validate_password(data)
        return data
     
    def validate_email(self, value):
        " Validate and  return username"
        if User.objects.filter(email=value):
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def create(self, validated_data):
        """ Create a new user with validated data"""
        user = User.objects.create_user(
            email= validated_data["email"],
            username= validated_data["username"],
            password= validated_data["password"],
            )
        return user
    
class UserOutSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "username", "role"]

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserOutSerilializer(read_only=True)
    profile_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            "profile_id", 
            "user", 
            "phone_number", 
            "address", 
            "profile_image",
            "state",
            "country",
            ]
        read_only_fields = ["profile_id", "created_at"]

    def get_profile_image(self, obj):
        avater = obj.user.avater 
        return {
                "image_url": avater.image_url if avater.image_url else None,
                "caption": avater.caption if avater.caption else None,
                "date_uploaded": avater.created_at.strftime("%d %B %Y"),
            }
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        token["username"] = user.username
        # token["email"] - user.email
 
        return token
    

class AvaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avater
        fields = ["avater_id", "image_url", "caption", "created_at"]

