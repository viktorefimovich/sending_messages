import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .forms import MailingUserCreationForm, MailingUserChangeForm
from .models import User


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = MailingUserCreationForm
    success_url = reverse_lazy("users:after_register")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()

        url = f"http://{host}/users/email_confirm/{token}/"

        self.send_welcome_email(user, url)
        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_data, url):
        user_email = user_data.email

        title = "Вы успешно прошли регистрацию!"
        message = f"Для подтверждения почты перейдите по ссылке {url}"
        recipient_list = [
            user_email,
        ]
        send_mail(
            subject=title,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )


class MailingUserDetailView(LoginRequiredMixin, DetailView):
    template_name = "users/profile_detail.html"
    model = User
    context_object_name = "user"

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [request.user.pk == query_item.pk]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class MailingUserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/register.html"
    model = User
    form_class = MailingUserChangeForm

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [request.user.pk == query_item.pk]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        redirect_pk = self.request.resolver_match.kwargs.get("pk")

        return reverse("users:profile_detail", kwargs={"pk": redirect_pk})


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect("users:login")


class ResetPasswordView(PasswordResetView):
    template_name = "users/pass_restore.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject"
    success_url = reverse_lazy("users:after_pass_restore")


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
