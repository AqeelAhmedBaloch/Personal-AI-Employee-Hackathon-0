#!/usr/bin/env python3
"""
LinkedIn Auto-Poster - Final Version

Uses persistent browser context to maintain LinkedIn session.
First run: Manual login required
Subsequent runs: Auto-login with saved session
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import logging

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInAutoPoster:
    """
    Posts to LinkedIn using persistent browser session.
    """
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize LinkedIn Auto-Poster.
        
        Args:
            dry_run: If True, only simulate posting
        """
        self.dry_run = dry_run
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        
        # Session storage
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Post templates
        self.templates = self._load_templates()
        
        self.logger.info(f'LinkedIn Auto-Poster initialized')
        self.logger.info(f'User data dir: {self.user_data_dir}')
    
    def _setup_logging(self) -> None:
        """Set up logging."""
        self.logger = logging.getLogger('LinkedInAutoPoster')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load post templates."""
        return {
            'general': '''Exciting updates from our business!

We're constantly working to deliver the best solutions for our clients. Our AI Employee system is now operational and helping us automate daily tasks efficiently.

#Business #Automation #AI #Innovation #Productivity''',
            
            'service': '''Need professional services?

We offer top-notch solutions tailored to your business needs. Our team is ready to help you achieve your goals.

Contact us today for a free consultation!

#Services #Business #Consulting #ProfessionalServices''',
            
            'product': '''Introducing Our Latest Product!

We're excited to announce our new product that will revolutionize how you work. Built with cutting-edge technology and designed for maximum efficiency.

Key Features:
- Automated workflows
- Smart decision-making
- 24/7 availability

Learn more: [Your Website Link]

#Product #Launch #Innovation #Technology''',
            
            'milestone': '''We Hit a Milestone!

Thanks to our amazing clients and team, we've achieved another significant milestone. This success motivates us to keep pushing forward.

Thank you for being part of our journey!

#Milestone #Success #Growth #Grateful #TeamWork''',
            
            'tip': '''Business Tip of the Day

"Automation is not about replacing people; it's about empowering them to do their best work."

Our AI Employee system proves this every day by handling routine tasks so we can focus on strategic decisions.

#BusinessTips #Automation #Leadership #Productivity''',
            
            'hire': '''We're Hiring!

Join our growing team! We're looking for talented individuals who are passionate about innovation and making a difference.

Positions Available:
- [Position 1]
- [Position 2]

Apply now: [Application Link]

#Hiring #Jobs #Career #Opportunity #JoinOurTeam'''
        }
    
    def post(self, post_type: str = 'general') -> Dict[str, Any]:
        """
        Post to LinkedIn.
        
        Args:
            post_type: Type of post (general, service, product, etc.)
            
        Returns:
            Result dictionary
        """
        self.logger.info(f'Posting to LinkedIn ({post_type})...')
        
        if self.dry_run:
            self.logger.info('[DRY RUN] Post not published')
            return {
                'status': 'dry_run',
                'message': 'Post would be published (dry run mode)',
                'post_type': post_type
            }
        
        try:
            from playwright.sync_api import sync_playwright
            
            # Get post content
            content = self.templates.get(post_type, self.templates['general'])
            
            with sync_playwright() as p:
                # Launch browser with persistent context
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=2000,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                    ],
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = browser.pages[0]
                
                # Hide automation
                page.add_init_script('''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                ''')
                
                # Navigate to LinkedIn
                self.logger.info('Navigating to LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=60000)
                
                # Wait for page to load
                time.sleep(5)
                
                # Check if logged in
                if 'login' in page.url:
                    self.logger.info('Not logged in. Attempting login...')
                    
                    # Login
                    page.fill('#username', self.email)
                    page.fill('#password', self.password)
                    time.sleep(2)
                    page.click('button[type="submit"]')
                    
                    # Wait for login
                    self.logger.info('Waiting for login... (may take 30-60 seconds)')
                    time.sleep(30)
                    
                    # Check if still on login page (2FA or verification)
                    if 'login' in page.url:
                        self.logger.warning('Still on login page. Manual verification may be required.')
                        self.logger.info('Please complete any CAPTCHA or 2FA verification manually.')
                        self.logger.info('Waiting up to 2 minutes for manual verification...')
                        
                        # Wait for manual verification
                        for i in range(12):  # 12 x 10 seconds = 2 minutes
                            time.sleep(10)
                            if 'feed' in page.url:
                                self.logger.info('Login successful!')
                                break
                        else:
                            self.logger.error('Login verification timeout.')
                            browser.close()
                            return {
                                'status': 'error',
                                'error': 'Login verification timeout. Please log in manually first.'
                            }
                
                # Navigate to feed if not already there
                if 'feed' not in page.url:
                    page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
                    time.sleep(3)
                
                # Find and click "Start a post" button
                self.logger.info('Looking for "Start a post" button...')
                
                # Multiple selector attempts
                selectors = [
                    '[aria-label="Start a post"]',
                    '.share-box-feed-entry__trigger',
                    'button:has-text("Start a post")',
                ]
                
                clicked = False
                for selector in selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            clicked = True
                            self.logger.info(f'Clicked with selector: {selector}')
                            time.sleep(3)
                            break
                    except Exception as e:
                        self.logger.debug(f'Selector {selector} failed: {e}')
                
                if not clicked:
                    self.logger.error('Could not find "Start a post" button')
                    browser.close()
                    return {
                        'status': 'error',
                        'error': 'Could not find "Start a post" button'
                    }
                
                # Fill post content
                self.logger.info('Filling post content...')
                
                # Find editor
                editor = page.locator('[role="textbox"]').first
                
                # Type content slowly
                for i, char in enumerate(content):
                    editor.type(char, delay=100)
                    if i % 100 == 0 and i > 0:
                        time.sleep(1)
                
                time.sleep(3)
                
                # Click Post button
                self.logger.info('Publishing post...')
                
                post_selectors = [
                    'button:has-text("Post")',
                    'button:has-text("Share")',
                ]
                
                for selector in post_selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            time.sleep(3)
                            break
                    except:
                        continue
                
                # Wait for confirmation
                time.sleep(5)
                
                self.logger.info('Post published!')
                
                browser.close()
                
                return {
                    'status': 'success',
                    'message': 'Post published to LinkedIn',
                    'post_type': post_type,
                    'content': content[:100] + '...'
                }
                
        except ImportError:
            self.logger.error('Playwright not installed')
            return {
                'status': 'error',
                'error': 'Playwright not installed'
            }
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {
                'status': 'error',
                'error': str(e)
            }


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Auto-Poster - Final Version')
    print('=' * 60)
    print('')
    
    # Check credentials
    email = os.getenv('LINKEDIN_EMAIL', '')
    if not email:
        print('Error: LinkedIn email not configured')
        return
    
    print(f'Email: {email}')
    print('')
    
    # Get post type
    if len(sys.argv) > 1:
        post_type = sys.argv[1]
    else:
        print('Available post types:')
        print('  general, service, product, milestone, tip, hire')
        post_type = input('Enter post type (default: general): ').strip() or 'general'
    
    print('')
    print(f'Post type: {post_type}')
    print('')
    
    # Create poster
    poster = LinkedInAutoPoster(dry_run=False)
    
    # Post
    print('Posting to LinkedIn...')
    print('')
    print('=' * 60)
    
    result = poster.post(post_type)
    
    print('')
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    print('=' * 60)


if __name__ == '__main__':
    main()
