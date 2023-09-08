from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room as Rooms,Topic,Message,User
from .forms import RoomForm,Userform,Myusercreationform
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.



def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms = Rooms.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    print(room_messages)
    context = {'rooms':rooms,'topics':topics ,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        try:
            user = User.objects.get(email=username)
            print("user")
            print(user.username)
        except:
            messages.error(request,'user does not exist')
        user =authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"incorrect")
        
            
    context ={'page':page}
    return render(request,'base/login_register.html',context)

def logoutpage(request):
    logout(request)
    return redirect('home',)

def registerpage(request):
    
    form = Myusercreationform()
    if request.method == 'POST':
        form = Myusercreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username =user.username.lower()
            form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration please try again")
    context ={'form':form}
    return render(request,'base/login_register.html',context)

def room(request,pk):
    room = Rooms.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message =Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
        
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


def userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics =Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createform(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Rooms.objects.create(
            host = request.user,
            topic =topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
            
    context = {'form':form,'topics':topics}
    return render(request,'base/roomform.html',context)

@login_required(login_url='login')
def update(request,pk):
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        print(topic_name)
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    
    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/roomform.html',context)

@login_required(login_url='login')
def delete(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.user != room.host and not request.user.is_superuser:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def deletemessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user :
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj':message} 
    return render(request,'base/delete.html',context)

@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = Userform(instance=user)
    if request.method == 'POST':
        form =Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile',pk=user.id)
    context = {'form':form}
    return render(request,'base/updateuser.html',context)

def topicspage(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    print("--------")
    print(topics)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)

def activitypage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request,'base/activity.html',context)