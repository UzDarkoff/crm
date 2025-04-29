from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Admin foydalanuvchi uchun maxsus permission.
    """
    def has_permission(self, request, view):
        return request.user.is_admin


class IsStaff(permissions.BasePermission):
    """
    Staff foydalanuvchi uchun maxsus permission.
    """
    def has_permission(self, request, view):
        return request.user.is_staff


class IsTeacher(permissions.BasePermission):
    """
    Teacher foydalanuvchi uchun maxsus permission.
    """
    def has_permission(self, request, view):
        return request.user.is_teacher


class IsStudent(permissions.BasePermission):
    """
    Student foydalanuvchi uchun maxsus permission.
    """
    def has_permission(self, request, view):
        return request.user.is_student


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Teacher yoki Admin foydalanuvchi uchun maxsus permission.
    Teacher faqat o‘z guruhidagi studentlarni ko‘ra oladi.
    """
    def has_permission(self, request, view):
        return request.user.is_teacher or request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher:
            # Teacher o'z guruhidagi studentlarni ko‘ra oladi
            return obj.group == request.user.group
        return True


class IsAdminOrStaff(permissions.BasePermission):
    """
    Admin yoki Staff foydalanuvchi uchun permission.
    Admin va Staff Teacher va Student CRUD qilish imkoniga ega.
    """
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff

