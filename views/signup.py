from ._import_package import *
from users.email import send_confirmation_email

@api_view(['POST'])
def signup(request):
  """
  Registers new User or reactivates soft deleted User.
  1. create/recovers User
  2. create email verification token.
  3. send email with link to activate account.
  
  Path:
    BASE_URL/api/signup/
    
  Requires:
    Body:
      username: <username>,
      password: <password>,
      password_confirmation: <password>,
      email: <email>
      
    Returns:
      200 OK if succesfull
        detail: User created. Confirmation email sent.
        
      400 BAD REQUEST if password != password confirmation
        detail: Password confirmation failed.
        
      400 BAD REQUEST if non-deleted user with email and/or username already exists
        detail:
          username: [
              A user with that username already exists.
          ],
          email: [
              "user with this email already exists."
          ]      
  """
  username = request.data.get('username')
  email = request.data.get('email')
  password = request.data.get('password')
  password_confirmation = request.data.get('password_confirmation')
  
  # Check password confirmation
  if password != password_confirmation:
    return Response({"detail": "Password confirmation failed."}, status=400)
  
  try:
    # In case user has been soft deleted.
    user = User.objects.get(email = email, is_active = False, deleted_at__isnull=False)
    user.restore()    
  except User.DoesNotExist:  
    # In case user is new.
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(): #check if username and email already exist
      serializer.save()
      user = User.objects.get(username=username)     
    else:    
      return Response({"detail":serializer.errors}, status=400)
    
  user.set_password(password)
  user.is_active = False      
  user.save()
  
  token, created = EmailVerificationToken.objects.update_or_create(user=user)
  send_confirmation_email(user, token)
  return Response({"detail":"User created. Confirmation email sent."})