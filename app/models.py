from django.db import models
from django.db.models import Avg
# from django.contrib.auth.models import User
from accounts.models import User
from django.utils.text import slugify
import math
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db.models import Q , Sum
from django.core.validators import MinValueValidator , MaxValueValidator
# Create your models here.

OTHER_CITY = 'Other'

CITY_CHOICES = (
    ('Karachi', 'Karachi'),
    ('Hyderabad', 'Hyderabad'),
    ('Lahore', 'Lahore'),
    ('Multan', 'Multan'),
    ('Peshawar', 'Peshawar'),
    ('Islamabad', 'Islamabad'),
    ('Quetta', 'Quetta'),
    ('Faisalabad', 'Faisalabad'),
    (OTHER_CITY, 'Other'),
)
class BilingAddress(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    address = models.CharField( max_length=500)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=11)
    area = models.CharField( max_length=200)
    
    def is_other_city(self):
        return self.city == self.OTHER_CITY
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    address = models.CharField( max_length=500)
    city = models.CharField(choices = CITY_CHOICES ,max_length=100)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=11)
    area = models.CharField( max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = RichTextField(blank=True, null=True)
    meta_tag_title = models.CharField(max_length=250 , blank=True , null=True)
    meta_tag_description = models.CharField(max_length=320 , blank=True , null=True)
    meta_tag_keywords = models.CharField(max_length=320 , blank=True , null=True)
    category_logo = models.ImageField( upload_to='categoryimg' , blank=True , null=True , default=None)
    
    def __str__(self):
        return str(self.name)
    
    def url(self):
        slug = slugify(self.name)
        slug = slug.replace(' ' , '-')
        url = reverse('shop' , args=[slug])
        return url

class Subcategory(models.Model):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True , null=True)
    meta_tag_title = models.CharField(max_length=250 , blank=True , null=True)
    meta_tag_description = models.CharField(max_length=320 , blank=True , null=True)
    meta_tag_keywords = models.CharField(max_length=320 , blank=True , null=True)
    subcategory_logo = models.ImageField( default="" ,blank=True , null=True , upload_to='subcategoryimg')
    
    def __str__(self):
        return str(self.name)
    
    def url(self):
        slug = slugify(self.name)
        slug1 = slugify(self.parent_category)
        slug = slug.replace(' ' , '-')
        slug1 = slug1.replace(' ' , '-')
        url = reverse('shop' , args=[slug1 , slug])
        return url
    

class SubSubcategory(models.Model):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent_subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True , null=True)
    meta_tag_title = models.CharField(max_length=250 , blank=True , null=True)
    meta_tag_description = models.CharField(max_length=320 , blank=True , null=True)
    meta_tag_keywords = models.CharField(max_length=320 , blank=True , null=True)
    subsubcategory_logo = models.ImageField( default="" , blank=True , null=True, upload_to='subsubcategoryimg')
    
    def __str__(self):
        return str(self.name)
    
    def url(self):
        slug = slugify(self.parent_category)
        slug = slug.replace(' ' , '-')
        slug1 = slugify(self.parent_subcategory)
        slug1 = slug1.replace(' ' , '-')
        slug2 = slugify(self.name)
        slug2 = slug2.replace(' ' , '-')
        url = reverse('shop' , args=[slug , slug1 ,slug2])
        return url
    
class Banner(models.Model):
    image = models.ImageField(upload_to = 'banner', height_field=None, width_field=None, max_length=None)
    mobile_image = models.ImageField( upload_to='mobileBanner', height_field=None, width_field=None, max_length=None , default="")
    url = models.URLField(max_length = 300 , blank=True , null=True , default="")
    
class TopCategory(models.Model):
    image = models.ImageField(upload_to = 'topCategory', height_field=None, width_field=None, max_length=None)
    url = models.URLField(max_length = 300 , blank=True , null=True , default="")
    

