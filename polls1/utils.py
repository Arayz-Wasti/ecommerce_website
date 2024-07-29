from django.core.mail import send_mail
from django.conf import settings
def send_email_to_user():
    subject = 'Order Confirmation - iPhone 15'
    message ="your order has been successfully done"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['naimatullahkhan0987@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

def forget_password_email(email,token):
    subject = 'Reset Password'
    message = f"Hi, click on the link to reset your password http://127.0.0.1:8098/forget_password/{token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list)