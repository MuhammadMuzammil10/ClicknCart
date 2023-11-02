from django.template.loader import get_template , render_to_string
from datetime import date
from django.template import RequestContext
from django.core.mail import send_mail
import json , datetime , csv
from django.db.models.functions import TruncQuarter , TruncMonth , TruncDay , TruncHour
from django.shortcuts import render, redirect 
from app.forms import LoginForm, Registerationform , MyPasswordChangeForm , TrackOrderForm , NewsLetterForm , CouponForm
from app.models import Product, Cart, BilingAddress, Order , OrderItem, Product_images , Reviews, TopCategory , Category , Subcategory , Banner , Brand , SubSubcategory , Information , FeaturedOffer , WishList , ProductVariation , ProductAttribute , ProductAttributeValue , Coupon , CartItem , FlashSale , FlashSaleItem
from django.contrib.auth import login, authenticate , update_session_auth_hash
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect , HttpResponse 
from app.forms import MyPasswordChangeForm, ProfileForm , ReviewsForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import JsonResponse , response
from django.db.models import Q , Min , Max
from accounts.models import User
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.db.models import Sum , Avg

from .forms import ProductForm , Product_imagesForm
from django.utils.text import slugify
from django.utils import timezone

from django.urls import reverse
# from .decorators import custom_login_required

def base(request):
    try:
        featured_offer = FeaturedOffer.objects.all()
    except FeaturedOffer.DoesNotExist:
        featured_offer = None
    try:
        bestsellers = Product.objects.filter(Q(show_in_bestseller_slider = True) & Q(status = "Published"))
    except Product.DoesNotExist:
        bestsellers = None
    try:
        banners = Banner.objects.all()
    except Banner.DoesNotExist:
        banners = None
    try:
        categories = Category.objects.all()
    except Category.DoesNotExist:
        categories = None
    try:
        flashsale = FlashSale.objects.get(Q(end_time__gt=timezone.now())).flashsaleitem_set.all()
    except:
        flashsale = None
    context = {'featured_offer':featured_offer,'bestsellers' : bestsellers , 'banners' : banners,'categories' : categories , 'flashsale' : flashsale}
    return render(request, 'app/main.html',context)

def flashSaleShop(request):
    flashsale = FlashSale.objects.get(end_time__gt=timezone.now())
    current_time = timezone.now()
    timer = flashsale.end_time - timezone.now()
    timer = datetime.timedelta.total_seconds(timer)
    products = Product.objects.filter(flashsaleitem__FlashSale=flashsale)

        
    paginator = Paginator(products,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request , 'app/shop.html' , {'page_obj' : page_obj , 'flashsale_obj' : True , 'current_time' : current_time , 'timer' : timer})

def brands_product(request , brand=None):
    if brand == None:
        brands = Brand.objects.all()
        return render(request , 'app/brands.html' , context = {'brands' : brands} )
    else:
        products = Product.objects.filter(Q(brand__brand_url = brand) & Q(status = "Published"))
        context = {'products' : products , 'brand' : brand}
        return render(request , 'app/shop-brand.html',context)

def shop_categories(request):
    categories = TopCategory.objects.all()
    return render(request, 'app/shop-category.html' , {'categories' : categories})

def user_login(request):
    if not request.user.is_authenticated and request.method != 'POST' :
        request.session['next']   = (request.META.get('HTTP_REFERER', '/'))
    if request.method == 'POST':
        if request.POST.get('form_type') == 'formOne':
                form1 = LoginForm(request=request, data=request.POST)
                if form1.is_valid():
                    uname = form1.cleaned_data['username']
                    upass = form1.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                        login(request, user)
                        next_url = request.session.get('next', '/')
                        # Redirect the user to the stored 
                        return JsonResponse({'status': 'success', 'redirect_url': next_url})
                else:
                    errors = form1.errors
                    if '__all__' in errors:
                        return JsonResponse({'status': 'error', 'errors': {'form':errors['__all__']}})
                    return JsonResponse({'status': 'error', 'errors': form1.errors})
                form = Registerationform()
                context = {'form': form, 'form1': form1}
        elif request.POST.get('form_type') == 'formTwo':
                form = Registerationform(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    uemail = form.cleaned_data['email']
                    upass = form.cleaned_data['password1']
                    user = authenticate(username=uemail, password=upass)
                    if user is not None:
                        login(request, user)
                        next_url = request.session.get('next', '/')
                        return JsonResponse({'status': 'success', 'redirect_url': next_url})
                else:
                    errors = form.errors
                    if '__all__' in errors:
                        return JsonResponse({'status': 'error', 'errors': {'form':errors['__all__']}})
                    return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form1 = LoginForm()
        form = Registerationform()
        context = {'form1': form1, 'form': form}
    return render(request, 'app/login.html', context)

def user_register(request):
    if request.method == 'POST':
        form = Registerationform(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = Registerationform()
    return render(request, 'app/register.html', {'form': form})

def coupon_form(request):
    cart = Cart.objects.get(cart_id = _cart_id( request))
    if request.method == "POST":
        coupon_code =  request.POST.get('coupon_code')
        cart_id =  request.POST.get('cart_id')
        try:
            coupon = Coupon.objects.get( Q(coupon_code = coupon_code) & Q( coupon_expire_date__lte = datetime.datetime.now()  ) )
            try:
                Cart.objects.get(Q(cart_id = _cart_id( request)) & Q(coupon = coupon))
                return JsonResponse({'status': 'already-exist'})
            except Cart.DoesNotExist:
                cart.coupon = coupon
                cart.save()
                cart.update_totals()
                data = {'amount':cart.subtotal,'totalAmount':cart.total , 'coupon_discount' : cart.coupon_discount }
                return JsonResponse({'status': 'success' , 'data' : data})
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'not-exist'})
            

