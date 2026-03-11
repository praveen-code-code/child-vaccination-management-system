from django.urls import path
from . import views

app_name = 'vaccine'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    
    # Main URLs
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Children URLs
    path('children/', views.child_list, name='child_list'),
    path('children/<int:pk>/', views.child_detail, name='child_detail'),
    path('children/add/', views.child_create, name='child_create'),
    path('children/<int:pk>/edit/', views.child_update, name='child_update'),
    path('children/<int:pk>/delete/', views.child_delete, name='child_delete'),
    
    # Vaccines URLs
    path('vaccines/', views.vaccine_list, name='vaccine_list'),
    path('vaccines/<int:pk>/', views.vaccine_detail, name='vaccine_detail'),
    path('vaccines/add/', views.vaccine_create, name='vaccine_create'),
    path('vaccines/<int:pk>/edit/', views.vaccine_update, name='vaccine_update'),
    
    # Schedules URLs
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/add/', views.schedule_create, name='schedule_create'),
    path('schedules/<int:pk>/edit/', views.schedule_update, name='schedule_update'),
    
    # Records URLs
    path('records/', views.record_list, name='record_list'),
    path('records/add/', views.record_create, name='record_create'),
    path('records/<int:pk>/edit/', views.record_update, name='record_update'),
    
    # Calendar URL
    path('calendar/', views.calendar_view, name='calendar'),
    
    # API URLs
    path('api/search/', views.search_api, name='search_api'),
]
