from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .models import User

_fake_sms = {}


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        phone = request.POST.get("phone")
        _fake_sms[phone] = "1234"
        request.session["temp_phone"] = phone

        next_url = request.GET.get("next") or request.POST.get("next")
        if next_url:
            request.session["next_url"] = next_url

        return redirect("verify")


class VerifyView(View):
    def get(self, request):
        return render(request, "users/verify.html")

    def post(self, request):
        phone = request.session.get("temp_phone")
        code = request.POST.get("code")
        if _fake_sms.get(phone) == code:
            user, _ = User.objects.get_or_create(phone=phone)
            login(request, user)
            request.session["phone"] = phone

            next_url = request.session.pop("next_url", "/profile/")
            return redirect(next_url)

        return render(request, "users/verify.html", {"error": "Неверный код"})


class ProfileView(View):
    def get(self, request):
        phone = request.session.get("phone")
        if not phone:
            return redirect("login")

        user = User.objects.get(phone=phone)
        referrals = user.referrals.all()
        return render(request, "users/profile.html", {
            "user": user,
            "referrals": referrals
        })

    def post(self, request):
        phone = request.session.get("phone")
        if not phone:
            return redirect("login")

        user = User.objects.get(phone=phone)
        code = request.POST.get("invite_code")

        if not user.activated_code and code != user.invite_code:
            target = User.objects.filter(invite_code=code).first()
            if target:
                user.activated_code = target
                user.save()

        referrals = user.referrals.all()
        return render(request, "users/profile.html", {
            "user": user,
            "referrals": referrals
        })
