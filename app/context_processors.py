from app.models import Cart , CartItem ,  Category , Brand , Order , Information , CompanyDetail , WishList , FlashSale
from django.utils import timezone
from app.forms import NewsLetterForm
from django.db.models import Sum , Q
import datetime


def totalCart(request):
    
    try:
        flashsale = FlashSale.objects.get(Q(end_time__gt=timezone.now()))
    except:
        flashsale = None
    # order_count = Order.objects.count()
    # orders = Order.objects.all().order_by('-id')[:5]
    # customer_count = Order.objects.values('user').distinct().count()
    # total_sales = Order.objects.aggregate(total_sales=Sum('total_amount'))['total_sales']

    # # Get current time in the timezone defined in your Django settings
    # now = timezone.now()

    # # Calculate the start date for the last 5 months (including the current month)
    # last_month_start = now - timezone.timedelta(days=30 * 5)

    # # Query orders using timezone-aware datetime objects
    # sales = Order.objects.filter(date__gte=last_month_start, date__lte=now).values('date__month').annotate(total_amount=Sum('total_amount')).order_by('date__month')


                    
    # # Extract month names and total amounts for sales data
    # month_names = [datetime.date(1900, month, 1).strftime('%B') for month in sales.values_list('date__month', flat=True)]
    # amounts = list(sales.values_list('total_amount', flat=True))

    try:
        order_count = Order.objects.filter(status = 'PENDING').count()
    except:
        order_count = None
    return{'order_count' : order_count , 'flashsale' : flashsale}