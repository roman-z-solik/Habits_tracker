from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Habit
from .validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "frequency",
            "reward",
            "duration",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate(self, data):
        instance = Habit(**data)
        if self.instance:
            for attr, value in data.items():
                setattr(self.instance, attr, value)
            instance = self.instance

        try:
            validate_habit(instance)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "frequency",
            "duration",
            "is_public",
            "created_at",
        ]
