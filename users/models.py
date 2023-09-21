from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class AdvUser(AbstractUser):

    SEX = [
        ('Man', 'М'),
        ('Woman', 'Ж')
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=5, choices=SEX)
    phone_number = PhoneNumberField(blank=True)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_message = models.BooleanField(default=True, verbose_name='Согласие на отправку уведомлений')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractUser.Meta):
        pass