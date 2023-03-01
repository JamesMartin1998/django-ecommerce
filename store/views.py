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