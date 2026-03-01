#!/usr/bin/env python3
"""
Email MCP Server

Sends emails via Gmail API.
Supports draft mode and approval workflow.
"""

import os
import sys
import base64
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


class EmailMCPServer:
    """
    MCP Server for email operations.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize Email MCP Server.
        
        Args:
            dry_run: If True, only log emails without sending
        """
        self.dry_run = dry_run
        
        # Email configuration
        self.email_address = os.getenv('GMAIL_EMAIL_ADDRESS', '')
        self.app_password = os.getenv('GMAIL_APP_PASSWORD', '')
        
        # Set up logging
        self._setup_logging()
        
        self.logger.info(f'Email MCP Server initialized (dry_run={dry_run})')
        self.logger.info(f'Email: {self.email_address}')
    
    def _setup_logging(self) -> None:
        """Set up logging."""
        self.logger = logging.getLogger('EmailMCP')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
        attachment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: If True, treat body as HTML
            attachment: Optional attachment path
            
        Returns:
            Result dictionary with status and message_id
        """
        self.logger.info(f'Sending email to: {to}')
        self.logger.info(f'Subject: {subject}')
        
        if self.dry_run:
            self.logger.info('[DRY RUN] Email not sent (dry run mode)')
            return {
                'status': 'dry_run',
                'message': 'Email would be sent (dry run mode)',
                'to': to,
                'subject': subject
            }
        
        try:
            # Import Gmail libraries only when needed
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request
            
            # Check credentials
            if not self.email_address or not self.app_password:
                raise ValueError('Gmail credentials not configured')
            
            # Create message
            message = self._create_message(
                self.email_address,
                to,
                subject,
                body,
                html,
                attachment
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
            
            self.logger.info(f'Email sent! Message ID: {sent_message["id"]}')
            
            return {
                'status': 'success',
                'message_id': sent_message['id'],
                'to': to,
                'subject': subject
            }
            
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')
            return {
                'status': 'error',
                'error': str(e),
                'to': to,
                'subject': subject
            }
    
    def _create_message(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False,
        attachment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create email message."""
        message = MIMEMultipart()
        message['from'] = from_email
        message['to'] = to_email
        message['subject'] = subject
        
        # Add body
        content_type = 'html' if html else 'plain'
        message.attach(MIMEText(body, content_type))
        
        # Add attachment if provided
        if attachment:
            with open(attachment, 'rb') as f:
                file_data = f.read()
                filename = Path(attachment).name
            
            part = MIMEText(base64.urlsafe_b64encode(file_data).decode())
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            message.attach(part)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        return {'raw': raw_message}
    
    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> Dict[str, Any]:
        """
        Create email draft (doesn't send).
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            html: If True, treat body as HTML
            
        Returns:
            Result dictionary with draft_id
        """
        self.logger.info(f'Creating draft email to: {to}')
        self.logger.info(f'Subject: {subject}')
        
        if self.dry_run:
            self.logger.info('[DRY RUN] Draft not created (dry run mode)')
            return {
                'status': 'dry_run',
                'message': 'Draft would be created (dry run mode)',
                'to': to,
                'subject': subject
            }
        
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Create message
            message = self._create_message(
                self.email_address,
                to,
                subject,
                body,
                html
            )
            
            # Authenticate
            creds = Credentials.from_authorized_user_info({
                'token': self.app_password
            })
            
            # Build service
            service = build('gmail', 'v1', credentials=creds)
            
            # Create draft
            draft = service.users().drafts().create(
                userId='me',
                body={'message': message}
            ).execute()
            
            self.logger.info(f'Draft created! Draft ID: {draft["id"]}')
            
            return {
                'status': 'success',
                'draft_id': draft['id'],
                'to': to,
                'subject': subject
            }
            
        except Exception as e:
            self.logger.error(f'Error creating draft: {e}')
            return {
                'status': 'error',
                'error': str(e),
                'to': to,
                'subject': subject
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test email connection.
        
        Returns:
            Connection status
        """
        self.logger.info('Testing email connection...')
        
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
            
            # Try to get profile
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


def main():
    """Main entry point for Email MCP Server."""
    import json
    
    print('=' * 60)
    print('Email MCP Server - Silver Tier')
    print('=' * 60)
    
    # Check if running in dry run mode
    dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'
    
    # Create server
    server = EmailMCPServer(dry_run=dry_run)
    
    print(f'Dry Run: {dry_run}')
    print('')
    
    # Test connection
    result = server.test_connection()
    print('Connection Test:')
    print(json.dumps(result, indent=2))
    print('')
    
    # If command line args provided, send email
    if len(sys.argv) >= 4:
        to = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        
        print(f'Sending test email to: {to}')
        result = server.send_email(to, subject, body)
        print('Result:')
        print(json.dumps(result, indent=2))
    
    print('')
    print('=' * 60)
    print('Email MCP Server ready!')
    print('=' * 60)


if __name__ == '__main__':
    main()
