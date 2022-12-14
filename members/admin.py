from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from mailing.models import EmailMessage
from .models import User


@admin.action(description="Delete all user mails")
def delete_mails(modeladmin, request, queryset):
    # TODO: Is that efficient?
    emails = EmailMessage.objects.filter(owner__in=queryset)
    emails.delete()
    # TODO: Some confirmation page?
    messages.info(request, "Emails deleted successfully")


class EmailMessageAdminInline(admin.StackedInline):
    model = EmailMessage
    fields = ("title", "due_to")


class UserAdminConfig(UserAdmin):
    search_fields = ("email", "first_name")
    ordering = ("-created_at",)
    list_display = ("email", "created_at", "email_count")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    actions = [
        delete_mails,
    ]

    inlines = (EmailMessageAdminInline,)

    # Dont display inlines if form is an add form
    def get_inlines(self, request, obj):
        inl = self.inlines if obj is not None else ()
        return inl

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "first_name", "is_active"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("email", "first_name"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
