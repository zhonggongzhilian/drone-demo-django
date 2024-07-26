# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('device_list/', views.device_list, name='device_list'),
    path('full_screen_video', views.full_screen_video, name='full_screen_video'),
    path('user_data', views.user_data, name='user_data'),
    path('change_user_email/', views.change_user_email, name='change_user_email'),
    path('delete_user_email/', views.delete_user_email, name='delete_user_email'),
    path('change_user_phone/', views.change_user_phone, name='change_user_phone'),
    path('change_password/', views.change_password, name='change_password'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('live/', views.live_view, name='live_view'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_drone/', views.add_drone, name='add_drone'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_users/', views.delete_users, name='delete_users'),
    path('notifications/', views.get_notifications, name='notifications'),
    path('notification_detail', views.notification_detail, name='notification_detail'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('admin_dashboard/add_drone/', views.admin_dashboard_add_drone, name='admin_dashboard_add_drone'),
    path('admin_dashboard/update_drone/<int:drone_id>/', views.admin_dashboard_update_drone, name='admin_dashboard_update_drone'),
    path('admin_dashboard/delete_drones/', views.admin_dashboard_delete_drones, name='admin_dashboard_delete_drones'),
    path('admin_dashboard/delete_notifications/', views.admin_dashboard_delete_notifications, name='delete_notifications'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),


]
