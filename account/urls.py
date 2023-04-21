from django.urls import path
from .views import LoginView, RegisterView, ProfileView, logout_view 
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    path("profile/", ProfileView.as_view(), name="profile"),

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
