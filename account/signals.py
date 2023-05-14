from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from basket.models import Basket
from account.models import CustomUser


@receiver(user_logged_in)
def on_user_logged_in(sender, user, request, **kwargs):
   
    basket_id = request.session.get("basket_id", None)# search for basket_id in user session

    if basket_id is not None:

        user_basket = Basket.get_basket(request)# get user basket
        session_basekt = Basket.objects.get(pk=basket_id)# get basket from user session

        basket_line = session_basekt.basket_line.select_related("product").all()
        for line in basket_line:
            user_basket.add_to_basket(line.product.id, line.quantity)

    """
        this signal is for when the user has added items to his basket
        and then decided to log in
        so we should add thoes items to his basket
        when he logs in
    
    """


@receiver(post_save, sender=CustomUser)# sendig welcome email to new users using signal
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to My Site!'
        message = f'Hi {instance.name},\n\nThanks for registering on My Site!'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, instance.email)
