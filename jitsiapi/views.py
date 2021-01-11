from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse
from .models import ConferenceUser
from django.contrib.auth import hashers
import requests
import subprocess
def user_status(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    status = request.GET.get('status')
    enc_pass = hashers.make_password(password)
    print(username, password, status)
    user = ConferenceUser(userid=username, password=enc_pass, status=status)
    user.save()
    import subprocess
    username = username
    password = password
    args = ['sudo', 'prosodyctl', 'register', username, 'jitsi.icodexa.com', password]
    subprocess.Popen(args)
    return JsonResponse({'status': 200, 'message': 'success','code':args})

def check_passwordapi(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = ConferenceUser.objects.get(userid=username)
    user_pass = user.password
    password = hashers.check_password(password, user_pass)
    print("yessssssssss",password)
    return JsonResponse({'password':password})
def userDetails(request):
    response = requests.get('https://store.orocast.com/api/meet-list/')
    print("yessssssssss",response)
    jsonData=response.json()
    userData=json.dumps(jsonData)
    userData=json.loads(userData)
    print(userData['meet'][0])
    try:
        for user in userData['meet']:
            id = user['id']
            slug = user['slug']
            password = user['password']
            print(id, slug)
            url = "https://store.orocast.com/api/update-meet"

            payload = {'id': id,
                       'slug': slug}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            args = ['sudo', 'prosodyctl', 'register', slug, 'jitsi.icodexa.com', password]
            subprocess.Popen(args)
        return JsonResponse({'status': 200, 'message': 'meet successfully created'})
    except Exception as e:
        print(e)
        return HttpResponse("No meetings Found")


