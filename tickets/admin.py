from django.contrib import admin
from .models import Ticket, Status


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "assigned_user",
        "assigned_group",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "note")
    list_filter = ("status", "assigned_user", "assigned_group")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
