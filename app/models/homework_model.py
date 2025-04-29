from django.db import models
from .teacher_model import Teacher
from .student_model import Student
from django.utils import timezone

class Homework(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Vazifani bergan o'qituvchi
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Vazifa berilgan talaba
    subject = models.CharField(max_length=100)  # Mavzu nomi
    description = models.TextField()  # Vazifaning tavsifi
    due_date = models.DateTimeField()  # Vazifa topshirilishi kerak bo'lgan sana
    submitted_at = models.DateTimeField(null=True, blank=True)  # Vazifa topshirilgan sana
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Vazifa bahosi

    def __str__(self):
        return f"Vazifa {self.subject} - {self.student.user.phone_number}"

    def is_overdue(self):
        return timezone.now() > self.due_date and self.submitted_at is None

