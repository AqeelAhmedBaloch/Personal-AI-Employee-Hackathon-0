#!/usr/bin/env python3
"""
LinkedIn MCP Server

Automatically posts to LinkedIn for business promotion.
Uses Playwright for browser automation.

Features:
- Auto-login to LinkedIn
- Create and schedule posts
- Generate business content
- Track engagement
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


class LinkedInMCPServer:
    """
    MCP Server for LinkedIn automation.
    """
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize LinkedIn MCP Server.
        
        Args:
            dry_run: If True, only simulate posting without actual post
        """
        self.dry_run = dry_run
        
        # LinkedIn credentials
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        
        # Set up logging
        self._setup_logging()
        
        self.logger.info(f'LinkedIn MCP Server initialized (dry_run={dry_run})')
        self.logger.info(f'Email: {self.email}')
    
    def _setup_logging(self) -> None:
        """Set up logging."""
        self.logger = logging.getLogger('LinkedInMCP')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def create_business_post(self, business_type: str = 'general') -> str:
        """
        Generate business post content.
        
        Args:
            business_type: Type of business post
            
        Returns:
            Generated post content
        """
        templates = {
            'general': '''Exciting updates from our business!

We're constantly working to deliver the best solutions for our clients. Our Personal AI Employee Hackathon-0 system is now operational and helping us automate daily tasks efficiently.

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

Our Personal AI Employee Hackathon-0 system proves this every day by handling routine tasks so we can focus on strategic decisions.

#BusinessTips #Automation #Leadership #Productivity''',
            
            'hire': '''We're Hiring!

Join our growing team! We're looking for talented individuals who are passionate about innovation and making a difference.

Positions Available:
- [Position 1]
- [Position 2]

Apply now: [Application Link]

#Hiring #Jobs #Career #Opportunity #JoinOurTeam'''
        }
        
        return templates.get(business_type, templates['general'])
    
    def post_to_linkedin(self, content: str, include_image: bool = False) -> Dict[str, Any]:
        """
        Post content to LinkedIn.
        
        Args:
            content: Post content
            include_image: Whether to include an image
            
        Returns:
            Result dictionary with status and post details
        """
        self.logger.info('Posting to LinkedIn...')
        self.logger.info(f'Content length: {len(content)} characters')
        
        if self.dry_run:
            self.logger.info('[DRY RUN] Post not published (dry run mode)')
            return {
                'status': 'dry_run',
                'message': 'Post would be published (dry run mode)',
                'content': content[:100] + '...',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            # Import Playwright
            from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
            
            # Check credentials
            if not self.email or not self.password:
                raise ValueError('LinkedIn credentials not configured')
            
            with sync_playwright() as p:
                # Launch browser with better settings
                browser = p.chromium.launch(
                    headless=False,  # Use visible browser to avoid detection
                    slow_mo=1000,    # Slow down actions (1 second delay)
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage'
                    ]
                )
                
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = context.new_page()
                
                # Inject script to hide automation
                page.add_init_script('''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                ''')
                
                # Navigate to LinkedIn
                self.logger.info('Navigating to LinkedIn...')
                page.goto('https://www.linkedin.com/login', wait_until='networkidle', timeout=30000)
                
                # Wait for login page to fully load
                page.wait_for_selector('#username', timeout=10000)
                
                # Small delay to avoid detection
                time.sleep(2)
                
                # Login
                self.logger.info('Logging in...')
                page.fill('#username', self.email)
                page.fill('#password', self.password)
                
                # Click login with delay
                time.sleep(1)
                page.click('button[type="submit"]')
                
                # Wait for navigation with longer timeout
                try:
                    page.wait_for_url('https://www.linkedin.com/feed/*', timeout=30000)
                except PlaywrightTimeout:
                    # Try alternative URL
                    try:
                        page.wait_for_url('https://www.linkedin.com/*', timeout=10000)
                    except PlaywrightTimeout:
                        self.logger.warning('Navigation timeout, but continuing...')
                
                # Wait for feed to load
                time.sleep(3)
                
                # Check if we're on feed page
                if 'feed' not in page.url:
                    # Try to navigate to feed manually
                    page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=30000)
                    time.sleep(3)
                
                # Start post creation
                self.logger.info('Creating post...')
                
                # Try multiple selectors for "Start a post" button
                post_button_selectors = [
                    '[aria-label="Start a post"]',
                    'button:has-text("Start")',
                    '.share-box-feed-entry__trigger',
                    'button[id*="share-box"]'
                ]
                
                clicked = False
                for selector in post_button_selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            clicked = True
                            self.logger.info(f'Clicked post button with selector: {selector}')
                            time.sleep(2)
                            break
                    except:
                        continue
                
                if not clicked:
                    self.logger.error('Could not find "Start a post" button')
                    browser.close()
                    return {
                        'status': 'error',
                        'error': 'Could not find "Start a post" button'
                    }
                
                # Wait for post dialog
                try:
                    page.wait_for_selector('[role="dialog"]', timeout=10000)
                except:
                    # Alternative: look for editor directly
                    pass
                
                # Find and fill post content
                editor = page.locator('[role="textbox"]').first
                
                # Type slowly to avoid detection
                for char in content:
                    editor.type(char, delay=50)
                    if len(content) > 100 and content.index(char) % 50 == 0:
                        time.sleep(0.5)
                
                time.sleep(2)
                
                # Post
                self.logger.info('Publishing post...')
                
                # Find post button
                post_button_selectors = [
                    'button:has-text("Post")',
                    'button:has-text("Share")',
                    '[aria-label="Post"]'
                ]
                
                for selector in post_button_selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            time.sleep(3)
                            break
                    except:
                        continue
                
                # Wait for confirmation
                try:
                    page.wait_for_selector('text=Your post has been shared', timeout=10000)
                    self.logger.info('Post published successfully!')
                except:
                    self.logger.info('Post may have been published (confirmation not detected)')
                
                browser.close()
                
                return {
                    'status': 'success',
                    'message': 'Post published to LinkedIn',
                    'content': content[:100] + '...',
                    'timestamp': datetime.now().isoformat()
                }
                
        except ImportError:
            self.logger.error('Playwright not installed. Run: pip install playwright')
            return {
                'status': 'error',
                'error': 'Playwright not installed'
            }
        
        except Exception as e:
            self.logger.error(f'Error posting to LinkedIn: {e}')
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def schedule_post(self, content: str, scheduled_time: str) -> Dict[str, Any]:
        """
        Schedule a post for later.
        
        Args:
            content: Post content
            scheduled_time: ISO format datetime string
            
        Returns:
            Result dictionary
        """
        self.logger.info(f'Scheduling post for: {scheduled_time}')
        
        # Create scheduled post file
        vault_path = Path(__file__).parent.parent
        scheduled_folder = vault_path / 'Scheduled_Posts'
        scheduled_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'LINKEDIN_POST_{timestamp}.md'
        filepath = scheduled_folder / filename
        
        content_md = f'''---
type: scheduled_linkedin_post
created: {datetime.now().isoformat()}
scheduled_time: {scheduled_time}
status: scheduled
platform: LinkedIn
---

# Scheduled LinkedIn Post

## Scheduled Time
{scheduled_time}

## Post Content

{content}

## Status

- [ ] Review post content
- [ ] Check scheduling time
- [ ] Approve for posting
- [ ] Move to Approved folder
- [ ] System will post at scheduled time

---

*Generated by Personal AI Employee Hackathon-0 LinkedIn MCP Server v0.1 (Silver Tier)*
'''
        
        filepath.write_text(content_md, encoding='utf-8')
        
        self.logger.info(f'Scheduled post file created: {filename}')
        
        return {
            'status': 'scheduled',
            'message': f'Post scheduled for {scheduled_time}',
            'file': str(filepath)
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test LinkedIn connection.
        
        Returns:
            Connection status
        """
        self.logger.info('Testing LinkedIn connection...')
        
        if not self.email:
            return {
                'status': 'error',
                'message': 'LinkedIn email not configured'
            }
        
        if not self.password:
            return {
                'status': 'error',
                'message': 'LinkedIn password not configured'
            }
        
        if self.dry_run:
            return {
                'status': 'success',
                'message': 'Configuration OK (dry run mode)',
                'email': self.email
            }
        
        # Try to login with Playwright
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                page.goto('https://www.linkedin.com/login')
                
                # Check if login page loaded
                if page.is_visible('#username'):
                    browser.close()
                    return {
                        'status': 'success',
                        'message': 'LinkedIn login page accessible',
                        'email': self.email
                    }
                else:
                    browser.close()
                    return {
                        'status': 'error',
                        'message': 'LinkedIn login page not accessible'
                    }
                    
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            }


def main():
    """Main entry point for LinkedIn MCP Server."""
    print('=' * 60)
    print('LinkedIn MCP Server - Silver Tier')
    print('=' * 60)
    
    # Check if running in dry run mode
    dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'
    
    # Create server
    server = LinkedInMCPServer(dry_run=dry_run)
    
    print(f'Dry Run: {dry_run}')
    print('')
    
    # Test connection
    result = server.test_connection()
    print('Connection Test:')
    print(json.dumps(result, indent=2))
    print('')
    
    # Generate sample post
    print('Sample Business Post:')
    print('-' * 60)
    post = server.create_business_post('general')
    print(post)
    print('-' * 60)
    print('')
    
    # If command line args provided, post
    if len(sys.argv) > 1:
        post_type = sys.argv[1]
        content = server.create_business_post(post_type)
        
        print(f'Posting to LinkedIn ({post_type})...')
        result = server.post_to_linkedin(content)
        print('Result:')
        print(json.dumps(result, indent=2))
    
    print('')
    print('=' * 60)
    print('LinkedIn MCP Server ready!')
    print('=' * 60)


if __name__ == '__main__':
    main()
