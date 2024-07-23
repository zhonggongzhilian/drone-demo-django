# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import logging

import requests
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ELocalStorageKey = {
    "Username": 'username',
    "WorkspaceId": 'fb9b3bb5-11f0-4aa5-840c-235384d71644',
    "Token": 'x-auth-token',
    "PlatformName": '桔梗燃烧监测平台',
    "WorkspaceName": '智能城乡监测系统',
    "WorkspaceDesc": '已登陆',
    "Flag": 'flag',
    "UserId": 'user_id',
    "Device": 'device',
    "DeviceList": "DeviceList",
    "FireDataList": "FireDataList",
    "GatewayOnline": 'gateway_online'
}

BACKEND = getattr(settings, 'BACKEND_URL', 'http://1.13.23.62:5000')


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def full_screen_video(request):
    return render(request, 'home/full_screen_video.html')


def user_data(request):
    user_info = {
        'username': 'root',
        'last_login_date': '2024年7月22日',
        'email': 'Null',
        'phone': 'Null',
        'video_stream_address': 'rtmp://1.13.23.62:1935/live/stream',
        'monitoring_address': 'rtmp://1.13.23.62:1935/live/stream'
    }

    try:
        response = requests.post(f'{BACKEND}/getUserInfo', json={"username": "root"})
        if response.status_code == 200:
            data = response.json()
            user_info['email'] = data.get('email', 'example@example.com')
            user_info['phone'] = data.get('phone', 'Null')
            logger.info(user_info['email'], user_info['phone'])
            print(user_info['email'], user_info['phone'])
        else:
            print(f"Failed to fetch user info: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}")

    return render(request, 'home/user_data.html', {'user_info': user_info})


@csrf_exempt
def change_user_email(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_info = request.POST.get('emailInfo')
        data = {
            "username": username,
            "alterItem": {
                "email": email_info
            }
        }
        try:
            response = requests.post(f'{BACKEND}/alterEmail', json=data)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to change email'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def delete_user_email(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email_info = request.POST.get('emailInfo')
        data = {
            "username": username,
            "alterItem": {
                "email": email_info
            }
        }
        try:
            response = requests.post(f'{BACKEND}/deleteEmail', json=data)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to delete email'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def change_user_phone(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_num = request.POST.get('phoneNum')
        data = {
            "username": username,
            "alterItem": {
                "phone": str(phone_num)
            }
        }
        print(data)
        try:
            response = requests.post(f'{BACKEND}/alterPhone', json=data)
            if response.status_code == 200:
                print("Change user phone success!")
                return JsonResponse(response.json())
            else:
                print("Failed changing user phone!")
                return JsonResponse({'error': 'Failed to change phone number'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
            "username": username,
            "alterItem": {
                "password": password
            }
        }
        try:
            response = requests.post(f'{BACKEND}/alterpassword', json=data)
            if response.status_code == 200:
                print('')
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to change password'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        avatar_image = request.FILES.get('avatar')
        if not avatar_image:
            return JsonResponse({'error': 'No avatar image provided'}, status=400)

        try:
            files = {'avatar': ('avatar.png', avatar_image.read(), avatar_image.content_type)}
            data = {'username': username}
            response = requests.post(f'{BACKEND}/upload', files=files, data=data)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to upload avatar'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
