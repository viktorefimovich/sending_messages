from mailing import views

from mailing.apps import MailingConfig

from django.urls import path

app_name = MailingConfig.name

urlpatterns = [
    path("", views.MailingListView.as_view(), name="main_page"),
    path("mailing_new/", views.MailingCreateView.as_view(), name="mailing_new"),
    path(
        "mailing_detail/<int:pk>/",
        views.MailingDetailView.as_view(),
        name="mailing_detail",
    ),
    path(
        "mailing_update/<int:pk>/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing_delete/<int:pk>/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailing_push/<int:pk>/", views.MailingPush.as_view(), name="mailing_push"),
    path(
        "mailing_cancel/<int:pk>/", views.MailingCancel.as_view(), name="mailing_cancel"
    ),
    path(
        "mailing_reopen/<int:pk>/", views.MailingReOpen.as_view(), name="mailing_reopen"
    ),
    path("receiver_list/", views.ReceiverListView.as_view(), name="receiver_list"),
    path("receiver_new/", views.ReceiverCreateView.as_view(), name="receiver_new"),
    path(
        "receiver_detail/<int:pk>/",
        views.ReceiverDetailView.as_view(),
        name="receiver_detail",
    ),
    path(
        "receiver_update/<int:pk>/",
        views.ReceiverUpdateView.as_view(),
        name="receiver_update",
    ),
    path(
        "receiver_delete/<int:pk>/",
        views.ReceiverDeleteView.as_view(),
        name="receiver_delete",
    ),
    path("message_list/", views.MessageListView.as_view(), name="message_list"),
    path("message_new/", views.MessageCreateView.as_view(), name="message_new"),
    path(
        "message_detail/<int:pk>/",
        views.MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "message_update/<int:pk>/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message_delete/<int:pk>/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("attempt_list/", views.AttemptListView.as_view(), name="attempt_list"),
    path(
        "attempt_detail/<int:pk>/",
        views.AttemptDetailView.as_view(),
        name="attempt_detail",
    ),
    path("stats/", views.StatisticTemplateView.as_view(), name="stats"),
    path("users_list/", views.UsersListView.as_view(), name="users_list"),
    path(
        "users_detail/<int:pk>/", views.UsersDetailView.as_view(), name="users_detail"
    ),
    path(
        "users_detail/<int:pk>/switch/",
        views.UsersActiveSwitch.as_view(),
        name="active_switch",
    ),
    path("access_denied/", views.AccessDenied.as_view(), name="access_denied"),
]
