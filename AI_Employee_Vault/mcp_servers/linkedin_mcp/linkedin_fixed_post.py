#!/usr/bin/env python3
"""
LinkedIn Fixed Post - With Proper Wait & Verification

Posts to LinkedIn and waits for dialog to close before confirming.
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


class LinkedInFixedPoster:
    """Fixed LinkedIn poster with proper wait."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_fixed_post.log'
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

        # Short post for faster typing
        self.post_content = '''🤖 AI Employee - Working 24/7!

My AI assistant now:
✅ Auto-replies to emails
✅ Monitors files
✅ Creates plans
✅ Posts daily to LinkedIn

#AI #Automation #Productivity #Innovation #FutureOfWork

🚀 Work smarter!'''

    def post(self):
        """Post to LinkedIn with proper wait."""
        self.logger.info('Starting LinkedIn fixed post...')
        
        try:
            from playwright.sync_api import sync_playwright, TimeoutError

            with sync_playwright() as p:
                # Launch browser
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=50,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                    ],
                    viewport={'width': 1920, 'height': 1080}
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                # Hide automation
                page.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

                # Go to LinkedIn
                self.logger.info('Going to LinkedIn...')
                page.goto('https://www.linkedin.com/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(3)

                # Login if needed
                if 'login' in page.url:
                    self.logger.info('Logging in...')
                    page.fill('#username', self.email)
                    page.fill('#password', self.password)
                    time.sleep(2)
                    page.click('button[type="submit"]')
                    time.sleep(10)

                # Navigate to feed
                self.logger.info('Navigating to feed...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(5)

                # Take pre-post screenshot
                screenshot_pre = Path(__file__).parent / f'pre_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_pre))
                self.logger.info(f'Pre screenshot: {screenshot_pre}')

                # Click "Start a post"
                self.logger.info('Clicking Start a post...')
                page.click('[aria-label="Start a post"]')
                time.sleep(5)

                # Take dialog screenshot
                screenshot_dialog = Path(__file__).parent / f'dialog_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_dialog))

                # Find editor
                self.logger.info('Finding editor...')
                editor = page.locator('[role="textbox"]').first
                editor.wait_for(state='visible', timeout=10000)
                self.logger.info('Editor found')

                # Type content FAST
                self.logger.info('Typing content...')
                editor.fill(self.post_content)
                time.sleep(2)

                # Take typed screenshot
                screenshot_typed = Path(__file__).parent / f'typed_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_typed))
                self.logger.info(f'Typed screenshot: {screenshot_typed}')

                # Click Post button - CRITICAL PART
                self.logger.info('Clicking POST button...')
                
                # Find Post button
                post_button = page.locator('button:has-text("Post")').first
                post_button.wait_for(state='visible', timeout=10000)
                
                # Click it
                post_button.click()
                self.logger.info('Post button CLICKED!')
                
                # WAIT for dialog to close (THIS IS THE KEY!)
                self.logger.info('Waiting for dialog to close...')
                
                dialog_closed = False
                for attempt in range(20):  # Wait up to 100 seconds
                    time.sleep(5)
                    
                    try:
                        # Check if dialog is still visible
                        dialog = page.locator('[role="dialog"]').first
                        is_visible = dialog.is_visible(timeout=3000)
                        
                        if not is_visible:
                            self.logger.info(f'✅ Dialog closed at attempt {attempt + 1}')
                            dialog_closed = True
                            break
                        else:
                            self.logger.info(f'Dialog still visible (attempt {attempt + 1})')
                    except:
                        # Dialog not found = closed!
                        self.logger.info(f'✅ Dialog not found (closed) at attempt {attempt + 1}')
                        dialog_closed = True
                        break

                # Take post-click screenshot
                screenshot_post = Path(__file__).parent / f'post_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_post))
                self.logger.info(f'Post screenshot: {screenshot_post}')

                browser.close()

                if dialog_closed:
                    self.logger.info('✅✅✅ POST PUBLISHED SUCCESSFULLY! ✅✅✅')
                    return {
                        'status': 'success',
                        'message': 'Post published! Dialog closed confirmed.',
                        'screenshots': [
                            str(screenshot_pre),
                            str(screenshot_dialog),
                            str(screenshot_typed),
                            str(screenshot_post)
                        ]
                    }
                else:
                    self.logger.warning('⚠️ Post button clicked but dialog did not close')
                    return {
                        'status': 'warning',
                        'message': 'Post button clicked but dialog still open',
                        'screenshots': [str(screenshot_post)]
                    }

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Fixed Post - With Dialog Wait')
    print('=' * 60)
    print()
    
    poster = LinkedInFixedPoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    
    if result["status"] in ['success', 'warning']:
        print()
        print('✅ Screenshots:')
        for ss in result.get('screenshots', []):
            print(f'   {ss}')
        print()
        print('Check LinkedIn:')
        print('https://www.linkedin.com/feed/')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
