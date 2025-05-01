from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from app import permissions
from app.models.teacher_model import Teacher
from app.serializers.teacher_serializer import TeacherSerializer
from app.permissions import IsAdminOrStaff, IsTeacherOrAdmin

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            # Faqat Admin yoki Staff CRUD qila oladi
            permission_classes = [IsAdminOrStaff]
        else:
            # Teacher o‘z guruhidagi studentlarni ko‘ra oladi
            permission_classes = [IsTeacherOrAdmin]

        return [permission() for permission in permission_classes]



class TeacherListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        teacher.delete()
        return Response({"detail": "Teacher deleted"}, status=status.HTTP_204_NO_CONTENT)
