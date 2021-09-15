from django.contrib import auth
from django.urls import path
from .views.auth import index,signIn,dashboard,signOut,signUp
from .views.post import add_post, profile,edit_profile,like_post,update_dp,add_comment, follow

urlpatterns = [
    # auth
    path("",signIn, name="home" ),
     path("register",signUp, name="login" ),
     path("dashboard",dashboard, name="dashboard" ),
     path("logout",signOut, name="logout" ),

    #  
    path("add_post",add_post, name="add_post" ),
    path("like/<post_id>",like_post, name="likepost" ),
    path("comment/<post_id>",add_comment, name="comment" ),
    path("follow/<username>",follow, name="follow" ),

    path("<username>",profile, name="profile" ),
    path("account/edit",edit_profile, name="edit_profile" ),
    path("account/update",update_dp, name="update_profile" ),
]
