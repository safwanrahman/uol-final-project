from rest_framework import generics

from .models import User, Persona, PersonaNamePart
from .serializers import UserSerializer, PersonaSerializer, PersonaNamePartSerializer


class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    List all users or create a new user.
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single user.
    """

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    lookup_field = "pk"


class PersonaListCreateAPIView(generics.ListCreateAPIView):
    """
    List all personas or create a new persona.
    """

    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single persona.
    """

    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    lookup_field = "pk"


class PersonaNamePartListCreateAPIView(generics.ListCreateAPIView):
    """
    List all persona name parts or create a new one.
    """

    queryset = PersonaNamePart.objects.all().order_by("persona_id", "display_order")
    serializer_class = PersonaNamePartSerializer


class PersonaNamePartRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve, update, or delete a single persona name part.
    """

    queryset = PersonaNamePart.objects.all().order_by("persona_id", "display_order")
    serializer_class = PersonaNamePartSerializer
    lookup_field = "pk"