class Brand(models.Model):
    brand_name = models.CharField( max_length=200)
    brand_logo = models.ImageField(upload_to='brandimg', height_field=None, width_field=None)
    brand_url = models.CharField(max_length=200)
    brand_description = RichTextField(blank=True, null=True , default="")
    meta_tag_title = models.CharField(max_length=250 , blank=True , null=True)
    meta_tag_description = models.CharField(max_length=320 , blank=True , null=True)
    meta_tag_keywords = models.CharField(max_length=320 , blank=True , null=True)

    def __str__(self):
        return str(self.brand_name)
    
STOCK_CHOICES = (
    ('In Stock', 'In Stock'),
    ('Out of Stock', 'Out of Stock')
)       
    
PRODUCT_STATUS = (
    ('Published', 'Published'),
    ('Draft', 'Draft'),
)    
PRODUCT_CHOICE = (
    ('1' , 'Simple Product'),
    ('2' , 'Variable Product'),
)    

class Product(models.Model):
    published_date = models.DateField( auto_now=True, auto_now_add=False)
    SKU_number = models.CharField(max_length=50 )
    url = models.CharField(max_length=250 , default='')
    title = models.CharField( max_length=200)
    selling_price = models.FloatField(blank=True , null=True)
    discounted_price = models.FloatField()
    original_selling_price = models.FloatField(editable=False , null= True)
    quantity = models.PositiveIntegerField(blank=True , null=True)
    main_picture = models.ImageField(upload_to='mainimg')
    available_stock = models.CharField( choices=STOCK_CHOICES , default="In Stock" , max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default='')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE , default='' , blank=True , null=True)
    subsubcategory = models.ForeignKey(SubSubcategory, on_delete=models.CASCADE , default='' , blank=True , null=True)
    short_description = RichTextField(blank=True, null=True , default="")
    long_description = RichTextField(blank=True, null=True , default="")
    meta_tag_title = models.CharField(max_length=250 , blank=True , null=True)
    meta_keywords = models.CharField(max_length=320,blank=True , null=True)
    meta_description = models.CharField(blank=True , null=True, max_length=320)
    status = models.CharField(choices=PRODUCT_STATUS , default="Published" , max_length=50)
    product_type = models.CharField(choices=PRODUCT_CHOICE , default="1" , max_length=50 , blank=True , null=True)
    show_in_bestseller_slider = models.BooleanField(default=False)   
     
    def __str__(self):
        return str(self.title) or ''
    
    @property
    def discount_perc(self):
        if self.selling_price:
            return round((self.selling_price - self.discounted_price)/100)
    
    @property
    def average_rating(self):
        reviews = self.reviews_set.all()
        average = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews else 0
        return  (average * 100 ) / 5
    
    @property
    def out_of_stock(self):
        if self.quantity:
            if self.quantity >= 1  and self.available_stock == 'Out of Stock':
                return True
        elif self.available_stock == 'Out of Stock' :
            return True
        else:
            return False
    
    def get_absolute_url(self):
        # create a slugified version of the title
        # slug1 = slugify(self.category.name)
        # slug2 = slugify(self.subcategory.name)
        # # replace spaces with hyphens
        # slug1 = slug1.replace(' ', '-')
        # slug2 = slug2.replace(' ', '-')
        # construct the URL using the slug and the primary key
        url = reverse('product_detail', args=[self.url, self.SKU_number])
        return url
    
    @property
    def has_active_flash_sale(self):
        now = timezone.now()
        active_flash_sales = FlashSale.objects.filter( Q(start_time__lte=now) | Q(start_time__gte=now) , flashsaleitem__product=self , end_time__gt=now)
        return active_flash_sales.exists()

    def get_flash_sale_remaining_time(self):
        if not self.has_active_flash_sale:
            return None
        now = timezone.now()
        active_flash_sale = FlashSale.objects.get(Q(start_time__lte=now) | Q(start_time__gte=now)  , flashsaleitem__product=self, end_time__gt=now)
        return active_flash_sale.end_time - now

    def save(self, *args, **kwargs):
        is_flash_sale_update = kwargs.pop('flash_sale_update', False)
        if self.pk :
            print("Self.pk exist")        
            if not is_flash_sale_update and self.original_selling_price != self.discounted_price:
                self.original_selling_price = self.discounted_price
        else:
            print("Self.pk not  exist")
            self.original_selling_price = self.discounted_price
        super(Product, self).save(*args, **kwargs)

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , blank=True , null= True , default="")
    attributes = models.ForeignKey(ProductAttributeValue , on_delete=models.CASCADE , default=None)
    sku = models.CharField(max_length=100 , blank=True , null=True , default="" )
    price = models.FloatField( blank= True , null= True , default= "")

    def __str__(self):
        return str(f'{self.product} - {self.attributes} ')

