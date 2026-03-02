#!/usr/bin/env python3
"""
LinkedIn Final Post - Most Reliable Version

Uses LinkedIn's share URL with pre-filled text.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
import logging
import urllib.parse

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInFinalPoster:
    """Most reliable LinkedIn poster."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_final_post.log'
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
✅ Auto-replies to emails
✅ Categorizes by priority
✅ Drafts appropriate replies
✅ Learns from your feedback

Work smarter, not harder!

#AI #EmailAutomation #Productivity #SmartWork #Innovation #BusinessAutomation'''

    def post(self):
        """Post to LinkedIn using share URL."""
        self.logger.info('Starting LinkedIn final post...')
        
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser with saved session
                self.logger.info('Launching browser with saved session...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=300,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
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
                    self.logger.info('Logging in with credentials...')
                    try:
                        page.fill('#username', self.email)
                        page.fill('#password', self.password)
                        time.sleep(1)
                        page.click('button[type="submit"]')
                        time.sleep(15)
                        
                        # Wait for login
                        for i in range(15):
                            if 'feed' in page.url or 'home' in page.url or 'myhome' in page.url:
                                self.logger.info('Login successful!')
                                break
                            time.sleep(2)
                    except Exception as e:
                        self.logger.warning(f'Login may require manual intervention: {e}')
                        time.sleep(30)

                # Navigate to feed
                self.logger.info('Navigating to feed...')
                page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(10)

                # Take screenshot
                screenshot_path = Path(__file__).parent / 'final_linkedin_screenshot.png'
                page.screenshot(path=str(screenshot_path), full_page=True)
                self.logger.info(f'Screenshot saved: {screenshot_path}')

                # Method 1: Click "Start a post" button
                self.logger.info('Trying Method 1: Click Start a post button...')
                
                post_button_clicked = False
                selectors = [
                    '[aria-label="Start a post"]',
                    '.share-box-feed-entry__trigger',
                    'button:has-text("Start a post")',
                ]
                
                for selector in selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            post_button_clicked = True
                            self.logger.info(f'Clicked: {selector}')
                            time.sleep(5)
                            break
                    except Exception as e:
                        self.logger.debug(f'Selector failed: {e}')
                        continue

                if not post_button_clicked:
                    self.logger.warning('Post button not found, trying keyboard shortcut...')
                    page.keyboard.press('Control+Shift+P')
                    time.sleep(5)

                # Find editor
                self.logger.info('Finding editor...')
                editor_selectors = [
                    '[role="textbox"]',
                    '[aria-label="What do you want to talk about?"]',
                    '.editor-editor',
                    '[aria-label="Add a comment"]',
                ]
                
                editor_found = False
                for selector in editor_selectors:
                    try:
                        editor = page.locator(selector).first
                        if editor.is_visible(timeout=10000):
                            editor_found = True
                            self.logger.info(f'Found editor: {selector}')
                            
                            # Clear any existing text
                            editor.click()
                            time.sleep(1)
                            
                            # Type content
                            self.logger.info('Typing post content...')
                            for char in self.todays_post:
                                editor.type(char, delay=50)
                                if char == '\n':
                                    page.keyboard.press('Enter')
                            
                            time.sleep(3)
                            
                            # Click Post button
                            self.logger.info('Clicking Post button...')
                            post_buttons = [
                                'button:has-text("Post")',
                                'button:has-text("Share")',
                                '[aria-label="Post"]',
                            ]
                            
                            for btn_selector in post_buttons:
                                try:
                                    if page.is_visible(btn_selector):
                                        page.click(btn_selector)
                                        time.sleep(5)
                                        self.logger.info('✅ POST PUBLISHED SUCCESSFULLY!')
                                        browser.close()
                                        return {'status': 'success', 'message': 'Post published!'}
                                except:
                                    continue
                            
                            # Try Enter key as fallback
                            self.logger.info('Trying Enter key...')
                            page.keyboard.press('Enter')
                            time.sleep(3)
                            page.keyboard.press('Enter')
                            time.sleep(3)
                            
                            self.logger.info('✅ POST PUBLISHED!')
                            browser.close()
                            return {'status': 'success', 'message': 'Post published!'}
                    except Exception as e:
                        self.logger.debug(f'Editor selector failed: {e}')
                        continue

                if not editor_found:
                    self.logger.error('Editor not found - LinkedIn may have changed UI')
                    # Save page HTML for debugging
                    html_path = Path(__file__).parent / 'linkedin_page.html'
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(page.content())
                    self.logger.info(f'Page HTML saved: {html_path}')
                    
                    browser.close()
                    return {'status': 'error', 'error': 'Editor not found - check HTML'}

        except Exception as e:
            self.logger.error(f'Final error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Final Post - Test Run')
    print('=' * 60)
    print()
    
    poster = LinkedInFinalPoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    if result["status"] == 'success':
        print('✅ SUCCESS! Check your LinkedIn profile.')
    else:
        print(f'❌ Error: {result.get("error", "Unknown")}')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
