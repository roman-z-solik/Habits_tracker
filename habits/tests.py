from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", telegram_chat_id="123456789"
        )

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Медитировать 5 минут",
            is_pleasant=True,
            duration=120,
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="07:00:00",
            action="Бегать 10 минут",
            duration=120,
            reward="Кофе",
        )
        self.assertEqual(habit.action, "Бегать 10 минут")
        self.assertFalse(habit.is_pleasant)

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки"""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Читать книгу",
            is_pleasant=True,
            reward="Не должно быть",  # Должно вызвать ошибку
            duration=120,
        )

        with self.assertRaises(Exception):
            habit.full_clean()


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", telegram_chat_id="123456789"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать 10 минут",
            "duration": 120,
            "reward": "Кофе",
        }

    def test_create_habit(self):
        response = self.client.post("/api/habits/habits/", self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Бегать 10 минут")

    def test_list_habits(self):
        Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get("/api/habits/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_public_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            duration=120,
            is_public=True,
        )

        response = self.client.get("/api/habits/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get("/api/habits/habits/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAPITest(APITestCase):
    def setUp(self):
        self.register_data = {
            "username": "newuser",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "email": "test@example.com",
        }

    def test_user_registration(self):
        response = self.client.post("/api/users/register/", self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_user_registration_password_mismatch(self):
        data = self.register_data.copy()
        data["password_confirm"] = "wrongpassword"
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
