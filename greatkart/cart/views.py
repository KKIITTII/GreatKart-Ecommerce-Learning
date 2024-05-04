from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse




# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart  = request.session.create()
    return cart 

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        print(request.POST)
        for item in request.POST:
            key = item
            value = request.POST[key]
            print("value:  ", value)
            try:
                variation = Variation.objects.get(product=product, variation_category=key, variation_value=value )
                product_variation.append(variation)
                print("variation:  ", variation)
                print("class:  ", isinstance(variation))
            except:
                pass
    print("product_variation:  ", product_variation)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))     # get cart with present session
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_item_id = []
    list_of_variations = []
    try:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        if cart_items:
            for c_item in cart_items:
                cart_item_id.append(c_item.id)
                cart_variations = c_item.variations.all()
                list_of_variations.append(cart_variations)
                print("cart_variations:  ", cart_variations)
                
                     
            if product_variation not in list_of_variations:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
                for v_item in product_variation:
                    cart_item.variations.add(v_item)
                cart_item.save()
            else:
                index = list_of_variations.index(product_variation)
                id = cart_item_id[index]
                cart_item = CartItem.objects.get(id = id)
                cart_item.quantity += 1
                cart_item.save()
                         
    except ObjectDoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        for v_item in product_variation:
            cart_item.variations.add(v_item)
        cart_item.save()
    return redirect('cart')

      
        # try: 
        #     cart_item = CartItem.objects.get(product=product, cart=cart)
        #     cart_item.quantity += 1
        #     cart_item.save()
        # except ObjectDoesNotExist:
        #     cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart) 
        #     cart_item.save()
        # return redirect('cart')

def cart(request, total=0, quantity=0, tax=0, grand_total=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        cart_items = cart.cartitem_set.filter(is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity 
        tax = (2 * total )/ 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total
    }
    return render(request, 'cart/cart.html', context)




def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(id = cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id )
    cart_item = CartItem.objects.get(id = cart_item_id)
    cart_item.delete()
    return redirect('cart')

# def remove_cart(request, product_id):
#     cart = Cart.objects.get(cart_id=_cart_id(request))
#     product = get_object_or_404(Product, id=product_id)
#     cart_item = CartItem.objects.get(product=product, cart=cart)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')


# def remove_cart_item(request, product_id):
#     cart = Cart.objects.get(cart_id=_cart_id(request))
#     product = get_object_or_404(Product, id=product_id )
#     cart_item = CartItem.objects.get(cart=cart, product=product)
#     cart_item.delete()
#     return redirect('cart')