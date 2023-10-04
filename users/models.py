from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class AdvUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    SEX = [
        ('Man', 'М'),
        ('Woman', 'Ж')
    ]
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name="фамилия")
    sex = models.CharField(max_length=5, choices=SEX, verbose_name="пол")
    phone_number = PhoneNumberField(blank=True, region="RU", verbose_name='номер телефона')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='активированый')
    send_message = models.BooleanField(default=True, verbose_name='Согласие на отправку уведомлений')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    username_register = models.CharField(max_length=255, default='', blank=True, verbose_name="ключ для отправки электронных писем")


    class Meta(AbstractUser.Meta):
        pass

    def save(self, *args, **kwargs):
        self.username_register = str(self.email).split('@')[0]
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None