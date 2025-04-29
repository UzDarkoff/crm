from rest_framework import serializers
from app.models.attendance_model import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):
        return Attendance.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_present = validated_data.get('is_present', instance.is_present)
        instance.save()
        return instance
