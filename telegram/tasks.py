from celery import shared_task
import requests
from django.conf import settings
from habits.models import Habit
from django.utils import timezone


@shared_task
def send_telegram_reminder(habit_id):
    try:
        from habits.models import Habit
        habit = Habit.objects.get(id=habit_id)
        user = habit.user

        if not user.telegram_chat_id:
            print(f"❌ У пользователя {user.username} не указан telegram_chat_id")
            return

        message = f"🔔 **Напоминание о привычке!**\n\n" \
                  f"📍 Место: {habit.place}\n" \
                  f"⏰ Время: {habit.time.strftime('%H:%M')}\n" \
                  f"🎯 Действие: {habit.action}\n" \
                  f"⏱️ Время на выполнение: {habit.duration} секунд"

        if habit.reward:
            message += f"\n🎁 Вознаграждение: {habit.reward}"
        elif habit.related_habit:
            message += f"\n🎁 Связанная привычка: {habit.related_habit.action}"

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': user.telegram_chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"✅ Напоминание отправлено пользователю {user.username}")

    except Exception as e:
        print(f"❌ Ошибка отправки напоминания: {e}")


@shared_task
def check_habits_for_reminders():
    """Проверяет привычки, которые нужно выполнить сейчас"""
    now = timezone.now()
    current_time = now.time()
    current_weekday = now.weekday()

    print(f"🔍 Проверка привычек в {current_time}")

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )

    for habit in habits:
        if habit.frequency == 'daily':
            send_telegram_reminder.delay(habit.id)
        elif habit.frequency == 'weekly' and current_weekday == 0:  # Понедельник
            send_telegram_reminder.delay(habit.id)

    print(f"📨 Найдено {habits.count()} привычек для напоминания")
