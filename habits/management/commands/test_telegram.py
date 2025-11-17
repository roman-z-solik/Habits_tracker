from django.core.management.base import BaseCommand
from habits.models import Habit
from django.contrib.auth import get_user_model
from telegram.tasks import send_telegram_reminder

User = get_user_model()


class Command(BaseCommand):
    help = "Test Telegram notifications"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username to test with")

    def handle(self, *args, **options):
        username = options.get("username")

        if username:
            try:
                user = User.objects.get(username=username)
                habits = Habit.objects.filter(user=user)

                if habits.exists():
                    self.stdout.write(f"Testing Telegram for user: {username}")
                    for habit in habits:
                        send_telegram_reminder.delay(habit.id)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Sent reminder for habit: {habit.action}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No habits found for user: {username}")
                    )

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User {username} not found"))
        else:
            self.stdout.write("Please specify --username parameter")
