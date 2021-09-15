from django.shortcuts import redirect, render
from ..models import Posts, Users
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout

# Create your views here.
def index(request):
    return render(request, "index.html")

def dashboard(request):
    posts=Posts.objects.all()
    return render(request, "dashboard.html",{"posts":posts})
    
def signUp(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            user = Users(username=username, email=email, password=make_password(password))
            user.save()
            messages.add_message(request, messages.INFO, 'Successfully Registered!')
            print("saved")
        else:
            print("password doesnt match")

    return render(request, "register.html")

def signIn(request):
     if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user= authenticate(email=email, password=password)

        if user is not None:
            login(request,user )
            messages.add_message(request, messages.INFO, 'Successfully logged in!')
            return redirect(dashboard)
 
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return redirect(signIn)

     else:
        return render(request, "index.html")

def signOut(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully!')
    return redirect(signIn)

