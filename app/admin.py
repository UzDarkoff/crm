from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models.attendance_model import Attendance
from .models.auth_users import User
from .models.payment_model import Payment
from .models.teacher_model import Teacher
from .models.student_model import Student

# UserAdmin sozlamalari
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone_number', 'email', 'is_active', 'is_admin', 'is_student', 'is_teacher']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),  # Telefon raqam va parol
        ('Personal Info', {'fields': ('email', 'username', 'group')}),  # Shaxsiy ma'lumotlar
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),  # Ruxsatnomalar
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_student', 'is_teacher'),
        }),
    )
    search_fields = ['phone_number', 'email']
    list_filter = ['is_active', 'is_teacher', 'is_student']

# TeacherAdmin sozlamalari
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['group']
    list_filter = []

# StudentAdmin sozlamalari
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    search_fields = ['group']
    list_filter = ['status']  # Talabaning holatini filtr qilish

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_present', 'date')
    search_fields = ['student__user__phone_number', 'lesson__subject']
    list_filter = ['is_present', 'lesson__date']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'date', 'status')
    search_fields = ['student__user__phone_number']
    list_filter = ['status', 'date']

# UserAdminni admin saytiga qo'shish
admin.site.register(User, UserAdmin)
