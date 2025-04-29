from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from app.models.student_model import Student
from app.paginations import StandardResultsSetPagination  # Paginationni import qilish
from datetime import datetime

class StudentStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # Paginationni viewsda ishlatish

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Sanalar mavjud bo'lsa, o'sha vaqtlarga moslashtirib filtrlaymiz
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            students_in_range = Student.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
        else:
            students_in_range = Student.objects.all()

        # Pagination qo'llash
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(students_in_range, request)

        ongoing_students_count = result_page.filter(status='ongoing').count()
        graduated_students_count = result_page.filter(status='graduated').count()

        return paginator.get_paginated_response({
            'ongoing_students_count': ongoing_students_count,
            'graduated_students_count': graduated_students_count
        })
