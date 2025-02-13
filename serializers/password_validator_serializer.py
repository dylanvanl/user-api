from rest_framework import serializers
import re

class Password_validation_serializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        errors = []
        
        # Minimum length
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        
        # Maximum length
        if len(value) > 20:
            errors.append("Password must not exceed 20 characters.")
        
        # Uppercase, lowercase, digit, special character
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|]', value):
            errors.append("Password must contain at least one special character.")
        
        # Common passwords
        common_passwords = ['password123', '123456', 'qwerty', 'password', '123456789']
        if value in common_passwords:
            errors.append("Password is too common.")
        
        # Repeated characters
        if re.search(r'(.)\1{2,}', value):
            errors.append("Password should not contain repeated characters.")
        
        # Common patterns
        if re.search(r'(123|abc|password|qwerty)', value, re.IGNORECASE):
            errors.append("Password should not contain common patterns.")
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value