#!/usr/bin/env python3
"""
Facebook Auto-Poster

Posts content to Facebook using Playwright browser automation.
Supports:
- Text posts
- Photo posts
- Scheduled posting
- Session persistence

Usage:
    python facebook_poster.py "Your post content here"
    python facebook_poster.py --photo path/to/image.jpg --caption "Caption"
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import logging
import argparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright")
    print("Then run: playwright install")
    sys.exit(1)


class FacebookPoster:
    """
    Facebook Auto-Poster using Playwright.
    """
    
    def __init__(self, vault_path: str, session_path: Optional[str] = None):
        """
        Initialize Facebook Poster.
        
        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session (optional)
        """
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path) if session_path else self.vault_path / '.facebook_session'
        self.logs_folder = self.vault_path / 'Logs'
        self.done_folder = self.vault_path / 'Done'
        
        # Ensure folders exist
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Facebook URL
        self.facebook_url = 'https://www.facebook.com'
        
        # Post content templates
        self.post_templates = self._load_post_templates()
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs_folder / f'facebook_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('FacebookPoster')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _load_post_templates(self) -> dict:
        """Load post content templates."""
        return {
            'business_update': [
                "Exciting updates from our business! We're constantly working to deliver the best solutions for our clients. #Business #Growth",
                "Grateful for our amazing clients and partners. Your support drives us forward every day! #Gratitude #Business",
                "New week, new opportunities! Ready to tackle challenges and achieve great results. #MondayMotivation #Business",
            ],
            'engagement': [
                "What's your biggest business challenge this week? Share in the comments! 👇 #Discussion #Business",
                "Tag someone who inspires you to be better! 💪 #Inspiration #Community",
                "Drop a 🔥 if you're ready for this week!",
            ],
            'value_post': [
                "💡 Business Tip: Consistency is key. Show up every day, even when you don't feel like it. #BusinessTips #Motivation",
                "📈 Growth happens outside your comfort zone. Take one small step today! #Growth #Mindset",
                "🎯 Focus on progress, not perfection. Every step counts! #Progress #Goals",
            ],
        }
    
    def post_to_facebook(self, content: str, photo_path: Optional[str] = None) -> bool:
        """
        Post content to Facebook.
        
        Args:
            content: Text content to post
            photo_path: Optional path to photo for post
            
        Returns:
            True if post successful, False otherwise
        """
        self.logger.info("Starting Facebook post...")
        self.logger.info(f"Content: {content[:100]}...")
        
        try:
            with sync_playwright() as p:
                # Launch browser with persistent context
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=False,  # Show browser for debugging
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                    ]
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                
                # Navigate to Facebook
                self.logger.info("Navigating to Facebook...")
                page.goto(self.facebook_url, wait_until='networkidle', timeout=60000)
                
                # Wait for login check
                self.logger.info("Checking login status...")
                try:
                    page.wait_for_selector('[aria-label="What\'s on your mind?"]', timeout=10000)
                    self.logger.info("Already logged in ✓")
                except PlaywrightTimeout:
                    self.logger.warning("Not logged in. Please login manually...")
                    # Wait for manual login
                    page.wait_for_selector('[aria-label="What\'s on your mind?"]', timeout=120000)
                    self.logger.info("Login detected ✓")
                
                # Click on "What's on your mind?" box
                self.logger.info("Opening post composer...")
                page.click('[aria-label="What\'s on your mind?"]')
                
                # Wait for composer to open
                page.wait_for_selector('[aria-label="What\'s on your mind?"]', timeout=10000)
                
                # Type post content
                self.logger.info("Typing post content...")
                post_box = page.locator('[aria-label="What\'s on your mind?"]').first
                post_box.fill(content)
                
                # If photo provided, add it
                if photo_path:
                    self.logger.info(f"Adding photo: {photo_path}")
                    # Wait for photo/video button
                    try:
                        photo_button = page.locator('[aria-label*="photo"], [aria-label*="video"]').first
                        photo_button.click()
                        
                        # Wait for file input and upload
                        file_input = page.locator('input[type="file"]').first
                        file_input.set_input_files(photo_path)
                        
                        # Wait for upload to complete
                        page.wait_for_timeout(3000)
                    except Exception as e:
                        self.logger.warning(f"Could not add photo: {e}")
                
                # Wait a moment for content to render
                page.wait_for_timeout(2000)
                
                # Click Post button
                self.logger.info("Clicking Post button...")
                try:
                    post_button = page.locator('[aria-label*="Post"], button:has-text("Post")').first
                    post_button.click()
                    
                    # Wait for post to complete
                    page.wait_for_timeout(5000)
                    
                    self.logger.info("✓ Post successful!")
                    
                    # Log success
                    self._log_post(content, photo_path, success=True)
                    
                    browser.close()
                    return True
                    
                except Exception as e:
                    self.logger.error(f"Could not click Post button: {e}")
                    browser.close()
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error posting to Facebook: {e}")
            self._log_post(content, photo_path, success=False, error=str(e))
            return False
    
    def _log_post(self, content: str, photo_path: Optional[str], success: bool, error: str = "") -> None:
        """Log post attempt to file."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'Facebook',
            'content': content[:200],
            'photo': photo_path,
            'success': success,
            'error': error
        }
        
        # Append to daily log
        log_file = self.logs_folder / f'facebook_posts_{datetime.now().strftime("%Y%m")}.json'
        
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))
        
        # Create action file in Done
        if success:
            done_file = self.done_folder / f'FACEBOOK_POST_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            done_file.write_text(f'''---
