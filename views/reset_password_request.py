from ._import_package import *
from users.email import send_password_reset_email

@api_view(['POST'])
def reset_password_request(request):
  """
  Send email request to change password.
  1. Get user with email or return 404.
  2. Delete auth token of user if any.
  3. Check if user is soft deleted return 404 if true.
  4. Set temporary random password overwriting the old one.
  5. Create email verification token.
  6. send email to user.

  Path:
    BASE_URL/api/reset-password/
    
  Requires:
    Body:
      email: <email>
      
    Returns:
      200 OK if succesfull
        detail: Email has been send
        
      404 NOT FOUND if user has been deleted
        detail: User does not exist

      404 NOT FOUND if user with <email> does not exist
        detail: User does not exist
  """
  
  email = request.data.get('email')  
  try:
    user = User.objects.get(email=email)
    try:
      user.auth_token.delete()
    except:
      pass      
    
    if not user.is_active:
      return Response({"detail":"User does not exist"}, status=404)
    else:
      password = User.objects.make_random_password(length=12, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%^&*')
      user.set_password(password)
      user.save()      
      
      verif_token, created =  EmailVerificationToken.objects.get_or_create(user=user)
      send_password_reset_email(user, verification_token=verif_token)
    return Response({"detail":"Email has been send."}, status=200)
  except User.DoesNotExist:
    return Response({"detail":"User does not exist"}, status=404)