from django.core.management import BaseCommand
from mailing.models import Mailing
from mailing.services import MailingService


class Command(BaseCommand):
    help = """
    Перевод рассылки в статус "Запущена" и выполнение отправки сообщений получателям.
    Выбор рассылки идёт по всем "Созданным" рассылкам.
    """

    def handle(self, *args, **options):

        mailings = Mailing.objects.all()
        posible_ints = []

        print('Введите ID рассылки, чтобы перевести её в статус "Запущена"\n')
        for mailing in mailings:
            posible_ints.append(mailing.pk)

            print(f"ID: {mailing.pk} | Тема: {mailing.message.subject}")

        user_input = input("\nID: ")

        if not user_input.isdigit():
            return print("ID должны содержать только цифры !!!")

        if int(user_input) not in posible_ints:
            return print("Нет такой рассылки")

        MailingService.mailing_push(int(user_input))
        return print("Рассылка запущена")
