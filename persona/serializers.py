from rest_framework import serializers

from .models import User, Persona, PersonaNamePart


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, source="hashed_password")
    class Meta:
        model = User
        fields = ["user_id", "email_enc", "password", "created_at"]
        read_only_fields = ["user_id", "created_at"]


class PersonaNamePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaNamePart
        fields = [
            "part_id",
            "persona",
            "part_type",
            "value",
            "display_order",
            "locale",
        ]
        read_only_fields = ["part_id"]


class PersonaSerializer(serializers.ModelSerializer):
    # Nested name parts for convenience; optional
    name_parts = PersonaNamePartSerializer(many=True, read_only=True)

    class Meta:
        model = Persona
        fields = [
            "persona_id",
            "user",
            "label",
            "is_default",
            "visibility_level",
            "name_parts",
        ]
        read_only_fields = ["persona_id"]


