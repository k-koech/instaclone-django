from account.views.auth import dashboard
from django.shortcuts import redirect, render
from ..models import Comments, Posts, Users
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
import cloudinary
# Create your views here.
  
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

def add_post(request):
     if request.method=="POST":
        caption=request.POST['caption']
        image=request.FILES['image']
        post = Posts(post_image=image, caption=caption, user=request.user, likes=[])
        post.save()
        messages.add_message(request, messages.SUCCESS, 'Post saved successfully!')
        return redirect(dashboard)
     else:
        return render(request, "dashboard.html")
        
def like_post(request, post_id):   
    post= Posts.objects.get(id=post_id)
    if len(post.likes) == 0:
        post.likes.insert(0,request.user.id)
        post.save()
        print("first one")
        return  redirect(dashboard)
    else:
        print(post.likes)   
        for i in post.likes:
            if int(i)!=request.user.id:
                post.likes.insert(0,request.user.id)
                post.save()
                return  redirect(dashboard)
            else:
                return  redirect(dashboard)            
    
    return redirect(dashboard)   
       
def profile(request, username):
    posts=Posts.objects.filter(user_id=request.user)
    no_of_posts = Posts.objects.filter(user_id=request.user).count()
    
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

    return render(request, "profile.html",{"posts":posts, "no_of_posts":no_of_posts})

def edit_profile(request):   
    if request.method=="POST":
        user = Users.objects.get(id=request.user.id)
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.phone=request.POST['phone']
        user.bio=request.POST['bio']
        user.name=request.POST['name']
        user.gender=request.POST['gender']

        user.save()
        messages.add_message(request, messages.INFO, 'Profile updated successfully!')
        return redirect(edit_profile)
    return render(request, "edit_profile.html")

def update_dp(request):
     if request.method=="POST":
        image=request.FILES['image']
        user = Users.objects.get(id=request.user.id)
        user.profile_image=image
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Profile Updated!')
        return redirect(edit_profile)
     else:
        return redirect(edit_profile)

def add_comment(request,post_id):
    if request.method=="POST":
        comment=request.POST['comment']
        comment = Comments(comment=comment, post_id=post_id, user_id=request.user.id)
        comment.save()
        messages.add_message(request, messages.SUCCESS, 'Success')
        return redirect(dashboard)
    else:
        return redirect(dashboard)


def follow(request):
    if request.method=="POST":
        comment=request.POST['comment']
        comment = Comments(comment=comment, post_id=post_id, user_id=request.user.id)
        comment.save()
        return redirect(dashboard)
    else:
        return redirect(dashboard)