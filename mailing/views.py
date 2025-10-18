from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView

from mailing import forms
from mailing.models import Mailing, Recipient, Message, MailingAttempt
from mailing.services import MailingService, MailingAttemptsService
from users.models import User


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/main_page.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        can_view_all = user.has_perm("mailing.can_manage_mailing")

        if user.is_authenticated:
            context["created"] = MailingService.get_created_mailing(
                user, show_all=can_view_all
            )
            context["started"] = MailingService.get_started_mailing(
                user, show_all=can_view_all
            )
            context["finished"] = MailingService.get_finished_mailing(
                user, show_all=can_view_all
            )

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = forms.MailingForm
    template_name = "mailing/mailing_new.html"
    success_url = reverse_lazy("mailing:main_page")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        user.save()

        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [
            request.user == query_item.owner,
            request.user.has_perm("mailing.can_manage_mailing"),
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = forms.MailingForm
    template_name = "mailing/mailing_new.html"

    def get_success_url(self):
        return reverse("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [
            request.user == query_item.owner,
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete_confirm.html"
    success_url = reverse_lazy("mailing:main_page")

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [request.user == query_item.owner]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class ReceiverListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailing/receiver_list.html"

    context_object_name = "receivers"

    def get_queryset(self):

        user = self.request.user

        if user.has_perm("mailing.can_manage_clients"):
            return Recipient.objects.all()

        queryset = user.receivers.all()

        return queryset


class ReceiverCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = forms.ReceiverForm
    template_name = "mailing/receiver_new.html"
    success_url = reverse_lazy("mailing:receiver_list")

    def form_valid(self, form):
        receiver = form.save()
        user = self.request.user
        receiver.owner = user
        user.save()

        return super().form_valid(form)


class ReceiverDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "mailing/receiver_detail.html"
    context_object_name = "receiver"

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        user = request.user

        can_view = [
            user == query_item.owner,
            user.has_perm("mailing.can_manage_clients"),
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class ReceiverUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = forms.ReceiverForm
    template_name = "mailing/receiver_new.html"

    def get_success_url(self):
        return reverse("mailing:receiver_detail", kwargs={"pk": self.object.pk})


class ReceiverDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailing/receiver_delete_confirm.html"
    success_url = reverse_lazy("mailing:receiver_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"

    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.can_manage_message"):
            return Message.objects.all()
        queryset = user.messages.all()

        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = forms.MessageForm
    template_name = "mailing/message_new.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        receiver = form.save()
        user = self.request.user
        receiver.owner = user
        user.save()

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])
        user = request.user

        can_view = [
            user == query_item.owner,
            user.has_perm("mailing.can_manage_message"),
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = forms.MessageForm
    template_name = "mailing/message_new.html"

    def get_success_url(self):
        return reverse("mailing:message_detail", kwargs={"pk": self.object.pk})

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [request.user == query_item.owner]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_delete_confirm.html"
    success_url = reverse_lazy("mailing:message_list")

    def get(self, request, *args, **kwargs):
        query_item = self.model.objects.get(pk=self.kwargs["pk"])

        can_view = [request.user == query_item.owner]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class AccessDenied(TemplateView):
    template_name = "mailing/access_denied.html"

    def get(self, request, *args, **kwargs):
        print(f"{request.user} Пытался получить доступ к запрещённому контенту.")
        return super().get(request, *args, **kwargs)


class AttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        queryset = MailingAttemptsService.get_my_attempts(self.request.user.pk)
        return queryset


class AttemptDetailView(DetailView):
    model = MailingAttempt
    template_name = "mailing/attempt_detail.html"
    context_object_name = "attempt"

    def get(self, request, *args, **kwargs):
        user = request.user
        attempt_pk = self.kwargs['pk']

        can_view = [
            MailingAttemptsService.is_attempt_owner(attempt_pk=attempt_pk, user=user)
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "mailing/users_list.html"
    context_object_name = "musers"

    def get(self, request, *args, **kwargs):

        can_view = [
            request.user.is_staff,
            request.user.has_perm("users.can_manage_users"),
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        current_user = self.request.user.pk
        queryset = User.objects.exclude(pk=current_user).exclude(is_staff=True)
        return queryset


class UsersDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "mailing/users_detail.html"
    context_object_name = "muser"

    def get(self, request, *args, **kwargs):

        can_view = [
            request.user.is_staff,
            request.user.has_perm("mailing.can_manage_users"),
        ]

        if not any(can_view):
            return redirect("mailing:access_denied")

        return super().get(request, *args, **kwargs)


class UsersActiveSwitch(LoginRequiredMixin, DetailView):
    model = User
    template_name = "mailing/users_detail.html"

    def get(self, request, *args, **kwargs):
        muser_id = self.kwargs["pk"]
        muser = User.objects.get(pk=muser_id)

        can_use = [
            request.user.has_perm("mailing.can_manage_mailing"),
        ]

        if not any(can_use):
            return redirect("mailing:access_denied")

        muser.is_active = muser.is_active is False
        muser.save()

        return redirect("mailing:mailing_detail", pk=muser_id)


class MailingPush(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get(self, request, *args, **kwargs):
        mailing_id = self.kwargs["pk"]
        mailing = Mailing.objects.get(pk=mailing_id)
        user = request.user

        can_use = [
            request.user.has_perm("mailing.can_manage_mailing"),
            user == mailing.owner,
        ]

        if not any(can_use):
            return redirect("mailing:access_denied")

        mailing.status = "Запущена"
        mailing.save()
        MailingService.mailing_push(mailing.pk)

        return redirect("mailing:mailing_detail", pk=mailing_id)


class MailingCancel(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get(self, request, *args, **kwargs):
        mailing_id = self.kwargs["pk"]
        mailing = Mailing.objects.get(pk=mailing_id)
        user = request.user

        can_use = [
            request.user.has_perm("mailing.can_manage_mailing"),
            user == mailing.owner,
        ]

        if not any(can_use):
            return redirect("mailing:access_denied")

        mailing.status = "Завершена"
        mailing.save()

        return redirect("mailing:mailing_detail", pk=mailing_id)


class MailingReOpen(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get(self, request, *args, **kwargs):
        mailing_id = self.kwargs["pk"]
        mailing = Mailing.objects.get(pk=mailing_id)
        user = request.user

        can_use = [
            request.user.has_perm("mailing.can_manage_mailing"),
            user == mailing.owner,
        ]

        if not any(can_use):
            return redirect("mailing:access_denied")

        mailing.status = "Создана"
        mailing.save()

        return redirect("mailing:mailing_detail", pk=mailing_id)


class StatisticTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "mailing/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        attempts = MailingAttemptsService.get_my_attempts(self.request.user.pk)

        context["mailings"] = self.request.user.mailings.all()
        context["attempts_success"] = sum([x.status == "Успешно" for x in attempts])
        context["attempts_failed"] = sum([x.status != "Успешно" for x in attempts])
        context["attempts_total"] = len(attempts)

        return context
