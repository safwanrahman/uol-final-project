from django.urls import path

from . import views

urlpatterns = [
    # Users
    path("me/users/", views.UserListCreateAPIView.as_view(), name="user-list-create"),
    path(
        "me/users/<uuid:pk>/",
        views.UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
    # Personas
    path(
        "me/personas/",
        views.PersonaListCreateAPIView.as_view(),
        name="persona-list-create",
    ),
    path(
        "me/personas/<uuid:pk>/",
        views.PersonaRetrieveUpdateDestroyAPIView.as_view(),
        name="persona-detail",
    ),
    # Persona name parts
    path(
        "me/personas/name-parts/",
        views.PersonaNamePartListCreateAPIView.as_view(),
        name="name-part-list-create",
    ),
    path(
        "me/personas/name-parts/<int:pk>/",
        views.PersonaNamePartRetrieveUpdateDestroyAPIView.as_view(),
        name="name-part-detail",
    ),
]



