#!/usr/bin/env python3
"""
Instagram Auto-Poster

Posts content to Instagram using Playwright browser automation.
Supports:
- Photo posts
- Caption with hashtags
- Session persistence

Note: Instagram has strict bot detection. Use with caution.

Usage:
    python instagram_poster.py --photo path/to/image.jpg --caption "Caption"
    python instagram_poster.py --daily
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import logging
import argparse

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright")
    print("Then run: playwright install")
    sys.exit(1)


class InstagramPoster:
    """
    Instagram Auto-Poster using Playwright.
    """
    
    def __init__(self, vault_path: str, session_path: Optional[str] = None):
        """
        Initialize Instagram Poster.
        
        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session (optional)
        """
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path) if session_path else self.vault_path / '.instagram_session'
        self.logs_folder = self.vault_path / 'Logs'
        self.done_folder = self.vault_path / 'Done'
        
        # Ensure folders exist
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Instagram URL
        self.instagram_url = 'https://www.instagram.com'
        
        # Hashtag sets for different content types
        self.hashtag_sets = {
            'business': [
                '#business', '#entrepreneur', '#success', '#motivation', '#hustle',
                '#businessowner', '#startup', '#mindset', '#goals', '#leadership'
            ],
            'inspiration': [
                '#inspiration', '#motivation', '#positivity', '#mindset', '#growth',
                '#success', '#goals', '#dreambig', '#believe', '#positivevibes'
            ],
            'lifestyle': [
                '#lifestyle', '#life', '#happy', '#love', '#instagood', '#photooftheday',
                '#beautiful', '#instadaily', '#picoftheday', '#follow'
            ],
        }
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs_folder / f'instagram_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('InstagramPoster')
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
    
    def post_to_instagram(self, photo_path: str, caption: str = "") -> bool:
        """
        Post photo to Instagram.
        
        Args:
            photo_path: Path to photo file
            caption: Post caption (optional)
            
        Returns:
            True if post successful, False otherwise
        """
        self.logger.info("Starting Instagram post...")
        self.logger.info(f"Photo: {photo_path}")
        self.logger.info(f"Caption: {caption[:50]}...")
        
        # Verify photo exists
        if not Path(photo_path).exists():
            self.logger.error(f"Photo not found: {photo_path}")
            return False
        
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
                
                # Navigate to Instagram
                self.logger.info("Navigating to Instagram...")
                page.goto(self.instagram_url, wait_until='networkidle', timeout=60000)
                
                # Wait for login check
                self.logger.info("Checking login status...")
                try:
                    page.wait_for_selector('svg[aria-label="Home"]', timeout=10000)
                    self.logger.info("Already logged in ✓")
                except PlaywrightTimeout:
                    self.logger.warning("Not logged in. Please login manually...")
                    # Wait for manual login (2 minutes)
                    try:
                        page.wait_for_selector('svg[aria-label="Home"]', timeout=120000)
                        self.logger.info("Login detected ✓")
                    except PlaywrightTimeout:
                        self.logger.error("Login timeout. Please login and try again.")
                        browser.close()
                        return False
                
                # Click New Post button (+ icon)
                self.logger.info("Opening new post dialog...")
                try:
                    # Try different selectors for new post button
                    new_post_selectors = [
                        'svg[aria-label="New post"]',
                        '[aria-label="Create"]',
                        'svg path[d*="M24 12"]',  # Plus icon
                    ]
                    
                    for selector in new_post_selectors:
                        try:
                            page.click(selector, timeout=3000)
                            break
                        except:
                            continue
                    else:
                        # If no button found, navigate to create page directly
                        page.goto('https://www.instagram.com/create/details/', timeout=30000)
                    
                    # Wait for file upload dialog
                    page.wait_for_timeout(3000)
                    
                except Exception as e:
                    self.logger.error(f"Could not open new post dialog: {e}")
                    browser.close()
                    return False
                
                # Upload photo
                self.logger.info("Uploading photo...")
                try:
                    file_input = page.locator('input[type="file"]').first
                    file_input.set_input_files(photo_path)
                    
                    # Wait for upload and editing
                    page.wait_for_timeout(5000)
                    
                except Exception as e:
                    self.logger.error(f"Could not upload photo: {e}")
                    browser.close()
                    return False
                
                # Click Next
                self.logger.info("Clicking Next...")
                try:
                    page.click('button:has-text("Next"), div[role="button"]:has-text("Next")')
                    page.wait_for_timeout(3000)
                    
                    # Click Next again for filters
                    page.click('button:has-text("Next"), div[role="button"]:has-text("Next")')
                    page.wait_for_timeout(2000)
                    
                except Exception as e:
                    self.logger.warning(f"Could not click Next: {e}")
                
                # Add caption
                if caption:
                    self.logger.info("Adding caption...")
                    try:
                        caption_box = page.locator('textarea[aria-label*="caption"], textarea[placeholder*="caption"]').first
                        caption_box.fill(caption)
                        page.wait_for_timeout(1000)
                    except Exception as e:
                        self.logger.warning(f"Could not add caption: {e}")
                
                # Click Share
                self.logger.info("Clicking Share...")
                try:
                    share_button = page.locator('button:has-text("Share"), div[role="button"]:has-text("Share")').first
                    share_button.click()
                    
                    # Wait for post to complete
                    page.wait_for_timeout(5000)
                    
                    self.logger.info("✓ Post successful!")
                    
                    # Log success
                    self._log_post(photo_path, caption, success=True)
                    
                    browser.close()
                    return True
                    
                except Exception as e:
                    self.logger.error(f"Could not click Share: {e}")
                    browser.close()
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")
            self._log_post(photo_path, caption, success=False, error=str(e))
            return False
    
    def _log_post(self, photo_path: str, caption: str, success: bool, error: str = "") -> None:
        """Log post attempt to file."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'Instagram',
            'photo': photo_path,
            'caption': caption[:200],
            'success': success,
            'error': error
        }
        
        # Append to monthly log
        log_file = self.logs_folder / f'instagram_posts_{datetime.now().strftime("%Y%m")}.json'
        
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
            done_file = self.done_folder / f'INSTAGRAM_POST_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            done_file.write_text(f'''---
