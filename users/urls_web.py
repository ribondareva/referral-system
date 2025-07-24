from django.urls import path
from .views_web import LoginView, VerifyView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('verify/', VerifyView.as_view(), name="verify"),
    path('profile/', ProfileView.as_view(), name="profile"),
]
