from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request, username, room_name):
    getusername = UserInfo.objects.get(userinfo=username)
    getroomname = Group.objects.get(name=room_name)
    
    chatData = Chat.objects.filter(room = getroomname)
  
    return render(request,'index.html', {'chats':chatData, 'user_name': username, 'room_name':room_name})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if UserInfo.objects.filter(userinfo=username, password=password).exists():
            return redirect('chatpage', username=username)
        # else:
        #     return redirect('register')
    
    else:   
        return render(request ,'login.html')
    
# def register(request):
#     if request.method == 'POST':
#         userinfo = request.POST['userinfo']
#         email = request.POST['email']
#         password = request.POST['password']
#         conf_password = request.POST["confirm_password"]
    
#         if password==conf_password:
#             if Group.objects.filter(name=userinfo, email=email).exists():
#                 messages.info(request, "User already exists.")
#                 return redirect("register")
#             else:
#                 data = Group.objects.create(name=userinfo, email= email, password=conf_password)
#                 data.save()
#                 return redirect("/")
#         else:
#             messages.info(request, "Invalid Password")
#             return redirect("register")
#     else:
#         return render(request, "register.html")


def chatpage(request,username):
    groups = Group.objects.all()
    context = {
        'username' : username,
        'groups' : groups
    }
    
    if request.method == 'POST':
        room_name = request.POST['roomname']
        
        if Group.objects.filter(name = room_name).exists():
            messages.info("Room Already exists.")
        else:
            mydata = Group.objects.create(name = room_name)
            mydata.save()
           
    
    return render(request, 'chatpage.html', context)