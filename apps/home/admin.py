# your_app/admin.py
from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'phone_number', 'is_admin')  # 显示字段
    list_filter = ('is_admin',)  # 过滤器
    search_fields = ('username', 'full_name', 'phone_number')

