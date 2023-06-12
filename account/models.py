from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from account.tasks import send_welcome_email_eco
from django.conf import settings
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def send_welcome_email(self, subject, message):
        from_email = settings.EMAIL_HOST_USER
        to = (self.email,)
        send_welcome_email_eco.apply_async(args=[subject, message, from_email, to],
                                            ignore_result=True,
                                            queue='Eemail',
                                            routing_key='Eemail'
                                             )
