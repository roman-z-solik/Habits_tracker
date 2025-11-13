from django.core.exceptions import ValidationError


def validate_habit(habit):
    """Валидация привычки согласно требованиям"""

    if habit.related_habit and habit.reward:
        raise ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение."
        )

    if habit.duration > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")

    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки могут попадать только приятные привычки."
        )

    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if habit.related_habit:
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )
