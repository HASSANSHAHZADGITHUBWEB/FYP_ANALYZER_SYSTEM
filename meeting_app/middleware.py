# # middleware.py
# from django.shortcuts import redirect
# from django.conf import settings

# class LoginRequiredMiddleware:
#     """
#     Middleware to ensure that a user is authenticated before accessing
#     specific views.
#     """
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Define the URL patterns that should be protected
#         protected_urls = ['/add_user/', '/dashboard/','/all-marks/','/marksheet/','/add-marks/']  # Add any other protected URLs

#         # Check if the user has successfully logged in
#         user_logged_in = self.is_user_logged_in(request)

#         # Check if the request path is in protected URLs and the user is not logged in
#         if request.path in protected_urls and not user_logged_in:
#             return redirect(settings.LOGIN_URL)  # Redirect to the login page

#         # Allow access to the login view without redirection
#         if request.path == settings.LOGIN_URL and user_logged_in:
#             return redirect('/dashboard/')  # Redirect authenticated users to the dashboard

#         # Block access to the Django admin panel if not logged in
#         if request.path.startswith('/admi/') and not user_logged_in:
#             return redirect(settings.LOGIN_URL)  # Redirect to the login page

#         response = self.get_response(request)
#         return response

#     def is_user_logged_in(self, request):
#         """
#         Custom method to check if the user is logged in.
#         Replace this logic with how you determine if a user is logged in.
#         """
#         # Check if a specific session variable is set
#         return request.session.get('is_logged_in', False)  # Adjust this logic as needed

from django.shortcuts import redirect
from django.conf import settings
from .models import User  # Update to match your actual user model path

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Role-to-URL permissions
        self.role_permissions = {
            'admin': [
                '/dashboard/', '/add_user/', '/add-marks/', '/marksheet/', '/group_all_marks/','/all-marks/'
            ],
            'faculty': [
                '/dashboard/', '/add-marks/', '/marksheet/'
            ]
        }

    def __call__(self, request):
        path = request.path
        user_logged_in = self.is_user_logged_in(request)

        # Always allow login
        if path == settings.LOGIN_URL:
            if user_logged_in:
                return redirect('/dashboard/')
            return self.get_response(request)

        # Role-based protection
        if user_logged_in:
            user_role = self.get_user_role(request)

            # If path is protected and not allowed for this role
            if self.is_protected(path) and not self.is_allowed(user_role, path):
                return redirect('/dashboard/')  # or return HttpResponseForbidden()

        # Block unauthenticated users from protected URLs
        if self.is_protected(path) and not user_logged_in:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)

    def is_user_logged_in(self, request):
        return request.session.get('is_logged_in', False)

    def get_user_role(self, request):
        try:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            designation = user.designation.designationname.lower()

            # Normalize role based on designation
            if designation in ['director', 'manager', 'coordinator']:
                return 'admin'
            else:
                return 'faculty'
        except:
            return 'guest'

    def is_protected(self, path):
        all_protected = set()
        for paths in self.role_permissions.values():
            all_protected.update(paths)
        return path in all_protected

    def is_allowed(self, role, path):
        return path in self.role_permissions.get(role, [])

