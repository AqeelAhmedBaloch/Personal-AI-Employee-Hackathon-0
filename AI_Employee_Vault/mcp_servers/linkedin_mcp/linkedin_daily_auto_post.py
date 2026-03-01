#!/usr/bin/env python3
"""
LinkedIn Daily AI Post - Auto Scheduler

Posts daily about AI topics to LinkedIn.
Run this once via Task Scheduler - will post automatically every day.

Setup:
1. Configure .env with LinkedIn API credentials
2. Schedule via Windows Task Scheduler (daily at 9 AM)
3. Done! Posts will be automatic
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInDailyAIposter:
    """
    Posts daily AI content to LinkedIn automatically.
    """
    
    def __init__(self):
        """Initialize poster."""
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        self.person_urn = os.getenv('LINKEDIN_PERSON_URN', '')
        self.api_base = 'https://api.linkedin.com/v2'
        
        # 30 days of AI content
        self.ai_posts = [
            {
                'day': 1,
                'content': '''🚀 AI is transforming how we work!

Our AI Employee system can now:
✅ Auto-reply to emails
✅ Monitor files and folders
✅ Create action plans
✅ Manage approvals

The future of work is here!

#AI #Automation #FutureOfWork #Productivity #Innovation'''
            },
            {
                'day': 2,
                'content': '''💡 Did You Know?

AI can process emails 10x faster than humans!

Our AI Employee:
- Reads incoming emails
- Categorizes by priority
- Drafts appropriate replies
- Learns from your responses

Work smarter, not harder!

#AI #EmailAutomation #Productivity #SmartWork'''
            },
            {
                'day': 3,
                'content': '''🎯 Monday Motivation!

"Automation is not about replacing people. It's about empowering them to do their best work."

Our AI Employee handles routine tasks so you can focus on:
✅ Strategy
✅ Creativity
✅ Growth

#MondayMotivation #AI #Leadership #Growth'''
            },
            {
                'day': 4,
                'content': '''📊 AI Tip of the Day!

Start small with automation:

1️⃣ Automate email replies
2️⃣ Auto-sort files
3️⃣ Schedule meetings automatically
4️⃣ Track tasks automatically

Small steps = Big results!

#AITips #Automation #Productivity #Success'''
            },
            {
                'day': 5,
                'content': '''🌟 Success Story!

This week our AI Employee:
✅ Processed 50+ emails
✅ Created 20+ action plans
✅ Saved 15+ hours of manual work
✅ Zero errors

That's the power of AI!

#SuccessStory #AI #Results #ROI #Automation'''
            },
            {
                'day': 6,
                'content': '''🔍 What is MCP?

Model Context Protocol (MCP) connects AI to:
✅ Email servers
✅ File systems
✅ Calendars
✅ Payment systems

It's the bridge between AI and real-world tools!

#MCP #AI #Technology #Integration'''
            },
            {
                'day': 7,
                'content': '''📚 Sunday Learning!

AI Terms You Should Know:

🤖 LLM - Large Language Model
🔗 API - Application Programming Interface
⚡ Automation - Automatic task execution
📊 Orchestrator - Coordinates AI actions

Knowledge is power!

#SundayLearning #AI #Education #TechTerms'''
            },
            {
                'day': 8,
                'content': '''🚀 New Week, New Possibilities!

This week with AI Employee:
✅ Zero missed emails
✅ All tasks tracked automatically
✅ 20+ hours saved
✅ 100% consistency

What will YOU achieve this week?

#MondayMotivation #AI #Goals #Success'''
            },
            {
                'day': 9,
                'content': '''💼 Business + AI = Success!

Companies using AI see:
📈 40% increase in productivity
💰 35% cost reduction
⏰ 25% time savings
😊 Higher employee satisfaction

The data is clear!

#BusinessAI #ROI #Productivity #Data'''
            },
            {
                'day': 10,
                'content': '''🎯 AI Myth vs Reality!

Myth: AI will replace all jobs
Reality: AI augments human capabilities

Myth: AI is too complex
Reality: Modern AI is user-friendly

Myth: AI is expensive
Reality: AI saves money long-term

#AIMyths #Facts #Education #Truth'''
            },
            {
                'day': 11,
                'content': '''⚡ Quick Win!

Automate these TODAY:
✅ Email responses to common questions
✅ File organization
✅ Meeting scheduling
✅ Task reminders

30 minutes setup = Hours saved daily!

#QuickWin #AI #TimeManagement #Efficiency'''
            },
            {
                'day': 12,
                'content': '''🌟 Feature Friday!

AI Employee Capabilities:

📧 Gmail Integration
📁 File System Monitoring
📋 Plan Generation
✅ Approval Workflows
📊 Daily Briefings
⏰ Task Scheduling

One system, endless possibilities!

#FeatureFriday #AI #Capabilities #Tech'''
            },
            {
                'day': 13,
                'content': '''📖 Saturday Story!

How AI Employee helps professionals:

Before AI:
❌ 100+ emails daily
❌ Missed important messages
❌ Manual file organization
❌ 60+ hour work weeks

After AI:
✅ Auto-prioritized emails
✅ Zero missed messages
✅ Automatic organization
✅ 40 hour work weeks

#Transformation #AI #WorkLifeBalance'''
            },
            {
                'day': 14,
                'content': '''🎉 Milestone Achieved!

Our AI Employee just completed:
✅ 1000+ emails processed
✅ 500+ action plans created
✅ 200+ hours saved
✅ 99.9% accuracy

Thank you for being part of this journey!

#Milestone #AI #Success #Grateful'''
            },
            {
                'day': 15,
                'content': '''🚀 The Future is Here!

AI in 2026:
✅ Natural language understanding
✅ Multi-step task completion
✅ Human-AI collaboration
✅ Ethical AI practices

We're living in the future!

#FutureTech #AI #2026 #Innovation'''
            },
            {
                'day': 16,
                'content': '''💡 Innovation Insight!

What makes AI Employee different?

🎯 Local-first architecture
🔒 Privacy-focused design
✅ Human-in-the-loop control
📊 Transparent decision-making
🔄 Continuous learning

Built for trust, designed for results!

#Innovation #AI #Privacy #Trust'''
            },
            {
                'day': 17,
                'content': '''📊 Monday Metrics!

AI Employee by the numbers:

⏱️ Average response time: < 1 second
📧 Emails processed daily: 50+
📋 Plans generated: 20+
💼 Hours saved weekly: 15+
🎯 Accuracy rate: 99%+

Numbers don't lie!

#MondayMetrics #AI #Data #Results'''
            },
            {
                'day': 18,
                'content': '''🔐 Security First!

How we protect your data:

✅ Local storage (your control)
✅ Encrypted credentials
✅ No data sharing
✅ Audit logging
✅ Human approval for sensitive actions

Your data, your rules!

#Security #Privacy #AI #DataProtection'''
            },
            {
                'day': 19,
                'content': '''🎓 AI Learning Path!

Want to start with AI?

1️⃣ Understand the basics
2️⃣ Identify automatable tasks
3️⃣ Start with one workflow
4️⃣ Expand gradually
5️⃣ Measure results

Journey of 1000 miles begins with one step!

#Learning #AI #Growth #Journey'''
            },
            {
                'day': 20,
                'content': '''🌟 Transformation Thursday!

From manual to automatic:

Email Management:
❌ Manual sorting → ✅ Auto-categorization
❌ Manual replies → ✅ Auto-responses
❌ Missed emails → ✅ Zero inbox

Small change, big impact!

#Transformation #AI #EmailManagement'''
            },
            {
                'day': 21,
                'content': '''💼 Professional's Guide to AI!

Top 5 tasks to automate FIRST:

1. Email responses
2. File organization
3. Meeting scheduling
4. Task tracking
5. Daily reports

Start here for maximum ROI!

#ProfessionalTips #AI #Automation #ROI'''
            },
            {
                'day': 22,
                'content': '''🎯 Focus Friday!

What AI Employee handles so you don't have to:

✅ Reading every email
✅ Sorting files manually
✅ Tracking every task
✅ Writing routine responses
✅ Scheduling meetings

Focus on what matters MOST!

#FocusFriday #AI #Priorities #Success'''
            },
            {
                'day': 23,
                'content': '''📈 Growth Mindset!

AI adoption stages:

🌱 Awareness → Learn about AI
🌿 Interest → Explore possibilities
🌳 Trial → Test one workflow
🌲 Integration → Expand usage
🏆 Mastery → Full automation

Where are you in this journey?

#GrowthMindset #AI #Journey #Development'''
            },
            {
                'day': 24,
                'content': '''⚡ Power Tip!

Combine AI tools for maximum impact:

AI Employee + Calendar = Smart scheduling
AI Employee + Email = Auto-replies
AI Employee + Files = Auto-organization
AI Employee + Tasks = Auto-tracking

Synergy is key!

#PowerTip #AI #Integration #Synergy'''
            },
            {
                'day': 25,
                'content': '''🎉 Weekend Wisdom!

"The best time to automate was yesterday. The second best time is now."

Don't wait for perfection:
✅ Start today
✅ Learn as you go
✅ Improve continuously

Action beats perfection!

#WeekendWisdom #AI #Action #Motivation'''
            },
            {
                'day': 26,
                'content': '''🚀 Sunday Success!

This week's AI wins:

✅ 60+ emails auto-processed
✅ 25+ plans auto-generated
✅ 18+ hours saved
✅ 100% task completion

Ready for an even better week!

#SundaySuccess #AI #Wins #Productivity'''
            },
            {
                'day': 27,
                'content': '''💡 Monday Inspiration!

AI is not your replacement.
AI is your amplification.

It amplifies your:
✅ Productivity
✅ Creativity
✅ Decision-making
✅ Impact

Be the conductor, let AI be the orchestra!

#MondayInspiration #AI #Leadership #Vision'''
            },
            {
                'day': 28,
                'content': '''📊 Tech Tuesday!

Behind the scenes of AI Employee:

🧠 Reasoning: Qwen Code
📁 Memory: Obsidian Vault
👀 Perception: Python Watchers
🤝 Action: MCP Servers
⚙️ Coordination: Orchestrator

Beautiful architecture!

#TechTuesday #AI #Architecture #Engineering'''
            },
            {
                'day': 29,
                'content': '''🎯 Workflow Wednesday!

Perfect AI workflow:

1. Watcher detects new input
2. Orchestrator creates plan
3. AI processes the task
4. Human approves (if needed)
5. Action executes
6. Result logged

Simple, elegant, effective!

#WorkflowWednesday #AI #Process #Efficiency'''
            },
            {
                'day': 30,
                'content': '''🌟 Month in Review!

30 days of AI content:

✅ 30 posts created
✅ Countless insights shared
✅ Community engaged
✅ Future of work discussed

Thank you for following this journey!

Here's to many more innovations! 🚀

#MonthInReview #AI #Community #Grateful #Innovation'''
            }
        ]
    
    def get_todays_post(self):
        """
        Get post for today based on day of month.
        
        Returns:
            Post content for today
        """
        day = datetime.now().day
        # Get post for today's day (1-30)
        # If day > 30, loop back to start
        post_index = (day - 1) % len(self.ai_posts)
        return self.ai_posts[post_index]
    
    def post_to_linkedin(self, content):
        """
        Post content to LinkedIn via API.
        
        Args:
            content: Post content
            
        Returns:
            Result dictionary
        """
        if not self.access_token:
            return {
                'status': 'error',
                'error': 'Access token not configured'
            }
        
        # Get person URN if not set
        person_urn = self.person_urn
        if not person_urn:
            try:
                person_urn = f'urn:li:person:{self._get_person_id()}'
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
        
        try:
            response = requests.post(url, headers=headers, json=post_data)
            
            if response.status_code == 201:
                result = response.json()
                return {
                    'status': 'success',
                    'post_id': result.get('id'),
                    'message': 'Post published successfully!',
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'error': f'API Error: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_person_id(self):
        """Get LinkedIn person ID."""
        url = f'{self.api_base}/me'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        return result['id']
    
    def run(self):
        """
        Run daily auto-post.
        
        Returns:
            Result dictionary
        """
        # Get today's post
        today_post = self.get_todays_post()
        day = datetime.now().day
        
        print(f'Day {day}: Posting to LinkedIn...')
        
        # Post to LinkedIn
        result = self.post_to_linkedin(today_post['content'])
        
        return result


def main():
    """Main entry point."""
    print('=' * 60)
    print('LinkedIn Daily AI Auto-Post')
    print('=' * 60)
    print('')
    
    # Create poster
    poster = LinkedInDailyAIposter()
    
    # Run auto-post
    result = poster.run()
    
    # Show result
    print('')
    print('=' * 60)
    print(f'Status: {result["status"]}')
    print(f'Message: {result.get("message", result.get("error", ""))}')
    
    if result['status'] == 'success':
        print('')
        print('✅ Daily AI post published!')
        print('')
        print('View your post:')
        print('https://www.linkedin.com/feed/')
    else:
        print('')
        print('❌ Posting failed!')
        if 'details' in result:
            print(f'Details: {result["details"]}')
    
    print('=' * 60)
    
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
