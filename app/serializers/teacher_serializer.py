from rest_framework import serializers
from app.models.teacher_model import *

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_instance = User.objects.create(**user, is_teacher=True)
        teacher = Teacher.objects.create(user=user_instance, **validated_data)
        return teacher
