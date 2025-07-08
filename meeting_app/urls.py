# meeting_app/urls.py
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
# or from meeting_app import views

urlpatterns = [
    path('', views.login_view, name='login'),  # or whatever view you're using
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('add_user/', views.add_user, name='add_user'),
    # path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('success_page/',views.success, name="success_page"),
    path('logout/', views.logout_view, name='logout'),
    path('add-marks/', views.add_marks, name='add_marks'),
    path('marksheet/', views.marksheet, name='marksheet'),
    path('all-marks/', views.group_all_marks, name='group_all_marks'),
    path('export-marks-pdf/', views.export_marks_pdf, name='export_marks_pdf'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