def product_detail(request, product_url):
    product = Product.objects.get(Q(url = product_url) & Q(status = "Published") )
    if request.method == "POST":
        rt = request.POST.get('rating') if request.POST.get('rating') != '' else 3
        fm = ReviewsForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            cm = fm.cleaned_data['comment']
            reg = Reviews(product = product , rating = rt , name = nm , email = em , comment = cm)
            reg.save()
    related_product = Product.objects.filter( Q(category=product.category,subcategory=product.subcategory,subsubcategory=product.subsubcategory ) & Q(status = "Published")).order_by('?')
    reviews = Reviews.objects.filter(Q(product=product) & Q(product__status = 'Published') & Q(status = 'APPROVED'))

    product_variations = ProductVariation.objects.filter(product=product)

    variation_dict = {}
    for variation in product_variations:
        attribute_name = variation.attributes.attribute.name
        if attribute_name in variation_dict:
            variation_dict[attribute_name].append(variation)
        else:
            variation_dict[attribute_name] = [variation]
    
    if reviews.exists():
        paginator = Paginator(reviews,2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = 'none'
    context = {'product': product,'related_product' : related_product,'subcategory':product.subcategory , 'form' : ReviewsForm() ,'page_obj':page_obj , 'variation_dict' :variation_dict  }
    
    return render(request, 'app/product-details.html', context)



def shop(request, category = None, subcategory = None , subsubcategory = None):
    if subsubcategory:
        subsubcategory = slugify(subsubcategory)
        subsubcategory = subsubcategory.replace('-' , ' ')
        products = Product.objects.filter(Q(subsubcategory__name__iexact = subsubcategory) & Q(status = "Published"))       
    elif subcategory:
        subcategory = slugify(subcategory)
        subcategory = subcategory.replace('-' , ' ')
        products = Product.objects.filter(Q(subcategory__name__iexact = subcategory) & Q(status = "Published"))       
    elif category:
        category = slugify(category)
        category = category.replace('-' , ' ')
        products = Product.objects.filter(Q(category__name__iexact = category) & Q(status = "Published"))       
    else:
        products = Product.objects.filter(status = "Published").order_by('?')
    paginator = Paginator(products,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    min_price = products.aggregate(min_price = Min('discounted_price'))['min_price']
    max_price = products.aggregate(max_price = Max('discounted_price'))['max_price']
    context = {'products':products,'page_obj':page_obj,'category':category, 'subcategory' : subcategory, 'subsubcategory' : subsubcategory , 'min_price' : min_price , 'max_price' : max_price} 
    return render(request,'app/shop.html',context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request):
    
    usr = request.user
    prod_id = request.GET.get('prod_id')
    prod_qty = int(request.GET.get('prod_qty')) if  request.GET.get('prod_qty') else None
    prod_vrnt = request.GET.get('variation_select')
    prod = Product.objects.get(pk = prod_id)
    if prod_vrnt != 'None':
        try:
            attribute_name, attribute_value = prod_vrnt.split(':')
            attribute_name = attribute_name.strip()
            attribute_value = attribute_value.strip()

            # Fetch the corresponding ProductAttribute and ProductAttributeValue objects
            attribute = ProductAttribute.objects.get(name=attribute_name)
            attribute_value = ProductAttributeValue.objects.get(attribute=attribute, value=attribute_value)

            # Fetch the ProductVariation object based on the attribute value
            variation = ProductVariation.objects.get(Q( attributes=attribute_value ) & Q(product = prod) )

            # The 'variation' variable now contains the desired ProductVariation object
            
        except (ValueError, ProductAttribute.DoesNotExist, ProductAttributeValue.DoesNotExist, ProductVariation.DoesNotExist):
            # Handle the case when the variation is not found or there's an error
            # ...
            pass
    try:
        cart = Cart.objects.get(cart_id =  _cart_id(request) )
    except Cart.DoesNotExist: 
        cart = None
    if (prod.quantity is None or prod.quantity > 0 ):
        try:
            item = CartItem.objects.get(Q(cart = cart) & Q(product = prod) )
            if prod.quantity is not None:
                if prod.quantity > 0 and ( prod.quantity > item.quantity) and not prod_qty :
                    item.quantity += 1
                    item.save()
                elif prod_qty and ( prod.quantity > item.quantity ) and ( prod.quantity > prod_qty) :
                    item.quantity += prod_qty
                    item.save()
                else:
                    return JsonResponse({'status' : 'quantity error' , 'error' : 'The requested quantity is not available' })
            else:
                if prod_qty:
                    item.quantity += prod_qty
                    item.save()
                else:
                    item.quantity += 1
                    item.save()
        except CartItem.DoesNotExist:
            try:
                cart =  Cart.objects.get(cart_id = _cart_id(request) )
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id = _cart_id(request) )
            if prod_qty and prod.quantity is not None and prod_vrnt != 'None' :
                if prod_qty <= prod.quantity:
                    reg = CartItem(cart = cart ,  product = prod , quantity = prod_qty , variant = variation)
                else:
                    return JsonResponse({'status' : 'quantity error' , 'error' : 'The requested quantity is not available' })
            elif prod_qty and (prod.quantity is None or (prod.quantity is not None and prod.quantity >= prod_qty ) ):
                reg = CartItem(cart = cart ,  product = prod , quantity = prod_qty)
            else:
                reg = CartItem(cart = cart , product = prod)
            reg.save()
        
        quantity = 0
        q = CartItem.objects.get(Q(cart = cart) & Q(product = prod_id ) )
        cart = Cart.objects.get(cart_id = _cart_id(request))
        item = list(Product.objects.filter(pk = prod_id).values())
        data = {"amount":cart.subtotal,"totalAmount":cart.total,'count':cart.total_quantity,'product':item,'quantity':q.quantity , 'product_img' : prod.main_picture.url}
        return JsonResponse({'status':'add', "data":data})
    else:
        return JsonResponse({'status' : 'quantity error' , 'error' : 'The requested quantity is not available' })



def select_variation(request , product_id , variation):
    product = Product.objects.get(id = product_id)
    attribute = ProductAttribute.objects.get()
    attributes = ProductVariation.objects.get( Q(product = product ) & Q(attributes__value = variation) )
    return JsonResponse({'status': 'success' })

def add_to_wishlist(request):
    usr = request.user
    prod_id = request.GET.get('prod_id')
    prod = Product.objects.get(pk = prod_id)
    if request.user.is_authenticated:
        try:
            item = WishList.objects.get(Q(user = usr) & Q(product = prod) )
            if item:  
                return JsonResponse({'status' : 'Already Exist'})      
        except:
            wish = WishList(user= usr , product = prod)
            wish.save()
        item = list(Product.objects.filter(pk = prod_id).values())
        data = {'product':item , 'product_img' : prod.main_picture.url}
        return JsonResponse({'status':'add', "data":data})
    elif not request.user.is_authenticated:
        request.session['next']   = (request.META.get('HTTP_REFERER', '/'))
        return JsonResponse({'status' : 'login' , 'redirect_url' : '/login/' })
    else:
        return JsonResponse({'status' : 'none' })

def showCart(request):
    usr = request.user
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        context = {'amount':cart.subtotal,'Shipping':cart.shipping_rate,'totalAmount':cart.total ,'carts':cart , 'form' : coupon_form}        
        return render(request,'app/cart.html',context)
    except Cart.DoesNotExist:
        return render(request , 'app/noncart.html')

def plus_cart(request):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    prod_id = request.GET.get('prod_id')
    c = CartItem.objects.get(Q(product = prod_id) & Q(cart = cart))
    c.quantity += 1
    c.save()
    cart = Cart.objects.get(cart_id = _cart_id(request))
    cart.update_totals()
    if cart.coupon:
        coupon_discount = cart.coupon_discount
    else:
        coupon_discount = None
    data = {'amount':cart.subtotal,'totalAmount':cart.total,"quantity":c.quantity,'per_price':c.per_price,'count':cart.total_quantity,'shipping':cart.shipping_rate , 'coupon_discount' : coupon_discount}
    return JsonResponse({"data":data})

def minus_cart(request):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    prod_id = request.GET.get('prod_id')
    item = CartItem.objects.get(Q(product = prod_id) & Q(cart = cart))
    if item.quantity >=1:
        # if prod.quantity and prod.quantity > item.quantity:
        item.quantity -= 1
        item.save()
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart.update_totals()
        if cart.coupon:
            coupon_discount = cart.coupon_discount
        else:
            coupon_discount = None
        data = {'amount':cart.subtotal,'totalAmount':cart.total,"quantity":item.quantity,'per_price':item.per_price,'count':cart.total_quantity,'shipping':cart.shipping_rate , 'coupon_discount' : coupon_discount}
    else:
        data = {}
    return JsonResponse({"data":data})
    
             
def delete_cart(request):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    prod_id = request.GET.get('prod_id')
    c = CartItem.objects.get( Q(product = prod_id) & Q(cart = cart) )
    c.delete()
    try: 
        cartitem = CartItem.objects.filter(cart = cart)
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart.update_totals()
        data = {'amount':cart.subtotal,'totalAmount':cart.total,'count':cart.total_quantity,'shipping': cart.shipping_rate}
        return JsonResponse({"data":data})
    except CartItem.DoesNotExist:
        data = {'amount':0,'totalAmount':0,'count':0,'shipping': 0}
        Cart.objects.get(cart_id = _cart_id(request)).delete()
        return JsonResponse({"data":data , 'status' : 'Empty Cart'})

        
def delete_wishlist(request):
    prod_id = request.GET.get('prod_id')
    c = WishList.objects.get( Q(product = prod_id) & Q(user = request.user) )
    c.delete()
    WishlistProduct = WishList.objects.filter(user = request.user)
    if WishlistProduct.exists():
        return JsonResponse({"status":'pass'})
    else:
        return JsonResponse({'status' : 'Empty Cart'})
        

@login_required
def address(request):
    adrs = BilingAddress.objects.filter(user = request.user)
    return render(request, 'app/address.html',{'add':adrs,'actives':'btn-primary'})


@method_decorator(login_required,name='dispatch')
class change_password(PasswordChangeView):
    template_name = 'app/account.html'
    form_class = MyPasswordChangeForm
    success_url = "/changepassworddone/"

def category(request,name):
    category = Product.objects.filter(Q(categories = name) & Q(status = "Published"))
    return render(request, 'app/category.html',{'category':category})

#def send_invoice_email(instance):
    user_email = instance.biling_address.email
    # Email subject
    subject = 'Order-Recipt Order Placed'
    # Email recipient
    to_email = user_email
    # Email sender
    from_email = 'zmuzammil74@gmail.com'
    # Render the HTML template
    template = get_template('app/invoice2.html')
    context = {'order': instance}
    message = render_to_string('app/invoice2.html',context)
    inline_html = transform(message)
    sent = send_mail(subject, inline_html, "WiseBuy", [to_email], html_message=inline_html)
    # Check if the email was sent successfully
    if sent > 0:
        print("Email sent successfully")
    else:
        print("Failed to send email")

def checkout(request):
    new_object_id = None
    try:
        terms_and_conditions = Information.objects.get( url = 'terms-and-conditions')
    except:
        terms_and_conditions = None
    pymnt_mthd = request.POST.get('payment-method-input')
    cart = Cart.objects.get(cart_id = _cart_id(request))

    # For Saving order placed address
    if request.method == 'POST':
        fm = ProfileForm(request.POST)
        if fm.is_valid():
            usr = request.user
            nm = fm.cleaned_data['first_name']
            ln = fm.cleaned_data['last_name']
            ad = fm.cleaned_data['address']
            ct = fm.cleaned_data['city']
            st = fm.cleaned_data['area']
            zip = fm.cleaned_data['zipcode']
            phn = fm.cleaned_data['phone']
            em = fm.cleaned_data['email']
            new_object = BilingAddress.objects.create(first_name=nm,last_name=ln,address=ad,city=ct,area=st,zipcode=zip,phone=phn,email=em)
            try:
                user = User.objects.get(email = em)
            except User.DoesNotExist:
                user = User.objects.create(first_name = nm , last_name = ln , email = em)
            new_object_id = new_object.id
            fm = ProfileForm()
    else:
        fm = ProfileForm()
    # Calculate total Amount
    if(new_object_id != None):
    
        notes = request.POST.get('notes')
        customer = BilingAddress.objects.get(id = new_object_id)
        order = Order.objects.create(user=user , biling_address = customer,  status='PENDING' , payment_method = pymnt_mthd , total_amount = cart.total , sub_total = cart.subtotal , flat_shipping_rate = cart.shipping_rate , notes = notes )
        for p in cart.cartitem_set.all():
            if p.variant:
                OrderItem(user = user , order = order , product = p.product , variant = p.variant , quantity = p.quantity ).save()
            else:
                OrderItem(user = user , order = order , product = p.product , quantity = p.quantity ).save()
            from_cart = Product.objects.get(id = p.product.id)
            if from_cart.quantity:
                from_cart.quantity -= p.quantity
                if from_cart.quantity <= 0:
                    from_cart.available_stock = "Out of Stock"
                from_cart.save()
            p.delete()
        cart.delete()
        # send_invoice_email(order)
        # return render(request , 'app/order.html', {'order':order , })
        return redirect(reverse("orders", kwargs={'id': order.id}))
    else:
        data = {"totalAmount":cart.total ,'amount': cart.subtotal ,'shipping': cart.shipping_rate ,"cart" : cart,'form':fm , 'terms_and_conditions' : terms_and_conditions}
        return render(request, 'app/checkout.html',data)

def orders(request , id):
    orders = Order.objects.get(id = id)
    return render(request, 'app/order.html',{"order":orders })


def search(request):
    if request.method == 'POST':
        data = request.POST['q']
        request.session['search-data'] = request.POST['q']
        products = Product.objects.filter(Q(title__icontains = data) & Q(status = "Published"))
        paginator = Paginator(products,3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'products':products,'page_obj':page_obj,'data':data,'subcategory':'all'}
        if products.exists():
            return render(request,'app/shop.html',context)
        else:
            return render(request,'app/no-result.html',context)   
    else:
        try:
            data = request.GET['q']
            suggestions = Product.objects.filter(Q(title__icontains = data) & Q(status = "Published"))
            suggestions_list = [ {'title' : product.title , 'img' : product.main_picture.url , 'url' : product.get_absolute_url() , 'price' : product.discounted_price } for product in suggestions]
            
            # suggestions_list = ['apple', 'banana', 'orange']  # Example suggestions
            return HttpResponse(json.dumps(suggestions_list), content_type='application/json')
        except:
            data = request.session.get('search-data', 'M')
            products = Product.objects.filter(Q(title__icontains = data) & Q(status = "Published"))
            paginator = Paginator(products,3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        context = {'products':products,'page_obj':page_obj,'data':data,'subcategory':'all'}
        return render(request,'app/shop.html',context)
    
@login_required
def account(request):
    orders = Order.objects.filter(user = request.user)
    addresses = BilingAddress.objects.filter(user = request.user)
    if request.method=="POST":
        fm = MyPasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': fm.errors})
    else:
            fm = MyPasswordChangeForm(user=request.user)
    context = {'orders' : orders,'form':fm, 'addresses':addresses}
    return render(request , 'app/account.html' , context)

def filter_products(request, option, category=None, subcategory=None, subsubcategory=None):
    
    if subsubcategory != 'None':
        subsubcategory = slugify(subsubcategory)
        subsubcategory = subsubcategory.replace('-', ' ')
        products = Product.objects.filter(subsubcategory__name__iexact = subsubcategory)

    elif subcategory != 'None':
        subcategory = slugify(subcategory)
        subcategory = subcategory.replace('-', ' ')
        products = Product.objects.filter(subcategory__name__iexact = subcategory)
        
    elif category != 'None':
        category = slugify(category)
        category = category.replace('-', ' ')
        products = Product.objects.filter(category__name__iexact = category)

    if option == "price-low":
        products = products.order_by('discounted_price')
    elif option == "price-high":
        products = products.order_by('-discounted_price')
    elif option == "latest":
        products = products.order_by('-id')
    elif option == "rating":
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    product_data = []
    for product in products:
        if product.product_images_set.first():
            hover_image_url = product.product_images_set.first().RelatedImages.url
        else:
            hover_image_url = None
        product_data.append({
            'id': product.id,
            'title': product.title,
            'quantity': product.quantity,
            'main_picture': product.main_picture.url,
            'discounted_price': product.discounted_price,
            'discount_perc': product.discount_perc,
            'selling_price': product.selling_price,
            'brand': product.brand.brand_name,
            'brand_url': product.brand.brand_url,
            'category': product.category.name,
            # 'subcategory': product.subcategory.name,
            'reviews': product.reviews_set.count(),
            'hover_image': hover_image_url,
            'rating': product.average_rating,
            'get_absolute_url': product.get_absolute_url(),
            'available_stock' : product.available_stock,
            'out_of_stock' : product.out_of_stock,
            'type' : product.product_type ,
            # ... other product fields
        })
    return JsonResponse(product_data, safe=False)


def filter_by_price(request , min_price , max_price ):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    subsubcategory = request.GET.get('subsubcategory')
    if subsubcategory != 'None':
        subsubcategory = slugify(subsubcategory)
        subsubcategory = subsubcategory.replace('-' , ' ')
        products = Product.objects.filter(Q(subsubcategory__name__iexact = subsubcategory) & Q(status = "Published"))       
    elif subcategory != 'None':
        subcategory = slugify(subcategory)
        subcategory = subcategory.replace('-' , ' ')
        products = Product.objects.filter(Q(subcategory__name__iexact = subcategory) & Q(status = "Published"))       

    elif category != 'None':
        category = slugify(category)
        category = category.replace('-' , ' ')
        products = Product.objects.filter(Q(category__name__iexact = category) & Q(status = "Published"))       
    else:
        products = Product.objects.filter(status = "Published").order_by('?')

    products = products.filter(discounted_price__range=(min_price , max_price))

    product_data = []
    for product in products:
        if product.product_images_set.first():
            hover_image_url = product.product_images_set.first().RelatedImages.url
        else:
            hover_image_url = None
        product_data.append({
            'id': product.id,
            'title': product.title,
            'quantity': product.quantity,
            'main_picture': product.main_picture.url,
            'discounted_price': product.discounted_price,
            'discount_perc': product.discount_perc,
            'selling_price': product.selling_price,
            'brand': product.brand.brand_name,
            'brand_url': product.brand.brand_url,
            'category': product.category.name,
            # 'subcategory': product.subcategory.name,
            'reviews': product.reviews_set.count(),
            'hover_image': hover_image_url,
            'rating': product.average_rating,
            'get_absolute_url': product.get_absolute_url(),
            'available_stock' : product.available_stock,
            'out_of_stock' : product.out_of_stock,
            'type' : product.product_type ,
            # ... other product fields
        })
    return JsonResponse(product_data, safe=False)

def update_total(request):
    payment_method = request.GET.get('paymentMethod')
    cart = Cart.objects.get(cart_id = _cart_id( request))
    if payment_method == 'Cash On Delivery':
        cart = Cart.calculate_cart_amount_on_cash(cart)
        data = {'amount':cart['amount'],'totalAmount':cart['total_amount'],'shipping':cart['shipping_amount']}
    else:
        cart = Cart.Cart_amount_on_credit_card(cart)
        data = {'amount':cart['amount'],'totalAmount':cart['total_amount'],'shipping':cart['shipping_amount'] ,'fix_discount':cart['fix_discount'] }
    return JsonResponse(data)


# def send_order_receipt_email(request):
       
    # Fetch the orders for the current user
    orders = Orderplaced.objects.filter(user=request.user)
    # Get the last order
    first_order = Orderplaced.objects.filter(user=request.user).last()
    customer = first_order.customer
    # Get the customer's email
    user_email = customer.email
    # Email subject
    subject = 'Order-Recipt Order Placed'
    # Email recipient
    to_email = user_email
    # Email sender
    from_email = 'zmuzammil74@gmail.com'
    # Total price of the orders
    total_price = sum([order.product.discounted_price * order.quantity for order in orders])

    # Render the HTML template
    template = get_template('app/general_5.html')
    context = {'orders': orders, 'amount': total_price, 'first_order': first_order}
    message = render_to_string('app/index.html',context)
    inline_html = transform(message)
    sent = send_mail(subject, inline_html, "Shopzy Store", [to_email], html_message=inline_html)
    # Check if the email was sent successfully
    if sent > 0:
        print("Email sent successfully")
    else:
        print("Failed to send email")
    return redirect('/orders/')

def quick_view(request):
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id = product_id)
    return render(request , 'app/quick-view.html', {'product' : product})

def subcategories_view(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(parent_category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
    

def subsubcategories_view(request):
    subcategory_id = request.GET.get('subcategory')
    subcategories = SubSubcategory.objects.filter(parent_subcategory_id=subcategory_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
    
    
def information_detail(request , name):
    title = slugify(name)
    title = title.replace('-' , ' ')
    information = Information.objects.get(url = name)
    return render(request , 'app/information.html' , {'information' : information})


def order_detail(request , id):
    order = Order.objects.get(id = id)
    return render(request, 'app/order-detail.html', {'order':order})
    
@login_required
def wishlist(request):
    wishlists = WishList.objects.filter(user = request.user)
    return render(request , 'app/wishlist.html' , {'wishlists' : wishlists} )

# def send_order_receipt_email(request):
   
#     # Fetch the orders for the current user
#     orders = Orderplaced.objects.filter(user=request.user)
#     # Get the last order
#     first_order = Orderplaced.objects.filter(user=request.user).last()
#     customer = first_order.customer
#     # Get the customer's email
#     user_email = customer.email
#     # Email subject
#     subject = 'Order-Recipt Order Placed'
#     # Email recipient
#     to_email = user_email
#     # Email sender
#     from_email = 'zmuzammil74@gmail.com'
#     # Total price of the orders
#     total_price = sum([order.product.discounted_price * order.quantity for order in orders])

#     # Render the HTML template
#     template = get_template('app/general_5.html')
#     context = {'orders': orders, 'amount': total_price, 'first_order': first_order}
#     html = render_to_string('app/index.html',context)
#     inline_html = transform(html)
#     # Create the email
#     email = EmailMultiAlternatives(
#             subject,
#             inline_html,
#             "Riode Store Order Recipt",
#             [to_email, 'zmuzammil74@gmail.com'],
#     )
#     # Attach the HTML
#     email.attach_alternative(html, 'text/html')

#     # Convert the HTML to PDF
#     pdf_file = open("template.pdf", "w+b")
#     pisa_status = pisa.CreatePDF(html, dest=pdf_file)
#     pdf_file.seek(0)
#     # Attach the PDF
#     email.attach("template.pdf", pdf_file.read(), "application/pdf")
#     pdf_file.close()
#     # Send the email
#     sent = email.send()

#     # Check if the email was sent successfully
#     if sent > 0:
#         print("Email sent successfully")
#     else:
#         print("Failed to send email")
#     return redirect('/orders/')



# ------------------------ For DashBoard-------------------------------------

def order_info(request , id):
    order = Order.objects.get(id = id)
    return render(request , 'admin/order_info.html' , {'order':order})

def sale_report(request):
    
    products = Product.objects.all()
    sales_data = []
    for product in products:
        quantity_sold = OrderItem.objects.filter(product = product).aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_sales = quantity_sold * product.discounted_price
        sales_data.append({'product' : product , 'quantity_sold' : quantity_sold , 'total_sales'  : total_sales})
    return render(request , 'app/sale_report.html', {'sales_data':sales_data})

def product_sales(request):
    sales_data = {}
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    order_status = request.GET.get('order_status')

    start_date = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    orders = Order.objects.filter(date__range = (start_date , end_date) )
    if order_status != "0":
        orders = orders.filter(status__iexact = order_status)
    for order in orders:
        orderitems = order.orderitem_set.all()
        for items in orderitems:
            product_name = items.product.title
            product_img = items.product.main_picture.url
            if product_name not in sales_data:
                sales_data[product_name] = {'quantity_sold' : 0 , 'total_sales'  : 0 }
            sales_data[product_name]['quantity_sold'] += items.quantity
            sales_data[product_name]['total_sales'] += items.quantity * items.product.discounted_price
            sales_data[product_name]['product_img'] = product_img
    return JsonResponse(sales_data)

def Customer_data(request):
    customer_data = {}
    users = User.objects.all()
    for user in users:
        customers = Order.objects.filter(user = user)
        for customer in customers:
            customer_name = customer.user if customer.user.username != " " else customer.user.first_name
            if customer_name not in customer_data:
                customer_data[customer_name] = {'orders' : 0 , 'total_spend' : 0 , 'email' : customer.user.email}
            customer_data[customer_name]['orders'] = customers.count() 
            customer_data[customer_name]['total_spend'] += customer.total_amount
    return render(request , 'app/customer.html' , {'customer_data' : customer_data})


def analytics_overview(request , period):
    now = datetime.datetime.now()
    if period == 'today':
        today_sale = Order.objects.filter(date__date = now.date())
        today_sale_amount = today_sale.annotate(hour=TruncHour('date')).values('hour').annotate(amount=Sum('total_amount'))  
        sales = [sale['amount'] for sale in today_sale_amount]
        x_axis_labels = [f"{sale['hour'].strftime('%I:%M:%p')}" for sale in today_sale_amount]  
        product_sold =  today_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        orders = today_sale.count()
        total_sales = today_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = today_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
    
    if period == 'yesterday':
        
        yesterday = now - datetime.timedelta(days=1)
        yesterday_sale = Order.objects.filter(date__date = yesterday)
        yesterday_sale_amount = yesterday_sale.annotate(hour=TruncHour('date')).values('hour').annotate(amount=Sum('total_amount'))  
        sales = [sale['amount'] for sale in yesterday_sale_amount]
        x_axis_labels = [f"{sale['hour'].strftime('%I:%M:%p')}" for sale in yesterday_sale_amount] 
        orders = yesterday_sale.count()
        product_sold =  yesterday_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        total_sales = yesterday_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = yesterday_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
        
    elif period == 'week':
        
        last_week_start = now - datetime.timedelta(days=7)
        week_sale = Order.objects.filter(date__gte=last_week_start, date__lte=now)
        week_sale_amount = week_sale.annotate(week=TruncDay('date')).values('week').annotate(amount=Sum('total_amount'))
        sales = [sale['amount'] for sale in week_sale_amount]
        x_axis_labels = [f"{sale['week'].strftime('%Y-%m-%d')}" for sale in week_sale_amount]        
        orders = week_sale.count()
        product_sold =  week_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        total_sales = week_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = week_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
        
    elif period == 'month':
        # Retrieve data for the current month
        month_sale = Order.objects.filter(date__month=now.month)
        month_sale_amount = month_sale.annotate(month=TruncDay('date')).values('month').annotate(total_sales=Sum('total_amount'))
        sales = [sale['total_sales'] for sale in month_sale_amount]
        x_axis_labels = [f"{sale['month'].strftime('%Y-%m-%d')}" for sale in month_sale_amount]   
        orders = month_sale.count()
        product_sold =  month_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        total_sales = month_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = month_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
             
    elif period == 'quarter':
        today = date.today()
        quarter = (today.month - 1) // 3 + 1
        quarterly_sale = Order.objects.filter(date__year=today.year, date__quarter__lte=quarter)
        quarterly_sale_amount = quarterly_sale.annotate(quarter=TruncQuarter('date')).values('quarter').annotate(total_sales=Sum('total_amount'))
        sales = [sale['total_sales'] for sale in quarterly_sale_amount]
        x_axis_labels = [f"{sale['quarter'].strftime('%B')} {sale['quarter'].year}" for sale in quarterly_sale_amount]
        orders = quarterly_sale.count()
        product_sold =  quarterly_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        total_sales = quarterly_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = quarterly_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
        
    elif period == 'year':

        yearly_sale = Order.objects.filter(date__year=now.year)
        yearly_sale_amount = yearly_sale.annotate(year=TruncMonth('date')).values('year').annotate(total_sales=Sum('total_amount'))
        sales = [sale['total_sales'] for sale in yearly_sale_amount]
        x_axis_labels = [f"{sale['year'].strftime('%B')} {sale['year'].year}" for sale in yearly_sale_amount]
        orders = yearly_sale.count()
        product_sold =  yearly_sale.aggregate(product_sold=Sum('orderitem__quantity'))['product_sold']      
        total_sales = yearly_sale.aggregate(total_sales=Sum('total_amount'))['total_sales']
        net_sales = yearly_sale.aggregate(net_sales=Sum('sub_total'))['net_sales']
        
    context = {'dates': x_axis_labels, 'amounts': sales , 'orders' : orders , 'total_sales' : total_sales , 'net_sales' : net_sales , 'product_sold' : product_sold}
    return render(request, 'app/analytics_overview.html', context)


#def print_invoice_view(request, object_id):
    # Retrieve the order object
    
    order = Order.objects.get(id=  object_id)

    # Generate the invoice PDF using a template and context
    context = {'order': order}
    template = get_template('app/invoice2.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.id}.pdf'
    pisa.CreatePDF(html, dest=response, encoding='utf-8')

    return response

def add_product(request):
    if request.method == "POST":
        files = request.FILES.getlist('RelatedImages')
        if files:
            for i in files:
                Product_images.objects.create( RelatedImages = i)
    else:
        imageform = Product_imagesForm()    
    
    context = {'imageform' : imageform}
    return render(request, 'app/add_product.html' , context) 

def track_order(request):
    if request.method == "POST":
        order_form = TrackOrderForm(request.POST)
        if order_form.is_valid():
            order_id = order_form.cleaned_data['order_id']
            Billing_email = order_form.cleaned_data['Billing_email']
            try:
                order = Order.objects.get(Q(id = order_id) & Q(biling_address__email = Billing_email))
                return redirect(f'/order-detail/{order.id}', {'order' : order})
            except Order.DoesNotExist:
                order_form.add_error(None , 'Sorry, the order could not be found. Please contact us if you are having difficulty finding your order details.')
    else:
        order_form = TrackOrderForm()
    return render(request , 'app/track-order.html' , {'form' : order_form})
    

def order_modal(request , id):
    try:
        order = Order.objects.get(id = id)
        order_item_data = []
        order_items = order.orderitem_set.all()
        for item in order_items:
            if item.variant and item.variant.price:
                per_price = item.quantity * item.variant.price
            else:
                per_price = item.quantity * item.product.discounted_price
            order_item_data.append({
                'product' : Product.objects.get(id = item.product.id ).title,
                'variant' : ProductVariation.objects.get(id = item.variant).attributes if item.variant else None,
                'quantity' : item.quantity ,
                'per_price' : per_price ,
            })
        billing_address = list(BilingAddress.objects.filter(id = order.biling_address.id).values())
        return JsonResponse( {'total_amount' : order.total_amount , 'subtotal' : order.sub_total , 'shipping_rate' : order.flat_shipping_rate , 'payment_method' : order.payment_method, 'id' : order.id , 'date' : order.date.date() , 'billing_address' : billing_address , 'orderitem' : order_item_data})    
    except Order.DoesNotExist: 
        return JsonResponse({'status' : 'error' })    

def handler404(request, exception):
    return render(request, 'app/404.html', status=404)

def export_products(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv" '
    writer = csv.writer(response)
    writer.writerow( ['ID' , 'Title' , 'Discounted (Original) Price' , 'Quantity' , 'Main Picture' , 'Available Stock' , 'Brand' , 'Category' , 'SubCategory' , 'SubSubCategory' , 'Status' , 'Product Type' , 'Short Description' , 'Long Description'])
    products = Product.objects.all()
    for product in products:
        
        writer.writerow([product.id , product.title , product.discounted_price , product.quantity , product.main_picture , product.available_stock , product.brand.brand_name , product.category.name , product.subcategory.name , product.subsubcategory.name , product.status , product.product_type , product.short_description , product.long_description])

    return response

#def export_sale_report(request , period):

    # Create a new Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook('sale_report.xlsx')
    worksheet = workbook.add_worksheet()

    # Define cell formats for different sections
    header_format = workbook.add_format({'bold': True, 'font_size': 10})
    date_format = workbook.add_format({'num_format': 'dd-mmm'})
    number_format = workbook.add_format({'num_format': '#,##0.00'})

    # Write the header row
    worksheet.write('A1', 'SALE REPORT', header_format)
    worksheet.write('A2', 'For The period of', header_format)

    # Write the column headers
    worksheet.write('A4', 'Date')
    worksheet.write('B4', 'Invoice No')
    worksheet.write('C4', 'EmailAddress')
    worksheet.write('D4', 'Product')
    worksheet.write('E4', 'Quantity')
    worksheet.write('F4', 'Pro. Pirce')
    worksheet.write('G4', 'Amount')
    worksheet.write('H4', 'Shipping fee')
    worksheet.write('I4', 'Total Amount')

    row = 5  # Start writing data from row 5

    now = datetime.datetime.now()
    if period == 'today':
        current_date = now.date()
        worksheet.write('B2', f'{ current_date }', header_format)
        orders = Order.objects.filter(date__date = now.date())
    # Loop through the data and write rows
    
    elif period == 'yesterday':
        yesterday = now - datetime.timedelta(days=1)
        worksheet.write('B2', f' { yesterday } ', header_format)
        orders = Order.objects.filter(date__date = yesterday)
        
    elif period == 'weekly':
        current_date = now.date()
        last_week_start = now - datetime.timedelta(days=7)
        worksheet.write('B2', f' { last_week_start } To { current_date } ', header_format)
        orders = Order.objects.filter(date__gte=last_week_start, date__lte=now)
    
    elif period == 'monthly':
        # Retrieve data for the current month
        month_name = now.strftime("%b") 
        worksheet.write('B2', f' { month_name } ', header_format)
        orders = Order.objects.filter(date__month=now.month)
        
    elif period == 'quarterly':
        today = date.today()
        quarter = (today.month - 1) // 3 + 1
        orders = Order.objects.filter(date__year=today.year, date__quarter__lte=quarter)
        strt_time = orders.first().date.date()
        last_time = orders.last().date.date() 
        worksheet.write('B2', f' { strt_time } To { last_time } ', header_format)
        
    elif period == 'yearly':
        
        worksheet.write('B2', f' { now.year } ', header_format)
        orders = Order.objects.filter(date__year=now.year)
        
    # orders = Order.objects.all()

    for order in orders:
        order_items = order.orderitem_set.all()  # Get the related OrderItem objects
        
        # Calculate shipping fee and total amount for the order
        invoice_no = order.id
        order_date = order.date.strftime('%d-%b-%Y') 
        email = order.biling_address.email
        shipping_fee = order.flat_shipping_rate
        total_amount = sum(item.quantity * item.product.discounted_price for item in order_items)
        for item in order_items:
            invoice_no = order.id if item == order_items.first() else ''  # Invoice number only for the first order item
            email = order.biling_address.email if item == order_items.first() else ''  # Email address only for the first order item
            
            worksheet.write(row, 0 ,  order_date if item == order_items.first() else '' , date_format)  # Format the date as desired
            worksheet.write(row, 1, invoice_no)
            worksheet.write(row, 2, email)
            worksheet.write(row, 3, item.product.title)
            worksheet.write_number(row, 4, item.quantity)
            worksheet.write_number(row, 5, item.product.discounted_price, number_format)
            worksheet.write_number(row, 6, item.quantity * item.product.discounted_price, number_format)
            worksheet.write(row, 7, shipping_fee if item == order_items.first() else '')
            worksheet.write(row, 8, total_amount if item == order_items.first() else '')
            
            row += 1

    # Set column widths
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 12)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)

    # Close the workbook
    workbook.close()
    # Prepare the HTTP response with the Excel file
    with open('sale_report.xlsx', 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={period} sale report.xlsx'

    return response

def check_flashsale(request):
    try:
        flash_sale = FlashSale.objects.get(end_time__lte = timezone.now())
        for item in flash_sale.flashsaleitem_set.all():
            product = item.product
            product.discounted_price = product.original_selling_price
            product.save()
        #     item.delete()
        # flash_sale.delete()
    except FlashSale.DoesNotExist:
        None
    return render(request , 'app/404.html')   


def error_404(request , exception):
        return render(request,'app/404.html', context={'status': 404} )

def error_500(request):
        return render(request,'app/404.html',context={'status': 500})
