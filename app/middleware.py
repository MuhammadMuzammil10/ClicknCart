from django.utils import timezone
from django.utils import timezone
from django.contrib.sessions.models import Session
from datetime import timedelta

class UpdateLastVisitedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.session.session_key

        response = self.get_response(request)

        # Check if the session has changed
        for session in Session.objects.filter(expire_date__gte=timezone.now()):
            session_data = session.get_decoded()
            if '_auth_user_id' in session_data:
                user_id = session_data.get('_auth_user_id')
                if user_id:
                    session.user_id = user_id
                    session.last_seen = timezone.now()
                    session.save()

        # Update the online users count
        online_users = Session.objects.filter(expire_date__gte=timezone.now() - timedelta(minutes=15))
        online_user_count = online_users.count()
        # Add the number of active users to the request context
        request.active_users = online_user_count
        if request.user.is_authenticated:
            request.user.last_visited = timezone.now()
            request.user.last_visited_url = request.path
            request.user.save()
        response = self.get_response(request)
        
        return response
    
    
class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current session key if it exists
        session_key = request.session.session_key

        response = self.get_response(request)

        # Check if the session has changed
        if session_key != request.session.session_key:
            # If the session has changed, delete the old session
            Session.objects.filter(session_key=session_key).delete()

        # Update the session with the current time
        request.session['last_active_time'] = str(timezone.now())

        # Get the number of active sessions (users)
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        num_active_users = active_sessions.count()

        # Add the number of active users to the request context
        request.active_users = num_active_users

        return response