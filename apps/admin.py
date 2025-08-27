from django.contrib import admin

from apps.models import Company, Hikvision


@admin.register(Company)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', 'telegram_id']


@admin.register(Hikvision)
class Hikvision(admin.ModelAdmin):
    list_display = ["id", 'company', 'devise_id']

    def company(self, obj):
        return obj.company.name
