#!/usr/bin/env python3
"""
Gmail Auto-Reply System

Automatically replies to emails based on templates and rules.
Integrates with Approval Workflow for sensitive emails.
"""

import sys
import os
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
import logging
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


class GmailAutoReplier:
    """
    Automatically replies to Gmail messages.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize Gmail Auto-Replier.
        
        Args:
            dry_run: If True, only simulate sending without actual send
        """
        self.dry_run = dry_run
        
        # Email credentials - Load from email_mcp .env file
        env_path = Path(__file__).parent / 'mcp_servers' / 'email_mcp' / '.env'
        load_dotenv(env_path)
        
        self.email_address = os.getenv('GMAIL_EMAIL_ADDRESS', '')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD', '')
        
        # Set up logging
        self._setup_logging()
        
        # Load reply templates
        self.templates = self._load_templates()
        
        self.logger.info(f'Gmail Auto-Replier initialized (dry_run={dry_run})')
        self.logger.info(f'Email: {self.email_address}')
    
    def _setup_logging(self) -> None:
        """Set up logging."""
        self.logger = logging.getLogger('GmailAutoReplier')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load email reply templates."""
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
            
            'out_of_office': '''Thank you for your email.

I am currently out of the office with limited access to email. I will return on [RETURN DATE].

For urgent matters, please contact [ALTERNATE CONTACT] at [ALTERNATE EMAIL].

Otherwise, I will respond to your email when I return.

Best regards,
[Your Name]''',
            
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
    
    def analyze_email(self, subject: str, body: str, from_email: str) -> str:
        """
        Analyze email and determine reply template.
        
        Args:
            subject: Email subject
            body: Email body
            from_email: Sender email
            
        Returns:
            Template name to use
        """
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Check for invoice-related keywords
        if any(kw in subject_lower or kw in body_lower for kw in ['invoice', 'billing', 'payment']):
            return 'invoice_inquiry'
        
        # Check for meeting request
        if any(kw in subject_lower or kw in body_lower for kw in ['meeting', 'call', 'schedule', 'appointment']):
            return 'meeting_request'
        
        # Check for payment confirmation
        if any(kw in subject_lower or kw in body_lower for kw in ['payment received', 'payment confirmation', 'receipt']):
            return 'payment_received'
        
        # Check for support request
        if any(kw in subject_lower or kw in body_lower for kw in ['support', 'help', 'issue', 'problem', 'error']):
            return 'support_ticket'
        
        # Default template
        return 'default'
    
    def send_reply(
        self,
        to: str,
        subject: str,
        original_body: str,
        from_email: str,
        custom_template: str = None
    ) -> Dict[str, Any]:
        """
        Send automatic reply.
        
        Args:
            to: Recipient email
            subject: Original email subject
            original_body: Original email body
            from_email: Sender email
            custom_template: Optional custom template name
            
        Returns:
            Result dictionary
        """
        # Determine template
        if custom_template:
            template_name = custom_template
        else:
            template_name = self.analyze_email(subject, original_body, from_email)
        
        # Get template content
        template = self.templates.get(template_name, self.templates['default'])
        
        # Customize template (replace placeholders)
        reply_body = template.replace('[AMOUNT]', '$XXX')
        reply_body = reply_body.replace('[DATE]', 'Today')
        reply_body = reply_body.replace('[REFERENCE]', 'REF-XXX')
        reply_body = reply_body.replace('[TICKET_ID]', f'TICKET-{len(original_body)}')
        reply_body = reply_body.replace('[PRIORITY]', 'Normal')
        reply_body = reply_body.replace('[RESPONSE_TIME]', '24-48 hours')
        
        self.logger.info(f'Sending auto-reply to: {to}')
        self.logger.info(f'Using template: {template_name}')
        
        if self.dry_run:
            self.logger.info('[DRY RUN] Email not sent (dry run mode)')
            return {
                'status': 'dry_run',
                'message': 'Auto-reply would be sent (dry run mode)',
                'to': to,
                'template': template_name,
                'reply_preview': reply_body[:200] + '...'
            }
        
        try:
            # Import Gmail libraries
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Check credentials
            if not self.email_address or not self.app_password:
                raise ValueError('Gmail credentials not configured')
            
            # Create message
            message = self._create_message(
                self.email_address,
                to,
                f'Re: {subject}',
                reply_body
            )
            
            # Authenticate
            creds = Credentials.from_authorized_user_info({
                'token': self.app_password
            })
            
            # Build service
            service = build('gmail', 'v1', credentials=creds)
            
            # Send email
            sent_message = service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            self.logger.info(f'Auto-reply sent! Message ID: {sent_message["id"]}')
            
            return {
                'status': 'success',
                'message_id': sent_message['id'],
                'to': to,
                'template': template_name,
                'reply_preview': reply_body[:200] + '...'
            }
            
        except Exception as e:
            self.logger.error(f'Error sending auto-reply: {e}')
            return {
                'status': 'error',
                'error': str(e),
                'to': to,
                'template': template_name
            }
    
    def _create_message(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        body: str
    ) -> Dict[str, Any]:
        """Create email message."""
        message = MIMEMultipart()
        message['from'] = from_email
        message['to'] = to_email
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        return {'raw': raw_message}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test email connection."""
        self.logger.info('Testing Gmail Auto-Replier connection...')
        
        if not self.email_address:
            return {
                'status': 'error',
                'message': 'Email address not configured'
            }
        
        if not self.app_password:
            return {
                'status': 'error',
                'message': 'App password not configured'
            }
        
        if self.dry_run:
            return {
                'status': 'success',
                'message': 'Configuration OK (dry run mode)',
                'email': self.email_address
            }
        
        # Try to authenticate
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            creds = Credentials.from_authorized_user_info({
                'token': self.app_password
            })
            
            service = build('gmail', 'v1', credentials=creds)
            profile = service.users().getProfile().execute()
            
            return {
                'status': 'success',
                'message': 'Connection successful',
                'email': profile['emailAddress']
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection failed: {str(e)}'
            }
    
    def get_available_templates(self) -> List[str]:
        """Get list of available reply templates."""
        return list(self.templates.keys())


def main():
    """Main entry point for Gmail Auto-Replier."""
    print('=' * 60)
    print('Gmail Auto-Replier - Silver Tier')
    print('=' * 60)
    
    # Check if running in dry run mode
    dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'
    
    # Create replier
    replier = GmailAutoReplier(dry_run=dry_run)
    
    print(f'Dry Run: {dry_run}')
    print('')
    
    # Test connection
    result = replier.test_connection()
    print('Connection Test:')
    print(json.dumps(result, indent=2))
    print('')
    
    # Show available templates
    print('Available Reply Templates:')
    for template in replier.get_available_templates():
        print(f'  - {template}')
    print('')
    
    # Test auto-reply
    print('Testing Auto-Reply:')
    print('-' * 60)
    test_result = replier.send_reply(
        to='test@example.com',
        subject='Invoice Inquiry',
        original_body='Can you send me the invoice?',
        from_email='client@example.com'
    )
    print(json.dumps(test_result, indent=2))
    print('-' * 60)
    print('')
    
    print('=' * 60)
    print('Gmail Auto-Replier ready!')
    print('=' * 60)


if __name__ == '__main__':
    main()
