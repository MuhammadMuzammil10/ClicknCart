from django.shortcuts import render , redirect
from django.contrib.auth import login
from models import User
# Create your views here.
from allauth.socialaccount.models import SocialAccount

def facebook_login_callback(request):
    # Get the user's Facebook account information
    try:
        social_account = SocialAccount.objects.get(provider='facebook', user=request.user)
        facebook_data = social_account.extra_data
    except SocialAccount.DoesNotExist:
        # Handle the case where the user didn't log in with Facebook
        pass
    else:
        # Check if the user is registered on our site
        email = facebook_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Redirect to a registration page
                return redirect('/register/')
            else:
                # Log the user in using Django's built-in authentication system
                login(request, user)

    # Redirect to the homepage
    return redirect('/')
def google_login_callback(request):
    print("Google auth run...........................")
    # Get the user's Facebook account information
    try:
        social_account = SocialAccount.objects.get(provider='facebook', user=request.user)
        facebook_data = social_account.extra_data
    except SocialAccount.DoesNotExist:
        # Handle the case where the user didn't log in with Facebook
        pass
    else:
        # Check if the user is registered on our site
        email = facebook_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Redirect to a registration page
                return redirect('/register/')
            else:
                # Log the user in using Django's built-in authentication system
                login(request, user)

    # Redirect to the homepage
    return redirect('/')
