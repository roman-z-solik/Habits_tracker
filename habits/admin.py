from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'frequency')
    search_fields = ('action', 'place', 'user__username')
    list_editable = ('is_public',)


admin.site.site_header = "Habits Tracker Administration"
admin.site.site_title = "Habits Tracker Admin"
