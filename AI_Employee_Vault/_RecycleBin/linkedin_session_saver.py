#!/usr/bin/env python3
"""
LinkedIn Session Saver

First-time setup: Manually login to LinkedIn
This saves the session for future auto-posting.
"""

import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


def save_session():
    """Save LinkedIn session by manual login."""
    print('=' * 60)
    print('LinkedIn Session Saver - First Time Setup')
    print('=' * 60)
    print('')
    
    email = os.getenv('LINKEDIN_EMAIL', '')
    print(f'Email: {email}')
    print('')
    
    if not email:
        print('Error: LinkedIn email not configured in .env')
        return False
    
    try:
        from playwright.sync_api import sync_playwright
        
        user_data_dir = Path(__file__).parent / 'linkedin_session'
        user_data_dir.mkdir(parents=True, exist_ok=True)
        
        print('Step 1: Browser open ho raha hai...')
        print('')
        
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=False,
                args=['--no-sandbox'],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0]
            
            print('Step 2: LinkedIn login page open karein...')
            page.goto('https://www.linkedin.com/login', wait_until='networkidle')
            
            print('')
            print('=' * 60)
            print('MANUAL LOGIN REQUIRED')
            print('=' * 60)
            print('')
            print('Instructions:')
            print('1. Apna email aur password enter karein')
            print('2. CAPTCHA ya 2FA complete karein (agar aaye)')
            print('3. Feed page tak pahuchein')
            print('4. Jab feed dikhe, browser KHULA CHHOD DEIN')
            print('')
            print('Main 3 minutes wait karunga...')
            print('=' * 60)
            print('')
            
            # Wait for manual login (3 minutes)
            for i in range(18):  # 18 x 10 seconds = 3 minutes
                time.sleep(10)
                
                # Check if on feed page
                if 'feed' in page.url:
                    print('')
                    print('=' * 60)
                    print('✅ LOGIN SUCCESSFUL!')
                    print('=' * 60)
                    print('')
                    print('Session save ho gaya hai!')
                    print('Ab aap auto-post kar sakte hain.')
                    print('')
                    print('Browser band kar sakte hain.')
                    print('')
                    
                    time.sleep(5)
                    browser.close()
                    
                    return True
            
            print('')
            print('=' * 60)
            print('⏰ TIMEOUT!')
            print('=' * 60)
            print('')
            print('3 minutes mein login complete nahi hua.')
            print('Please dobara try karein.')
            print('')
            
            browser.close()
            return False
            
    except ImportError:
        print('Error: Playwright not installed')
        print('Run: pip install playwright')
        return False
    
    except Exception as e:
        print(f'Error: {e}')
        return False


def test_session():
    """Test if saved session works."""
    print('=' * 60)
    print('LinkedIn Session Test')
    print('=' * 60)
    print('')
    
    user_data_dir = Path(__file__).parent / 'linkedin_session'
    
    if not user_data_dir.exists():
        print('❌ Session not found!')
        print('Pehle save_session() run karein.')
        return False
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=False,
                args=['--no-sandbox'],
            )
            
            page = browser.pages[0]
            
            print('Loading LinkedIn with saved session...')
            page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=30000)
            
            time.sleep(5)
            
            if 'feed' in page.url:
                print('')
                print('=' * 60)
                print('✅ SESSION WORKING!')
                print('=' * 60)
                print('')
                print('Saved session se login successful hai.')
                print('Ab aap auto-post kar sakte hain.')
                print('')
                
                browser.close()
                return True
            else:
                print('')
                print('=' * 60)
                print('❌ SESSION NOT WORKING!')
                print('=' * 60)
                print('')
                print('Session expired ya invalid hai.')
                print('Dobara save_session() run karein.')
                print('')
                
                browser.close()
                return False
                
    except Exception as e:
        print(f'Error: {e}')
        return False


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'save':
            save_session()
        elif command == 'test':
            test_session()
        else:
            print('Unknown command. Use: save or test')
    else:
        print('=' * 60)
        print('LinkedIn Session Manager')
        print('=' * 60)
        print('')
        print('Commands:')
        print('  save  - Save LinkedIn session (manual login)')
        print('  test  - Test saved session')
        print('')
        
        command = input('Enter command (save/test): ').strip()
        
        if command == 'save':
            save_session()
        elif command == 'test':
            test_session()
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()
