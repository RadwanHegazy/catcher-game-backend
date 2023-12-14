from django.db import models
from users.models import User
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save


class Battle (models.Model) : 
    uuid = models.UUIDField(null=True,blank=True)
    red_player = models.ForeignKey(User, related_name='user_red_player' ,on_delete=models.PROTECT,null=True,blank=True)
    blue_player = models.ForeignKey(User, related_name='user_blue_player'  ,on_delete=models.PROTECT,null=True,blank=True)
    winner = models.CharField(choices=(
        ('red','red'),
        ('blue','blue'),
    ),max_length=10,null=True,blank=True)
    is_wait = models.BooleanField(default=False)
    def __str__(self) : 
        return f'{self.red_player} vs {self.blue_player}'
    
@receiver(post_save,sender=Battle)
def BattleSignal(created, instance, **kwargs) :
    if created : 
        instance.uuid = uuid4()
        instance.save()