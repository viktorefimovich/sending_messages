from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
)

from .models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs["class"] = "form-control flatpickr-basic"
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs["class"] = "form-control datepicker"
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs["class"] = "form-control flatpickr-time"
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs["class"] = "form-control select2 select2-multiple"
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs["class"] = "form-control select2"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=True, help_text="Введите ваш номер телефона."
    )
    username = forms.CharField(max_length=50, required=True, help_text="Псевдоним")
    country = forms.CharField(
        max_length=20, required=True, help_text="Страна проживания"
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "password1",
            "password2",
        )


class MailingUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
            "first_name",
            "last_name",
            "phone_number",
            "country",
        )


class MailingUserPassRestore(PasswordResetForm):
    class Meta:
        model = User
        fields = ("email",)
