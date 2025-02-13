from postmarker.core import PostmarkClient
from django.conf import settings

def send_postmark_email(to_email, subject, message):
  """
  Sends email using postmark

  Args:
      to_email (String): email string
      subject (String): email subject string
      message (String): html string

  Returns:
      _type_: postmarker response
  """
  client = PostmarkClient(server_token=settings.POSTMARK_API_KEY)
  
  if settings.DEBUG and not settings.POSTMARK_DEBUG_SEND_EMAIL:
    print(message)
  else:    
    if settings.POSTMARK_DEBUG_SEND_EMAIL and settings.POSTMARK_DEBUG_RECEIVER_EMAIL:
      to_email = settings.POSTMARK_DEBUG_RECEIVER_EMAIL
      
    email = client.emails.Email(
      From = settings.POSTMARK_SENDER_EMAIL,
      To = to_email,
      Subject = subject,
      HtmlBody = message,
      MessageStream = 'outbound',
    )
    
    response = email.send()  
    return response