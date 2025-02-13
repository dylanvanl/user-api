from django.contrib.auth.hashers import make_password

from .password_validator_serializer import Password_validation_serializer
from rest_framework import serializers
from users.models import User
import re

class UserSerializer(Password_validation_serializer, serializers.ModelSerializer):
    #Ensure that the password serializer is also used when creating new instance
    class Meta(object):
        model = User
        fields = ['password','username','email']
        extra_kwargs = {
            'password': {'write_only':True},
        }
        
    def validate_username(self, value):
        
        # Check length
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if len(value) > 25:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        return value
    
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)