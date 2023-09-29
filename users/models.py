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
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
        null=True
    )
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