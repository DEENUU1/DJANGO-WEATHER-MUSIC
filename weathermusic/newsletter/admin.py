from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import UserInfo


@admin.register(UserInfo)
class RegisteredUsers(ExportActionMixin,admin.ModelAdmin):
    list_display = ['email', 'localization', 'date']
    list_filter = ['localization', 'date']


