from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, Optional

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
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
    success_url = '/#/profile'

    def form_valid(self, form: SignupForm):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm


class UserLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'


@require_http_methods(["GET"])
def profile_detail(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)
    payload = user_to_profile_payload(request.user)
    return JsonResponse(payload)


def _parse_profile_update(data: Dict[str, Any]) -> ProfileUpdate:
    date_of_birth: Optional[date] = None
    if 'date_of_birth' in data and data['date_of_birth']:
        date_of_birth = date.fromisoformat(str(data['date_of_birth']))
    return ProfileUpdate(
        username=data.get('username'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        date_of_birth=date_of_birth,
    )


@require_http_methods(["PUT", "PATCH"])
def profile_update(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)
    payload: Dict[str, Any]
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        payload = request.POST.dict()
    else:
        try:
            payload = json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

        if not isinstance(payload, dict):
            return JsonResponse({'error': 'JSON payload must be an object.'}, status=400)

    update = _parse_profile_update(payload)
    user = request.user
    update_fields = []

    if update.username is not None:
        user.username = update.username
        update_fields.append('username')
    if update.first_name is not None:
        user.first_name = update.first_name
        update_fields.append('first_name')
    if update.last_name is not None:
        user.last_name = update.last_name
        update_fields.append('last_name')
    if update.email is not None:
        user.email = update.email
        update_fields.append('email')
    if update.date_of_birth is not None:
        user.date_of_birth = update.date_of_birth
        update_fields.append('date_of_birth')
    if request.FILES.get('profile_image'):
        user.profile_image = request.FILES['profile_image']
        update_fields.append('profile_image')

    user.full_clean(validate_unique=False)
    user.save(update_fields=update_fields or None)

    return JsonResponse(user_to_profile_payload(user))
