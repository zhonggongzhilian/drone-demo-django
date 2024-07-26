# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
import logging

from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import DroneForm
from .forms import EditProfileForm
from .models import CustomUser
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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests


@login_required(login_url="/login/")
def index(request):
    # 获取当前用户
    user = request.user

    # 从数据库中获取当前用户的所有无人机记录
    drones = Drone.objects.filter(user=user)

    # 提取所有 drone_sn
    drone_sns = [drone.drone_sn for drone in drones]

    notifications = []
    fire_points = []
    for drone_sn in drone_sns:
        # 请求外部接口获取数据
        response = requests.post('http://1.13.23.62:5000/getInfoBySN', json={'droneSN': drone_sn})
        if response.status_code == 200:
            data = response.json()
            notifications.extend(data)
            # 处理通知数据
            fire_points.extend([(item['Latitude'], item['Longitude']) for item in data if
                                float(item['Latitude']) > 0 and float(item['Longitude']) > 0])

    return render(request, 'home/index.html', {
        'user': user,
        'drones': drones,
        'notifications': notifications,
        'fire_points': fire_points  # 将火点数据传递给模板
    })


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


def _device_list(request):
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
def device_list(request):
    devices = Drone.objects.filter(user=request.user)
    print(devices)
    return render(request, 'home/device_list.html', {'devices': devices})


@login_required
def add_drone(request):
    if request.method == 'POST':
        form = DroneForm(request.POST)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.user = request.user
            drone.save()
            return redirect('device_list')
    else:
        form = DroneForm()
    return render(request, 'home/add_drone.html', {'form': form})


# def live_view(request):
#     devices = [
#         # 示例设备数据，替换为实际数据
#         {'id': 1, 'name': 'Device 1', 'stream_url': 'http://192.168.43.21/hls/stream1.m3u8'},
#         {'id': 2, 'name': 'Device 2', 'stream_url': 'http://192.168.43.21/hls/stream2.m3u8'},
#         {'id': 3, 'name': 'Device 3', 'stream_url': 'http://192.168.43.21/hls/stream3.m3u8'},
#         {'id': 4, 'name': 'Device 4', 'stream_url': 'http://192.168.43.21/hls/stream4.m3u8'},
#         {'id': 5, 'name': 'Device 5', 'stream_url': 'http://192.168.43.21/hls/stream5.m3u8'},
#         {'id': 6, 'name': 'Device 6', 'stream_url': 'http://192.168.43.21/hls/stream6.m3u8'},
#         {'id': 7, 'name': 'Device 7', 'stream_url': 'http://192.168.43.21/hls/stream7.m3u8'},
#         {'id': 8, 'name': 'Device 8', 'stream_url': 'http://192.168.43.21/hls/stream8.m3u8'},
#         {'id': 9, 'name': 'Device 9', 'stream_url': 'http://192.168.43.21/hls/stream9.m3u8'},
#     ]
#     print(devices)
#     return render(request, 'home/live_view.html', {'devices': devices})


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


# 确保只有管理员可以访问
# @staff_member_required(login_url='/login/')
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'home/admin_dashboard.html', context)


# 后台管理页面
def admin_dashboard(request):
    users = CustomUser.objects.all()
    drones = Drone.objects.all()
    notifications = []  # 添加通知信息
    # 提取所有 drone_sn
    drone_sns = [drone.drone_sn for drone in drones]

    for drone_sn in drone_sns:
        # 请求外部接口获取数据
        response = requests.post('http://1.13.23.62:5000/getInfoBySN', json={'droneSN': drone_sn})
        if response.status_code == 200:
            notifications.extend(response.json())

    print(users)
    print(drones)
    print(notifications)

    return render(request, 'home/admin_dashboard.html', {
        'users': users,
        'drones': drones,
        'notifications': notifications
    })


# 添加用户
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if not all([username, full_name, email, phone_number, password]):
            return JsonResponse({'success': False, 'message': '所有字段都是必填的'})

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': '用户名已存在'})

        user = CustomUser.objects.create_user(
            username=username,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': '无效的请求方法'})


# 删除用户
@csrf_exempt
def delete_users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        CustomUser.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': '无效的请求方法'})


def get_notifications(request):
    print("get notifications!")
    return render(request, 'home/notifications.html')


def notification_detail(request):
    video_url = request.GET.get('videoUrl')
    info = request.GET.get('info')

    # 获取当前用户
    user = request.user

    # 从数据库中获取当前用户的所有无人机记录
    drones = Drone.objects.filter(user=user)

    # 提取所有 drone_sn
    drone_sns = [drone.drone_sn for drone in drones]

    data = []
    if info == '火情监控':
        for drone_sn in drone_sns:
            # 请求外部接口获取数据
            response = requests.post('http://1.13.23.62:5000/getInfoBySN', json={'droneSN': drone_sn})
            if response.status_code == 200:
                data.extend(response.json())

    return render(request, 'home/notification_detail.html', {
        'video_url': video_url,
        'info': info,
        'data': data
    })


# @csrf_exempt
# def update_user(request, user_id):
#     from django.contrib.auth.hashers import make_password
#     if request.method == 'POST':
#         user = CustomUser.objects.get(pk=user_id)
#         data = json.loads(request.body.decode('utf-8'))
#         user.username = data.get('username')
#         user.full_name = data.get('full_name')
#         user.email = data.get('email')
#         user.phone_number = data.get('phone_number')
#         user.is_admin = data.get('is_admin') == 'true'
#         if 'password' in data:
#             user.password = make_password(data.get('password'))
#         user.save()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False}, status=400)


def get_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        data = {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'is_admin': user.is_admin
        }
        return JsonResponse(data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_POST
def update_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        data = json.loads(request.body)

        user.username = data.get('username', user.username)
        user.full_name = data.get('full_name', user.full_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.is_admin = data.get('is_admin', user.is_admin)
        user.save()

        return JsonResponse({'success': True})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@login_required
def admin_dashboard_add_drone(request):
    if request.method == 'POST':
        form = DroneForm(request.POST)
        if form.is_valid():
            drone = form.save(commit=False)
            drone.user = request.user
            drone.save()
            return redirect('device_list')
    else:
        form = DroneForm()
    return render(request, 'home/admin_dashboard.html', {'form': form})


@csrf_exempt
def admin_dashboard_update_drone(request, drone_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            drone = Drone.objects.get(id=drone_id)
            drone.drone_model = data['drone_model']
            drone.drone_sn = data['drone_sn']
            drone.remote_sn = data['remote_sn']
            drone.workspace_id = data['workspace_id']
            drone.status = data['status']
            drone.user_id = data['user_id']
            drone.longitude = data['longitude']
            drone.latitude = data['latitude']
            drone.save()
            return JsonResponse({'success': True})
        except Drone.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Drone not found'})


@csrf_exempt
def admin_dashboard_delete_drones(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        Drone.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True})


@csrf_exempt
@require_POST
def admin_dashboard_delete_notifications(request):
    try:
        data = json.loads(request.body)
        for item in data:
            drone_sn = item.get('droneSN')
            timestamp = item.get('timeStamp')

            if not drone_sn or not timestamp:
                continue

            # Call the external API to delete the notification
            response = requests.post(
                'http://1.13.23.62:5000/delFireData',
                json={
                    'droneSN': drone_sn,
                    'timeStamp': timestamp
                }
            )

            if response.status_code != 200:
                return JsonResponse({'success': False, 'message': 'API 请求失败'})

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required()
def live_view(request):
    drones = Drone.objects.filter(user=request.user)
    return render(request, 'home/live_view.html', {'drones': drones})
