from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from users.apps import user_registered
from users.models import AdvUser


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'send_message')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    phone_number = PhoneNumberField(region='RU')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_texts())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValueError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name', 'send_message')