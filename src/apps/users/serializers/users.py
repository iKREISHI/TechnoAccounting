from rest_framework import serializers
from apps.users.models import User
from apps.university.models import UniversityUnit


class UserFullSerializer(serializers.ModelSerializer):
    university_unit = serializers.PrimaryKeyRelatedField(queryset=UniversityUnit.objects.all())

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'last_name', 'first_name', 'patronymic',
            'phone_number', 'university_unit'
        ]


class UserMiniSerializer(serializers.ModelSerializer):
    university_unit = serializers.PrimaryKeyRelatedField(queryset=UniversityUnit.objects.all())

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone_number', 'university_unit'
        ]