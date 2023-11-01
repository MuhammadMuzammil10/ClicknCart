from django.contrib import admin
from django.forms import ModelChoiceField
from django.utils.translation import gettext_lazy as _
from app.models import BilingAddress , Product, Cart , CartItem , OrderItem ,Order, Product_images , Reviews , Brand , Banner , Category , Subcategory , FlashSale , ShippingCalculation , Information , SubSubcategory , CompanyDetail , NewsLetter , WishList , TopCategory , FeaturedOffer , ProductAttribute , ProductAttributeValue , ProductVariation , Coupon , FlashSaleItem , Sale , SaleItem
# Register your models here.
from .forms import ProductForm , BrandForm , InformationForm , Product_imagesForm , ProductAttributeForm , ProductAttributeValueForm , ProductVariationForm
from django.utils.html import format_html
from accounts.models import User
from django.utils.safestring import mark_safe
admin.site.register(User)
admin.site.register(Coupon)

class Product_imagesInline(admin.TabularInline):
    form = Product_imagesForm
    model = Product_images
    extra = 1

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue



class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

def make_best_seller(modeladmin, request, queryset):
    queryset.update(show_in_bestseller_slider=True)

make_best_seller.short_description = "Mark selected items as best seller"

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ ProductVariationInline]
    form = ProductForm
    list_display = ['id','title','discounted_price', 'quantity' ,'category','brand', 'show_in_bestseller_slider' , 'subcategory', 'subsubcategory']
    actions = [make_best_seller]
    def save_model(self, request, obj, form, change):
        # Save the main Product object first
        obj.save()

        # Get the list of related images from the form's file input field
        files = request.FILES.getlist('RelatedImages')
        if files:
            # Iterate over the files and create Product_images objects
            for file in files:
                Product_images.objects.create(product=obj, RelatedImages=file)

    # Include the additional form in the change form
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if request.method == 'POST':
            # Check if the related images form is valid
            imageform = Product_imagesForm(request.POST, request.FILES)
            if imageform.is_valid():
                files = request.FILES.getlist('RelatedImages')
                if files:
                    return super().add_view(request, form_url, extra_context)
                else:
                    pass
        else:
            imageform = Product_imagesForm()
        extra_context['imageform'] = imageform
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        try:
            relatedimages = Product_images.objects.filter(product = object_id)
            files = request.FILES.getlist('RelatedImages')
            if request.method == 'POST' and files:
                if relatedimages:
                    relatedimages.delete()
            extra_context['imageform'] = Product_imagesForm()
            extra_context['images'] = Product_images.objects.filter(product = object_id)
            return super().change_view(request, object_id, form_url, extra_context)
        except Product_images.DoesNotExist:
            pass
    # Override the save_model method to handle saving the related images form


class ProductAttributeAdmin(admin.ModelAdmin):
    form = ProductAttributeForm


class ProductAttributeValueAdmin(admin.ModelAdmin):
    form = ProductAttributeValueForm


admin.site.register(ProductVariation)
admin.site.register(Product_images)

@admin.register(BilingAddress)
class BilingAddressModelAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','address','city','zipcode','area']


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    form = BrandForm
    list_display = ['id' , 'brand_name' , 'brand_logo', 'brand_url']

@admin.register(Information)
class InformationModelAdmin(admin.ModelAdmin):
    form = InformationForm
    list_display = ['information_title']
    
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' ]
    
@admin.register(Subcategory)
class SubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id' ,'parent_category', 'name']
    
@admin.register(SubSubcategory)
class SubSubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id' ,'parent_category','parent_subcategory', 'name']
    
@admin.register(Banner)
class BanneryModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'image','url']


@admin.register(Reviews)
class ReviewsModelAdmin(admin.ModelAdmin):
    list_display = ['name','rating','comment','product','email']
    

    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','subtotal' , 'total']
    
    
@admin.register(WishList)
class WishListModelAdmin(admin.ModelAdmin):
    list_display = ['user','product' ]
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity' , 'variant']
    extra = 0
    can_delete = True

class FlashSaleItemInline(admin.TabularInline):
    model = FlashSaleItem
    fields = ['product', 'flash_sale_price' ]
    extra = 0
    can_delete = True

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    fields = ['product', 'sale_price' ]
    extra = 0
    can_delete = True

    

@admin.register(FlashSale)
class FlashSaleModelAdmin(admin.ModelAdmin):
    list_display = ['id','start_time' , 'end_time']
    inlines = [FlashSaleItemInline]

@admin.register(Sale)
class FlashSaleModelAdmin(admin.ModelAdmin):
    list_display = ['sale_name','start_time' , 'end_time']
    inlines = [SaleItemInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ['product', 'quantity' , 'variant']
    extra = 0
    can_delete = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'variant':
            product_id = request.resolver_match.kwargs.get('object_id')
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    pass
                else:
                    kwargs['queryset'] = ProductVariation.objects.filter(product=product)
                    kwargs['label'] = _('Variant')
                    return ModelChoiceField(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id','status'  , 'show_detail' ,'user','date','payment_method','total_amount')
    inlines = [OrderItemInline]
    search_fields = ['id','status','user','date','payment_method','total_amount']
    
    def show_detail(self, obj):
        return mark_safe('<a href="#" onclick="show_order_detail({0});"><i class="fa fa-eye"></i></a>'.format(obj.id))
    show_detail.allow_tags = True
    
    def order_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return format_html('<br>'.join([f'{item.product.title} - {item.quantity}' for item in items]))
    order_items.short_description = 'Order Items'

    def user(self, obj):
        return obj.user.username if obj.user else 'N/A'
    user.short_description = 'User'

    def total_amount(self, obj):
        return format_html(f"${obj.total_amount:,}")
    total_amount.short_description = 'Total Amount'
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        subtotal = 0
        shipping_amount = ShippingCalculation.objects.first().flat_rate
        for item in obj.orderitem_set.all():
            subtotal += item.product.discounted_price * item.quantity
        total = subtotal + shipping_amount
        obj.sub_total = subtotal
        obj.flat_shipping_rate = shipping_amount
        obj.total_amount = total
        obj.save()
        
    actions = ['change_status_bulk_action']  # Add your custom bulk action here

    # Define your custom bulk action
    def change_status_bulk_action(self, request, queryset):
        # Update the status field for selected objects
        queryset.update(status='DELEIVERED')  # Replace 'new_status' with the status you want to set

    change_status_bulk_action.short_description = 'Change status to Deleivered'  # Display name for the custom action

    
    
@admin.register(ShippingCalculation)
class ShippingCalculationModelAdmin(admin.ModelAdmin):
    list_display = ['id','flat_rate']
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)
    
    
@admin.register(CompanyDetail)
class CompanyDetailAdmin(admin.ModelAdmin):
    list_display = ['company_name' , 'phone']


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(TopCategory)
class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ['image' , 'url']

@admin.register(FeaturedOffer)
class FeaturedOfferAdmin(admin.ModelAdmin):
    list_display = ['offer_image' , 'url']

class RequiredModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field_name, field in form.base_fields.items():
            if field.required:
                field.label = f"{field.label} <span class='asterisk' style='color:red'>*</span>"
        return form