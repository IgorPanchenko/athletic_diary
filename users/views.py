from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
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
        username_register = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(AdvUser, username_register=username_register)
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
    success_url = reverse_lazy('users:password_reset_complete')
