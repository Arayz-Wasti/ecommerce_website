from django.core.mail import send_mail
from django.conf import settings
def send_email_to_user():
    subject = 'Order Confirmation - iPhone 15'
    message ="""
Dear Momina Saeed,
Thank you for shopping with Daraz. We are pleased to confirm your order for the iPhone 15.
Order Details:
Product: iPhone 15 (Black)
Order Number: DZ-ORD-1202747382
Payment Method: Cash on Delivery (COD)
Recipient Details:
Name: Momina Saeed
Father's Name: Saeed Ahmad
Location: Bahawalpur, Pakistan
Mobile Number: +92 322 4485135
Your order is being processed and will be shipped to you soon. You will receive a notification once the order is dispatched along with tracking details.

Note: Please be aware that in the unlikely event you do not receive your order, the price of the order will be deducted from your bank account by tracing your account information. If necessary, we may also take legal action to ensure compliance with our payment policies.
If you have any questions or need further assistance, please do not hesitate to contact our customer support team.
Thank you for choosing Daraz. We hope you enjoy your new iPhone 15!
Best regards,
Customer Support Team
Daraz
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['naimatullahkhan0987@gmail.com']
    send_mail(subject, message, from_email, recipient_list)

def forget_password_email(email,token):
    subject = 'Reset Password'
    message = f"Hi, click on the link to reset your password http://127.0.0.1:8098/forget_password/{token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list)