class FlashSale(models.Model):
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    
class FlashSaleItem(models.Model):
    FlashSale = models.ForeignKey(FlashSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    flash_sale_price = models.IntegerField()
    
    def save(self , *args, **kwargs):
        super(FlashSaleItem , self).save(*args, **kwargs)
        original_product = Product.objects.get(pk= self.product.pk)
        original_product.discounted_price = self.flash_sale_price
        original_product.save(flash_sale_update=True)
        print('------------flash price save---------')
        
        

class Sale(models.Model):
    sale_name = models.CharField( max_length=50)
    descripion = RichTextField(blank=True , null= True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    
class SaleItem(models.Model):
    Sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    sale_price = models.IntegerField()    

REVIEWS_STATUS = (
    ( 'APPROVED' , 'APPROVED' ),
    ( 'DENIED' , 'DENIED' ),
)    
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50)
    description = models.TextField(blank=True , null=True , default="")
    discount = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    coupon_expire_date = models.DateField( auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return str(self.coupon_code)

class Reviews(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField( max_length=50)
    email = models.EmailField(max_length=254)
    comment = models.TextField()
    status = models.CharField( choices=REVIEWS_STATUS , default="DENIED", max_length=50)
    
    @property
    def average_rating(self):
        reviews = self.rating
        return  (reviews * 100 ) / 5
    
class Product_images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    RelatedImages = models.ImageField( upload_to='relatedimage')
    
    def __str__(self):
        return str(self.RelatedImages) or ''
    
class Cart(models.Model):
    cart_id = models.CharField( max_length=100 , default="" , blank=True , null=True)
    subtotal = models.PositiveIntegerField(blank=True , null=True , default=0) 
    total = models.PositiveIntegerField(blank=True , null=True , default=0)
    coupon = models.ForeignKey(Coupon,  on_delete=models.CASCADE , blank=True , null=True , default=None)
    coupon_discount = models.IntegerField( blank=True  , null=True , default=0 )
    total_quantity = models.PositiveIntegerField(default=0)
    shipping_rate = models.PositiveIntegerField(default=0 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.cart_id)
    
    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)
    
    def update_totals(self , force_update = False):
        try: 
            shipping_rate = ShippingCalculation.objects.first().flat_rate
        except ShippingCalculation.DoesNotExist:
            shipping_rate = 0
        cart_items = CartItem.objects.filter(cart=self)
        subtotal = 0
        for item in cart_items:
            subtotal += item.per_price
        self.shipping_rate = shipping_rate
        self.subtotal = subtotal
        self.total_quantity = sum(item.quantity for item in self.cartitem_set.all())
        if self.coupon:
            print(self.coupon , 'coupon')
            self.coupon_discount = math.ceil( ( self.subtotal / 100 ) * self.coupon.discount)
            self.total = ( self.subtotal + float( self.shipping_rate ) ) - self.coupon_discount  # You can apply any additional calculations or discounts here
        else:
            self.total = self.subtotal + self.shipping_rate
        print(self.total)    
        self.save()
        
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , null=True )
    date = models.DateTimeField( auto_now=True )
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default = 1)

    @property
    def per_price(self):
        if self.variant and self.variant.price :
            return self.quantity * self.variant.price
        else:    
            return self.quantity * self.product.discounted_price
        
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_totals()

    @staticmethod
    def calculate_cart_amount_on_cash(carts):
        total_amount = 0.0
        amount = 0.0
        shipping_amount = ShippingCalculation.objects.first().flat_rate
        quantity = 0
        for cart in carts:
            quantity += cart.quantity
            if cart.variant and cart.variant.price:
                amount += cart.quantity * cart.variant.price
            else:
                amount += cart.quantity * cart.product.discounted_price
        if cart.coupon:
            amount = ( amount / 100 ) * cart.coupon.discount   
        total_amount = amount + shipping_amount
        return {'total_amount': total_amount, 'amount': amount, 'shipping_amount': shipping_amount, 'quantity': quantity}
    
