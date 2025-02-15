from ._import_package import *

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
  """
  Get user info
  1. Return serialized data

  Path:
    BASE_URL/api/get_user/
    
  Requires:
    Header:
      Authorization: Token <value>

  Returns:
    200 OK if succesfull
      detail: 
        username: <username>,
        email: <email>
    
    403 FORBIDDEN if invalid auth token
      detail: Invalid token.    
  """  
  
  serializer = UserSerializer(request.user)
  return Response({"detail":serializer.data})