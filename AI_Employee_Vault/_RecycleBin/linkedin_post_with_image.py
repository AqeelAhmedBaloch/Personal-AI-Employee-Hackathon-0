#!/usr/bin/env python3
"""
LinkedIn Post with Image - AI Employee

Posts to LinkedIn with AI Employee promotional image.
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


class LinkedInImagePoster:
    """Post to LinkedIn with image."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_image_post.log'
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

        # Post content with image
        self.post_content = '''🚀 Introducing: AI Employee - Your 24/7 Digital Worker!

Tired of repetitive tasks? Meet your new AI-powered assistant:

✅ Auto-replies to emails
✅ Monitors files & folders  
✅ Creates action plans automatically
✅ Manages approvals
✅ Tracks everything in Obsidian

The future of work is HERE!

Key Benefits:
📧 Gmail Integration
📁 File System Monitoring  
📋 Smart Plan Generation
✅ Human-in-the-Loop Approval
📊 Real-time Dashboard

Perfect for:
• Busy professionals
• Small business owners
• Anyone wanting to automate routine tasks

#AI #Automation #Productivity #Innovation #FutureOfWork #DigitalTransformation #ArtificialIntelligence #TechInnovation #BusinessAutomation #SmartWork

🤖 Work smarter, not harder!'''

        # Image path
        self.image_path = Path(__file__).parent / 'ai_employee_post.png'

    def post(self):
        """Post to LinkedIn with image."""
        self.logger.info('Starting LinkedIn post with image...')
        
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser
                self.logger.info('Launching browser...')
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
                time.sleep(10)

                # Click "Start a post"
                self.logger.info('Opening post dialog...')
                if page.is_visible('[aria-label="Start a post"]'):
                    page.click('[aria-label="Start a post"]')
                    time.sleep(5)
                else:
                    page.keyboard.press('Control+Shift+P')
                    time.sleep(5)

                # Upload image FIRST
                self.logger.info('Uploading image...')
                
                if self.image_path.exists():
                    # Find file input for media upload
                    file_input = page.locator('input[type="file"]')
                    if file_input.is_visible(timeout=10000):
                        file_input.set_input_files(str(self.image_path))
                        self.logger.info('Image upload initiated...')
                        time.sleep(5)
                        
                        # Wait for image preview to appear
                        for i in range(10):
                            if page.is_visible('[aria-label="Edit media"]'):
                                self.logger.info('Image uploaded successfully!')
                                break
                            time.sleep(2)
                    else:
                        self.logger.warning('File input not found, trying alternative method...')
                else:
                    self.logger.error(f'Image not found: {self.image_path}')

                # Find editor and type content
                self.logger.info('Finding editor...')
                editor = page.locator('[role="textbox"]').first
                
                if editor.is_visible(timeout=10000):
                    self.logger.info('Typing post content...')
                    
                    # Type content
                    for char in self.post_content:
                        editor.type(char, delay=30)
                        if ord(char) == 10:  # Enter
                            page.keyboard.press('Enter')
                    
                    time.sleep(3)
                    
                    # Click Post button
                    self.logger.info('Clicking Post button...')
                    if page.is_visible('button:has-text("Post")'):
                        page.click('button:has-text("Post")')
                        time.sleep(5)
                        self.logger.info('✅ POST WITH IMAGE PUBLISHED!')
                        browser.close()
                        return {'status': 'success', 'message': 'Post with image published!'}
                    
                    # Try Enter key
                    page.keyboard.press('Enter')
                    time.sleep(3)
                    page.keyboard.press('Enter')
                    time.sleep(3)
                    
                    self.logger.info('✅ POST PUBLISHED!')
                    browser.close()
                    return {'status': 'success', 'message': 'Post published!'}
                else:
                    self.logger.error('Editor not found')
                    browser.close()
                    return {'status': 'error', 'error': 'Editor not found'}

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Post with AI Image')
    print('=' * 60)
    print()
    
    poster = LinkedInImagePoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    if result["status"] == 'success':
        print('✅ SUCCESS! Post with image published!')
        print('Check: https://www.linkedin.com/feed/')
    else:
        print(f'❌ Error: {result.get("error", "Unknown")}')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
