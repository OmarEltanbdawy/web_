from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, Optional

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView

from accounts.forms import SignupForm
from accounts.serializers import ProfileUpdate, user_to_profile_payload


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form: SignupForm):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm


class UserLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


@login_required
@require_http_methods(["GET"])
def profile_detail(request: HttpRequest) -> JsonResponse:
    payload = user_to_profile_payload(request.user)
    return JsonResponse(payload)


def _parse_profile_update(data: Dict[str, Any]) -> ProfileUpdate:
    date_of_birth: Optional[date] = None
    if 'date_of_birth' in data and data['date_of_birth']:
        date_of_birth = date.fromisoformat(str(data['date_of_birth']))
    return ProfileUpdate(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        date_of_birth=date_of_birth,
    )


@login_required
@require_http_methods(["PUT", "PATCH"])
def profile_update(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'JSON payload must be an object.'}, status=400)

    update = _parse_profile_update(payload)
    user = request.user

    if update.first_name is not None:
        user.first_name = update.first_name
    if update.last_name is not None:
        user.last_name = update.last_name
    if update.email is not None:
        user.email = update.email
    if update.date_of_birth is not None:
        user.date_of_birth = update.date_of_birth

    user.full_clean(validate_unique=False)
    user.save(update_fields=['first_name', 'last_name', 'email', 'date_of_birth'])

    return JsonResponse(user_to_profile_payload(user))
