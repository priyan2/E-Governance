from django.urls import path
from . import views
urlpatterns = [

    path('',views.public_register,name='public_register'),
    path('home/',views.home,name='home'),
    path('public_login/',views.public_login,name='public_login'),
    path('staff_login/',views.staff_login,name='staff_login'),
    path('public_logout/',views.public_logout,name='public_logout'),
    path('public_dashboard/',views.public_dashboard,name='public_dashboard'),
    path('send_query/',views.send_query,name='send_query'),
    path('manage_query/',views.manage_query,name='manage_query'),
    path('water_dashboard/',views.water_dashboard,name='water_dashboard'),
    path('electricity_dashboard/',views.electricity_dashboard,name='electricity_dashboard'),
    path('drain_dashboard/',views.drain_dashboard,name='drain_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('view_complaint/',views.view_complaint,name='view_complaint'),
    path('water_complaint/',views.water_complaint,name='water_complaint'),
    path('electricity_complaint/',views.electricity_complaint,name='electricity_complaint'),
    path('drain_complaint/',views.drain_complaint,name='drain_complaint'),
    path('update/<str:pk>/<int:ids>/',views.update,name='update'),
    path('water_update/<str:pk>/<int:ids>/',views.water_update,name='water_update'),
    path('electricity_update/<str:pk>/<int:ids>/',views.electricity_update,name='electricity_update'),
    path('drain_update/<str:pk>/<int:ids>/',views.drain_update,name='drain_update'),
    path('pending_complaint/',views.pending_complaint,name='pending_complaint'),
    path('feedback/',views.feedback,name='feedback'),
    path('verify_email/',views.verify_email,name='verify_email'),
]