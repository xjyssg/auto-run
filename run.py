import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import the function from fetch.py
import sys
sys.path.append('.')
from fetch import check_target_room_found

def send_email(content):
    # Email configuration
    sender_email = os.environ["EMAIL_USER"]
    sender_password = os.environ["EMAIL_PASS"]
    receiver_email = os.environ["EMAIL_TO"]
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Joellll Japan Hotel Notification"
    
    # Email body
    body = f"Found available date{content}."
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
    print("Checking for target room...")
    date_list = ["2026-02-21 00:00:00",
                 "2026-02-22 00:00:00"
                 "2026-02-23 00:00:00",
                 "2026-02-25 00:00:00"]
    result = []
    for date in date_list:
        if check_target_room_found(date):
            print("Target room found at %s!", date)
            result.append(date)
    if result:
        send_email("".join(result))
    else:
        print("Target room not found.")
