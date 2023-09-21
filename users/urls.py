from django.urls import path

from users.views import BBLoginView, profile, BBLogoutView, ChangeUserInfoView, BBPasswordChangeView, RegisterUserView, \
    RegisterDoneView, user_activate, DeleteUserView

app_name = 'users'


urlpatterns = [
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