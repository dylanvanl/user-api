from ._import_package import *
from django.shortcuts import get_object_or_404
from django.db.models import Q

@api_view(['POST'])
def login(request):
  """
  Logs in the user.
  can use either username or email.
  creates and/or returns auth token for user.
  
  Path:
    BASE_URL/api/login/
  
  Requires:
    Body:
      username_or_email: <username_or_email>
      password: <password>

    Returns:
      200 OK if succesfull        
        token: <auth_token>,
        user:
          username: <username>,
          email: <email>
          
      404 NOT FOUND if failed
        detail: No User matches the given query.
  """
  username_or_password = request.data.get('username_or_email')
  user = get_object_or_404(User, (Q(username = username_or_password) | Q(email = username_or_password)))  # find user with username or email
  #make sure that user has active profile and password is correct
  if not user.check_password(request.data['password']) or not user.is_active:
    return Response({"detail":"No User matches the given query."}, status=404)
  
  token, created = Token.objects.get_or_create(user=user) # create auth token  
  serializer = UserSerializer(user) # create return body
  return Response({'token': token.key, 'user': serializer.data}, status=200)