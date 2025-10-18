from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailing import forms
from mailing.models import Mailing, Recipient
from mailing.services import MailingService


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
