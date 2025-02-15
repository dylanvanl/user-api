from ._import_package import *
from django.core.exceptions import ObjectDoesNotExist

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
  """
  Soft deletes the user.
  Removes missing tokens if they exist.
  
  Path:
    BASE_URL/api/delete/

  Requires:
    Header:
      Authorization: Token <value>    

  Returns:
    200 OK if succesfull
    
    400 BAD REQUEST if user or related objects don't exist
    
    403 FORBIDDEN if invalid auth token
      detail: Invalid token.
  """
  try:
    user = request.user
    user.soft_delete()
    # delete authentication when user get's deleted.
    user.auth_token.delete()
    try: 
      # verification token might not exist, but delete if it does.
      user.verification_token.delete()
    except:
      pass
    user.save()
  except (ObjectDoesNotExist, AttributeError):
    return Response(status=400)
  return Response(status=200)