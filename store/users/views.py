from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from users.models import EmailVerification, User

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("products:index"))
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/signup.html"
    success_message = "Вы успешно зарегистрированы!"
    title = "Store - Регистрация"

    def get_success_url(self):
        return reverse("users:login")


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    title = "Store - Профиль"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("products:index"))


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - Подтверждение електронной почты"
    template_name = "users/email_verification.html"

    def get(self, request, *agrs, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *agrs, **kwargs)
        else:
            return HttpResponseRedirect(reverse("products:index"))
