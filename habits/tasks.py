from celery import shared_task
from telegram.tasks import check_habits_for_reminders


@shared_task
def send_daily_reminders():
    """Ежедневная проверка привычек для напоминаний"""
    check_habits_for_reminders.delay()
    return "Daily reminders check completed"
