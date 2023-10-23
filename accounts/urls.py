from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns...
    path('accounts/facebook/login/callback/', views.facebook_login_callback, name='facebook_login_callback'),
    path('accounts/google/login/callback/', views.google_login_callback, name='google_login_callback'),
]
