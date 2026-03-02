#!/usr/bin/env python3
"""
Twitter/X Auto-Poster

Posts content to Twitter/X using Playwright browser automation.
Supports:
- Text tweets (280 characters)
- Thread posting
- Image tweets
- Session persistence

Note: Twitter has strict bot detection. Use with caution and respect rate limits.

Usage:
    python twitter_poster.py "Your tweet content here"
    python twitter_poster.py --photo path/to/image.jpg --caption "Caption"
    python twitter_poster.py --daily
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


class TwitterPoster:
    """
    Twitter/X Auto-Poster using Playwright.
    """
    
    def __init__(self, vault_path: str, session_path: Optional[str] = None):
        """
        Initialize Twitter Poster.
        
        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session (optional)
        """
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path) if session_path else self.vault_path / '.twitter_session'
        self.logs_folder = self.vault_path / 'Logs'
        self.done_folder = self.vault_path / 'Done'
        
        # Ensure folders exist
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Twitter URL
        self.twitter_url = 'https://twitter.com'
        self.twitter_compose_url = 'https://twitter.com/compose/tweet'
        
        # Tweet templates
        self.tweet_templates = self._load_tweet_templates()
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs_folder / f'twitter_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('TwitterPoster')
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
    
    def _load_tweet_templates(self) -> dict:
        """Load tweet content templates."""
        return {
            'business': [
                "Exciting updates from our business! We're constantly working to deliver the best solutions. #Business #Growth #Entrepreneur",
                "Grateful for our amazing clients and partners. Your support drives us forward! #Gratitude #Business #Success",
                "New week, new opportunities! Ready to tackle challenges and achieve great results. #MondayMotivation #Goals",
            ],
            'tips': [
                "💡 Business Tip: Consistency is key. Show up every day, even when you don't feel like it. #BusinessTips #Motivation #Success",
                "📈 Growth happens outside your comfort zone. Take one small step today! #Growth #Mindset #PersonalDevelopment",
                "🎯 Focus on progress, not perfection. Every step counts! #Progress #Goals #Achievement",
            ],
            'engagement': [
                "What's your biggest business challenge this week? Drop it below! 👇 #Discussion #Business #Entrepreneur",
                "Tag someone who inspires you to be better! 💪 #Inspiration #Community #Motivation",
                "Drop a 🔥 if you're ready for this week! #MondayVibes #Motivation #Hustle",
            ],
            'thread_starters': [
                "🧵 Thread: Here's what I learned about building a business in 2026...",
                "🧵 Let me share something important about productivity...",
                "🧵 Hot take: Most business advice is wrong. Here's why...",
            ],
        }
    
    def post_to_twitter(self, content: str, photo_path: Optional[str] = None) -> bool:
        """
        Post content to Twitter/X.
        
        Args:
            content: Tweet content (max 280 chars for single tweet)
            photo_path: Optional path to photo for tweet
            
        Returns:
            True if post successful, False otherwise
        """
        self.logger.info("Starting Twitter post...")
        
        # Check content length
        if len(content) > 280:
            self.logger.warning(f"Content exceeds 280 characters ({len(content)} chars). Consider using a thread.")
        
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
                
                # Navigate to Twitter
                self.logger.info("Navigating to Twitter...")
                page.goto(self.twitter_url, wait_until='networkidle', timeout=60000)
                
                # Wait for login check
                self.logger.info("Checking login status...")
                try:
                    page.wait_for_selector('[data-testid="tweetButton"]', timeout=10000)
                    self.logger.info("Already logged in ✓")
                except PlaywrightTimeout:
                    self.logger.warning("Not logged in. Please login manually...")
                    # Wait for manual login
                    page.wait_for_selector('[data-testid="tweetButton"]', timeout=120000)
                    self.logger.info("Login detected ✓")
                
                # Navigate to compose page
                self.logger.info("Navigating to compose page...")
                page.goto(self.twitter_compose_url, wait_until='networkidle', timeout=30000)
                
                # Wait for textarea
                page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
                
                # Type tweet content
                self.logger.info("Typing tweet content...")
                textarea = page.locator('[data-testid="tweetTextarea_0"]').first
                textarea.fill(content)
                
                # If photo provided, add it
                if photo_path:
                    self.logger.info(f"Adding photo: {photo_path}")
                    try:
                        # Click media button
                        media_button = page.locator('[data-testid="addImageButton"]').first
                        media_button.click()
                        
                        # Wait for file input and upload
                        page.wait_for_timeout(2000)
                        file_input = page.locator('input[type="file"]').first
                        file_input.set_input_files(photo_path)
                        
                        # Wait for upload to complete
                        page.wait_for_timeout(5000)
                        
                        self.logger.info("Photo uploaded ✓")
                    except Exception as e:
                        self.logger.warning(f"Could not add photo: {e}")
                
                # Wait a moment for content to render
                page.wait_for_timeout(2000)
                
                # Click Tweet button
                self.logger.info("Clicking Tweet button...")
                try:
                    tweet_button = page.locator('[data-testid="tweetButton"]').first
                    tweet_button.click()
                    
                    # Wait for tweet to complete
                    page.wait_for_timeout(5000)
                    
                    # Check for success indicators
                    try:
                        page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=3000, state='detached')
                        self.logger.info("✓ Tweet successful!")
                        
                        # Log success
                        self._log_post(content, photo_path, success=True)
                        
                        browser.close()
                        return True
                    except PlaywrightTimeout:
                        # Textarea still visible - might have failed
                        self.logger.warning("Tweet button clicked but textarea still visible")
                        browser.close()
                        return False
                    
                except Exception as e:
                    self.logger.error(f"Could not click Tweet button: {e}")
                    browser.close()
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error posting to Twitter: {e}")
            self._log_post(content, photo_path, success=False, error=str(e))
            return False
    
    def _log_post(self, content: str, photo_path: Optional[str], success: bool, error: str = "") -> None:
        """Log post attempt to file."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'Twitter',
            'content': content[:280],
            'photo': photo_path,
            'success': success,
            'error': error
        }
        
        # Append to monthly log
        log_file = self.logs_folder / f'twitter_posts_{datetime.now().strftime("%Y%m")}.json'
        
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
            done_file = self.done_folder / f'TWITTER_POST_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            done_file.write_text(f'''---
