from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt

# Agora App Credentials
APP_ID = 'beefa750c8a944caae4837eef48352b6'
APP_CERTIFICATE = '4910bbe8c18d4526abdebff2f8e2d5e3'

# Generate Token
def getToken(request):
    try:
        # Get channel name from the request
        channelName = request.GET.get('channel')
        if not channelName:
            return JsonResponse({'error': 'Channel name is required'}, status=400)

        # Generate unique UID
        uid = random.randint(1, 230)

        # Token expiration setup
        expirationTimeInSeconds = 3600 * 24  # 24 hours
        currentTimeStamp = time.time()
        privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds

        # Role 1 (publisher)
        role = 1

        # Generate token
        token = RtcTokenBuilder.buildTokenWithUid(APP_ID, APP_CERTIFICATE, channelName, uid, role, privilegeExpiredTs)
        return JsonResponse({'token': token, 'uid': uid}, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Failed to generate token: {str(e)}'}, status=500)

# Lobby view
def lobby(request):
    return render(request, 'base/lobby.html')

# Room view
def room(request):
    return render(request, 'base/room.html')

# Create Member API
@csrf_exempt
def createMember(request):
    try:
        # Parse request body
        data = json.loads(request.body)

        # Get or create member
        member, created = RoomMember.objects.get_or_create(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )

        return JsonResponse({'name': member.name}, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Failed to create member: {str(e)}'}, status=500)

# Get Member API
def getMember(request):
    try:
        # Get UID and room name from query parameters
        uid = request.GET.get('UID')
        room_name = request.GET.get('room_name')

        if not uid or not room_name:
            return JsonResponse({'error': 'UID and room name are required'}, status=400)

        # Retrieve the member
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        return JsonResponse({'name': member.name}, safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to retrieve member: {str(e)}'}, status=500)

# Delete Member API
@csrf_exempt
def deleteMember(request):
    try:
        # Parse request body
        data = json.loads(request.body)

        # Retrieve and delete the member
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to delete member: {str(e)}'}, status=500)


def home(request):
    return render(request,'base/home.html')



from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirm_password')

        if password==confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username alredy taken")
                return redirect('register/')

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email alredy taken")
                return redirect('register/')
            else:
                user_reg=User.objects.create_user(username=username,email=email,password=password)
                user_reg.save()
                messages.info(request, "Successfully Created....!")
                return redirect('/')

        else:
            messages.info(request, "Password doesn't match")
            return redirect('register/')

    return render(request,'base/register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None :
            auth.login(request,user)
            messages.info(request, "Sign-In Success....")
            return redirect('/')
        else:
            messages.info(request, "Invalid....!!!!")
            return redirect('register/')

    return render(request,'base/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')