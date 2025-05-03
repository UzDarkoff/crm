from datetime import timezone

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models.attendance_model import Attendance
from .models.auth_users import User
from .models.payment_model import Payment
from .models.teacher_model import Teacher
from .models.student_model import Student
from .models.group_model import *
# UserAdmin sozlamalari

class UserAdmin(BaseUserAdmin):
    # Admin panelida foydalanuvchi maydonlari qanday ko‘rinishini belgilash
    ordering = ['id']

    # Ko‘rsatiladigan maydonlar ro‘yxati
    list_display = ['phone_number', 'email', 'is_active', 'is_admin', 'is_student', 'is_teacher']

    # Foydalanuvchi yaratishda ko‘rsatiladigan maydonlar
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),  # Telefon raqam va parol
        ('Personal Info', {'fields': ('email', 'username', 'group')}),  # Shaxsiy ma'lumotlar
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_admin', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),
    # Ruxsatnomalar
    )

    # Yangi foydalanuvchi qo‘shishda ko‘rsatiladigan maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_student', 'is_teacher'),
        }),
    )

    # Qidiruv maydonlari
    search_fields = ['phone_number', 'email']

    # Filtrlash imkoniyatlari
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
    list_display = ['student', 'group', 'date', 'status']
    list_filter = ['group', 'date', 'status']
    search_fields = ['student__phone_number']

# Custom action: davomat yozuvlarini avtomatik yaratish
def create_attendance_for_group(modeladmin, request, queryset):
    today = timezone.now().date()
    for group in queryset:
        students = User.objects.filter(group=group, is_student=True)
        for student in students:
            Attendance.objects.get_or_create(
                student=student,
                group=group,
                date=today,
                defaults={'status': 'absent'}
            )

create_attendance_for_group.short_description = "Bugungi davomatni avtomatik yaratish (status: absent)"

@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'start_date', 'end_date']
    actions = [create_attendance_for_group]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'date', 'status')
    search_fields = ['student__user__phone_number']
    list_filter = ['status', 'date']

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['title', 'descriptions']
    search_fields = ['title']

@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ['title', 'descriptions']
    search_fields = ['title']

@admin.register(TableType)
class TableTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'descriptions']
    search_fields = ['title']

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'room', 'type', 'descriptions']
    list_filter = ['room', 'type']
    search_fields = ['descriptions']


# UserAdminni admin saytiga qo'shish
admin.site.register([User,Departments,Course,])
