from ._import_package import *
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
  """
  logs out the user.
  1. Delete auth token if exists ignore otherwise  

  Path:
    BASE_URL/api/logout/
    
  Requires:
    Header:
      Authorization: Token <value>

  Returns:
    200 OK if succesfull
  
    403 FORBIDDEN if invalid auth token
      detail: Invalid token.
  """
  try:
    request.user.auth_token.delete()
  except (AttributeError, ObjectDoesNotExist):
      pass  
  return Response(status=200)