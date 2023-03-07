from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request, category_slug=None):
    # should probably just be called category
    categories = None
    products = None

    # if store url is followed by a category slug
    if category_slug != None:
        # get the category object
        categories = get_object_or_404(Category, slug=category_slug)
        # get all products that are of the particular category and available
        products = Product.objects.filter(category=categories, is_available=True)
        # set what to show and how many per page
        paginator = Paginator(products, 6)
        # page number
        page = request.GET.get('page')
        # products on page
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    else:
        # get all the available products (no slug)
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # set what to show and how many per page
        paginator = Paginator(products, 6)
        # page number
        page = request.GET.get('page')
        # products on page
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # access then category model via FK, then slug field
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # get the cart items in the user's cart, then returns True or False if items exist
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart
    }


    return render(request, 'store/product_detail.html', context)

def search(request):
    # if keyword is in the url
    if 'keyword' in request.GET:
        # save the value of the keyword
        keyword = request.GET['keyword']
        # if keyword is not blank
        if keyword:
            # get products that contain the keyword within their description, and order by most recently created
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)