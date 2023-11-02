from django.urls import path,include , re_path
from django.views.generic import TemplateView , RedirectView
from django.contrib.auth import views as auth_view 
from app import views 
from app.admin import OrderModelAdmin
from app.forms import MyPasswordReset , MySetPasswordForm


urlpatterns = [
    re_path(r'^favicon\.ico$',RedirectView.as_view(url='/static/app/images/logo.png')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.base,name='/'),
    path('main/', views.base,name='main'),
    path('contact-us/', TemplateView.as_view(template_name = 'app/contact-us.html') ,name='contact-us'),
    path('faq/',TemplateView.as_view(template_name = 'app/faq.html') ,name='faq'),
    path('categories/', views.shop_categories,name='categories'),
    path('brand/<slug:brand>/', views.brands_product,name='brand'),
    path('brand/', views.brands_product,{'brand' : None},name='brand'),
    # path('product-detail/<int:id>/', views.product_deta, name='product-detail'),
    path('product/<str:product_url>/', views.product_detail, name='product_detail'),
    path('subcategories/', views.subcategories_view, name='subcategories_view'),
    path('subsubcategories/', views.subsubcategories_view, name='subsubcategories_view'),
    
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('cart/', views.showCart, name='show-cart'),
    path('plus_cart/', views.plus_cart, name='pluscart'),
    path('minus_cart/', views.minus_cart, name='minuscart'),
    path('delete_cart/', views.delete_cart, name='deletecart'),
    path('delete_wishlist/', views.delete_wishlist, name='deletewishlist'),
    path('update_total/', views.update_total, name='update-total'),
    path('quick-view/', views.quick_view, name='quick-view'),
    
    path('shop/', views.shop, {'category': None ,'subcategory': None , 'subsubcategory': None}, name='shop'),
    path('shop/<str:category>/', views.shop, {'subcategory': None , 'subsubcategory': None}, name='shop'),
    path('shop/<str:category>/<str:subcategory>', views.shop,{'subsubcategory': None}, name='shop'),
    path('shop/<str:category>/<str:subcategory>/<str:subsubcategory>/', views.shop , name='shop'),
    
    path('falshsale/' , views.flashSaleShop , name="falshsale"),
    
    # path('send-email/', views.send_order_receipt_email, name='send-email'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('account/', views.account, name='account'),
    path('address/', views.address, name='address'),
    path('orders/<int:id>/', views.orders, name='orders'),
    path('search/', views.search, name='search'),
    
    path('changepassworddone/', views.PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html'), name='changepassworddone'),
    
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset_form.html',form_class =MyPasswordReset , success_url = "/password-reset/done/" ), name='password_reset'),
    
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html' ), name='passwordresetdone'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class =MySetPasswordForm  ), name='password_reset_confirm'),
    
    path('password-reset-complete', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    
    path('category/<slug:name>/', views.category, name='category'),
    
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('filter-by-price/<int:min_price>/<int:max_price>/', views.filter_by_price, name='filter_by_price'),
    path('checkout/', views.checkout, name='checkout'),
    path('filter-products/<str:option>/<str:category>/', views.filter_products,   {'subcategory': '' , 'subsubcategory': ''}  , name='filter_products'),
    path('filter-products/<str:option>/<str:category>/<str:subcategory>/' , views.filter_products,  { 'subsubcategory': ''},  name='filter_products'),
    path('filter-products/<str:option>/<str:category>/<str:subcategory>/<str:subsubcategory>/', views.filter_products, name='filter_products'),
    
    
    path('select-variation/<str:product_id>/<str:variation>/', views.select_variation , name='select-variation'),
    
    
    path('filter-by-price/<int:min_price>/<int:max_price>/', views.filter_by_price, name='filter_by_price'),
    path('track-order/', views.track_order, name='track-order'),
    path('coupon-form/', views.coupon_form, name='coupon-form'),
    path('order_modal/<slug:id>/', views.order_modal, name='order_modal'),
    path('order-detail/<id>/', views.order_detail, name='order-detail'),
    # path('export-product/',views.export_products, name='export_products'),
    # path('export-sales-report/<str:period>/',views.export_sale_report, name='export_sales_report'),
    # path('reverse/', views.reverseGeocode, name='reverseGeocode'),
    
# ------------------------ For DashBoard-------------------------------------
    
    
    path('order-info/<id>/', views.order_info, name='order_info'),
    path('product-analytics/', views.sale_report, name='product-analytics'),
    path('product-sales/', views.product_sales, name='product-sales'),
    path('customer-analytics/', views.Customer_data, name='customer-analytics'),
    path('analysis/<str:period>/', views.analytics_overview, name='analysis'),
    # path('print-invoice/<int:object_id>/', views.print_invoice_view, name='app_order_print_invoice'),
    path('add-product/', views.add_product, name='add-product'),
    
    path('check/', views.check_flashsale, name='check'),
    
    
    path('<str:name>/', views.information_detail, name='information'),
]
