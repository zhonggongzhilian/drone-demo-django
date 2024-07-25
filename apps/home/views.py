# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
import logging

import requests
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import DroneForm
from .forms import EditProfileForm
from .models import Drone

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

    return render(request, 'home/user.html', {'user_info': user_info})


@csrf_exempt
def change_user_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email_info = data.get('emailInfo')
            payload = {
                "username": username,
                "alterItem": {
                    "email": email_info
                }
            }
            print(payload)
            response = requests.post(f'{BACKEND}/alterEmail', json=payload)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to change email'}, status=response.status_code)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def delete_user_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email_info = data.get('emailInfo')
            payload = {
                "username": username,
                "alterItem": {
                    "email": email_info
                }
            }
            print("delete email: ", payload)
            response = requests.post(f'{BACKEND}/deleteEmail', json=payload)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to delete email'}, status=response.status_code)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def change_user_phone(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            phone_num = data.get('phoneNum')
            payload = {
                "username": username,
                "alterItem": {
                    "phone": phone_num
                }
            }
            response = requests.post(f'{BACKEND}/alterPhone', json=payload)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to change phone number'}, status=response.status_code)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            payload = {
                "username": username,
                "alterItem": {
                    "password": password
                }
            }
            response = requests.post(f'{BACKEND}/alterpassword', json=payload)
            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to change password'}, status=response.status_code)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
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


def device_list(request):
    devices = [
        {'drone_sn': '1581F5FHD23BP00DP8VH', 'remote_sn': '5YSZLBH0034M17', 'workspace_id': 'Not Given',
         'status': '在线'},
        {'drone_sn': '1581F5FJD23AB00D6U1P', 'remote_sn': '5YSZLBH0034M17', 'workspace_id': 'Not Given',
         'status': '在线'},
        {'drone_sn': '1971F5FYJ98HP00DP9QV', 'remote_sn': '5YSZLA90033XY2', 'workspace_id': 'Not Given',
         'status': '在线'},
        {'drone_sn': '1971F5FYJ98HP00DP9QV', 'remote_sn': '9H86LBH1196M66', 'workspace_id': 'Not Given',
         'status': '在线'}
    ]
    for d in devices:
        print(d)
    return render(request, 'home/device_list.html', {'devices': devices})


@login_required
def _device_list(request):
    user = request.user
    devices = Drone.objects.filter(user=user)

    if request.method == "POST":
        form = DroneForm(request.POST)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.user = user
            drone.save()
            return redirect('device_list')
    else:
        form = DroneForm()
    for d in devices:
        print(d.drone_model)
    return render(request, 'home/device_list.html', {'devices': devices, 'form': form})


@login_required(login_url="/login/")
def add_drone(request):
    if request.method == 'POST':
        drone_model = request.POST.get('drone_model')
        drone_sn = request.POST.get('drone_sn')
        remote_sn = request.POST.get('remote_sn')
        workspace_id = request.POST.get('workspace_id')
        status = request.POST.get('status')

        Drone.objects.create(
            drone_model=drone_model,
            drone_sn=drone_sn,
            remote_sn=remote_sn,
            workspace_id=workspace_id,
            status=status,
            user=request.user
        )
        return redirect(reverse('device_list'))
    return redirect(reverse('device_list'))


def live_view(request):
    devices = [
        # 示例设备数据，替换为实际数据
        {'id': 1, 'name': 'Device 1', 'stream_url': 'http://192.168.43.21/hls/stream1.m3u8'},
        {'id': 2, 'name': 'Device 2', 'stream_url': 'http://192.168.43.21/hls/stream2.m3u8'},
        {'id': 3, 'name': 'Device 3', 'stream_url': 'http://192.168.43.21/hls/stream3.m3u8'},
        {'id': 4, 'name': 'Device 4', 'stream_url': 'http://192.168.43.21/hls/stream4.m3u8'},
        {'id': 5, 'name': 'Device 5', 'stream_url': 'http://192.168.43.21/hls/stream5.m3u8'},
        {'id': 6, 'name': 'Device 6', 'stream_url': 'http://192.168.43.21/hls/stream6.m3u8'},
        {'id': 7, 'name': 'Device 7', 'stream_url': 'http://192.168.43.21/hls/stream7.m3u8'},
        {'id': 8, 'name': 'Device 8', 'stream_url': 'http://192.168.43.21/hls/stream8.m3u8'},
        {'id': 9, 'name': 'Device 9', 'stream_url': 'http://192.168.43.21/hls/stream9.m3u8'},
    ]
    print(devices)
    return render(request, 'home/live_view.html', {'devices': devices})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '信息已更新')
            return redirect('user_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'home/user.html', {'form': form})
