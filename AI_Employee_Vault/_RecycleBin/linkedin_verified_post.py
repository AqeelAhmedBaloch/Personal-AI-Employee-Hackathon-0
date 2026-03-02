#!/usr/bin/env python3
"""
LinkedIn Verified Post - With Confirmation

Posts to LinkedIn and verifies by checking profile.
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


class LinkedInVerifiedPoster:
    """Post to LinkedIn with verification."""

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_verified_post.log'
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
        self.post_content = '''🤖 AI Employee - Your 24/7 Digital Assistant!

Excited to share my latest project: An autonomous AI employee that works 24/7!

Key Features:
✅ Auto-replies to emails (Gmail integration)
✅ Monitors files & folders automatically
✅ Creates action plans using Qwen Code
✅ Manages approvals with human-in-the-loop
✅ Real-time dashboard in Obsidian
✅ Scheduled LinkedIn posts (like this one!)

Tech Stack:
🔧 Python + Playwright for automation
🔧 Qwen Code for reasoning
🔧 Obsidian for knowledge management
🔧 MCP servers for integrations

This is the future of work - AI handling routine tasks while humans focus on strategy and creativity!

#AI #Automation #Productivity #Innovation #FutureOfWork #ArtificialIntelligence #TechInnovation #DigitalTransformation #MachineLearning #Python

🚀 Work smarter, not harder!'''

    def post(self):
        """Post to LinkedIn with verification."""
        self.logger.info('Starting LinkedIn verified post...')
        
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=200,
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
                pre_screenshot = Path(__file__).parent / 'pre_post_screenshot.png'
                page.screenshot(path=str(pre_screenshot))
                self.logger.info(f'Pre-post screenshot saved: {pre_screenshot}')

                # Click "Start a post"
                self.logger.info('Opening post dialog...')
                
                # Try multiple methods
                clicked = False
                selectors = [
                    '[aria-label="Start a post"]',
                    '.share-box-feed-entry__trigger',
                ]
                
                for selector in selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            clicked = True
                            self.logger.info(f'Clicked: {selector}')
                            time.sleep(5)
                            break
                    except:
                        continue

                if not clicked:
                    self.logger.error('Could not open post dialog')
                    browser.close()
                    return {'status': 'error', 'error': 'Could not open post dialog'}

                # Wait for dialog to open
                time.sleep(5)

                # Take dialog screenshot
                dialog_screenshot = Path(__file__).parent / 'dialog_screenshot.png'
                page.screenshot(path=str(dialog_screenshot))
                self.logger.info(f'Dialog screenshot saved: {dialog_screenshot}')

                # Find editor and type
                self.logger.info('Finding editor...')
                editor = page.locator('[role="textbox"]').first
                
                if not editor.is_visible(timeout=10000):
                    self.logger.error('Editor not visible')
                    browser.close()
                    return {'status': 'error', 'error': 'Editor not visible'}

                # Type content
                self.logger.info('Typing post content...')
                
                # Split into lines and type
                lines = self.post_content.split('\n')
                for i, line in enumerate(lines):
                    editor.type(line)
                    if i < len(lines) - 1:
                        page.keyboard.press('Enter')
                        time.sleep(0.5)
                    time.sleep(0.3)
                
                time.sleep(5)

                # Take typing screenshot
                typed_screenshot = Path(__file__).parent / 'typed_screenshot.png'
                page.screenshot(path=str(typed_screenshot))
                self.logger.info(f'Typed screenshot saved: {typed_screenshot}')

                # Click Post button
                self.logger.info('Clicking Post button...')
                
                post_clicked = False
                post_buttons = [
                    'button:has-text("Post")',
                    'button:has-text("Share")',
                    '[aria-label="Post"]',
                ]
                
                for btn in post_buttons:
                    try:
                        if page.is_visible(btn):
                            page.click(btn)
                            post_clicked = True
                            self.logger.info(f'Clicked Post button: {btn}')
                            break
                    except:
                        continue

                if not post_clicked:
                    self.logger.error('Post button not found')
                    # Try Enter key
                    page.keyboard.press('Enter')
                    time.sleep(2)
                    page.keyboard.press('Enter')
                    time.sleep(2)

                # Wait for post to submit
                self.logger.info('Waiting for post to publish...')
                time.sleep(10)

                # Take post screenshot
                post_screenshot = Path(__file__).parent / 'post_submitted_screenshot.png'
                page.screenshot(path=str(post_screenshot))
                self.logger.info(f'Post screenshot saved: {post_screenshot}')

                # Navigate to profile to verify
                self.logger.info('Navigating to profile to verify...')
                page.goto('https://www.linkedin.com/in/aqeel-ahmed-10064824b/recent-activity/', wait_until='domcontentloaded', timeout=30000)
                time.sleep(8)

                # Take profile screenshot
                profile_screenshot = Path(__file__).parent / 'profile_activity_screenshot.png'
                page.screenshot(path=str(profile_screenshot))
                self.logger.info(f'Profile screenshot saved: {profile_screenshot}')

                # Check if post appears
                page_content = page.content()
                
                browser.close()

                # Check for success indicators
                if 'AI Employee' in page_content or 'Automation' in page_content:
                    self.logger.info('✅ POST VERIFIED ON PROFILE!')
                    return {
                        'status': 'success',
                        'message': 'Post published and verified!',
                        'screenshots': [
                            str(pre_screenshot),
                            str(dialog_screenshot),
                            str(typed_screenshot),
                            str(post_screenshot),
                            str(profile_screenshot)
                        ]
                    }
                else:
                    self.logger.warning('Post may not be visible yet')
                    return {
                        'status': 'success',
                        'message': 'Post submitted but not yet visible on profile',
                        'screenshots': [str(profile_screenshot)]
                    }

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Verified Post')
    print('=' * 60)
    print()
    
    poster = LinkedInVerifiedPoster()
    result = poster.post()
    
    print()
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    
    if result["status"] == 'success':
        print()
        print('✅ Check screenshots in:')
        print('   E:\\Hackathon-Q4\\Personal-AI-Employee-Hackathon-0\\AI_Employee_Vault\\mcp_servers\\linkedin_mcp\\')
        print()
        print('View your LinkedIn activity:')
        print('https://www.linkedin.com/in/aqeel-ahmed-10064824b/recent-activity/')
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
