#!/usr/bin/env python3
"""
LinkedIn Quick Post

Uses existing Chrome session to post to LinkedIn.
Requires: Chrome open with LinkedIn logged in.
"""

import sys
import os
import time
from pathlib import Path


def quick_post():
    """Post to LinkedIn using existing Chrome session."""
    print('=' * 60)
    print('LinkedIn Quick Post - Using Existing Session')
    print('=' * 60)
    print('')
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Get Chrome user data directory
        # Windows default location
        chrome_data_dirs = [
            Path(os.environ['LOCALAPPDATA']) / 'Google' / 'Chrome' / 'User Data',
            Path(os.environ['APPDATA']) / 'Chrome' / 'User Data',
        ]
        
        chrome_dir = None
        for dir_path in chrome_data_dirs:
            if dir_path.exists():
                chrome_dir = dir_path
                break
        
        if not chrome_dir:
            print('❌ Chrome not found!')
            print('Please install Chrome and login to LinkedIn.')
            return False
        
        print(f'Chrome data dir: {chrome_dir}')
        print('')
        
        with sync_playwright() as p:
            # Launch Chrome with existing profile
            print('Launching Chrome with your profile...')
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(chrome_dir),
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            # Navigate to LinkedIn feed
            print('Opening LinkedIn...')
            page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=30000)
            
            time.sleep(3)
            
            # Check if logged in
            if 'login' in page.url:
                print('')
                print('❌ Not logged in!')
                print('Please login to LinkedIn in Chrome first.')
                browser.close()
                return False
            
            print('✅ Logged in!')
            print('')
            
            # Post content
            post_content = '''Exciting updates from our business!

We're constantly working to deliver the best solutions for our clients. Our AI Employee system is now operational and helping us automate daily tasks efficiently.

#Business #Automation #AI #Innovation #Productivity'''
            
            print('Creating post...')
            
            # Click "Start a post"
            selectors = [
                '[aria-label="Start a post"]',
                '.share-box-feed-entry__trigger',
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    if page.is_visible(selector):
                        page.click(selector)
                        clicked = True
                        print(f'Clicked: {selector}')
                        time.sleep(2)
                        break
                except:
                    continue
            
            if not clicked:
                print('❌ Could not find "Start a post" button')
                print('Please try manually.')
                browser.close()
                return False
            
            # Fill content
            print('Filling content...')
            
            editor = page.locator('[role="textbox"]').first
            
            # Type slowly
            for char in post_content:
                editor.type(char, delay=50)
            
            time.sleep(2)
            
            # Click Post
            print('Publishing...')
            
            post_selectors = [
                'button:has-text("Post")',
                'button:has-text("Share")',
            ]
            
            for selector in post_selectors:
                try:
                    if page.is_visible(selector):
                        page.click(selector)
                        print(f'Clicked: {selector}')
                        time.sleep(3)
                        break
                except:
                    continue
            
            time.sleep(3)
            
            print('')
            print('=' * 60)
            print('✅ POST PUBLISHED!')
            print('=' * 60)
            print('')
            print('Check your LinkedIn profile to verify.')
            print('')
            
            browser.close()
            
            return True
            
    except ImportError:
        print('❌ Playwright not installed!')
        print('Run: pip install playwright')
        return False
    
    except Exception as e:
        print(f'❌ Error: {e}')
        print('')
        print('Alternative: Post manually on LinkedIn')
        return False


def main():
    """Main entry point."""
    success = quick_post()
    
    if success:
        print('🎉 LinkedIn post successful!')
    else:
        print('')
        print('Manual posting instructions:')
        print('1. Open: https://www.linkedin.com/feed/')
        print('2. Click: "Start a post"')
        print('3. Paste your content')
        print('4. Click: "Post"')


if __name__ == '__main__':
    main()
