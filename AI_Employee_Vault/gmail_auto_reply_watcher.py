#!/usr/bin/env python3
"""
Gmail Auto-Reply Watcher

Continuously monitors Gmail for new emails and sends automatic replies.
Runs 24/7 in the background.
"""

import sys
import os
import time
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent / 'mcp_servers' / 'email_mcp' / '.env'
load_dotenv(env_path)

# Import Gmail libraries
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GmailAutoReplyWatcher:
    """
    Monitors Gmail and sends automatic replies.
    """
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize watcher.
        
        Args:
            check_interval: Seconds between checks (default: 60)
        """
        self.email_address = os.getenv('GMAIL_EMAIL_ADDRESS', '')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD', '').replace(' ', '')
        self.check_interval = check_interval
        
        # Track processed message IDs
        self.processed_ids: set = set()
        
        # Reply templates
        self.templates = self._load_templates()
        
        # Set up logging
        self._setup_logging()
        
        self.logger.info(f'Gmail Auto-Reply Watcher initialized')
        self.logger.info(f'Monitoring: {self.email_address}')
        self.logger.info(f'Check interval: {check_interval}s')
    
    def _setup_logging(self) -> None:
        """Set up logging."""
        self.logger = logging.getLogger('GmailAutoReplyWatcher')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            log_file = Path(__file__).parent / 'Logs' / 'gmail_auto_reply.log'
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load reply templates."""
        return {
            'invoice_inquiry': '''Dear Valued Client,

Thank you for your inquiry regarding our invoice.

We have received your message and our team is reviewing it. We will get back to you within 24 hours with a detailed response.

If this is urgent, please call us at [Your Phone Number].

Best regards,
Personal AI Employee Hackathon-0 System
[Your Company Name]''',
            
            'general_inquiry': '''Thank you for contacting us!

We have received your email and appreciate your interest in our services.

Our team will review your message and respond within 24-48 hours.

In the meantime, feel free to visit our website: [Your Website]

Best regards,
Personal AI Employee Hackathon-0 System''',
            
            'meeting_request': '''Thank you for your meeting request.

We have received your request and will check our availability.

Our team will respond with available time slots within 24 hours.

Looking forward to connecting with you!

Best regards,
Personal AI Employee Hackathon-0 System''',
            
            'payment_received': '''Dear Valued Client,

We have received your payment. Thank you!

Payment Details:
- Amount: [AMOUNT]
- Date: [DATE]
- Reference: [REFERENCE]

Your account has been updated accordingly.

If you have any questions, please don't hesitate to contact us.

Best regards,
Personal AI Employee Hackathon-0 System''',
            
            'support_ticket': '''Dear Customer,

Thank you for contacting our support team.

Your support ticket has been created:
Ticket ID: [TICKET_ID]
Priority: [PRIORITY]
Estimated Response Time: [RESPONSE_TIME]

Our team will assist you shortly.

Best regards,
Support Team''',
            
            'default': '''Thank you for your email.

We have received your message and will respond as soon as possible.

Best regards,
Personal AI Employee Hackathon-0 System'''
        }
    
    def check_for_new_emails(self) -> List[Dict[str, Any]]:
        """
        Check for new unread emails.
        
        Returns:
            List of new emails
        """
        new_emails = []
        
        try:
            # Import Gmail libraries
            import smtplib
            
            # Check credentials
            if not self.email_address or not self.app_password:
                self.logger.error('Gmail credentials not configured')
                return []
            
            # Connect to Gmail IMAP to fetch emails
            import imaplib
            
            self.logger.info('Connecting to Gmail IMAP...')
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email_address, self.app_password)
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                return []
            
            email_ids = messages[0].split()
            
            self.logger.info(f'Found {len(email_ids)} unread email(s)')
            
            for email_id in email_ids:
                email_id_str = email_id.decode()
                
                # Skip if already processed
                if email_id_str in self.processed_ids:
                    continue
                
                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                # Parse email
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = self._parse_email(response_part[1])
                        
                        if msg:
                            new_emails.append(msg)
                            self.processed_ids.add(email_id_str)
                            
                            self.logger.info(f'New email from: {msg["from"]}')
                            self.logger.info(f'Subject: {msg["subject"]}')
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            self.logger.error(f'Error checking emails: {e}')
        
        return new_emails
    
    def _parse_email(self, raw_email: bytes) -> Dict[str, Any]:
        """Parse raw email data."""
        from email.parser import BytesParser
        from email.policy import default
        
        msg = BytesParser(policy=default).parsebytes(raw_email)
        
        return {
            'from': msg.get('From', ''),
            'to': msg.get('To', ''),
            'subject': msg.get('Subject', ''),
            'date': msg.get('Date', ''),
            'body': self._get_email_body(msg),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_email_body(self, msg) -> str:
        """Extract email body."""
        body = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = msg.get_payload()
        
        return body[:1000]  # Limit to 1000 characters
    
    def analyze_email(self, subject: str, body: str) -> str:
        """Determine reply template based on email content."""
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check for invoice-related keywords
        if any(kw in subject_lower or kw in body_lower for kw in ['invoice', 'billing', 'payment']):
            return 'invoice_inquiry'
        
        # Check for meeting request
        if any(kw in subject_lower or kw in body_lower for kw in ['meeting', 'call', 'schedule', 'appointment']):
            return 'meeting_request'
        
        # Check for support request
        if any(kw in subject_lower or kw in body_lower for kw in ['support', 'help', 'issue', 'problem', 'error']):
            return 'support_ticket'
        
        # Default template
        return 'default'
    
    def send_reply(self, to: str, subject: str, body: str) -> bool:
        """
        Send automatic reply.
        
        Args:
            to: Recipient email
            subject: Original email subject
            body: Original email body
            
        Returns:
            True if sent successfully
        """
        import smtplib
        from email.mime.text import MIMEText
        
        # Determine template
        template_name = self.analyze_email(subject, body)
        template = self.templates.get(template_name, self.templates['default'])
        
        # Create reply
        reply_subject = f'Re: {subject}'
        reply_body = template
        
        # Create message
        msg = MIMEText(reply_body, 'plain')
        msg['From'] = self.email_address
        msg['To'] = to
        msg['Subject'] = reply_subject
        
        try:
            # Connect to Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.app_password)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f'Auto-reply sent to: {to}')
            self.logger.info(f'Template used: {template_name}')
            
            # Log to file
            self._log_reply(to, subject, template_name, 'success')
            
            return True
            
        except Exception as e:
            self.logger.error(f'Error sending reply: {e}')
            self._log_reply(to, subject, template_name, f'error: {e}')
            
            return False
    
    def _log_reply(self, to: str, subject: str, template: str, status: str) -> None:
        """Log reply to CSV file."""
        log_file = Path(__file__).parent / 'Logs' / 'auto_reply_log.csv'
        
        # Create file if doesn't exist
        if not log_file.exists():
            log_file.write_text('timestamp,to,subject,template,status\n')
        
        # Append log entry
        timestamp = datetime.now().isoformat()
        log_entry = f'{timestamp},{to},"{subject}",{template},{status}\n'
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def run_continuous(self) -> None:
        """Run watcher continuously."""
        self.logger.info('Starting continuous Gmail monitoring...')
        self.logger.info('Press Ctrl+C to stop')
        print('')
        print('=' * 60)
        print('Gmail Auto-Reply Watcher is now running!')
        print('=' * 60)
        print(f'Monitoring: {self.email_address}')
        print(f'Check interval: {self.check_interval} seconds')
        print('')
        print('Waiting for new emails...')
        print('Press Ctrl+C to stop')
        print('=' * 60)
        
        try:
            while True:
                # Check for new emails
                new_emails = self.check_for_new_emails()
                
                # Send replies
                for email in new_emails:
                    self.logger.info(f'Processing email from {email["from"]}')
                    
                    success = self.send_reply(
                        to=email['from'],
                        subject=email['subject'],
                        body=email['body']
                    )
                    
                    if success:
                        print(f'✅ Auto-reply sent to: {email["from"]}')
                    else:
                        print(f'❌ Failed to send reply to: {email["from"]}')
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Watcher stopped by user')
            print('')
            print('Watcher stopped.')


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        check_interval = int(sys.argv[1])
    else:
        check_interval = 60  # Default: check every 60 seconds
    
    # Create watcher
    watcher = GmailAutoReplyWatcher(check_interval)
    
    # Run continuously
    watcher.run_continuous()


if __name__ == '__main__':
    main()
