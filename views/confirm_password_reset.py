from ._import_package import *

@api_view(['PATCH'])
def confirm_password_reset(request):
  """ 
  Assign new password to user.
  1. Check correct password confirmation.
  2. Check correct token.
  3. Check active user.
  4. Validate password rules.
  5. Set password.  
  6. Delete token.
  
  Path:
    BASE_URL/api/confirm-password-reset/
    
  Requires:
    Body:
      token: <email_verification_token>,
      password: <password>,
      password_confirmation: <password>
  
  Returns:
    200 OK if succesfull
      detail: Password succesfully reset.
      
    400 BAD REQUEST if password != password confirmation
      detail: Password confirmation failed.
    
    400 BAD REQUEST if token doesn't exist.
      detail: Invalid token: <token>
    
    400 BAD REQUEST if token has expired.
      detail: Expired token: <token>
    
    400 BAD REQUEST if password is invalid.
      detail: 
        password: [<stringlist with errors>]
    
    404 NOT FOUND user doens't exist or is deleted.
      detail: No User matches the given query.
  """
  

  token = request.data.get('token')
  if request.data.get('password') != request.data.get('password_confirmation'):
    return Response({"detail": "Password confirmation failed."}, status=400)
  try:

    token_obj = EmailVerificationToken.objects.get(token=token)
  except EmailVerificationToken.DoesNotExist:
    return Response({"detail": "Invalid token: " + str(token)}, status=400)
  
  if token_obj.is_expired():
    return Response({"detail": "Expired token: " + str(token_obj.token)}, status=400)
  
  user = token_obj.user

  if not user.is_active:
    return Response({"detail": "No User matches the given query."}, status=404)
  new_password = request.data.get('password')

  serializer = Password_validation_serializer(data={'password':new_password})
  if serializer.is_valid():
    user.restore()
    user.set_password(new_password)
    user.save()

    token_obj.delete()
    return Response({"detail":"Password succesfully reset."}, status=200)
  else:
    return Response({"detail":serializer.errors}, status=400)