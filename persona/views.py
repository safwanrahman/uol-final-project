from rest_framework import generics, exceptions, permissions
from django.core.signing import Signer, BadSignature
from django.db.models import Q

from .models import User, Persona, PersonaNamePart, APIToken
from .serializers import UserSerializer, PersonaSerializer, PersonaNamePartSerializer


def restrict_queryset_by_token(request, qs, is_name_part=False):
    auth = getattr(request, "auth", None)
    if isinstance(auth, APIToken) and (auth and not auth.has_full_access):
        if is_name_part:
            return qs.filter(persona__api_tokens=auth)
        return qs.filter(api_tokens=auth)
    return qs


def get_custom_user(request):
    if not request.user.is_authenticated:
        return None
    email_or_username = request.user.email or request.user.username
    return User.objects.filter(email_enc=email_or_username).first()


class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    List all users or create a new user.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            return User.objects.filter(id=custom_user.id).order_by("-created_at")
        return User.objects.none()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single user.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            return User.objects.filter(id=custom_user.id).order_by("-created_at")
        return User.objects.none()


class PersonaListCreateAPIView(generics.ListCreateAPIView):
    """
    List all personas or create a new persona.
    """

    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            qs = Persona.objects.filter(user=custom_user)
            return restrict_queryset_by_token(self.request, qs)
        return Persona.objects.none()

    def perform_create(self, serializer):
        custom_user = get_custom_user(self.request)
        serializer.save(user=custom_user)


class PersonaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single persona.
    """

    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            qs = Persona.objects.filter(user=custom_user)
            return restrict_queryset_by_token(self.request, qs)
        return Persona.objects.none()


class SharedPersonaAPIView(generics.RetrieveAPIView):
    """
    Retrieve a shared persona via a signed URL token.
    """

    serializer_class = PersonaSerializer

    def get_object(self):
        token = self.kwargs.get("token")
        signer = Signer()
        try:
            persona_id = signer.unsign(token)
            return Persona.objects.get(pk=persona_id)
        except (BadSignature, Persona.DoesNotExist):
            raise exceptions.NotFound("Invalid or expired share link")


class IdentityContextAPIView(generics.ListAPIView):
    """
    Search for a User's Persona given a context (label).
    Enforces visibility constraints: public is always visible, internal requires auth, private is owner only.
    """

    serializer_class = PersonaSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        context_val = self.request.query_params.get("context")

        if not user_id:
            return Persona.objects.none()

        qs = Persona.objects.filter(user_id=user_id)

        if context_val:
            qs = qs.filter(Q(label__iexact=context_val) | Q(type__iexact=context_val))

        custom_user = get_custom_user(self.request)

        if custom_user and str(custom_user.id) == str(user_id):
            return restrict_queryset_by_token(self.request, qs)
        elif custom_user:
            return qs.filter(
                Q(visibility_level="public") | Q(visibility_level="internal")
            )
        else:
            return qs.filter(visibility_level="public")


class PersonaNamePartListCreateAPIView(generics.ListCreateAPIView):
    """
    List all persona name parts or create a new one.
    """

    serializer_class = PersonaNamePartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            qs = PersonaNamePart.objects.filter(persona__user=custom_user).order_by(
                "persona_id", "display_order"
            )
            return restrict_queryset_by_token(self.request, qs, is_name_part=True)
        return PersonaNamePart.objects.none()


class PersonaNamePartRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or delete a single persona name part.
    """

    serializer_class = PersonaNamePartSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        custom_user = get_custom_user(self.request)
        if custom_user:
            qs = PersonaNamePart.objects.filter(persona__user=custom_user).order_by(
                "persona_id", "display_order"
            )
            return restrict_queryset_by_token(self.request, qs, is_name_part=True)
        return PersonaNamePart.objects.none()
