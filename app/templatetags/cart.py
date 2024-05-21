from django.template import Library
from app.models import *

register = Library()

@register.inclusion_tag('includes/dropdown_cart.html')
def total_cart(request):
    try:
        cart = Cart.objects.get(cart_id = request.session.session_key)
        total_quantity = cart.total_quantity
        subtotal = cart.subtotal
    except Cart.DoesNotExist:
        cart = None
        total_quantity = 0
        subtotal = 0
        
    context = {'count': total_quantity,'nav_cart':cart,'Subtotal': subtotal  }
    return context