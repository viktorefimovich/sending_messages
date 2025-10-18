from django.forms import ModelForm
from mailing.models import Mailing, Message, Recipient


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = ["receivers", "message"]


class ReceiverForm(ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "commentary"]


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "message_text"]
