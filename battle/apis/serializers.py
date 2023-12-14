from rest_framework import serializers
from users.models import User
from battle.models import Battle


class UserSerializer (serializers.ModelSerializer) : 
    class Meta :
        model = User
        fields = ('full_name','picture','uuid',)


class BattleSerializer (serializers.ModelSerializer) : 
    red_player = UserSerializer()
    blue_player = UserSerializer()

    class Meta : 
        model = Battle
        fields = ('red_player','blue_player','winner')