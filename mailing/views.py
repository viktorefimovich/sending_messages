from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from mailing.models import Mailing
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

