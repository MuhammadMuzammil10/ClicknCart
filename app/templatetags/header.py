from django.template import Library
from app.models import *

register = Library()

@register.inclusion_tag('includes/header.html')
def header(request):
    category = Category.objects.all()
    brands = Brand.objects.all()
    try:
        wishlist = WishList.objects.filter(user = request.user)
    except:
        wishlist = None
    try:
        cart = Cart.objects.get(cart_id = request.session.session_key)
        total_quantity = cart.total_quantity
        subtotal = cart.subtotal
    except Cart.DoesNotExist:
        cart = None
        total_quantity = 0
        subtotal = 0
    context = {'main_categories' : category , 'brands': brands,'count': total_quantity,'nav_cart':cart,'Subtotal': subtotal,'wishlist' : wishlist }
    return context