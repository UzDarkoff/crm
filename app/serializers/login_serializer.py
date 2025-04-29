from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        # Telefon raqami va parolni tekshirish
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        return {'user': user}
