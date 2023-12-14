from rest_framework import decorators, status
from rest_framework.response import Response
from users.models import User
from rest_framework.authtoken.models import Token


@decorators.api_view(['POST'])
def LoginView (request) : 
    try : 
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        
        
        if email is None or password is None :
            return Response({
                'message' : 'please fill email and password '
            },status=status.HTTP_400_BAD_REQUEST)
            
        auth = User.login(email=email,password=password)

        if auth['errors'] : 
            return Response({
                'message' : auth['errors']
            },status=status.HTTP_400_BAD_REQUEST)
            
        user = auth['user']

    
        return Response({
            'token' : Token.objects.get(user=user).key,
        },status=status.HTTP_200_OK) 



    except Exception as error : 
        return Response({
            'message' : f'there is an error accured : {error}'
        },status=status.HTTP_400_BAD_REQUEST)