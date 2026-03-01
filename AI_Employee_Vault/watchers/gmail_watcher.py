#!/usr/bin/env python3
"""
Gmail Watcher

Monitors Gmail for new important emails.
Uses Gmail API to fetch unread messages.

Setup Required:
1. Enable Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com
2. Create OAuth credentials
3. Download credentials.json to this folder
"""

import sys
import time
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import base watcher
sys.path.insert(0, str(Path(__file__).parent / 'watchers'))
from base_watcher import BaseWatcher


class GmailWatcher(BaseWatcher):
    """
    Watcher that monitors Gmail for new messages.
    """
    
    def __init__(self, vault_path: str, credentials_path: str = None, check_interval: int = 120):
        """
        Initialize Gmail watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            credentials_path: Path to Gmail credentials file
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        
        self.credentials_path = credentials_path or (Path(__file__).parent / 'credentials.json')
        
        # Keywords to prioritize
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 'important']
        
        # Track processed message IDs
        self.processed_ids: set = set()
        
        self.logger.info(f'Credentials path: {self.credentials_path}')
        self.logger.info(f'Priority keywords: {self.priority_keywords}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new Gmail messages.
        
        Returns:
            List of new messages to process
        """
        new_messages = []
        
        try:
            # Import Gmail libraries only when needed
            from google.oauth2.credentials import Credentials
            from google.oauth2 import client_secrets
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            
            # Check if credentials exist
            if not self.credentials_path.exists():
                self.logger.error(f'Credentials file not found: {self.credentials_path}')
                self.logger.error('Please download credentials.json from Google Cloud Console')
                return []
            
            # Load client secrets
            client_secrets_data = client_secrets.load_credentials_file(
                str(self.credentials_path),
                scopes=['https://www.googleapis.com/auth/gmail.readonly']
            )
            
            # Try to load existing token
            token_path = Path(__file__).parent / 'token.json'
            creds = None
            
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(
                    str(token_path),
                    scopes=['https://www.googleapis.com/auth/gmail.readonly']
                )
            
            # If no valid credentials, run OAuth flow
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path),
                        scopes=['https://www.googleapis.com/auth/gmail.readonly']
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save token for future use
                token_path.write_text(creds.to_json())
            
            # Build Gmail service
            service = build('gmail', 'v1', credentials=creds)
            
            # Search for unread important messages
            results = service.users().messages().list(
                userId='me',
                q='is:unread -category:promotions -category:social',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            for message in messages:
                if message['id'] not in self.processed_ids:
                    # Get full message details
                    msg = service.users().messages().get(
                        userId='me',
                        id=message['id'],
                        format='metadata',
                        metadataHeaders=['From', 'To', 'Subject', 'Date']
                    ).execute()
                    
                    # Extract headers
                    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                    
                    # Determine priority
                    subject = headers.get('Subject', '').lower()
                    from_email = headers.get('From', '').lower()
                    priority = 'high' if any(kw in subject or kw in from_email for kw in self.priority_keywords) else 'normal'
                    
                    new_messages.append({
                        'id': message['id'],
                        'from': headers.get('From', 'Unknown'),
                        'to': headers.get('To', ''),
                        'subject': headers.get('Subject', 'No Subject'),
                        'date': headers.get('Date', ''),
                        'snippet': msg.get('snippet', ''),
                        'priority': priority,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    self.processed_ids.add(message['id'])
                    self.logger.info(f'Found email from {headers.get("From", "Unknown")}: {headers.get("Subject", "No Subject")}')
            
        except ImportError:
            self.logger.error('Gmail libraries not installed. Run: pip install google-auth google-api-python-client')
            return []
        
        except FileNotFoundError:
            self.logger.error('Gmail credentials not configured')
            return []
        
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
        
        return new_messages
    
    def create_action_file(self, message: Dict[str, Any]) -> Optional[Path]:
        """
        Create an action file for a Gmail message.
        
        Args:
            message: Message dictionary
            
        Returns:
            Path to created action file
        """
        try:
            # Generate frontmatter
            frontmatter = self.generate_frontmatter(
                item_type='email',
                from_contact=message['from'],
                subject=message['subject'],
                priority=message['priority']
            )
            
            # Create action file content
            content = f'''{frontmatter}

# Email Message

## Email Details
- **From:** {message['from']}
- **To:** {message['to']}
- **Subject:** {message['subject']}
- **Date:** {message['date']}
- **Priority:** {message['priority']}
- **Received:** {message['timestamp']}

## Email Content

{message['snippet']}

## Suggested Actions

- [ ] Read full email content
- [ ] Identify email type (inquiry, invoice, urgent, etc.)
- [ ] Check if sender is in contacts
- [ ] Draft appropriate response
- [ ] Check if response requires approval
- [ ] Send email via MCP Email Server (requires approval)
- [ ] Mark email as read/archived
- [ ] Log action
- [ ] Move to /Done when complete

## Response Draft

Type your response here:

---

## Notes

Add additional context or notes:

'''
            
            # Write action file
            safe_subject = message['subject'].replace(' ', '_').replace('/', '_')[:30]
            safe_from = message['from'].split('<')[-1].replace('>', '').replace('@', '_at_').replace('.', '_')
            action_filepath = self.get_unique_filename(f'EMAIL_{safe_from}_{safe_subject}')
            action_filepath.write_text(content, encoding='utf-8')
            
            self.logger.info(f'Gmail action file created: {action_filepath.name}')
            return action_filepath
            
        except Exception as e:
            self.logger.error(f'Error creating Gmail action file: {e}')
            return None
    
    def run_continuous(self) -> None:
        """
        Run Gmail watcher continuously.
        """
        self.logger.info('Starting continuous Gmail monitoring')
        self.logger.info(f'Checking every {self.check_interval} seconds')
        self.logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                items = self.check_for_updates()
                
                if items:
                    self.logger.info(f'Found {len(items)} new message(s)')
                    for item in items:
                        self.create_action_file(item)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Gmail watcher stopped by user')


def main():
    """Main entry point for Gmail watcher."""
    if len(sys.argv) < 2:
        print('Usage: python gmail_watcher.py <vault_path> [credentials_path] [check_interval]')
        print('')
        print('Arguments:')
        print('  vault_path         Path to the Obsidian vault root')
        print('  credentials_path   Path to Gmail credentials.json (default: credentials.json)')
        print('  check_interval     Seconds between checks (default: 120)')
        print('')
        print('Setup Instructions:')
        print('1. Go to: https://console.cloud.google.com/apis/library/gmail.googleapis.com')
        print('2. Enable Gmail API')
        print('3. Create OAuth 2.0 credentials')
        print('4. Download credentials.json')
        print('5. Place credentials.json in AI_Employee_Vault folder')
        print('6. Run: python gmail_watcher.py "./AI_Employee_Vault"')
        print('')
        print('Note: First run will open browser for OAuth authorization.')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    credentials_path = sys.argv[2] if len(sys.argv) > 2 else None
    check_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create watcher
    watcher = GmailWatcher(vault_path, credentials_path, check_interval)
    
    print('=' * 60)
    print('Gmail Watcher - Silver Tier')
    print('=' * 60)
    print(f'Vault: {vault_path}')
    print(f'Check Interval: {check_interval}s')
    print('')
    print('Starting Gmail monitoring...')
    print('First run will open browser for authorization.')
    print('Press Ctrl+C to stop')
    print('')
    
    # Run watcher
    watcher.run_continuous()


if __name__ == '__main__':
    main()
