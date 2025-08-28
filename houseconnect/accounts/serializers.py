from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=250)
    role = serializers.CharField(max_length=100)

    def validate(self, data):
        """ validate and return user password """

        # Check against using username as password
        if data["username"].lower() in data["password"]:
            raise serializers.ValidationError("Password can't be your username")
        
        # Check against password being all numeric
        if data["password"].isdigit():
            raise serializers.ValidationError("Password Can't be entirely numeric")
        
        return data

    def validate_role(self, value):
        """ validate role to only allow house owners and tenants """
        ALLOWED_ROLE = ["Owner", "Tenant"]
        if value not in ALLOWED_ROLE:
            raise serializers.ValidationError(f"Roles allowed {ALLOWED_ROLE}")
        return value
    
    def validate_username(self, value):
        " Validate and  return username"
        users = User
        # validate against having duplicate users with the same username
        if users.objects.filter(username=value):
            raise serializers.ValidationError("User with this username already exists")
        return value
    
    def create(self, validated_data):
        """ Create a new user with validated data"""
        user = User.objects.create_user(
            email= validated_data["email"],
            username= validated_data["username"],
            password= validated_data["password"],
            role = validated_data["role"]
            )
        return user
    
    def validate_email(self, value):
        """ Validate and return email"""

        if User.objects.filter(email=value):
            raise serializers.ValidationError(f"User with this {value} already exists")
        
        return value
    


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    role = serializers.ReadOnlyField(source="user.role")
    class Meta:
        model = Profile
        fields = ["id", "user", "phone_number", "address", "profile_picture", "role"]


class UserOutputSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role"]
        