from rest_framework import status, decorators, permissions
from rest_framework.response import Response
from battle.models import Battle
from ..serializers import BattleSerializer

@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def GetBattleView (request, battleuuid) : 
    try : 
        
        try : 
            battle = Battle.objects.get(uuid=battleuuid,is_wait=False)
        except Battle.DoesNotExist :
            return Response({
                'message' : f'battle not found'
            },status=status.HTTP_404_NOT_FOUND)
            

        if battle.red_player is None or battle.blue_player is None :
            return Response({
                'message' : "battle doesn't complete with players"
            },status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        players = [battle.red_player, battle.blue_player]

        if current_user not in players : 
            return Response({
                'message' : "invalid battle uuid"
            },status=status.HTTP_400_BAD_REQUEST)

        serializer = BattleSerializer(battle)

        return Response(serializer.data,status=status.HTTP_200_OK)

    except Exception as error : 
        return Response({
            'message' : f'an error accured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)