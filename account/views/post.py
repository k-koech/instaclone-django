from account.views.auth import dashboard
from django.shortcuts import redirect, render
from ..models import Comments, Posts, Users
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
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

@login_required(login_url='/')   
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
    
@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def add_comment(request,post_id):
    if request.method=="POST":
        comment=request.POST['comment']
        comment = Comments(comment=comment, post_id=post_id, user_id=request.user.id)
        comment.save()
        messages.add_message(request, messages.SUCCESS, 'Success')
        return redirect(dashboard)
    else:
        return redirect(dashboard)

@login_required(login_url='/')
def follow(request, username):
    user= Users.objects.get(id=request.user.id)
    followed_user= Users.objects.get(username=username)

    if len(user.following) == 0 and len(followed_user.followers) == 0:
        user.following.insert(0,username)
        followed_user.followers.insert(0,request.user.username)
        print(username)
        user.save()
        followed_user.save()
        return redirect(dashboard)
      

    elif len(user.following) != 0 and len(followed_user.followers) == 0:
        for following in user.following:
            if following==username:
                print("exist")
                return redirect(dashboard)
            else:
                user.following.insert(0,username)
                followed_user.followers.insert(0,request.user.username)
                print(username)
                user.save()
                followed_user.save()
                return redirect(dashboard)            

    else:
        for following in user.following:
            for followers in followed_user.following:
            # print("following" +following) 
            # print("username"+ username)
            # return redirect(dashboard)
                if following==username and followers==username:
                    print("exist")
                    return redirect(dashboard)
                else:
                    user.following.insert(0,username)
                    followed_user.followers.insert(0,request.user.username)
                    user.save()
                    followed_user.save()
                    

    return redirect(dashboard)
 