type: social_media
platform: Instagram
timestamp: {datetime.now().isoformat()}
status: published
---

# Instagram Post Published

**Photo:** {photo_path}

**Caption:**
{caption}

**Result:** Success ✓
''')
    
    def post_daily_content(self, photo_path: str, day_number: Optional[int] = None) -> bool:
        """
        Post daily content with appropriate hashtags.
        
        Args:
            photo_path: Path to photo
            day_number: Day number for content selection
            
        Returns:
            True if successful
        """
        if day_number is None:
            day_number = datetime.now().day
        
        # Select hashtag set based on day
        hashtag_types = list(self.hashtag_sets.keys())
        hashtag_index = day_number % len(hashtag_types)
        hashtag_type = hashtag_types[hashtag_index]
        
        # Get hashtags
        hashtags = self.hashtag_sets[hashtag_type]
        
        # Add day-specific caption
        captions = {
            0: "Starting the week strong! 💪",
            1: "Tuesday vibes ✨",
            2: "Hump day motivation 🎯",
            3: "Thursday thoughts 💭",
            4: "Friday feeling! 🎉",
            5: "Saturday adventures 🌟",
            6: "Sunday relaxation 😌",
        }
        
        today = datetime.now().weekday()
        caption = captions.get(today, "Great day! ☀️")
        
        # Combine caption and hashtags
        full_caption = f"{caption}\n\n{' '.join(hashtags[:10])}"
        
        return self.post_to_instagram(photo_path, full_caption)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Instagram Auto-Poster',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post with photo and caption
  python instagram_poster.py --photo image.jpg --caption "Hello Instagram!"
  
  # Post daily content
  python instagram_poster.py --daily --photo image.jpg
  
  # Post with specific day
  python instagram_poster.py --photo image.jpg --day 5
        """
    )
    
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault (default: current directory)'
    )
    parser.add_argument(
        '--photo',
        required=True,
        help='Path to photo for post'
    )
    parser.add_argument(
        '--caption',
        help='Photo caption (optional)'
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
    poster = InstagramPoster(str(vault_path))
    
    print("=" * 60)
    print('📷 Instagram Auto-Poster')
    print("=" * 60)
    
    # Post content
    if args.daily:
        print(f'Posting daily content (day {args.day or "auto"})...')
        success = poster.post_daily_content(args.photo, day_number=args.day)
    elif args.caption:
        print(f'Posting photo with caption...')
        success = poster.post_to_instagram(args.photo, args.caption)
    else:
        # Generate simple caption
        caption = f"Posted from Personal AI Employee Hackathon-0 🤖"
        print(f'Posting photo with auto-caption...')
        success = poster.post_to_instagram(args.photo, caption)
    
    print('')
    print('=' * 60)
    if success:
        print('✓ Instagram post successful!')
    else:
        print('✗ Instagram post failed. Check logs for details.')
    print('=' * 60)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
