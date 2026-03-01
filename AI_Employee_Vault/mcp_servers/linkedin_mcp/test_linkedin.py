#!/usr/bin/env python3
"""
LinkedIn Post Test

Tests LinkedIn MCP Server and shows available post templates.
"""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_server import LinkedInMCPServer

def main():
    print('=' * 60)
    print('LinkedIn Post Test - Silver Tier')
    print('=' * 60)
    print('')
    
    # Create server (dry run)
    server = LinkedInMCPServer(dry_run=True)
    
    # Show available post types
    print('Available Post Templates:')
    print('-' * 60)
    post_types = ['general', 'service', 'product', 'milestone', 'tip', 'hire']
    for i, post_type in enumerate(post_types, 1):
        print(f'{i}. {post_type.title()}')
    print('-' * 60)
    print('')
    
    # Generate sample posts
    print('Sample Posts:')
    print('=' * 60)
    
    for post_type in post_types:
        print(f'\n--- {post_type.upper()} POST ---\n')
        post = server.create_business_post(post_type)
        print(post)
        print()
    
    print('=' * 60)
    print('Test complete!')
    print('=' * 60)

if __name__ == '__main__':
    main()