class WishList(models.Model):
    date = models.DateTimeField( auto_now=True )
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.user)


    
    
class ShippingCalculation(models.Model):
    
    flat_rate = models.IntegerField()
    bank_account_detail = models.TextField(blank=True , null=True)
    
STATUS_CHOICES = (
    ('ACCEPTED','ACCEPTED'),
    ('PACKED','PACKED'),
    ('PENDING','PENDING'),
    ('ON THE WAY','ON THE WAY'),
    ('DELEIVERED','DELEIVERED'),
    ('CANCEL','CANCEL'),
    ('RETURN','RETURN'),
)

PAYMENT_CHOICES = (
    ('Cash On Delivery','Cash On Delivery'),
    ('Manual Bank Transfer','Manual Bank Transfer'),
)

class Order(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE , null=True)
    biling_address = models.ForeignKey( BilingAddress , on_delete=models.CASCADE , default=None , blank=True , null= True)
    shipping_address = models.ForeignKey( ShippingAddress , on_delete=models.CASCADE , default=None , blank=True , null= True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(choices= STATUS_CHOICES , default = 'PENDING', max_length=50)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=50)
    sub_total = models.PositiveIntegerField(blank=True , null=True)
    flat_shipping_rate = models.CharField(max_length=50 , default = "" , blank=True , null=True)
    total_amount = models.PositiveIntegerField(default=0 , blank=True , null=True)
    notes = models.TextField(blank=True , null=True , default="")
    def __str__(self):
        return f'Order {self.id} by {self.user}'

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariation , on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default = 1)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.title} in Order {self.order.id} by {self.order.user}'
    
    @property
    def per_price(self):
        if self.variant and self.variant.price :
            return self.quantity * self.variant.price
        else:    
            return self.quantity * self.product.discounted_price

    
class Information(models.Model):
    information_title = models.CharField(max_length=100)
    url = models.CharField( max_length=100)
    description = models.TextField()
    meta_tag_title = models.CharField( default="" , max_length=100 , blank=True , null=True)
    meta_tag_keywords = models.TextField(  blank=True , null=True)
    meta_tag_description = models.TextField(  blank=True , null=True)
    status = models.CharField( choices=PRODUCT_STATUS, max_length=100 , blank=True , null=True , default="Published")
    def __str__(self): 
        return str(self.information_title)

    def get_absolute_url(self):
        slug = slugify(self.information_title)
        slug = slug.replace('' , '-')
        return reverse("Information_detail", kwargs={"pk": self.pk} , args=[slug])

class FeaturedOffer(models.Model):
    offer_image = models.ImageField( upload_to='featuredOffer')
    url = models.URLField( max_length=500)
    
class CompanyDetail(models.Model): 
    company_name = models.CharField( max_length=100)
    phone = models.CharField( blank=True , null=True , default="" , max_length=50)
    email = models.EmailField(  blank=True , null=True , default="" , max_length=254)
    Address = models.CharField( blank=True , null=True , default="" , max_length=100)
    facebook_account = models.CharField( blank=True , null=True , default="" , max_length=100)
    instagram_account = models.CharField( blank=True , null=True , default="" , max_length=100)
    whatsapp_account = models.CharField( blank=True , null=True , default="" , max_length=100)
    

class NewsLetter(models.Model):
    email = models.EmailField( max_length=254 , default="")


