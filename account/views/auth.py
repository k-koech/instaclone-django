from django.shortcuts import redirect, render
from ..models import Comments, Users,Profile, Image as Posts
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

""" DASHBOARD VIEW """
@login_required(login_url='/')
def dashboard(request):
    profile_images=Profile.objects.all()

    profile_details=Profile.objects.get(user=request.user.id)
    loggedin_user = Users.objects.get(id=request.user.id)

    following_list=[request.user.id]
    for following in loggedin_user.following:
        users_i_follow = Users.objects.get(username=following)
        following_list.append(int(users_i_follow.id))
    
    print(following_list)
    posts=Posts.objects.filter(user__in=following_list)
    print(posts)
   
    users = Users.objects.exclude(id=request.user.id)
    comments=Comments.objects.all()
    context= {"posts":posts,"comments":comments,"users":users,"profile_details":profile_details,"profile_images":profile_images}
    return render(request, "dashboard.html",context)

""" USER REGISTRATION VIEW """  
def signUp(request):
    
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        username_exist=Users.objects.filter(username=username).count()
        email_exist=Users.objects.filter(email=email).count()
        if username_exist<1:
            if email_exist<1:
                if password==confirm_password:
                    user = Users(username=username, email=email,followers=[],following=[], password=make_password(password))
                    user.save()

                    user = Users.objects.get(username=username)
                    print(user.id)
                    profile=Profile(user=user.id)
                    profile.save()

                    messages.add_message(request, messages.SUCCESS, 'Successfully Registered!')
                    return redirect(signIn)
                else:
                    messages.add_message(request, messages.ERROR, "Password doesn't match ")
                    return redirect(signUp)
            else:
                    messages.add_message(request, messages.ERROR, "Email exist!")
                    return redirect(signUp)
        else:
                messages.add_message(request, messages.ERROR, "Username exist!! ")
                return redirect(signUp)
    else:
        return render(request, "register.html")

""" LOGIN VIEW """
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

""" LOGOUT VIEW """
def signOut(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully!')
    return redirect(signIn)

