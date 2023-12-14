from rest_framework import decorators, status
from rest_framework.response import Response
from users.models import User
from rest_framework.authtoken.models import Token

@decorators.api_view(['POST'])
def RegisterView (request) : 
    try: 
        full_name = request.data.get('full_name',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        picture = request.data.get('picture',None)
        
        if full_name == None or email == None or password == None :
            return Response({
                'message' : 'there is a missing field'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists() : 
            return Response({
                'message' : 'this email already used !'
            },status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            full_name = full_name,
            email = email,
            password = password,
        )

        if picture is not None : 
            user.picture = picture

        user.save()

        return Response({
            'token' : Token.objects.get(user=user).key,
        },status=status.HTTP_200_OK) 

    except Exception as error :
        return Response({
            'message' : f'there is an error accured : {error}'
        }, status=status.HTTP_400_BAD_REQUEST)
