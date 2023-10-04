from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.views import BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView, RegisterUserView, \
    RegisterDoneView, user_activate, DeleteUserView, UserPasswordResetConfirmView

app_name = 'users'

urlpatterns = [
    path("reset/done/", PasswordResetCompleteView.as_view(
        template_name='users/password_confirmed.html'),
         name="password_reset_complete"
         ),
    path('profile/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('profile/password_reset/', PasswordResetView.as_view(
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/email/password_reset_subject.txt',
        template_name='users/password_reset_form.html',
        title='Сброс пароля',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
    path('password/change', BBPasswordChangeView.as_view(), name='password_change'),
    path('profile/change', ChangeUserInfoView.as_view(), name='profile_change'),
    path('logout/', BBLogoutView.as_view(), name='logout'),
    # path('accounts/profile/change/<int:pk>', profile_bb_change, name='profile_bb_change'),
    # path('accounts/profile/delete/<int:pk>', profile_bb_delete, name='profile_bb_delete'),
    # path('accounts/profile/add', profile_bb_add, name='profile_bb_add'),
    path('profile/', profile, name='profile'),
    path('login/', BBLoginView.as_view(), name='login'),
]
