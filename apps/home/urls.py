# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('full_screen_video', views.full_screen_video, name='full_screen_video'),
    path('user_data', views.user_data, name='user_data'),
    path('change_user_email/', views.change_user_email, name='change_user_email'),
    path('delete_user_email/', views.delete_user_email, name='delete_user_email'),
    path('change_user_phone/', views.change_user_phone, name='change_user_phone'),
    path('change_password/', views.change_password, name='change_password'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
