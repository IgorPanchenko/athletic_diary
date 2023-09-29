from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, INTERNAL_RESET_SESSION_TOKEN, UserModel
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.signing import BadSignature
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import UpdateView, CreateView, TemplateView, DeleteView

from users.forms import ChangeUserInfoForm, RegisterUserForm
from users.models import AdvUser
from users.utilities import signer


class BBLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:profile1')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'users/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('users:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Пароль пользователя изменен'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'users/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('users:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'


def user_activate(request, sign):
    try:
        first_name = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(AdvUser, first_name=first_name)
    if user.is_activated:
        template = 'users/user_is_activated.html'
    else:
        template = 'users/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template_name=template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:login')


    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'

    def form_valid(self, form):
        # Переопределите этот метод для выполнения действий, связанных с регистрацией по электронной почте.
        # Например, обновление пароля пользователя.
        # После успешной обработки формы, можно перенаправить пользователя на страницу входа или другую страницу.
        # Возвращайте HttpResponseRedirect или JsonResponse, как это требуется.
        # Пример:
        user = form.save()
        # Дополнительные действия здесь
        return super().form_valid(form)

    def get_success_url(self):
        # Укажите URL-адрес, на который будет перенаправлен пользователь после успешной регистрации.
        return reverse('users:login')  # Замените 'login' на свой URL-адрес

    def get_email_context(self, user, token):
        # Переопределите этот метод для настройки контекста электронной почты.
        # Это может включать в себя настройку текста или темы сообщения.
        context = super().get_email_context(user, token)
        # Дополнительные настройки здесь
        return context