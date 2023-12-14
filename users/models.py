from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import threading, time
from uuid import uuid4

class User (AbstractUser):
    username = None
    groups = None
    first_name = None
    last_name = None


    picture = models.ImageField(upload_to='pictures/',default='default.png')
    full_name = models.CharField(_('Full Name'),max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    points = models.IntegerField(default=0)
    uuid = models.UUIDField(null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name
    
    def login (**kwargs) : 
        email = kwargs['email']
        password = kwargs['password']

        user = User.objects.filter(email=email)
        
        response = {
            'errors':''
        }

        if not user.exists() or user.count() > 1 :
            response['errors'] = 'خطأ في البريد الالكتروني'
            return response
        
        user = user.first()

        if not user.check_password(password) :
            response['errors'] = 'خطأ في كلمة السر'
            return response
        
        response['user'] = user

        return response

    class Meta:
        ordering = ('-points',)
    
    def get_leaders () :

        leaders = []
        users = User.objects.all()[:5]

        for user in users : 
            leaders.append({
                'full_name' : user.full_name,
                'picture' : user.picture.url,
                'points' : user.points,
            })
         

        return leaders
    
@receiver(post_save, sender=User)
def CreateUserToken (created, instance, **kwargs) : 
    if created : 
        instance.uuid = uuid4()
        instance.save()
        Token.objects.create(user=instance)



def updateing () :
    time.sleep(1)
    leaders = User.get_leaders()
    
    layer = "MAIN"

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        layer,
        {
            'type':'send_to_all',
            'data' : leaders
        }
    )


@receiver(pre_save, sender=User)
def UpdateWebsocket ( instance, **kwargs) : 
    threading.Thread(target=updateing).start()
