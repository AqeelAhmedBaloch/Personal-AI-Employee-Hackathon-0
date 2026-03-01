#!/usr/bin/env python3
"""
Simple Gmail Test

Sends test email using Gmail SMTP (simple method).
No OAuth required - just App Password.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / 'mcp_servers' / 'email_mcp' / '.env'
load_dotenv(env_path)

def send_simple_email(to_email, subject, body):
    """
    Send email using Gmail SMTP.
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
    """
    from_email = os.getenv('GMAIL_EMAIL_ADDRESS', '')
    password = os.getenv('GMAIL_APP_PASSWORD', '')
    
    # Remove spaces from password
    password = password.replace(' ', '')
    
    if not from_email or not password:
        print('Error: Email credentials not configured')
        return False
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail SMTP
        print(f'Connecting to Gmail SMTP...')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print(f'Logging in as {from_email}...')
        server.login(from_email, password)
        
        # Send email
        print(f'Sending email to {to_email}...')
        server.send_message(msg)
        server.quit()
        
        print('')
        print('Email sent successfully!')
        print(f'From: {from_email}')
        print(f'To: {to_email}')
        print(f'Subject: {subject}')
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f'Authentication Error: {e}')
        print('')
        print('Possible solutions:')
        print('1. Make sure you are using App Password, not regular password')
        print('2. Generate App Password from: https://myaccount.google.com/apppasswords')
        print('3. Make sure 2-Step Verification is enabled')
        return False
        
    except Exception as e:
        print(f'Error: {e}')
        return False


def main():
    print('=' * 60)
    print('Simple Gmail Test - Silver Tier')
    print('=' * 60)
    print('')
    
    # Get recipient email
    to_email = input('Enter recipient email (or press Enter for self-test): ').strip()
    
    if not to_email:
        to_email = os.getenv('GMAIL_EMAIL_ADDRESS', '')
        print(f'Using configured email: {to_email}')
    
    if not to_email:
        print('Error: No recipient email provided')
        return
    
    # Email content
    subject = 'Test Email from AI Employee'
    body = '''Hello!

This is a test email from your AI Employee system.

If you are receiving this email, it means your Gmail Auto-Replier is configured correctly and can send emails!

Best regards,
AI Employee System
'''
    
    print('')
    print(f'To: {to_email}')
    print(f'Subject: {subject}')
    print('')
    print('Sending...')
    print('-' * 60)
    
    # Send email
    success = send_simple_email(to_email, subject, body)
    
    print('-' * 60)
    print('')
    
    if success:
        print('Test completed successfully!')
        print('Check your inbox for the test email.')
    else:
        print('Test failed. Please check the error message above.')

if __name__ == '__main__':
    main()
