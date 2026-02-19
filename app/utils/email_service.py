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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    configured = bool(EMAIL_USERNAME and EMAIL_PASSWORD)
    logger.info(f"Checking email configuration: HOST={EMAIL_HOST}, USER={EMAIL_USERNAME}, PASS_SET={bool(EMAIL_PASSWORD)}")
    return configured


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
    logger.info(f"Attempting to send email to {to_email} with subject: {subject}")
    
    if not is_email_configured():
        logger.warning("Email not configured. Check EMAIL_USERNAME and EMAIL_PASSWORD in .env file.")
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
        logger.info(f"Connecting to SMTP server {EMAIL_HOST}:{EMAIL_PORT}...")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.set_debuglevel(1)  # Enable detailed SMTP debug output
        
        logger.info("Starting TLS...")
        server.starttls()
        
        # Login with App Password
        logger.info(f"Attempting login for {EMAIL_USERNAME}...")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        # Send email
        logger.info(f"Sending email from {EMAIL_FROM} to {to_email}...")
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        
        # Close connection
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logger.error(f"SMTP Authentication failed for {EMAIL_USERNAME}. Verify App Password.")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred while sending to {to_email}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending email to {to_email}: f{str(e)}")
        import traceback
        logger.error(traceback.format_exc())
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
    <body style="font-family: 'Inter', Arial, sans-serif; padding: 20px; background-color: #f8fafc; color: #0f172a;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 32px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h2 style="color: #059669; margin-top: 0;">Payment Sent Successfully</h2>
            <p>Hello {sender_name},</p>
            <p>Your payment has been processed successfully.</p>
            <div style="background-color: #f1f5f9; padding: 20px; border-radius: 6px; margin: 24px 0;">
                <p style="margin: 8px 0;"><strong>Amount:</strong> ₹{amount}</p>
                <p style="margin: 8px 0;"><strong>Sent To:</strong> {receiver_name}</p>
                <p style="margin: 8px 0;"><strong>Transaction ID:</strong> #{transaction_id}</p>
                <p style="margin: 8px 0;"><strong>Description:</strong> {description or 'N/A'}</p>
                <p style="margin: 8px 0;"><strong>Date & Time:</strong> {formatted_time}</p>
            </div>
            <p style="color: #64748b; font-size: 12px; margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
                This is an automated notification from UPI Payment Simulator.<br>
                Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Email to receiver
    receiver_subject = f"💰 Payment Received - ₹{amount}"
    receiver_body = f"""
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; padding: 20px; background-color: #f8fafc; color: #0f172a;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 32px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h2 style="color: #0f172a; margin-top: 0;">Payment Received</h2>
            <p>Hello {receiver_name},</p>
            <p>You have received a payment to your account.</p>
            <div style="background-color: #f1f5f9; padding: 20px; border-radius: 6px; margin: 24px 0;">
                <p style="margin: 8px 0;"><strong>Amount:</strong> ₹{amount}</p>
                <p style="margin: 8px 0;"><strong>Received From:</strong> {sender_name}</p>
                <p style="margin: 8px 0;"><strong>Transaction ID:</strong> #{transaction_id}</p>
                <p style="margin: 8px 0;"><strong>Description:</strong> {description or 'N/A'}</p>
                <p style="margin: 8px 0;"><strong>Date & Time:</strong> {formatted_time}</p>
            </div>
            <p style="color: #64748b; font-size: 12px; margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
                This is an automated notification from UPI Payment Simulator.<br>
                Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Send emails
    sender_sent = send_transaction_email(sender_email, sender_subject, sender_body)
    receiver_sent = send_transaction_email(receiver_email, receiver_subject, receiver_body)
    
    return sender_sent, receiver_sent
