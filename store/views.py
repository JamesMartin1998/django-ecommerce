from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

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
        product_count = products.count()
    
    else:
        # get all the available products (no slug)
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        # access then category model via FK, then slug field
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug )
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }


    return render(request, 'store/product_detail.html', context)