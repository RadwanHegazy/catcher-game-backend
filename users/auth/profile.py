from rest_framework import decorators, permissions, status
from rest_framework.response import Response
import json



@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
def ProfileView(request) :
    try : 
        user = request.user
        return Response({
            'full_name' : user.full_name,
            'points' : user.points,
            'picture' :user.picture.url,
            'uuid' : str(user.uuid), 
        },status=status.HTTP_200_OK)
    except Exception as error :
        return Response({
            "message" : f"an error accured : {error}"
        },status=status.HTTP_400_BAD_REQUEST)