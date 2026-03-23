from django.db import models
from django.conf import settings
import uuid
import binascii
import os


class User(models.Model):
    """
    Core user/account table, separate from Django's auth user.
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Encrypted email bytes (e.g. output of an encryption library)
    email_enc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return str(self.user_id)


class Persona(models.Model):
    """
    A user can have many personas (professional, gaming, legal, etc.).
    """

    class VisibilityLevel(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"
        RESTRICTED = "restricted", "Restricted"

    class PersonaType(models.TextChoices):
        LEGAL = "legal", "Legal"
        PROFESSIONAL = "professional", "Professional"
        ANONYMOUS = "anonymous", "Anonymous"
        GAMING = "gaming", "Gaming"
        SOCIAL = "social", "Social"
        OTHER = "other", "Other"

    persona_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personas")
    label = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    type = models.CharField(
        max_length=30,
        choices=PersonaType.choices,
        default=PersonaType.OTHER,
    )
    username = models.CharField(max_length=150, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    visibility_level = models.CharField(
        max_length=20,
        choices=VisibilityLevel.choices,
        default=VisibilityLevel.PRIVATE,
    )

    class Meta:
        db_table = "personas"

    def __str__(self) -> str:
        return f"{self.label} ({self.user_id})"


class PersonaNamePart(models.Model):
    """
    Stores ordered name parts for a persona (supports global naming formats).
    """

    class PartType(models.TextChoices):
        GIVEN_NAME = "given_name", "Given name"
        FAMILY_NAME = "family_name", "Family name"
        PATRONYMIC = "patronymic", "Patronymic"
        TITLE = "title", "Title"
        NICKNAME = "nickname", "Nickname"

    part_id = models.BigAutoField(primary_key=True)
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="name_parts"
    )
    part_type = models.CharField(max_length=20, choices=PartType.choices)
    # NVARCHAR-equivalent: Django's CharField is Unicode-capable
    value = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField()
    # Locale/language tag, e.g. "en-US", "zh-CN"
    locale = models.CharField(max_length=32)

    class Meta:
        db_table = "persona_name_parts"
        ordering = ["persona_id", "display_order"]

    def __str__(self) -> str:
        return f"{self.part_type}: {self.value}"


class APIToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="api_tokens", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    has_full_access = models.BooleanField(default=True)
    allowed_personas = models.ManyToManyField(
        "Persona", blank=True, related_name="api_tokens"
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f"{self.name or 'Token'} ({self.key[:6]}...)"
