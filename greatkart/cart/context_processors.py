from .models import Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist



def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = cart.cartitem_set.filter(is_active=True)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
            
    return {"cart_count": cart_count}