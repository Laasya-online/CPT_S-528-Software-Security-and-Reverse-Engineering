from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import login as otp_login
from django.contrib import messages
import qrcode
from io import BytesIO
from django.http import HttpResponse

@login_required
def enable_mfa(request):
    # Ensure the user has an MFA device
    if not TOTPDevice.objects.filter(user=request.user).exists():
        if request.method == "POST":
            TOTPDevice.objects.create(user=request.user, name="default")
            return redirect("mfa_qr")  # Redirect to the QR code view after creation
    return render(request, "mfa/enable.html")

@login_required
def mfa_qr(request):
    # Generate the QR code for the user's device
    try:
        device = TOTPDevice.objects.get(user=request.user, name="default")
        qr = qrcode.make(device.config_url)
        buffer = BytesIO()
        qr.save(buffer)
        buffer.seek(0)
        return HttpResponse(buffer, content_type="image/png")
    except TOTPDevice.DoesNotExist:
        messages.error(request, "No MFA device found. Please set up MFA first.")
        return redirect("enable_mfa")

@login_required
def mfa_verification(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        try:
            # Get the user's TOTP device
            device = TOTPDevice.objects.get(user=request.user, name="default")
            # Verify the entered OTP
            if device.verify_token(otp):
                otp_login(request, device)
                return redirect("sample_list")  # Redirect to your app's main page
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        except TOTPDevice.DoesNotExist:
            messages.error(request, "MFA is not configured for your account.")
            return redirect("enable_mfa")  # Redirect to MFA setup if not configured

    return render(request, "mfa/verify.html")
