from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingAttempt
from users.models import User


class MailingService:

    @staticmethod
    def get_created_mailing(user, show_all=False):
        if show_all:
            return Mailing.objects.filter(status="Создана")
        return user.mailings.filter(status="Создана")

    @staticmethod
    def get_started_mailing(user, show_all=False):
        if show_all:
            return Mailing.objects.filter(status="Запущена")
        return user.mailings.filter(status="Запущена")

    @staticmethod
    def get_finished_mailing(user, show_all=False):
        if show_all:
            return Mailing.objects.filter(status="Завершена")
        return user.mailings.filter(status="Завершена")

    @staticmethod
    def mailing_push(mailing_pk):

        mailing = Mailing.objects.get(pk=mailing_pk)

        subject = mailing.message.subject
        text = mailing.message.message_text
        receivers = [x.email for x in mailing.receivers.all()]

        for rec_email in receivers:

            try:
                result = send_mail(
                    subject=subject,
                    message=text,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[
                        rec_email,
                    ],
                )

            except Exception as err:
                result = err

            attempt = MailingAttempt(
                status="Успешно" if result == 1 else "Не успешно",
                server_response=result,
                mailing=mailing,
            )
            attempt.save()

        mailing.status = "Завершена"
        mailing.save()


class MailingAttemptsService:

    @staticmethod
    def get_my_attempts(user_pk):
        user = User.objects.get(pk=user_pk)
        user_mailings = user.mailings.all()

        attempts = []

        for x in user_mailings:
            attempts.extend(x.mailingattempt_set.all())

        attempts.sort(key=lambda x: x.attempt_at)

        return attempts

    @staticmethod
    def is_attempt_owner(attempt_pk, user):
        user_attempt = MailingAttempt.objects.get(pk=attempt_pk)

        return user_attempt.mailing.owner == user
