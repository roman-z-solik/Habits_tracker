from django.db import models
from django.conf import settings

from habits.validators import validate_habit


class Habit(models.Model):
    PERIOD_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=500, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
        verbose_name="Связанная привычка",
    )
    frequency = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        default="daily",
        verbose_name="Периодичность",
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время на выполнение (в секундах)",
        help_text="Время выполнения должно быть не больше 120 секунд",
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}: {self.action}"

    def clean(self):
        validate_habit(self)
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
