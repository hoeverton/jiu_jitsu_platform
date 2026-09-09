from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "username",
        "email",
        "telefone",
        "tipo_usuario",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "tipo_usuario",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "telefone",
    )

    ordering = (
        "-date_joined",
    )