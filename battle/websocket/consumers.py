from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from battle.models import Battle
from django.core.exceptions import ValidationError
import json
from users.models import User
from random import choices, randint

# recived x, y from front

class BattleConsumer (WebsocketConsumer) :
    
    def connect(self):

        self.user = self.scope['user']

        battle_uuid = self.scope['url_route']['kwargs']['battleuuid']

        if self.user.is_anonymous : 
            self.close()

        try : 
            self.battle = Battle.objects.get(uuid=battle_uuid)

            if self.battle.red_player == self.user or self.battle.blue_player == self.user:
                self.accept()
            else:
                self.close() 

        except (Battle.DoesNotExist, ValidationError):
            self.close()
        
        self.battle_layer = f'battle_{battle_uuid}'
        async_to_sync(self.channel_layer.group_add)(
            self.battle_layer,
            self.channel_name
        )
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.battle_layer,
            self.channel_name
        )

    def receive(self, text_data):

        data = json.loads(text_data)

        data['sender'] = str(self.user.uuid)


        if 'winner' in data :
            winner_user_uuid = data['winner']

            try :
                winner = User.objects.get(uuid=winner_user_uuid)

                if winner in [self.battle.red_player, self.battle.blue_player] and self.battle.winner is None: 
                    winner.points += 5
                    
                    if winner == self.battle.red_player : 
                        team = 'red'
                    elif winner == self.battle.blue_player : 
                        team = 'blue'
                    
                    self.battle.winner = team
                    self.battle.save()
                    
                    winner.save()

                self.close()

            except User.DoesNotExist :
                self.close()

        async_to_sync(self.channel_layer.group_send)(
            self.battle_layer,
            {
                'type' : 'send_x_y',
                'data' : data
            }
        )


    def send_x_y (self, data) :
        self.send(text_data=json.dumps(data['data']))


class CreateBattleConsumer (WebsocketConsumer) : 

    def connect(self) : 
        self.accept()
        
        user = self.scope['user']

        if user.is_anonymous : 
            self.close()



        battles = Battle.objects.filter(is_wait=True)
        
        data = {}

        if battles.count() >= 1 :
            battle = battles.order_by('?').first()
            


            if battle.red_player is None and battle.blue_player != user: 
                battle.red_player = user
                

            elif battle.blue_player is None and battle.red_player != user : 
                battle.blue_player = user


            if battle.blue_player and battle.red_player : 
                battle.is_wait = False
                battle.save()


        else : 
            red_or_blue = ['red','blue']
            battle = Battle.objects.create(is_wait=True)
            choice = choices(red_or_blue)[0]

            if choice == 'red' : 
                battle.red_player = user
            else : 
                battle.blue_player = user
            
            battle.save()


        self.layer = f"random_battle_layer_{battle.uuid}"

        async_to_sync(self.channel_layer.group_add)(
            self.layer,
            self.channel_name
        )



        if battle.red_player and battle.blue_player :
            
            msg = {
                'uuid':str(battle.uuid)
            }

            async_to_sync(self.channel_layer.group_send)(
                self.layer,
                {
                    'type' : 'x',
                    'msg' : msg
                }
            )


    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.layer,
            self.channel_name
        )

    
    def x (self, msg) : 
        self.send(text_data=json.dumps(msg['msg']))        



class HomeConsumer (WebsocketConsumer) :
    
    def connect(self):
        
        self.user = self.scope['user']
        self.layer = "MAIN"

        if self.user.is_anonymous :
            self.close()

        self.accept()
        
        async_to_sync(self.channel_layer.group_add)(
            self.layer,
            self.channel_name
        )

        leaders = User.get_leaders()
        
        async_to_sync(self.channel_layer.group_send)(
            self.layer,
            {
                'type':'send_to_all',
                'data' : leaders
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.layer,
            self.channel_name
        )
        
    def send_to_all(self, data):
        self.send(text_data=json.dumps(data['data']))