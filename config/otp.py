import random
import smtplib

def generate_otp():
    # Generate a 6-digit OTP
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "sender.usb.simulation@gmail.com"
    smtp_password = "qbnnswihmmudjsou"

    # Email content
    sender_email = "sender.usb.simulation@gmail.com"
    receiver_email = email
    subject = "OTP Verification"
    body = f"Your OTP is: {otp}"

    # Create SMTP connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send email
        server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")