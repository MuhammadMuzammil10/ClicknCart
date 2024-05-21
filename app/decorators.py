# from django.shortcuts import redirect
# from django.contrib.auth.decorators import user_passes_test

# def custom_login_required(view_func):
#     """
#     Custom login required decorator that redirects to register page if user is not registered,
#     but redirects to login page if user is registered but not logged in.
#     """
#     def test_func(user):
#         return user.is_active

#     decorated_view_func = user_passes_test(
#         test_func,
#         login_url=None,
#         redirect_unauthenticated_users=True
#     )(view_func)
#     return decorated_view_func
