#!/usr/bin/env python3
"""
WhatsApp Watcher

Monitors WhatsApp Web for new messages with keywords.
Uses Playwright for browser automation.

Note: Requires WhatsApp Web session to be active.
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import base watcher
sys.path.insert(0, str(Path(__file__).parent / 'watchers'))
from base_watcher import BaseWatcher


class WhatsAppWatcher(BaseWatcher):
    """
    Watcher that monitors WhatsApp Web for messages.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize WhatsApp watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        super().__init__(vault_path, check_interval)
        
        # Keywords to monitor
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'important']
        
        # Track processed messages
        self.processed_messages: set = set()
        
        self.logger.info(f'Keywords: {self.keywords}')
    
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Check for new WhatsApp messages.
        
        Returns:
            List of new messages to process
        """
        new_messages = []
        
        try:
            # Import playwright only when needed
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to WhatsApp Web
                page.goto('https://web.whatsapp.com', wait_until='networkidle')
                
                # Wait for chat list (with timeout)
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                except Exception:
                    self.logger.warning('WhatsApp Web not loaded or not logged in')
                    browser.close()
                    return []
                
                # Get all chat items
                chat_items = page.query_selector_all('[role="row"]')
                
                for chat in chat_items:
                    try:
                        # Get chat name
                        name_elem = chat.query_selector('[dir="auto"]')
                        if not name_elem:
                            continue
                        
                        chat_name = name_elem.inner_text()
                        
                        # Get last message
                        msg_elem = chat.query_selector('[dir="auto"]:last-child')
                        if not msg_elem:
                            continue
                        
                        message_text = msg_elem.inner_text().lower()
                        
                        # Check for keywords
                        for keyword in self.keywords:
                            if keyword in message_text:
                                # Create unique message ID
                                msg_id = f'{chat_name}_{message_text[:20]}_{datetime.now().strftime("%Y%m%d")}'
                                
                                if msg_id not in self.processed_messages:
                                    new_messages.append({
                                        'from': chat_name,
                                        'text': message_text,
                                        'keyword': keyword,
                                        'timestamp': datetime.now().isoformat()
                                    })
                                    self.processed_messages.add(msg_id)
                                    self.logger.info(f'Found message from {chat_name} with keyword "{keyword}"')
                                
                                break
                                
                    except Exception as e:
                        self.logger.debug(f'Error processing chat: {e}')
                        continue
                
                browser.close()
                
        except ImportError:
            self.logger.error('Playwright not installed. Run: pip install playwright')
            return []
        
        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')
        
        return new_messages
    
    def create_action_file(self, message: Dict[str, Any]) -> Optional[Path]:
        """
        Create an action file for a WhatsApp message.
        
        Args:
            message: Message dictionary
            
        Returns:
            Path to created action file
        """
        try:
            # Generate frontmatter
            frontmatter = self.generate_frontmatter(
                item_type='whatsapp',
                from_contact=message['from'],
                keyword=message['keyword'],
                priority='high' if message['keyword'] in ['urgent', 'asap'] else 'normal'
            )
            
            # Create action file content
            content = f'''{frontmatter}

# WhatsApp Message

## Message Details
- **From:** {message['from']}
- **Keyword:** {message['keyword']}
- **Received:** {message['timestamp']}

## Message Content

{message['text']}

## Suggested Actions

- [ ] Review message urgency
- [ ] Draft appropriate response
- [ ] Check if approval needed for response
- [ ] Send response via WhatsApp
- [ ] Log conversation
- [ ] Move to /Done when complete

## Response Draft

Type your response here:

---

## Notes

Add additional context or notes:

'''
            
            # Write action file
            safe_name = message['from'].replace(' ', '_').replace('/', '_')
            action_filepath = self.get_unique_filename(f'WHATSAPP_{safe_name}')
            action_filepath.write_text(content, encoding='utf-8')
            
            self.logger.info(f'WhatsApp action file created: {action_filepath.name}')
            return action_filepath
            
        except Exception as e:
            self.logger.error(f'Error creating WhatsApp action file: {e}')
            return None
    
    def run_continuous(self) -> None:
        """
        Run WhatsApp watcher continuously.
        
        Note: This is resource-intensive. Use scheduled checks instead.
        """
        self.logger.info('Starting continuous WhatsApp monitoring')
        self.logger.warning('WhatsApp Web requires active session and QR login')
        self.logger.warning('Press Ctrl+C to stop')
        
        try:
            while True:
                items = self.check_for_updates()
                
                if items:
                    self.logger.info(f'Found {len(items)} new message(s)')
                    for item in items:
                        self.create_action_file(item)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('WhatsApp watcher stopped by user')


def main():
    """Main entry point for WhatsApp watcher."""
    if len(sys.argv) < 2:
        print('Usage: python whatsapp_watcher.py <vault_path> [check_interval]')
        print('')
        print('Arguments:')
        print('  vault_path       Path to the Obsidian vault root')
        print('  check_interval   Seconds between checks (default: 60)')
        print('')
        print('Example:')
        print('  python whatsapp_watcher.py "./AI_Employee_Vault" 120')
        print('')
        print('Note: WhatsApp Web requires QR code login in browser.')
        print('      For automation, use WhatsApp Business API instead.')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create watcher
    watcher = WhatsAppWatcher(vault_path, check_interval)
    
    print('=' * 60)
    print('WhatsApp Watcher - Silver Tier')
    print('=' * 60)
    print(f'Vault: {vault_path}')
    print(f'Check Interval: {check_interval}s')
    print(f'Keywords: {watcher.keywords}')
    print('')
    print('Starting WhatsApp monitoring...')
    print('Press Ctrl+C to stop')
    print('')
    
    # Run watcher
    watcher.run_continuous()


if __name__ == '__main__':
    main()
