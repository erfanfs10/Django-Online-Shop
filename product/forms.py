from django.forms import ModelForm, NumberInput
from .models import Rating
from order.models import OrderItem


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ("point", "title", "body")
        widgets = {
            "point": NumberInput(attrs={"max_value": 10, "min_value": 1}),  
        }

    def clean_point(self):
        point = self.cleaned_data["point"]
        if point >= 0 and point <= 10:
            return point
        else:
            self.errors["point"] = ["The point must be between 1 to 10!"]
            return point  
        
    def check_buy(self, user, product, form):
        orders = OrderItem.objects.filter(order__user=user)
        for i in orders:
            if i.product == product:
                return True
        form.add_error("title", "you must buy this product to rate!")    
        return False    
       
