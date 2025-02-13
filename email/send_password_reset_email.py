from .send_email import send_postmark_email
from django.template.loader import render_to_string
from users.models import EmailVerificationToken, User
from django.conf import settings

def send_password_reset_email(user:User, verification_token:EmailVerificationToken):
  """
  Create email content and send.
  Assume that frontend link exists:
  FRONT_END_URL/user/reset-succes?idvalue=<uuid>
  where the uuid is the verification token value.
  This token is used to verify the password reset.
  """  
  url_id = settings.FRONT_END_URL + '/user/reset-succes?idvalue=' + str(verification_token.token)
  
  context = {
    'username':user.username,
    'site_url':url_id
  }  
  
  html_message = render_to_string('password_reset_email.html', context)
    
  send_postmark_email(to_email=user.email,subject='confirm sign-up',message=html_message)