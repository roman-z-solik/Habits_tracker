from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="""
        API для трекера полезных привычек по книге "Атомные привычки".

        ## Особенности:
        - JWT аутентификация
        - Валидация привычек согласно правилам книги
        - Telegram уведомления
        - Публичные привычки

        ## Эндпоинты требующие авторизации:
        - Все эндпоинты /api/habits/
        - /api/users/profile/

        ## Публичные эндпоинты:
        - /api/users/register/
        - /api/token/
        - /api/habits/habits/public/
        """,
        contact=openapi.Contact(email="admin@habittracker.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def health_check(request):
    return JsonResponse({"status": "healthy", "service": "Habit Tracker API"})


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/habits/", include("habits.urls")),
    path("api/users/", include("users.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

admin.site.site_header = "Панель управления Habits Tracker"
admin.site.site_title = "Habits Tracker Admin"
admin.site.index_title = "Добро пожаловать в панель управления"
