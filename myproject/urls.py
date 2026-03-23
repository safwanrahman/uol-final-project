"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from persona.ui_views import (
    IndexView,
    RegisterView,
    DashboardView,
    PersonaCreateView,
    PersonaDetailView,
    SharedPersonaDetailView,
    GenerateTokenView,
    DeleteTokenView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("persona/create", PersonaCreateView.as_view(), name="create_persona"),
    path("persona/generate-token", GenerateTokenView.as_view(), name="generate_token"),
    path(
        "persona/delete-token/<str:key>", DeleteTokenView.as_view(), name="delete_token"
    ),
    path("persona/<uuid:pk>", PersonaDetailView.as_view(), name="persona_detail"),
    path(
        "persona/shared/<str:token>",
        SharedPersonaDetailView.as_view(),
        name="shared_persona",
    ),
    path(
        "login.html",
        auth_views.LoginView.as_view(
            template_name="login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register.html", RegisterView.as_view(), name="register"),
    path("admin/", admin.site.urls),
    path("api/", include("persona.urls")),
    # API Documentation Routes
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
