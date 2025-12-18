from django.db import models
import uuid


class User(models.Model):
    """
    Core user/account table, separate from Django's auth user.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Encrypted email bytes (e.g. output of an encryption library)
    email_enc = models.CharField(max_length=255)
    # Store a password hash (e.g. Argon2/bcrypt) – never plain text
    hashed_password = models.CharField(max_length=255)
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

    persona_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personas")
    label = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
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
