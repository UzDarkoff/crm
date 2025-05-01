from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from app.models.student_model import Student
from app.paginations import StandardResultsSetPagination
from datetime import datetime
from rest_framework.permissions import IsAuthenticated

class StudentStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            students_in_range = Student.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
        else:
            students_in_range = Student.objects.all()

        # Hisoblashlar — to‘g‘ridan-to‘g‘ri to‘liq querysetdan
        ongoing_students_count = students_in_range.filter(status='ongoing').count()
        graduated_students_count = students_in_range.filter(status='graduated').count()
        total_students_count = students_in_range.count()

        # Faqatgina student listini paginate qilish
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(students_in_range, request)

        return paginator.get_paginated_response({
            'total': total_students_count,
            'ongoing': ongoing_students_count,
            'graduated': graduated_students_count,
            'students': [student.id for student in result_page]  # yoki serializer orqali qaytarishingiz mumkin
        })
