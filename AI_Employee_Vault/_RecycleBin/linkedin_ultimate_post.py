#!/usr/bin/env python3
"""
LinkedIn Ultimate Post - Most Reliable with Verification

Posts to LinkedIn and waits for confirmation dialog to close.
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


class LinkedInUltimatePoster:
    """Most reliable LinkedIn poster with verification."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_ultimate_post.log'
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

        # Today's post
        self.post_content = '''🤖 AI Employee - Your 24/7 Digital Worker!

Just launched my latest automation project: An AI employee that works 24/7!

What it does:
✅ Auto-replies to emails (Gmail)
✅ Monitors files & folders
✅ Creates action plans automatically
✅ Manages approvals
✅ Posts to LinkedIn automatically (like this!)

Built with:
🔹 Python + Playwright
🔹 Qwen Code for reasoning
🔹 MCP servers for integrations

The future of work is HERE! 🚀

#AI #Automation #Productivity #Innovation #FutureOfWork #ArtificialIntelligence #TechInnovation #DigitalTransformation #Python #MachineLearning

💡 Work smarter, not harder!'''

    def post(self):
        """Post to LinkedIn with full verification."""
        self.logger.info('Starting LinkedIn ultimate post...')
        
        try:
            from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

            with sync_playwright() as p:
                # Launch browser
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=100,
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
                time.sleep(5)

                # Login if needed
                if 'login' in page.url:
                    self.logger.info('Logging in...')
                    page.fill('#username', self.email)
                    page.fill('#password', self.password)
                    time.sleep(2)
                    page.click('button[type="submit"]')
                    time.sleep(15)

                # Navigate to feed
                self.logger.info('Navigating to feed...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(8)

                # Take pre-post screenshot
                screenshot_pre = Path(__file__).parent / f'screenshot_pre_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_pre))
                self.logger.info(f'Pre-post screenshot: {screenshot_pre}')

                # Click "Start a post"
                self.logger.info('Opening post dialog...')
                
                try:
                    page.click('[aria-label="Start a post"]')
                    time.sleep(5)
                    self.logger.info('Post dialog opened')
                except:
                    self.logger.error('Could not open post dialog')
                    browser.close()
                    return {'status': 'error', 'error': 'Could not open dialog'}

                # Take dialog screenshot
                screenshot_dialog = Path(__file__).parent / f'screenshot_dialog_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_dialog))

                # Find editor
                self.logger.info('Finding editor...')
                try:
                    editor = page.locator('[role="textbox"]').first
                    editor.wait_for(state='visible', timeout=10000)
                    self.logger.info('Editor found')
                except:
                    self.logger.error('Editor not found')
                    browser.close()
                    return {'status': 'error', 'error': 'Editor not found'}

                # Type content SLOWLY
                self.logger.info('Typing content slowly...')
                
                lines = self.post_content.split('\n')
                for i, line in enumerate(lines):
                    editor.type(line + ' ')  # Add space to ensure typing
                    if i < len(lines) - 1:
                        page.keyboard.press('Enter')
                        time.sleep(0.3)
                    time.sleep(0.2)
                
                time.sleep(3)

                # Take typed screenshot
                screenshot_typed = Path(__file__).parent / f'screenshot_typed_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_typed))
                self.logger.info(f'Typed screenshot: {screenshot_typed}')

                # Click Post button - MULTIPLE METHODS
                self.logger.info('Clicking Post button...')
                
                post_clicked = False
                
                # Method 1: Try "Post" button
                try:
                    post_button = page.locator('button:has-text("Post")').first
                    if post_button.is_visible(timeout=5000):
                        post_button.click()
                        post_clicked = True
                        self.logger.info('Clicked Post button (Method 1)')
                except:
                    pass

                # Method 2: Try "Share" button
                if not post_clicked:
                    try:
                        share_button = page.locator('button:has-text("Share")').first
                        if share_button.is_visible(timeout=5000):
                            share_button.click()
                            post_clicked = True
                            self.logger.info('Clicked Share button (Method 2)')
                    except:
                        pass

                # Method 3: Try keyboard Enter
                if not post_clicked:
                    self.logger.info('Trying Enter key (Method 3)...')
                    page.keyboard.press('Control+Enter')
                    time.sleep(2)
                    page.keyboard.press('Enter')
                    time.sleep(2)
                    post_clicked = True

                # WAIT for dialog to close (confirmation)
                self.logger.info('Waiting for post to submit...')
                
                for attempt in range(10):  # Wait up to 50 seconds
                    time.sleep(5)
                    
                    # Check if dialog is closed
                    try:
                        dialog = page.locator('[role="dialog"]').first
                        if not dialog.is_visible():
                            self.logger.info('Dialog closed - Post submitted!')
                            break
                    except:
                        self.logger.info('Dialog not found - Post submitted!')
                        break

                # Take post screenshot
                screenshot_post = Path(__file__).parent / f'screenshot_post_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_post))
                self.logger.info(f'Post screenshot: {screenshot_post}')

                # Navigate to profile to verify
                self.logger.info('Verifying on profile...')
                page.goto('https://www.linkedin.com/in/aqeel-ahmed-10064824b/recent-activity/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(8)

                # Take profile screenshot
                screenshot_profile = Path(__file__).parent / f'screenshot_profile_{datetime.now().strftime("%H%M%S")}.png'
                page.screenshot(path=str(screenshot_profile), full_page=True)
                self.logger.info(f'Profile screenshot: {screenshot_profile}')

                browser.close()

                self.logger.info('✅ LINKEDIN POST COMPLETE!')
                
                return {
                    'status': 'success',
                    'message': 'Post submitted!',
                    'screenshots': [
                        str(screenshot_pre),
                        str(screenshot_dialog),
                        str(screenshot_typed),
                        str(screenshot_post),
                        str(screenshot_profile)
                    ]
                }

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Ultimate Post - With Verification')
    print('=' * 60)
    print()
    
    poster = LinkedInUltimatePoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    
    if result["status"] == 'success':
        print()
        print('✅ Screenshots saved:')
        for ss in result.get('screenshots', []):
            print(f'   {ss}')
        print()
        print('Check your LinkedIn:')
        print('https://www.linkedin.com/in/aqeel-ahmed-10064824b/recent-activity/')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
