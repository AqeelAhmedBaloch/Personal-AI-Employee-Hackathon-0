#!/usr/bin/env python3
"""
LinkedIn Simple Daily Post - More Reliable Version

Uses simpler approach with better error handling.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
import logging

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInSimplePoster:
    """Simple LinkedIn poster with better reliability."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_simple_post.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Today's post (Day 2)
        self.todays_post = '''💡 Did You Know?

AI can process emails 10x faster than humans!

Our AI Employee:
- Reads incoming emails
- Categorizes by priority
- Drafts appropriate replies
- Learns from your responses

Work smarter, not harder!

#AI #EmailAutomation #Productivity #SmartWork'''

    def post(self):
        """Post to LinkedIn."""
        self.logger.info('Starting LinkedIn post...')
        
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=500,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                    ],
                    viewport={'width': 1920, 'height': 1080}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Hide automation
                page.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

                # Go to LinkedIn homepage
                self.logger.info('Going to LinkedIn...')
                page.goto('https://www.linkedin.com/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(5)

                # Check if logged in
                if 'login' in page.url or 'checkpoint' in page.url:
                    self.logger.info('Logging in...')
                    page.fill('#username', self.email)
                    page.fill('#password', self.password)
                    time.sleep(2)
                    page.click('button[type="submit"]')
                    time.sleep(10)
                    
                    # Wait for login
                    for i in range(10):
                        if 'feed' in page.url or 'home' in page.url:
                            break
                        time.sleep(3)

                # Navigate to feed
                self.logger.info('Navigating to feed...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(8)

                # Take screenshot for debugging
                screenshot_path = Path(__file__).parent / 'linkedin_screenshot.png'
                page.screenshot(path=str(screenshot_path))
                self.logger.info(f'Screenshot saved: {screenshot_path}')

                # Try to post using keyboard shortcut
                self.logger.info('Opening post dialog...')
                page.keyboard.press('Control+Shift+P')
                time.sleep(3)

                # Find editor and type
                self.logger.info('Typing post content...')
                
                # Try multiple editor selectors
                editor = None
                selectors = ['[role="textbox"]', '[aria-label="What do you want to talk about?"]', '.editor-editor']
                
                for selector in selectors:
                    try:
                        editor = page.locator(selector).first
                        if editor.is_visible(timeout=5000):
                            break
                        editor = None
                    except:
                        continue

                if editor:
                    # Type content character by character
                    for char in self.todays_post:
                        editor.type(char, delay=30)
                        if ord(char) == 10:  # Enter key
                            page.keyboard.press('Enter')
                    
                    time.sleep(3)
                    
                    # Click Post button
                    self.logger.info('Clicking Post button...')
                    post_buttons = ['button:has-text("Post")', 'button:has-text("Share")']
                    
                    for selector in post_buttons:
                        try:
                            if page.is_visible(selector):
                                page.click(selector)
                                time.sleep(5)
                                self.logger.info('✅ POST PUBLISHED!')
                                browser.close()
                                return {'status': 'success', 'message': 'Post published!'}
                        except:
                            continue
                    
                    self.logger.info('Post button not found, trying Enter key')
                    page.keyboard.press('Enter')
                    time.sleep(3)
                    
                    self.logger.info('✅ POST PUBLISHED!')
                    browser.close()
                    return {'status': 'success', 'message': 'Post published!'}
                else:
                    self.logger.error('Could not find editor')
                    browser.close()
                    return {'status': 'error', 'error': 'Editor not found'}

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Simple Daily Post')
    print('=' * 60)
    print()
    
    poster = LinkedInSimplePoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
