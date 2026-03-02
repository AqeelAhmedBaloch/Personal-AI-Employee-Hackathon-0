#!/usr/bin/env python3
"""
Social Media Unified Controller

Unified interface for posting to all social media platforms.
Supports:
- Facebook
- Instagram
- Twitter/X
- LinkedIn

Features:
- Cross-platform posting
- Platform-specific formatting
- Scheduling support
- Content templates

Usage:
    python social_media_controller.py --platforms all --content "Your post"
    python social_media_controller.py --platforms facebook,twitter --daily
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
import logging
import argparse

# Import platform posters
try:
    from facebook_poster import FacebookPoster
    from instagram_poster import InstagramPoster
    from twitter_poster import TwitterPoster
    
    # LinkedIn poster from existing implementation
    sys.path.insert(0, str(Path(__file__).parent / 'mcp_servers' / 'linkedin_mcp'))
    from linkedin_daily_auto_post import LinkedInAutoPoster
except ImportError as e:
    print(f"Error importing platform posters: {e}")
    print("Make sure all platform posters are installed.")
    sys.exit(1)


class SocialMediaController:
    """
    Unified controller for all social media platforms.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize Social Media Controller.
        
        Args:
            vault_path: Path to Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logs_folder = self.vault_path / 'Logs'
        
        # Ensure logs folder exists
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Initialize platform posters
        self.facebook = FacebookPoster(str(vault_path))
        self.instagram = InstagramPoster(str(vault_path))
        self.twitter = TwitterPoster(str(vault_path))
        self.linkedin = LinkedInAutoPoster() if hasattr(self, 'linkedin') else None
        
        self.logger.info("Social Media Controller initialized")
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs_folder / f'social_media_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('SocialMediaController')
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
    
    def post_to_platform(
        self,
        platform: str,
        content: str,
        photo_path: Optional[str] = None
    ) -> bool:
        """
        Post to a specific platform.
        
        Args:
            platform: Platform name (facebook, instagram, twitter, linkedin)
            content: Post content
            photo_path: Optional photo path
            
        Returns:
            True if successful
        """
        platform = platform.lower()
        
        self.logger.info(f"Posting to {platform}...")
        
        try:
            if platform == 'facebook':
                return self.facebook.post_to_facebook(content, photo_path)
            
            elif platform == 'instagram':
                if not photo_path:
                    self.logger.error("Instagram requires a photo")
                    return False
                return self.instagram.post_to_instagram(photo_path, content)
            
            elif platform == 'twitter':
                return self.twitter.post_to_twitter(content, photo_path)
            
            elif platform == 'linkedin':
                # LinkedIn uses different interface
                if self.linkedin:
                    return self.linkedin.post_content(content)
                else:
                    self.logger.warning("LinkedIn poster not available")
                    return False
            
            else:
                self.logger.error(f"Unknown platform: {platform}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error posting to {platform}: {e}")
            return False
    
    def post_to_all(
        self,
        content: str,
        platforms: Optional[List[str]] = None,
        photo_path: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Post to multiple platforms.
        
        Args:
            content: Post content
            platforms: List of platforms (default: all)
            photo_path: Optional photo path
            
        Returns:
            Dictionary of platform -> success status
        """
        if platforms is None:
            platforms = ['facebook', 'twitter', 'linkedin']
        
        results = {}
        
        for platform in platforms:
            # Skip Instagram if no photo
            if platform == 'instagram' and not photo_path:
                self.logger.info(f"Skipping Instagram (no photo)")
                results[platform] = False
                continue
            
            success = self.post_to_platform(platform, content, photo_path)
            results[platform] = success
            
            # Small delay between posts
            if platform != platforms[-1]:
                import time
                time.sleep(2)
        
        return results
    
    def post_daily_content(
        self,
        platforms: Optional[List[str]] = None,
        photo_path: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Post daily template content to all platforms.
        
        Args:
            platforms: List of platforms
            photo_path: Optional photo for Instagram
            
        Returns:
            Dictionary of platform -> success status
        """
        if platforms is None:
            platforms = ['facebook', 'twitter', 'linkedin']
        
        results = {}
        day = datetime.now().day
        
        for platform in platforms:
            try:
                if platform == 'facebook':
                    success = self.facebook.post_daily_content(day_number=day)
                elif platform == 'instagram':
                    if photo_path:
                        success = self.instagram.post_daily_content(photo_path, day)
                    else:
                        self.logger.info("Skipping Instagram (no photo)")
                        success = False
                elif platform == 'twitter':
                    success = self.twitter.post_daily_content(day_number=day)
                elif platform == 'linkedin':
                    if self.linkedin:
                        success = self.linkedin.post_day(day)
                    else:
                        success = False
                else:
                    success = False
                
                results[platform] = success
                
            except Exception as e:
                self.logger.error(f"Error posting daily to {platform}: {e}")
                results[platform] = False
        
        return results
    
    def get_platform_stats(self) -> Dict[str, Dict]:
        """
        Get posting statistics for all platforms.
        
        Returns:
            Dictionary of platform statistics
        """
        stats = {}
        
        for platform in ['facebook', 'instagram', 'twitter', 'linkedin']:
            log_file = self.logs_folder / f'{platform}_posts_{datetime.now().strftime("%Y%m")}.json'
            
            if log_file.exists():
                try:
                    logs = json.loads(log_file.read_text())
                    total = len(logs)
                    successful = sum(1 for log in logs if log.get('success', False))
                    
                    stats[platform] = {
                        'total_posts': total,
                        'successful': successful,
                        'failed': total - successful,
                        'success_rate': (successful / total * 100) if total > 0 else 0
                    }
                except:
                    stats[platform] = {'error': 'Could not read logs'}
            else:
                stats[platform] = {'total_posts': 0}
        
        return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Social Media Unified Controller',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post to all platforms
  python social_media_controller.py --content "Hello World!"
  
  # Post to specific platforms
  python social_media_controller.py --platforms facebook,twitter --content "Hello!"
  
  # Post daily content
  python social_media_controller.py --daily
  
  # Post with photo
  python social_media_controller.py --photo image.jpg --caption "Check this!"
  
  # Get stats
  python social_media_controller.py --stats
        """
    )
    
    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault (default: current directory)'
    )
    parser.add_argument(
        '--content', '-c',
        help='Post content'
    )
    parser.add_argument(
        '--platforms', '-p',
        default='all',
        help='Platforms: all, facebook, instagram, twitter, linkedin (comma-separated)'
    )
    parser.add_argument(
        '--photo',
        help='Photo path (required for Instagram)'
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
        '--stats',
        action='store_true',
        help='Show platform statistics'
    )
    
    args = parser.parse_args()
    
    # Determine vault path
    vault_path = Path(args.vault).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create controller
    controller = SocialMediaController(str(vault_path))
    
    print("=" * 60)
    print('📱 Social Media Unified Controller')
    print("=" * 60)
    
    # Show stats
    if args.stats:
        stats = controller.get_platform_stats()
        print("\nPlatform Statistics (This Month):\n")
        for platform, data in stats.items():
            if 'error' in data:
                print(f"  {platform.capitalize()}: {data['error']}")
            else:
                total = data.get('total_posts', 0)
                successful = data.get('successful', 0)
                rate = data.get('success_rate', 0)
                print(f"  {platform.capitalize()}: {total} posts, {successful} successful ({rate:.1f}%)")
        print()
        sys.exit(0)
    
    # Determine platforms
    if args.platforms.lower() == 'all':
        platforms = ['facebook', 'twitter', 'linkedin']
        if args.photo:
            platforms.append('instagram')
    else:
        platforms = [p.strip() for p in args.platforms.split(',')]
    
    print(f"Platforms: {', '.join(platforms)}")
    print()
    
    # Post content
    if args.daily:
        print("Posting daily content...")
        results = controller.post_daily_content(platforms, photo_path=args.photo)
    elif args.caption:
        print(f"Posting: {args.caption[:50]}...")
        results = controller.post_to_all(args.caption, platforms, photo_path=args.photo)
    elif args.content:
        print(f"Posting: {args.content[:50]}...")
        results = controller.post_to_all(args.content, platforms, photo_path=args.photo)
    else:
        print("Error: No content provided. Use --help for usage.")
        sys.exit(1)
    
    # Show results
    print()
    print("=" * 60)
    print("Results:\n")
    for platform, success in results.items():
        icon = "✓" if success else "✗"
        status = "Success" if success else "Failed"
        print(f"  {icon} {platform.capitalize()}: {status}")
    print("=" * 60)
    
    # Exit with appropriate code
    all_success = all(results.values())
    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
