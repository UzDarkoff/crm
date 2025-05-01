from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.attendance_view import AttendanceViewSet
from .views.login_view import *
from app.views.student_view import StudentViewSet
from app.views.teacher_view import *
from rest_framework.routers import DefaultRouter

from .views.otp_view import OTPRequiredView, OTPVerifyView
from .views.payment_view import PaymentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'attendance', AttendanceViewSet)
router.register(r'payments', PaymentViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('teachers/', TeacherListCreateView.as_view(), name='teacher_list_create'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('otp/', OTPRequiredView.as_view(), name='otp_required'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
from app.views.statistics_view import StudentStatisticsView

urlpatterns += [
    path('api/students/statistics/', StudentStatisticsView.as_view(), name='student-statistics'),
]

urlpatterns += router.urls