type: social_media
platform: Facebook
timestamp: {datetime.now().isoformat()}
status: published
---

# Facebook Post Published

**Content:**
{content}

**Photo:** {photo_path if photo_path else "None"}

**Result:** Success ✓
''')
    
    def post_daily_content(self, day_number: Optional[int] = None) -> bool:
        """
        Post daily content from templates.
        
        Args:
            day_number: Day number (1-30) for scheduled content
            
        Returns:
            True if successful
        """
        if day_number is None:
            day_number = datetime.now().day
        
        # Select template based on day
        template_types = list(self.post_templates.keys())
        template_index = day_number % len(template_types)
        template_type = template_types[template_index]
        
        # Get content for this day
        content_list = self.post_templates[template_type]
        content_index = day_number % len(content_list)
        content = content_list[content_index]
        
        # Add date-specific hashtag
        today = datetime.now()
        hashtags = {
            0: "#MondayMotivation",
            1: "#TuesdayThoughts",
            2: "#WednesdayWisdom",
            3: "#ThursdayThoughts",
            4: "#FridayFeeling",
            5: "#SaturdayVibes",
            6: "#SundayFunday",
        }
        
        day_hashtag = hashtags.get(today.weekday(), "#Business")
        content = f"{content} {day_hashtag}"
        
        return self.post_to_facebook(content)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Facebook Auto-Poster',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post text
  python facebook_poster.py "Hello Facebook!"
  
  # Post with photo
  python facebook_poster.py --photo image.jpg --caption "Check this out!"
  
  # Post daily content
  python facebook_poster.py --daily
        """
    )
    
    parser.add_argument(
        'content',
        nargs='?',
        default=None,
        help='Post content'
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault (default: current directory)'
    )
    parser.add_argument(
        '--photo',
        help='Path to photo for post'
    )
    parser.add_argument(
        '--caption',
        help='Photo caption'
    )
    parser.add_argument(
        '--daily',
        action='store_true',
        help='Post daily template content'
    )
    parser.add_argument(
        '--day',
        type=int,
        help='Day number for daily content (1-30)'
    )
    
    args = parser.parse_args()
    
    # Determine vault path
    vault_path = Path(args.vault).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create poster
    poster = FacebookPoster(str(vault_path))
    
    print("=" * 60)
    print('📘 Facebook Auto-Poster')
    print("=" * 60)
    
    # Post content
    if args.daily:
        print(f'Posting daily content (day {args.day or "auto"})...')
        success = poster.post_daily_content(day_number=args.day)
    elif args.content:
        print(f'Posting: {args.content[:50]}...')
        success = poster.post_to_facebook(args.content, photo_path=args.photo)
    elif args.photo and args.caption:
        print(f'Posting photo with caption...')
        success = poster.post_to_facebook(args.caption, photo_path=args.photo)
    else:
        print("Error: No content provided. Use --help for usage.")
        sys.exit(1)
    
    print('')
    print('=' * 60)
    if success:
        print('✓ Facebook post successful!')
    else:
        print('✗ Facebook post failed. Check logs for details.')
    print('=' * 60)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
