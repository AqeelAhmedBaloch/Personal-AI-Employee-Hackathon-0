#!/usr/bin/env python3
"""
CEO Briefing Generator

Autonomous weekly business audit that generates "Monday Morning CEO Briefing" reports.
Runs every Sunday night via Task Scheduler.

Features:
- Revenue tracking from bank transactions
- Completed tasks analysis
- Bottleneck identification
- Subscription audit
- Proactive suggestions

Usage:
    python ceo_briefing.py /path/to/vault
"""

import sys
import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import csv


class CEOBriefingGenerator:
    """
    Generates weekly CEO Briefing reports with business insights.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize CEO Briefing Generator.
        
        Args:
            vault_path: Path to Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.business_goals = self.vault_path / 'Business_Goals.md'
        self.briefings_folder = self.vault_path / 'Briefings'
        self.logs_folder = self.vault_path / 'Logs'
        self.done_folder = self.vault_path / 'Done'
        self.accounting_folder = self.vault_path / 'Accounting'
        
        # Ensure folders exist
        self.briefings_folder.mkdir(parents=True, exist_ok=True)
        self.accounting_folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Subscription patterns for audit
        self.subscription_patterns = {
            'netflix.com': 'Netflix',
            'spotify.com': 'Spotify',
            'adobe.com': 'Adobe Creative Cloud',
            'notion.so': 'Notion',
            'slack.com': 'Slack',
            'zoom.us': 'Zoom',
            'microsoft.com': 'Microsoft 365',
            'github.com': 'GitHub',
            'aws.amazon.com': 'Amazon Web Services',
            'heroku.com': 'Heroku',
        }
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        self.logger = logging.getLogger('CEOBriefingGenerator')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def _parse_business_goals(self) -> Dict[str, Any]:
        """
        Parse Business_Goals.md to extract targets and metrics.
        
        Returns:
            Dictionary with business goals and targets
        """
        goals = {
            'revenue_target': 10000,  # Default $10,000
            'active_projects': [],
            'subscription_rules': []
        }
        
        if not self.business_goals.exists():
            self.logger.warning("Business_Goals.md not found, using defaults")
            return goals
        
        content = self.business_goals.read_text(encoding='utf-8')
        
        # Extract revenue target
        revenue_match = re.search(r'Monthly goal:?\s*\$?([\d,]+)', content)
        if revenue_match:
            goals['revenue_target'] = float(revenue_match.group(1).replace(',', ''))
        
        # Extract current MTD
        mtd_match = re.search(r'Current MTD:?\s*\$?([\d,]+)', content)
        if mtd_match:
            goals['revenue_mtd'] = float(mtd_match.group(1).replace(',', ''))
        else:
            goals['revenue_mtd'] = 0
        
        # Extract active projects
        project_pattern = r'(\d+)\.\s*(Project \w+).*?Due\s+([\w\s\d,]+).*?Budget\s*\$?([\d,]+)'
        for match in re.finditer(project_pattern, content):
            goals['active_projects'].append({
                'id': match.group(1),
                'name': match.group(2),
                'due': match.group(3),
                'budget': float(match.group(4).replace(',', ''))
            })
        
        return goals
    
    def _analyze_completed_tasks(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Analyze completed tasks from the past week.
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of completed tasks with metadata
        """
        completed_tasks = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        if not self.done_folder.exists():
            return completed_tasks
        
        # Scan Done folder for markdown files
        for file in self.done_folder.glob('*.md'):
            try:
                content = file.read_text(encoding='utf-8')
                
                # Try to extract date from filename or content
                file_date = datetime.fromtimestamp(file.stat().st_mtime)
                
                if file_date >= cutoff_date:
                    completed_tasks.append({
                        'file': file.name,
                        'date': file_date,
                        'type': self._extract_task_type(content)
                    })
            except Exception as e:
                self.logger.debug(f"Error reading {file.name}: {e}")
        
        return completed_tasks
    
    def _extract_task_type(self, content: str) -> str:
        """Extract task type from markdown content."""
        if 'type: email' in content.lower():
            return 'Email'
        elif 'type: file_drop' in content.lower():
            return 'File'
        elif 'invoice' in content.lower():
            return 'Invoice'
        elif 'payment' in content.lower():
            return 'Payment'
        else:
            return 'General'
    
    def _analyze_subscriptions(self) -> List[Dict[str, Any]]:
        """
        Analyze bank transactions for subscription audit.
        
        Returns:
            List of subscriptions found with status
        """
        subscriptions_found = []
        
        # Look for transaction logs
        transaction_files = list(self.logs_folder.glob('transactions_*.csv'))
        transaction_files.extend(self.accounting_folder.glob('*.md'))
        
        for file in transaction_files:
            try:
                if file.suffix == '.csv':
                    with open(file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            subscription = self._check_subscription(row.get('description', ''))
                            if subscription:
                                subscriptions_found.append(subscription)
                else:
                    content = file.read_text(encoding='utf-8')
                    for line in content.split('\n'):
                        subscription = self._check_subscription(line)
                        if subscription:
                            subscriptions_found.append(subscription)
            except Exception as e:
                self.logger.debug(f"Error analyzing {file.name}: {e}")
        
        return subscriptions_found
    
    def _check_subscription(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Check if text contains a subscription payment.
        
        Args:
            text: Transaction description
            
        Returns:
            Subscription info if found, None otherwise
        """
        text_lower = text.lower()
        
        for pattern, name in self.subscription_patterns.items():
            if pattern in text_lower:
                # Try to extract amount
                amount_match = re.search(r'\$?([\d.]+)', text)
                amount = float(amount_match.group(1)) if amount_match else 0
                
                return {
                    'name': name,
                    'pattern': pattern,
                    'amount': amount,
                    'source': text
                }
        
        return None
    
    def _identify_bottlenecks(self, completed_tasks: List[Dict]) -> List[Dict[str, Any]]:
        """
        Identify bottlenecks from task completion patterns.
        
        Args:
            completed_tasks: List of completed tasks
            
        Returns:
            List of identified bottlenecks
        """
        bottlenecks = []
        
        # Count tasks by type
        type_counts = {}
        for task in completed_tasks:
            task_type = task.get('type', 'Unknown')
            type_counts[task_type] = type_counts.get(task_type, 0) + 1
        
        # Identify potential bottlenecks
        total_tasks = len(completed_tasks)
        for task_type, count in type_counts.items():
            if total_tasks > 5:  # Only analyze if enough data
                percentage = (count / total_tasks) * 100
                if percentage > 40:  # More than 40% of tasks are this type
                    bottlenecks.append({
                        'type': task_type,
                        'count': count,
                        'percentage': percentage,
                        'issue': f'{task_type} tasks dominating workflow ({percentage:.1f}%)'
                    })
        
        return bottlenecks
    
    def _generate_briefing(self) -> str:
        """
        Generate the complete CEO Briefing report.
        
        Returns:
            Markdown content for the briefing
        """
        # Get business goals
        goals = self._parse_business_goals()
        
        # Analyze completed tasks
        completed_tasks = self._analyze_completed_tasks(days_back=7)
        
        # Analyze subscriptions
        subscriptions = self._analyze_subscriptions()
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(completed_tasks)
        
        # Calculate metrics
        revenue_mtd = goals.get('revenue_mtd', 0)
        revenue_target = goals.get('revenue_target', 10000)
        revenue_percentage = (revenue_mtd / revenue_target * 100) if revenue_target > 0 else 0
        
        # Determine trend
        if revenue_percentage >= 80:
            trend = "On track"
        elif revenue_percentage >= 50:
            trend = "Behind but recoverable"
        else:
            trend = "Significantly behind"
        
        # Generate date info
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        # Build briefing content
        briefing = f"""---
generated: {today.isoformat()}
period: {week_start.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}
type: ceo_briefing
---

# Monday Morning CEO Briefing

**Generated:** {today.strftime('%A, %B %d, %Y at %I:%M %p')}

**Period:** Week of {week_start.strftime('%B %d, %Y')}

---

## Executive Summary

{self._generate_executive_summary(revenue_percentage, trend, len(completed_tasks), len(bottlenecks))}

---

## Revenue Tracking

| Metric | Value |
|--------|-------|
| **This Week** | ${revenue_mtd:,.2f} |
| **MTD (Month-to-Date)** | ${revenue_mtd:,.2f} |
| **Monthly Target** | ${revenue_target:,.2f} |
| **Progress** | {revenue_percentage:.1f}% |
| **Trend** | {trend} |

### Revenue Trend
{"✅ On track to meet monthly goal" if revenue_percentage >= 80 else "⚠️ Need to accelerate revenue generation" if revenue_percentage >= 50 else "🚨 Critical: Significant revenue gap identified"}

---

## Completed Tasks

**Total Tasks Completed:** {len(completed_tasks)}

### By Type
| Type | Count |
|------|-------|
"""
        
        # Add task type breakdown
        type_counts = {}
        for task in completed_tasks:
            task_type = task.get('type', 'Unknown')
            type_counts[task_type] = type_counts.get(task_type, 0) + 1
        
        for task_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            briefing += f"| {task_type} | {count} |\n"
        
        briefing += f"""
### Recent Activity
"""
        
        # List recent tasks
        for task in completed_tasks[:10]:  # Show last 10
            briefing += f"- [x] {task['file']} ({task['date'].strftime('%Y-%m-%d')})\n"
        
        briefing += f"""
---

## Bottlenecks Identified

"""
        
        if bottlenecks:
            briefing += """| Issue | Impact | Recommendation |
|-------|--------|----------------|
"""
            for bottleneck in bottlenecks:
                briefing += f"| {bottleneck['issue']} | High | Consider automation or delegation |\n"
        else:
            briefing += "*No significant bottlenecks identified this week.* ✅\n"
        
        briefing += f"""
---

## Subscription Audit

"""
        
        if subscriptions:
            briefing += """| Subscription | Monthly Cost | Status |
|--------------|--------------|--------|
"""
            total_subscriptions = 0
            for sub in subscriptions:
                briefing += f"| {sub['name']} | ${sub['amount']:.2f} | Active |\n"
                total_subscriptions += sub['amount']
            
            briefing += f"| **Total** | **${total_subscriptions:.2f}/month** | |\n"
            
            # Add proactive suggestions
            briefing += f"""
### Cost Optimization Suggestions

Based on your subscription analysis:

"""
            for sub in subscriptions:
                if sub['amount'] > 50:
                    briefing += f"- **{sub['name']}** (${sub['amount']:.2f}/mo): Review usage and consider downgrade if underutilized\n"
        else:
            briefing += "*No subscription transactions detected in logs.*\n"
        
        briefing += f"""
---

## Active Projects

"""
        
        for project in goals.get('active_projects', []):
            briefing += f"""### {project['name']}
- **Due:** {project['due']}
- **Budget:** ${project['budget']:,.2f}
- **Status:** In Progress

"""
        
        briefing += f"""
---

## Proactive Suggestions

{self._generate_suggestions(subscriptions, bottlenecks, revenue_percentage)}

---

## Upcoming Deadlines

"""
        
        # Add upcoming deadlines from projects
        for project in goals.get('active_projects', []):
            briefing += f"- ⏰ {project['name']} due: {project['due']}\n"
        
        briefing += f"""
---

## Action Items for This Week

1. [ ] Review subscription costs and identify cancellation opportunities
2. [ ] Address identified bottlenecks
3. [ ] Check active project progress
4. [ ] Respond to any pending approvals in /Pending_Approval

---

*Briefing generated automatically by Personal AI Employee Hackathon-0 CEO Briefing Generator v1.0*

**Next Briefing:** {today.strftime('%A, %B %d, %Y')} at 8:00 AM
"""
        
        return briefing
    
    def _generate_executive_summary(self, revenue_pct: float, trend: str, tasks_completed: int, bottlenecks_count: int) -> str:
        """Generate executive summary based on metrics."""
        summaries = []
        
        if revenue_pct >= 80:
            summaries.append(f"Strong performance with revenue at {revenue_pct:.1f}% of target.")
        elif revenue_pct >= 50:
            summaries.append(f"Moderate performance with revenue at {revenue_pct:.1f}% of target. Acceleration needed.")
        else:
            summaries.append(f"Revenue concern at {revenue_pct:.1f}% of target. Immediate action required.")
        
        if tasks_completed > 20:
            summaries.append(f"High productivity with {tasks_completed} tasks completed.")
        elif tasks_completed > 10:
            summaries.append(f"Steady progress with {tasks_completed} tasks completed.")
        else:
            summaries.append(f"Low activity with only {tasks_completed} tasks completed.")
        
        if bottlenecks_count > 0:
            summaries.append(f"{bottlenecks_count} bottleneck(s) identified requiring attention.")
        else:
            summaries.append("No significant bottlenecks detected.")
        
        return " ".join(summaries)
    
    def _generate_suggestions(self, subscriptions: List, bottlenecks: List, revenue_pct: float) -> str:
        """Generate proactive suggestions."""
        suggestions = []
        
        # Subscription suggestions
        expensive_subs = [s for s in subscriptions if s['amount'] > 50]
        if expensive_subs:
            suggestions.append(f"### Cost Reduction\nReview {len(expensive_subs)} expensive subscription(s) for potential cancellation or downgrade.\n")
        
        # Bottleneck suggestions
        if bottlenecks:
            suggestions.append("### Process Improvement\nConsider automating recurring task types to reduce bottlenecks.\n")
        
        # Revenue suggestions
        if revenue_pct < 50:
            suggestions.append("### Revenue Generation\nFocus on high-value activities to improve revenue trajectory.\n")
        
        if not suggestions:
            return "*No critical suggestions at this time. Operations running smoothly.* ✅"
        
        return "\n".join(suggestions)
    
    def run(self) -> Path:
        """
        Run the CEO Briefing Generator.
        
        Returns:
            Path to generated briefing file
        """
        self.logger.info("Starting CEO Briefing Generation...")
        
        # Generate briefing
        briefing_content = self._generate_briefing()
        
        # Save to file
        today = datetime.now()
        filename = f"{today.strftime('%Y-%m-%d')}_Monday_Briefing.md"
        filepath = self.briefings_folder / filename
        
        filepath.write_text(briefing_content, encoding='utf-8')
        
        self.logger.info(f"CEO Briefing generated: {filepath}")
        self.logger.info(f"File size: {filepath.stat().st_size} bytes")
        
        return filepath


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python ceo_briefing.py /path/to/vault")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create generator
    generator = CEOBriefingGenerator(vault_path)
    
    print("=" * 60)
    print('Personal AI Employee Hackathon-0 - CEO Briefing Generator')
    print("=" * 60)
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Vault: {vault_path}')
    print('')
    
    # Generate briefing
    filepath = generator.run()
    
    print('')
    print('=' * 60)
    print(f'✓ CEO Briefing generated successfully!')
    print(f'  File: {filepath}')
    print('=' * 60)


if __name__ == '__main__':
    main()
