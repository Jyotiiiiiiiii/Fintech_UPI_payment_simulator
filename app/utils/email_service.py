"""
Email service for sending transaction notifications
Uses Gmail SMTP with Google App Password for authentication
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration - these should be set in environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@Fin_UPI.com")


def is_email_configured() -> bool:
    """Check if email is properly configured"""
    return bool(EMAIL_USERNAME and EMAIL_PASSWORD)


def send_transaction_email(
    to_email: str,
    subject: str,
    body: str
) -> bool:
    """
    Send an email to the specified address
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not is_email_configured():
        logger.warning("Email not configured. Skipping email notification.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        
        # Login with App Password
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # Send email
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        
        # Close connection
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def send_transaction_notification(
    sender_email: str,
    sender_name: str,
    receiver_email: str,
    receiver_name: str,
    amount: float,
    transaction_id: int,
    description: Optional[str] = None,
    timestamp: Optional[datetime] = None
) -> tuple[bool, bool]:
    """
    Send transaction notification emails to both sender and receiver
    
    Args:
        sender_email: Sender's email address
        sender_name: Sender's name
        receiver_email: Receiver's email address
        receiver_name: Receiver's name
        amount: Transaction amount
        transaction_id: Transaction ID
        description: Optional transaction description
        timestamp: Transaction timestamp
    
    Returns:
        tuple: (sender_email_sent, receiver_email_sent)
    """
    if timestamp is None:
        timestamp = datetime.utcnow()
    
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Email to sender
    sender_subject = f"💸 Payment Sent - ₹{amount}"
    sender_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2E7D32;">Payment Sent Successfully!</h2>
        <p>Hello {sender_name},</p>
        <p>Your payment has been processed successfully.</p>
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Amount:</strong> ₹{amount}</p>
            <p><strong>Sent To:</strong> {receiver_name}</p>
            <p><strong>Transaction ID:</strong> #{transaction_id}</p>
            <p><strong>Description:</strong> {description or 'N/A'}</p>
            <p><strong>Date & Time:</strong> {formatted_time}</p>
        </div>
        <p style="color: #666; font-size: 12px;">
            This is an automated notification from Fin_UPI.<br>
            Please do not reply to this email.
        </p>
    </body>
    </html>
    """
    
    # Email to receiver
    receiver_subject = f"💰 Payment Received - ₹{amount}"
    receiver_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #1565C0;">Payment Received!</h2>
        <p>Hello {receiver_name},</p>
        <p>You have received a payment.</p>
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Amount:</strong> ₹{amount}</p>
            <p><strong>Received From:</strong> {sender_name}</p>
            <p><strong>Transaction ID:</strong> #{transaction_id}</p>
            <p><strong>Description:</strong> {description or 'N/A'}</p>
            <p><strong>Date & Time:</strong> {formatted_time}</p>
        </div>
        <p style="color: #666; font-size: 12px;">
            This is an automated notification from Fin_UPI.<br>
            Please do not reply to this email.
        </p>
    </body>
    </html>
    """
    
    # Send emails
    sender_sent = send_transaction_email(sender_email, sender_subject, sender_body)
    receiver_sent = send_transaction_email(receiver_email, receiver_subject, receiver_body)
    
    return sender_sent, receiver_sent
