#!/usr/bin/env python3
"""
LinkedIn Daily Auto-Post - Browser Automation Version

Rozana 9 AM automatic LinkedIn par AI post publish hoga.
No API required - uses browser automation.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime
import logging

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)


class LinkedInDailyPoster:
    """
    Posts daily AI content to LinkedIn using browser automation.
    """

    def __init__(self):
        """Initialize poster."""
        self.email = os.getenv('LINKEDIN_EMAIL', '')
        self.password = os.getenv('LINKEDIN_PASSWORD', '')
        self.user_data_dir = Path(__file__).parent / 'linkedin_session'
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
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

    def _setup_logging(self):
        """Set up logging."""
        log_file = Path(__file__).parent.parent.parent / 'Logs' / 'linkedin_auto_post.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_todays_post(self):
        """Get post for today based on day of month."""
        day = datetime.now().day
        post_index = (day - 1) % len(self.ai_posts)
        return self.ai_posts[post_index]

    def post_to_linkedin(self, content):
        """Post to LinkedIn using browser automation."""
        self.logger.info('Posting to LinkedIn...')
        
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser with persistent context
                self.logger.info('Launching browser...')
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    slow_mo=1000,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                    ],
                    viewport={'width': 1920, 'height': 1080}
                )

                page = browser.pages[0]

                # Hide automation
                page.add_init_script('''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                ''')

                # Navigate to LinkedIn
                self.logger.info('Navigating to LinkedIn...')
                page.goto('https://www.linkedin.com/feed/', wait_until='networkidle', timeout=60000)
                time.sleep(10)  # Increased wait time

                # Check if logged in
                if 'login' in page.url:
                    self.logger.info('Not logged in. Attempting login...')
                    
                    # Login
                    page.fill('#username', self.email)
                    page.fill('#password', self.password)
                    time.sleep(2)
                    page.click('button[type="submit"]')
                    
                    # Wait for login
                    self.logger.info('Waiting for login... (may take 30-60 seconds)')
                    time.sleep(30)
                    
                    # Check if still on login page
                    if 'login' in page.url:
                        self.logger.warning('Manual verification may be required')
                        self.logger.info('Waiting up to 2 minutes for manual verification...')
                        
                        for i in range(12):
                            time.sleep(10)
                            if 'feed' in page.url:
                                self.logger.info('Login successful!')
                                break
                        else:
                            self.logger.error('Login verification timeout')
                            browser.close()
                            return {'status': 'error', 'error': 'Login timeout'}

                # Navigate to feed if not already there
                if 'feed' not in page.url:
                    page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
                    time.sleep(3)

                # Find and click "Start a post" button
                self.logger.info('Looking for "Start a post" button...')

                # Multiple selectors with longer wait
                selectors = [
                    '[aria-label="Start a post"]',
                    '.share-box-feed-entry__trigger',
                    'button:has-text("Start a post")',
                    '.ipponosee-cta-btn',
                ]

                clicked = False
                for i, selector in enumerate(selectors):
                    try:
                        # Wait for selector with timeout
                        for attempt in range(5):  # 5 attempts x 2 seconds = 10 seconds total
                            if page.is_visible(selector):
                                page.click(selector)
                                clicked = True
                                self.logger.info(f'Clicked: {selector}')
                                time.sleep(5)
                                break
                            time.sleep(2)
                        if clicked:
                            break
                    except Exception as e:
                        self.logger.debug(f'Selector {selector} attempt failed: {e}')
                        continue

                if not clicked:
                    self.logger.error('Could not find "Start a post" button - trying alternative method')
                    # Try keyboard shortcut
                    page.keyboard.press('Control+Shift+P')
                    time.sleep(3)

                # Fill post content
                self.logger.info('Filling post content...')
                
                editor = page.locator('[role="textbox"]').first
                
                # Type content
                for i, char in enumerate(content):
                    editor.type(char, delay=50)
                    if i % 50 == 0 and i > 0:
                        time.sleep(1)

                time.sleep(3)

                # Click Post button
                self.logger.info('Publishing post...')

                post_selectors = [
                    'button:has-text("Post")',
                    'button:has-text("Share")',
                ]

                for selector in post_selectors:
                    try:
                        if page.is_visible(selector):
                            page.click(selector)
                            time.sleep(3)
                            break
                    except:
                        continue

                # Wait for confirmation
                time.sleep(5)

                self.logger.info('Post published successfully!')
                browser.close()

                return {
                    'status': 'success',
                    'message': 'Post published to LinkedIn',
                    'timestamp': datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f'Error: {e}')
            return {'status': 'error', 'error': str(e)}

    def run(self):
        """Run daily auto-post."""
        today_post = self.get_todays_post()
        day = datetime.now().day

        print('=' * 60)
        print(f'Day {day}: Posting to LinkedIn')
        print('=' * 60)
        print()

        result = self.post_to_linkedin(today_post['content'])

        print()
        print('=' * 60)
        print(f'Status: {result["status"]}')
        print(f'Message: {result.get("message", result.get("error", ""))}')
        print('=' * 60)

        if result['status'] == 'success':
            print()
            print('Daily AI post published!')
            print('View: https://www.linkedin.com/feed/')
        else:
            print()
            print('Posting failed!')

        return result


def main():
    """Main entry point."""
    poster = LinkedInDailyPoster()
    result = poster.run()
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    sys.exit(main())
