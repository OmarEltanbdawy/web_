from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from accounts.serializers import user_to_profile_payload


def main_spa(request: HttpRequest) -> HttpResponse:
    auth_context = {
        'isAuthenticated': request.user.is_authenticated,
        'user': user_to_profile_payload(request.user) if request.user.is_authenticated else None,
    }
    return render(request, 'api/spa/index.html', {'auth_context': auth_context})
