import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Email configuration
    sender_email = os.environ.get("EMAIL_USER", "your_email")
    sender_password = os.environ.get("EMAIL_PASS", "your_app_password")
    receiver_email = os.environ.get("EMAIL_TO", "your_receiver")
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Scheduled Notification"
    
    # Email body
    body = "This is an automated email sent every 5 minutes."
    message.attach(MIMEText(body, "plain"))
    
    # Check if credentials are properly set
    if sender_email == "your_email" or sender_password == "your_app_password":
        print("Email credentials not set. Please configure SENDER_EMAIL and SENDER_PASSWORD environment variables.")
        return False
    
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"Email authentication failed. Please check your email credentials. Error: {e}")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("hello world")
    send_email()
