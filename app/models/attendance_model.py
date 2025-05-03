from django.db import models

from app.models import User, GroupStudent


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Keldi'),
        ('late', 'Kechikdi'),
        ('absent', 'Kelmagan'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    class Meta:
        unique_together = ('student', 'group', 'date')  # Bir kunga bitta yozuv bo‘lsin
