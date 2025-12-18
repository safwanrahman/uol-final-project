from django.contrib import admin

from .models import User, Persona, PersonaNamePart


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "email_enc", "created_at")
    search_fields = ("email_enc",)
    ordering = ("-created_at",)


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("persona_id", "user", "label", "is_default", "visibility_level")
    list_filter = ("visibility_level", "is_default")
    search_fields = ("label",)


@admin.register(PersonaNamePart)
class PersonaNamePartAdmin(admin.ModelAdmin):
    list_display = ("part_id", "persona", "part_type", "value", "display_order", "locale")
    list_filter = ("part_type", "locale")
    search_fields = ("value",)
    ordering = ("persona", "display_order")
