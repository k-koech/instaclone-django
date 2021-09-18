from django.contrib import admin
from .models import Profile,Users,Comments,Image
# Register your models here.
admin.site.register(Users)
admin.site.register(Image)
admin.site.register(Comments)
admin.site.register(Profile)

"""
    Editing admin page
"""
admin.site.site_header = "INSTAGRAM ADMIN"
admin.site.site_title = "Instaclone Admin Portal"
admin.site.index_title = "Instaclone Portal"