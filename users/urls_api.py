from django.urls import path
from .views_api import SendCodeView, VerifyCodeView, ProfileView

urlpatterns = [
    path('send-code/', SendCodeView.as_view()),
    path('verify-code/', VerifyCodeView.as_view()),
    path('profile/', ProfileView.as_view()),
]
