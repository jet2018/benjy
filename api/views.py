from django.contrib.auth.models import User, auth
from django.shortcuts import render
from api.serializers import UsageDataSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from django.http.response import JsonResponse
# Create your views here.

from .models import UsageData


class ViewAllStatistics(generics.ListAPIView):
    queryset = UsageData.objects.all()
    serializer_class = UsageDataSerializer


@api_view(['POST'])
def PostData(request):
    username = request.data.get(
        'username')

    facebook = request.data.get(
        'facebook') if request.data.get('facebook') else 0
    twitter = request.data.get(
        'twitter') if request.data.get('twitter') else 0
    snapchat = request.data.get(
        'snapchat') if request.data.get('snapchat') else 0
    instagram = request.data.get(
        'instagram') if request.data.get('instagram') else 0
    reddit = request.data.get('reddit') if request.data.get('reddit') else 0
    whatsapp = request.data.get(
        'whatsapp') if request.data.get('whatsapp') else 0

    try:
        # get the user
        user = User.objects.get(username=username)
        # create the usage data
        usage_data = UsageData(
            user=user,
            facebook=facebook,
            twitter=twitter,
            snapchat=snapchat,
            whatsapp=whatsapp,
            instagram=instagram,
            reddit=reddit
        )
        usage_data.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Not found'})


@api_view(['POST'])
def fake_login(request):
    username = request.data.get(
        'username')
    password = request.data.get(
        'password')

    user = auth.authencticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@api_view(['POST'])
def fake_logout(request):
    auth.logout(request)
    return JsonResponse({'status': 'success'})


@api_view(['POST'])
def fake_register(request):
    username = request.data.get(
        'username')
    first_name = request.data.get(
        'first_name')
    last_name = request.data.get(
        'last_name')
    password = request.data.get(
        'password')

    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,

    )
    user.save()
    return JsonResponse({'status': 'success'})
