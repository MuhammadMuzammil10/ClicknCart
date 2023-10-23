from app.models import Cart , CartItem ,  Category , Brand , Order , Information , CompanyDetail , WishList , FlashSale
from django.utils import timezone
from app.forms import NewsLetterForm
from django.contrib import messages
from django.db.models import Sum 
import datetime
from django.db.models import Q


def totalCart(request):
    try:
        about_us = Information.objects.get( Q(information_title__iexact = 'About Us') & Q(status = "Published") )
    except Information.DoesNotExist:
        about_us = None
    try:
        company = CompanyDetail.objects.first()
    except:
        company = None
    try:
        flashsale = FlashSale.objects.get(Q(end_time__gt=timezone.now()))
        print("Flash Sale in context processor" , flashsale)
    except:
        flashsale = None
    category = Category.objects.all()
    brands = Brand.objects.all()
    order_count = Order.objects.count()
    orders = Order.objects.all().order_by('-id')[:5]
    customer_count = Order.objects.values('user').distinct().count()
    total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales']
    now = datetime.datetime.now()
    last_month_start = now - datetime.timedelta(days=30 * 5)
    sales = Order.objects.filter(date__gte=last_month_start, date__lte=now).values('date__month').annotate(total_amount=Sum('total_amount')).order_by('date__month')

                    
    # Extract month names and total amounts for sales data
    month_names = [datetime.date(1900, month, 1).strftime('%B') for month in sales.values_list('date__month', flat=True)]
    amounts = list(sales.values_list('total_amount', flat=True))
    try:
        cart = Cart.objects.get(cart_id = request.session.session_key)
        print(cart , 'cart')
        total_quantity = cart.total_quantity
        subtotal = cart.subtotal
    except Cart.DoesNotExist:
        cart = None
        total_quantity = 0
        subtotal = 0
    pages = Information.objects.filter(status = "Published")
    if request.method == "POST":
        newsLetterform = NewsLetterForm(request.POST)
        if newsLetterform.is_valid():
            newsLetterform.save()
            messages.success(request , 'Subscribed SuccessFully!!!')
    else:
        newsLetterform = NewsLetterForm()
    try:
        wishlist = WishList.objects.filter(user = request.user)
    except:
        wishlist = None
    try:
        order_count = Order.objects.filter(status = 'PENDING').count()
    except:
        order_count = None
    return{'count': total_quantity,'nav_cart':cart,'Subtotal': subtotal , 'main_categories' : category , 'brands': brands , 'orders_count': order_count, 'customer_count': customer_count, 'total_sales': total_sales , 'orders' : orders , 'dates': month_names, 'amounts': amounts , 'about_us' : about_us , 'company' : company , 'pages' : pages, 'newsLetterform' : newsLetterform , 'wishlist' : wishlist , 'order_count' : order_count , 'flashsale' : flashsale}