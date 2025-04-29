from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.register_serializer import UserRegisterSerializer

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Foydalanuvchi muvaffaqiyatli yaratildi.',
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
