from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

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

    return redirect('cart')


def remove_cart(request, product_id):
    """
    decrement quantity of cart items by one using the - button
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    # when a cart item's quantity is one, we can just delete it 
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request, cart_items=None, total=0, quantity=0):
    """
    Get all cart items in a cart, as well as the total price and quanity of items in the cart
    """
    try:
        tax = 0
        grand_total = 0
        # get the cart using the session id as cart id
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # get the cart items in the cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # loop through each cart item and edit the total cart price and quanity
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    
    # if no cart or cart items
    except ObjectDoesNotExist:
        pass # don't do anything

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)