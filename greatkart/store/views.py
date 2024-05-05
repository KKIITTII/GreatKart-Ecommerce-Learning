from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from cart.models import Cart
from cart.views import _cart_id
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def store(request, category_slug=None):
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = categories.product_set.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        # products = Product.objects.filter(category=categories, is_available=True)
        # products = Product.objects.filter(category__slug = category_slug, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    context = { 'products': paged_products, "product_count": product_count}
    return render(request,  'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exceptions as E:
        raise E     
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))     # get cart with present session
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
    in_cart = cart.cartitem_set.filter(product=single_product).exists()
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)
    

def search(request):
    
    products = []
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(category__category_name__icontains=keyword) | Q(product_name__icontains=keyword) ).order_by('-created_date')
            product_count = products.count()
            
    context = { 'products': products,  'product_count': product_count}
    return render(request, 'store/store.html', context)