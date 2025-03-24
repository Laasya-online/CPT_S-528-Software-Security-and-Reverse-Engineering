from django.urls import path
from . import views

urlpatterns = [
    path('enable/', views.enable_mfa, name='enable_mfa'),
    path('qr/', views.mfa_qr, name='mfa_qr'),
    path('verify/', views.mfa_verification, name='mfa_verify'),
]
