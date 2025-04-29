from rest_framework import serializers
from app.models.homework_model import Homework

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

    def create(self, validated_data):
        return Homework.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.submitted_at = validated_data.get('submitted_at', instance.submitted_at)
        instance.save()
        return instance
