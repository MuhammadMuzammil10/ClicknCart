from django.template import Library
from app.models import *
from app.forms import NewsLetterForm
from django.contrib import messages
register = Library()

@register.inclusion_tag('includes/footer.html')
def footer(request):
    try:
        pages = Information.objects.filter(status = "Published")
    except Information.DoesNotExist:
        pages = None
    if request.method == "POST":
        newsLetterform = NewsLetterForm(request.POST)
        if newsLetterform.is_valid():
            newsLetterform.save()
            messages.success(request , 'Subscribed SuccessFully!!!')
    else:
        newsLetterform = NewsLetterForm()
        
    try:
        about_us = Information.objects.get( Q(information_title__iexact = 'About Us') & Q(status = "Published") )
    except Information.DoesNotExist:
        about_us = None
    try:
        company = CompanyDetail.objects.first()
    except:
        company = None
     
    context = {'pages' : pages, 'newsLetterform' : newsLetterform ,'about_us' : about_us , 'company' : company ,}    
        
    return context