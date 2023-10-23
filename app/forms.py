from django import forms
from accounts.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from app.models import BilingAddress , Reviews , Product , Brand , Category , Subcategory , Information , SubSubcategory , Product_images , NewsLetter , ProductAttribute , ProductAttributeValue , ProductVariation

class BrandChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.brand_name
    
class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("__all__")
    
class InformationForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'richtext_field'}))
    class Meta:
        model = Information
        fields = ("__all__")
        
class Product_imagesForm(forms.ModelForm):
    RelatedImages = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}) , required=False)
    class Meta:
        model = Product_images
        fields = ("RelatedImages",)

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['name']

class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = [ 'attribute' , 'value']

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['sku', 'price', 'attributes']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("__all__")
        attrs = {'enctype': 'multipart/form-data'}

    brand = BrandChoiceField(queryset=Brand.objects.all(), empty_label = '--------')
    category = CategoryChoiceField(queryset=Category.objects.all(), empty_label='--------')
    subcategory = CategoryChoiceField(queryset=Subcategory.objects.all(), empty_label='--------')
    subsubcategory = CategoryChoiceField(queryset=SubSubcategory.objects.all(), empty_label='--------' , required=False)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.category_id:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(parent_category=self.instance.category_id)
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.all()
            
        if self.instance.subcategory_id:
            self.fields['subsubcategory'].queryset = SubSubcategory.objects.filter(parent_subcategory=self.instance.subcategory_id)
        else:
            self.fields['subsubcategory'].queryset = SubSubcategory.objects.all()
        self.fields['category'].widget.attrs['onChange'] = 'filterSubcategories(this.value);'
        self.fields['subcategory'].widget.attrs['onChange'] = 'filterSubSubcategories(this.value);'
        self.fields['product_type'].widget.attrs['onChange'] = 'ShowVariations(this.value);'
    
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        subsubcategory = cleaned_data.get('subsubcategory')
        if category and subcategory:
            if subcategory.parent_category != category:
                raise forms.ValidationError('The selected subcategory does not belong to the selected category.')
        if subcategory and subsubcategory:
            if subsubcategory.parent_subcategory != subcategory:
                raise forms.ValidationError('The selected Subsubcategory does not belong to the selected subcategory.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subcategory.parent_category = instance.category
        instance.subsubcategory.parent_subcategory = instance.subcategory
        if commit:
            instance.save()
        return instance

        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(
        attrs={"autofocus": True, 'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Password'}),
    )


class Registerationform(UserCreationForm):
    password1 = forms.CharField(label='Password: ', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password (again)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    email = forms.EmailField(required=True,label='Email',
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    class Meta:
        model = User
        fields = ['id', 'email', 'password1', 'password2']
        widgets = {}


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Current password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password",
                   "autofocus": True, 'class': 'form-control'}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class MyPasswordReset(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}),
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class ProfileForm(forms.ModelForm):
    
    
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

    city = forms.CharField( widget=forms.Select( choices=CITY_CHOICES ,  attrs={'class': 'form-control'}))

    def clean_city(self):
        city = self.cleaned_data.get('city')
        print(city , ' city function runs.....')
        if city not in [choice[0] for choice in self.CITY_CHOICES] or  city == '':
            raise forms.ValidationError('Select a valid choice or choose "Other" for city.')
        return city

    class Meta:
        model = BilingAddress
        fields = ['first_name', 'last_name', 'address', 'city', 'area', 'zipcode', 'phone', 'email']
        labels = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'address': 'Street Address *',
            'city': 'Town / City *',
            'area': 'Area *',
            'zipcode': 'ZIP *',
            'phone': 'Phone *',
            'email': 'Email Address *'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House number and street name'}),
            # 'city': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '03* ********'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''



class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name' , 'email' , 'comment']
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Name *'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email *'}),
            'comment' : forms.Textarea(attrs={'class' : 'form-control mb-4' , 'placeholder' : 'Comment *', 'cols' : '30' , 'rows' : '6'}),
        }

class TrackOrderForm(forms.Form):
    order_id = forms.CharField( max_length=50, required=True , label='Order ID' , label_suffix='' , widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Found in your order confirmation email.'}) ,error_messages={'required':'Please enter a valid order ID'})
    Billing_email = forms.EmailField(required=True , label='Billing email' , label_suffix='' , widget=forms.EmailInput(attrs={'class':'form-control' , 'placeholder':'Email you used during checkout.'}) ,error_messages={'required':'Please enter a valid email Address'})
    
class CouponForm(forms.Form):
    
    coupon_code = forms.CharField( max_length=50, required=True  , widget=forms.TextInput(attrs={'class':'input-text form-control ls-m mb-4' , 'placeholder':'Enter coupon code here...'}) ,error_messages={'required':'Please Enter a Coupon Code'})
    
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        labels = {'email' : ''}
        fields = ['email']
        widgets = {
            'email' : forms.EmailInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email Address here...'}),
        }
    
