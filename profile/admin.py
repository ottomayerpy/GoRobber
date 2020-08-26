from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'level', 'experience', 'is_connection', 'admin_mode']
    # exclude = ['is_connection', 'quantity_connections']

    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)
