from django.contrib import admin

from products.admin import BasketAdmin

from .models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "user",
        "experation",
    )
    fields = ("code", "user", "experation", "created")
    readonly_fields = ("created",)