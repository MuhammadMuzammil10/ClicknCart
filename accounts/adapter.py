from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.urls import resolve, Resolver404 
from django.shortcuts import redirect
from .models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    print("CustomAccountAdapter run")
    def pre_social_login(self, request, sociallogin):
        if not sociallogin.is_existing:
            # Auto-connect if there is only one social account registered
            # with the email address provided by the social provider.
            email_addresses = [email.email for email in sociallogin.email_addresses]
            accounts = SocialLogin.objects.filter(
                provider__in=['google', 'facebook'],
                account__email__in=email_addresses
            ).exclude(user=sociallogin.user)
            if accounts.exists():
                # Just connect the account with the social login.
                sociallogin.connect(accounts.first())
            else:
                sociallogin.autoconnect = True
        return super().pre_social_login(request, sociallogin)
    def save_user(self, request, user, form, commit=True):
        print("CustomAccountAdapter save function run")
        user = super().save_user(request, user, form, commit=False)
        print(form)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.custom_field = form.cleaned_data['custom_field']
        if commit:
            user.save()
        return user
    def get_login_redirect_url(self, request):
        redirect_url = request.session.get('next', '/')
        print(redirect_url , 'redirect url')
        return redirect_url