type: social_media
platform: Twitter/X
timestamp: {datetime.now().isoformat()}
status: published
---

# Twitter Post Published

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
        template_types = list(self.tweet_templates.keys())
        # Exclude thread_starters for single tweets
        template_types = [t for t in template_types if t != 'thread_starters']
        
        template_index = day_number % len(template_types)
        template_type = template_types[template_index]
        
        # Get content for this day
        content_list = self.tweet_templates[template_type]
        content_index = day_number % len(content_list)
        content = content_list[content_index]
        
        # Add day-specific hashtag
        today = datetime.now()
        day_hashtags = {
            0: "#MondayMotivation",
            1: "#TuesdayThoughts",
            2: "#WednesdayWisdom",
            3: "#ThursdayThoughts",
            4: "#FridayFeeling",
            5: "#SaturdayVibes",
            6: "#SundayFunday",
        }
        
        hashtag = day_hashtags.get(today.weekday(), "")
        if hashtag and hashtag not in content:
            content = f"{content} {hashtag}"
        
        return self.post_to_twitter(content)
    
    def post_thread(self, tweets: List[str]) -> bool:
        """
        Post a thread of tweets.
        
        Args:
            tweets: List of tweet contents
            
        Returns:
            True if successful
        """
        self.logger.info(f"Starting thread with {len(tweets)} tweets...")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled']
                )
                
                page = browser.pages[0] if browser.pages else browser.new_page()
                
                # Navigate and login
                page.goto(self.twitter_compose_url, wait_until='networkidle', timeout=60000)
                page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=30000)
                
                # First tweet
                textarea = page.locator('[data-testid="tweetTextarea_0"]').first
                textarea.fill(tweets[0])
                
                # Add remaining tweets
                for i, tweet in enumerate(tweets[1:], 1):
                    try:
                        # Click "Add another tweet" button
                        add_button = page.locator('[aria-label*="Add another tweet"]').first
                        add_button.click()
                        page.wait_for_timeout(2000)
                        
                        # Fill next textarea
                        textareas = page.locator('[data-testid="tweetTextarea_0"]').all()
                        if len(textareas) > i:
                            textareas[i].fill(tweet)
                    except Exception as e:
                        self.logger.warning(f"Could not add tweet {i}: {e}")
                
                # Post all
                tweet_button = page.locator('[data-testid="tweetButton"]').first
                tweet_button.click()
                
                page.wait_for_timeout(5000)
                
                self.logger.info("✓ Thread posted!")
                browser.close()
                return True
                
        except Exception as e:
            self.logger.error(f"Error posting thread: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Twitter/X Auto-Poster',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post text tweet
  python twitter_poster.py "Hello Twitter!"
  
  # Post with photo
  python twitter_poster.py --photo image.jpg --caption "Check this out!"
  
  # Post daily content
  python twitter_poster.py --daily
        """
    )
    
    parser.add_argument(
        'content',
        nargs='?',
        default=None,
        help='Tweet content'
    )
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault (default: current directory)'
    )
    parser.add_argument(
        '--photo',
        help='Path to photo for tweet'
    )
    parser.add_argument(
        '--caption',
        help='Photo caption (overrides content arg)'
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
    poster = TwitterPoster(str(vault_path))
    
    print("=" * 60)
    print('🐦 Twitter/X Auto-Poster')
    print("=" * 60)
    
    # Post content
    if args.daily:
        print(f'Posting daily content (day {args.day or "auto"})...')
        success = poster.post_daily_content(day_number=args.day)
    elif args.caption:
        print(f'Posting photo with caption...')
        success = poster.post_to_twitter(args.caption, photo_path=args.photo)
    elif args.content:
        print(f'Posting: {args.content[:50]}...')
        success = poster.post_to_twitter(args.content, photo_path=args.photo)
    else:
        print("Error: No content provided. Use --help for usage.")
        sys.exit(1)
    
    print('')
    print('=' * 60)
    if success:
        print('✓ Twitter post successful!')
    else:
        print('✗ Twitter post failed. Check logs for details.')
    print('=' * 60)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
