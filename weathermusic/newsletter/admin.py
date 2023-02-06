from django.contrib import admin
from .models import UserInfo
from import_export.admin import ExportActionMixin


@admin.register(UserInfo)
class RegisteredUsers(ExportActionMixin,admin.ModelAdmin):
    list_display = ['email', 'localization', 'date']
    list_filter = ['localization', 'date']


