from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from basket.models import Basket


@receiver(user_logged_in)
def on_user_logged_in(sender, user, request, **kwargs):
    print("from signal")
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