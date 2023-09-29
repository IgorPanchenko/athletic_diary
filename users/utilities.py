from django.conf.global_settings import ALLOWED_HOSTS
from django.core.signing import Signer
from django.template.loader import render_to_string

signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.first_name)}
    subject = render_to_string('users/email/activation_letter_subject.txt', context)
    body_text = render_to_string('users/email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)

