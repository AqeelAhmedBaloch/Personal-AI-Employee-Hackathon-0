#!/usr/bin/env python3
"""
LinkedIn API Auto-Poster

Official LinkedIn API integration for posting.
Requires LinkedIn Developer App approval.

Setup Guide:
1. Create LinkedIn Developer Account: https://www.linkedin.com/developers/
2. Create App: https://www.linkedin.com/developers/apps
3. Get Client ID and Client Secret
4. Generate Access Token
5. Run this script
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInAPIPoster:
    """
    Post to LinkedIn using official API.
    """
    
    def __init__(self):
        """Initialize LinkedIn API Poster."""
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID', '')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', '')
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        self.person_urn = os.getenv('LINKEDIN_PERSON_URN', '')
        
        self.api_base = 'https://api.linkedin.com/v2'
        
        # Post templates
        self.templates = {
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
    
    def get_authorization_url(self, redirect_uri='http://localhost:8080'):
        """
        Get LinkedIn OAuth authorization URL.
        
        Returns:
            Authorization URL to open in browser
        """
        base_url = 'https://www.linkedin.com/oauth/v2/authorization'
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': 'w_member_social r_basicprofile'
        }
        
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f'{base_url}?{query_string}'
    
    def exchange_code_for_token(self, authorization_code, redirect_uri='http://localhost:8080'):
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: Code from OAuth callback
            redirect_uri: Same redirect URI used in authorization
            
        Returns:
            Access token string
        """
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        
        result = response.json()
        return result['access_token']
    
    def get_person_urn(self):
        """
        Get current user's LinkedIn URN.
        
        Returns:
            Person URN (e.g., urn:li:person:ABC123)
        """
        if not self.access_token:
            raise ValueError('Access token required')
        
        url = f'{self.api_base}/me'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        return result['id']
    
    def post(self, post_type='general', comment=None):
        """
        Post to LinkedIn using API.
        
        Args:
            post_type: Type of post (general, service, product, etc.)
            comment: Optional custom comment
            
        Returns:
            Result dictionary with post ID
        """
        if not self.access_token:
            return {
                'status': 'error',
                'error': 'Access token not configured'
            }
        
        # Get post content
        content = self.templates.get(post_type, self.templates['general'])
        
        # Add custom comment if provided
        if comment:
            content = f'{comment}\n\n{content}'
        
        # Get person URN if not set
        person_urn = self.person_urn
        if not person_urn:
            try:
                person_urn = f'urn:li:person:{self.get_person_urn()}'
            except Exception as e:
                return {
                    'status': 'error',
                    'error': f'Failed to get person URN: {e}'
                }
        
        # Create post
        url = f'{self.api_base}/ugcPosts'
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }
        
        post_data = {
            'author': person_urn,
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': content
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }
        
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            result = response.json()
            return {
                'status': 'success',
                'post_id': result.get('id'),
                'message': 'Post published successfully!',
                'content': content[:100] + '...'
            }
        else:
            return {
                'status': 'error',
                'error': f'API Error: {response.status_code}',
                'details': response.text
            }


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn API Poster - Official Integration')
    print('=' * 60)
    print('')
    
    # Check if access token is configured
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    
    if not access_token:
        print('⚠️  Access token not configured!')
        print('')
        print('Setup Instructions:')
        print('1. Create LinkedIn Developer App:')
        print('   https://www.linkedin.com/developers/apps')
        print('')
        print('2. Get Client ID and Client Secret')
        print('')
        print('3. Generate Access Token:')
        print('   - Open authorization URL')
        print('   - Authorize the app')
        print('   - Copy authorization code')
        print('   - Exchange for access token')
        print('')
        print('4. Add to .env file:')
        print('   LINKEDIN_ACCESS_TOKEN=your_token_here')
        print('')
        
        # Show authorization URL
        client_id = os.getenv('LINKEDIN_CLIENT_ID', '')
        if client_id:
            poster = LinkedInAPIPoster()
            auth_url = poster.get_authorization_url()
            print('Authorization URL:')
            print(auth_url)
            print('')
        
        return
    
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
    poster = LinkedInAPIPoster()
    
    # Post
    print('Posting to LinkedIn via API...')
    print('')
    
    result = poster.post(post_type)
    
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    
    if result['status'] == 'success':
        print(f'Post ID: {result["post_id"]}')
        print('')
        print('✅ Post published successfully!')
        print('')
        print('View your post:')
        print('https://www.linkedin.com/feed/')
    else:
        print('')
        print('❌ Posting failed!')
        if 'details' in result:
            print(f'Details: {result["details"]}')
    
    print('=' * 60)


if __name__ == '__main__':
    main()
