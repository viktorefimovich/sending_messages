from django.contrib import admin
from .models import Mailing, MailingAttempt, Recipient, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "message")
    list_filter = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "status")
    list_filter = ("status",)


@admin.register(Recipient)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")
    list_filter = ("id", "email", "full_name")
    search_fields = ("email", "name", "commentary")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject")
    search_fields = (" subject", "message_text")
