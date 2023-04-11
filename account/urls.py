from django.urls import path
from .views import login_view, logout_view, register_view
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
     path('password_reset/',
          auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'),
            name='password_reset'
            ),
    path('password_reset_sent/',
          auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
            name='password_reset_done'
            ),
    path('password_reset_confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
            name='password_reset_confirm'
            ),
    path('password_reset_complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
            name='password_reset_complete'
            ),
]
