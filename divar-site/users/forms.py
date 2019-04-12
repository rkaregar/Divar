from django.contrib.auth.forms import UserCreationForm
from users.models import Member, ActivationCode
from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _


class MemberCreationForm(UserCreationForm):
    email_validator = EmailValidator(message=_("Please enter your email correctly"))
    phone_validator = RegexValidator(regex=r'^\d{8,12}$', message=_("Please enter your phone number correctly!"))
    email = forms.CharField(validators=[email_validator])
    phone = forms.CharField(validators=[phone_validator])

    class Meta:
        model = Member
        fields = ('username', 'email', 'password1', 'password2', 'phone')


class MemberActivationForm(forms.ModelForm):

    class Meta:
        model = ActivationCode
        fields = ('code',)
