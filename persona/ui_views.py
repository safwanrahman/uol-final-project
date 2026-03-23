from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import Signer, BadSignature
from django.http import Http404
from .models import Persona, User as CustomUser, PersonaNamePart, APIToken


class IndexView(TemplateView):
    template_name = "index.html"


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    context_object_name = "personas"

    def get_queryset(self):
        email_or_username = self.request.user.email or self.request.user.username
        return Persona.objects.filter(user__email_enc=email_or_username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tokens = APIToken.objects.filter(user=self.request.user).order_by("-created_at")
        context["api_tokens"] = tokens
        return context


class GenerateTokenView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "").strip()
        access_type = request.POST.get("access_type", "full")

        has_full_access = access_type == "full"

        token = APIToken.objects.create(
            user=request.user,
            name=name if name else "My API Token",
            has_full_access=has_full_access,
        )

        if not has_full_access:
            persona_ids = request.POST.getlist("persona_ids")
            if persona_ids:
                personas = Persona.objects.filter(
                    persona_id__in=persona_ids,
                    user__email_enc=request.user.email or request.user.username,
                )
                token.allowed_personas.set(personas)

        messages.success(request, "New API Token generated successfully.")
        return redirect("dashboard")


class DeleteTokenView(LoginRequiredMixin, View):
    def post(self, request, key, *args, **kwargs):
        APIToken.objects.filter(key=key, user=request.user).delete()
        messages.success(request, "API Token deleted.")
        return redirect("dashboard")


class PersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    template_name = "persona_detail.html"
    context_object_name = "persona"

    def get_queryset(self):
        email_or_username = self.request.user.email or self.request.user.username
        return Persona.objects.filter(user__email_enc=email_or_username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        signer = Signer()
        token = signer.sign(str(self.object.persona_id))
        context["share_url"] = self.request.build_absolute_uri(
            f"/persona/shared/{token}"
        )
        context["api_share_url"] = self.request.build_absolute_uri(
            f"/api/shared/{token}/"
        )
        return context


class SharedPersonaDetailView(DetailView):
    model = Persona
    template_name = "persona_detail.html"
    context_object_name = "persona"

    def get_object(self, queryset=None):
        token = self.kwargs.get("token")
        signer = Signer()
        try:
            persona_id = signer.unsign(token)
            return Persona.objects.get(pk=persona_id)
        except (BadSignature, Persona.DoesNotExist):
            raise Http404("Invalid or expired share link")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_shared"] = True
        return context


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = "create_persona.html"
    fields = ["label", "type", "username", "website", "visibility_level", "is_default"]
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        email_or_username = self.request.user.email or self.request.user.username
        # Ensure a matching custom User exists
        custom_user, created = CustomUser.objects.get_or_create(
            email_enc=email_or_username
        )

        form.instance.user = custom_user
        response = super().form_valid(form)

        part_types = self.request.POST.getlist("part_type[]")
        part_values = self.request.POST.getlist("part_value[]")
        display_orders = self.request.POST.getlist("display_order[]")
        locales = self.request.POST.getlist("locale[]")

        for p_type, p_val, d_order, loc in zip(
            part_types, part_values, display_orders, locales
        ):
            if p_type and p_val:
                PersonaNamePart.objects.create(
                    persona=self.object,
                    part_type=p_type,
                    value=p_val,
                    display_order=d_order or 1,
                    locale=loc or "en-US",
                )

        return response
