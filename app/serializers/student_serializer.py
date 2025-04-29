from rest_framework import serializers

from app.models.student_model import *



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # Barcha fieldlarni chiqarish
