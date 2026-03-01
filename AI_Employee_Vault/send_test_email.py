#!/usr/bin/env python3
"""
Send Test Email

Sends a test email to verify Gmail Auto-Replier is working.
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from gmail_auto_replier import GmailAutoReplier

def main():
    print('=' * 60)
    print('Sending Test Email')
    print('=' * 60)
    
    # Get recipient email
    if len(sys.argv) > 1:
        recipient = sys.argv[1]
    else:
        recipient = input('Enter recipient email: ')
    
    # Create auto-replier
    replier = GmailAutoReplier(dry_run=False)
    
    print(f'\nSending to: {recipient}')
    print('')
    
    # Send test email
    result = replier.send_reply(
        to=recipient,
        subject='Test Email from AI Employee',
        original_body='This is a test email to verify the auto-replier is working.',
        from_email=recipient,
        custom_template='general_inquiry'
    )
    
    print('Result:')
    print(f"  Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"  Message ID: {result['message_id']}")
        print(f"  Template: {result['template']}")
        print('\n✅ Email sent successfully!')
    elif result['status'] == 'error':
        print(f"  Error: {result['error']}")
        print('\n❌ Email sending failed!')
    else:
        print(f"  Message: {result['message']}")
    
    print('')
    print('=' * 60)

if __name__ == '__main__':
    main()
