from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app import permissions
from app.models.student_model import Student
from app.paginations import StandardResultsSetPagination
from app.serializers.student_serializer import StudentSerializer
from app.permissions import IsAdminOrStaff, IsTeacherOrAdmin, IsStudent

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            # Faqat Admin yoki Staff CRUD qila oladi
            permission_classes = [IsAdminOrStaff]
        else:
            # Student faqat o‘zining ma'lumotlarini ko‘ra oladi
            permission_classes = [IsStudent]

        return [permission() for permission in permission_classes]

class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        students = Student.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
