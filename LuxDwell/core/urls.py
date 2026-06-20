from django.urls import path
from . import views # This works here because core/views.py exists!

urlpatterns = [
    # Public & Auth
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Property Details & Booking
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:pk>/book/', views.book_property, name='book_property'),
    
    # Dashboards
    path('dashboard/agent/', views.agent_dashboard, name='agent_dashboard'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    
    # Property Actions
    path('property/add/', views.add_property, name='add_property'),
    path('respond-to-inquiry/<int:booking_id>/', views.respond_to_inquiry, name='respond_to_inquiry'),
    path('appointment/<int:booking_id>/<str:action>/', views.handle_appointment, name='handle_appointment'),
    path('toggle-status/<int:prop_id>/', views.toggle_property_status, name='toggle_property_status'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('agent-delete-inquiry/<int:booking_id>/', views.agent_delete_inquiry, name='agent_delete_inquiry'),

    # Admin Portal (Standardized to admin-portal/)
    path('admin-portal/', views.custom_admin, name='custom_admin'),
    path('admin-portal/add-user/', views.admin_add_user, name='admin_add_user'),
    path('admin-portal/property/edit/<int:property_id>/', views.admin_edit_property, name='admin_edit_property'),
    path('admin-portal/property/delete/<int:property_id>/', views.delete_property, name='delete_property'),
    
    # Admin Controls (Adding prefix here makes them more secure/organized)
    path('admin-portal/approve/<int:property_id>/', views.approve_property, name='approve_property'),
    path('admin-portal/reject/<int:property_id>/', views.reject_property, name='reject_property'),
    path('admin-portal/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-portal/toggle-agent/<int:user_id>/', views.toggle_agent_status, name='toggle_agent'),
]