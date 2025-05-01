# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status


class OTPRequiredView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        device, created = TOTPDevice.objects.get_or_create(user=user, name="default")

        # OTP yuborish
        if not device.is_valid():
            device.generate_challenge()

        # OTP yuborilganini bildiruvchi javob
        return Response({"message": "OTP yuborildi"}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        device = TOTPDevice.objects.get(user=user)

        # OTPni tekshirish
        otp_code = request.data.get('otp_code')  # foydalanuvchidan OTPni olish
        if device.verify_token(otp_code):
            return Response({"message": "OTP tasdiqlandi"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "OTP xato"}, status=status.HTTP_400_BAD_REQUEST)
