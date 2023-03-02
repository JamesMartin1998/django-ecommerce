from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse

# Create your views here.

def _cart_id(request):
    """
    returns the session key in the cart variable
    """
    # get session id
    cart = request.session.session_key
    # if no session, create a session and get the key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """
    Add a product to the cart
    """
    # get the product
    product = Product.objects.get(id=product_id)
    # gets cart with a cart_id(session_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        # if no cart, need to create a cart using the session key
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    # if a cart item already exists, need to get it and increment its quantity by 1
    try:
        # need to get cart item by its product and cart instances
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    # if a cart item doesn't exist yet, need to create the cart item with a quantity of 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return HttpResponse(cart_item.product)
    exit()
    return redirect('cart')



def cart(request):
    return render(request, 'store/cart.html')