from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="API для трекера полезных привычек",
        contact=openapi.Contact(email="admin@habittracker.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/habits/", include("habits.urls")),
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
