from django.shortcuts import redirect
from django_otp import user_has_device

class EnforceMFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for anonymous users and MFA pages
        if request.user.is_authenticated and not user_has_device(request.user):
            if not request.path.startswith('/mfa/'):
                return redirect('enable_mfa')
        return self.get_response(request)
