from django.db import models
from .student_model import Student
from .teacher_model import Teacher
from .lesson_model import Lesson

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)  # Kelgan yoki kelmaganligini belgilaydi
    date = models.DateField(auto_now_add=True)  # Yo'qlama sanasi

    class Meta:
        unique_together = ('student', 'lesson', 'date')  # Bir dars va talaba uchun bir vaqtni belgilash

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.lesson.subject} - {self.is_present}"
