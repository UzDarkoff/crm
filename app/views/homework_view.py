from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.homework_model import Homework
from app.serializers.homework_serializer import HomeworkSerializer
from app.permissions import IsTeacherOrAdmin, IsStudentOrAdmin

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            # O'qituvchi o'z guruhidagi talabalarga vazifa berishi mumkin
            return Homework.objects.filter(teacher__user=user)
        elif user.is_student:
            # Talaba faqat o'z vazifalarini ko'rishi mumkin
            return Homework.objects.filter(student__user=user)
        return Homework.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_teacher:
            serializer.save(teacher=user.teacher)
        else:
            serializer.save(student=user.student)
