from django.db.models.fields import IntegerField, TextField
from instaclone.settings import DEFAULT_AUTO_FIELD
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime as dt
from cloudinary.models import CloudinaryField
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(" User must have an email address")
        if not username:
            raise ValueError(" User must have an username!")    
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username=username,
        )
        user.email = email
        user.is_admin = True 
        user.is_staff = True 
        user.is_superuser = True 
        user.save(using=self._db)
        return user
        
class Users(AbstractBaseUser):
    username = models.CharField( max_length=20, unique=True)  
    email = models.CharField( max_length=50, unique=True)
    name = models.CharField( max_length=50, unique=False, default="Male")
    profile_image =  CloudinaryField('image', default='image/upload/v1631717620/default_uomrne.jpg')  
    bio= models.TextField(null=True)
    gender = models.CharField( max_length=20)
    phone = models.CharField( max_length=50, unique=False,null=True)
    following = ArrayField(models.CharField(max_length=50, default=list ),size=1000)
    followers = ArrayField(models.CharField(max_length=50, default=list),size=1000)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(default=dt.datetime.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField( max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects=MyAccountManager()
     
    def _str_(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Posts(models.Model):
    post_image =  CloudinaryField('image')
    caption = models.TextField()
    user = models.ForeignKey('Users', on_delete=models.CASCADE)   
    date_posted = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    likes = ArrayField(models.CharField(max_length=50, null=True),size=8 )

class Comments(models.Model):
    comment = models.TextField()
    date_posted = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)   

