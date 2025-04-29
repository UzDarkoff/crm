from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.attendance_model import Attendance
from app.serializers.attendance_serializer import AttendanceSerializer
from app.permissions import IsTeacherOrAdmin

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        # Agar foydalanuvchi o'qituvchi bo'lsa, o'z guruhining talabalarining yo'qlamasini ko'rsatsin
        user = self.request.user
        if user.is_teacher:
            return Attendance.objects.filter(lesson__teacher__user=user)
        return Attendance.objects.all()  # Boshqa foydalanuvchilar uchun barcha yo'qlama qaytariladi
