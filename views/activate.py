from ._import_package import *


@api_view(['GET'])
def activate(request, token):
  """ 
  Activates the user acount. allowing them to login.
  1. check for valid token.
  2. set user.is_active to true.
  3. delete token.
  
  Path:
    BASE_URL/api/activate/<token>
    
  Requires:
    Empty
  
  Returns:
    200 OK if succesfull
      detail: Account activated succesfully.
  
    400 BAD REQUEST if token doesn't exist.
      detail: Invalid token: <token>
    
    400 BAD REQUEST if token has expired.
      detail: Expired token: <token>
  
  """  
  try:
    token_obj = EmailVerificationToken.objects.get(token=token)
  except EmailVerificationToken.DoesNotExist:
    return Response({"detail": "Invalid token: " + str(token)}, status=400)
  
  if token_obj.is_expired():
    token_obj.delete()
    return Response({"detail": "Expired token: " + str(token)}, status=400)
  
  user = token_obj.user
  user.is_active = True
  user.save()
  
  token_obj.delete()
  return Response({"detail": "Account activated succesfully."}, status=200)