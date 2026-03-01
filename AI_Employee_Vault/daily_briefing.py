#!/usr/bin/env python3
"""
Daily Briefing Generator

Generates daily briefing reports for the AI Employee.
Runs every day at 8:00 AM via Task Scheduler.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


class DailyBriefing:
    """
    Generates daily briefing reports.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize daily briefing generator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.done = self.vault_path / 'Done'
        self.briefings = self.vault_path / 'Briefings'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure Briefings folder exists
        self.briefings.mkdir(parents=True, exist_ok=True)
    
    def generate_briefing(self, date: datetime = None) -> Path:
        """
        Generate daily briefing for specified date.
        
        Args:
            date: Date for briefing (default: today)
            
        Returns:
            Path to generated briefing file
        """
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y-%m-%d')
        day_name = date.strftime('%A')
        
        # Get yesterday's date range
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)
        
        # Count completed tasks
        completed_tasks = self._count_completed_tasks(start_of_day, end_of_day)
        
        # Get activity summary
        activity_summary = self._get_activity_summary()
        
        # Get pending items
        pending_items = self._get_pending_items()
        
        # Generate briefing content
        content = self._create_briefing_content(
            date=date,
            day_name=day_name,
            completed_tasks=completed_tasks,
            activity_summary=activity_summary,
            pending_items=pending_items
        )
        
        # Save briefing
        filename = f'{date_str}_{day_name}_Briefing.md'
        filepath = self.briefings / filename
        filepath.write_text(content, encoding='utf-8')
        
        print(f'[OK] Daily briefing generated: {filename}')
        return filepath
    
    def _count_completed_tasks(self, start: datetime, end: datetime) -> Dict:
        """Count tasks completed in time range."""
        completed = {
            'total': 0,
            'files': []
        }
        
        for file in self.done.glob('*.md'):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if start <= mtime < end:
                completed['total'] += 1
                completed['files'].append({
                    'name': file.name,
                    'time': mtime.strftime('%H:%M')
                })
        
        return completed
    
    def _get_activity_summary(self) -> Dict:
        """Get summary of recent activity."""
        summary = {
            'total_actions': 0,
            'by_type': {}
        }
        
        # Count from logs
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
                summary['total_actions'] = len(logs)
                
                for log in logs:
                    action_type = log.get('action_type', 'unknown')
                    summary['by_type'][action_type] = summary['by_type'].get(action_type, 0) + 1
                    
            except (json.JSONDecodeError, Exception):
                pass
        
        return summary
    
    def _get_pending_items(self) -> Dict:
        """Get count of pending items."""
        pending = {
            'needs_action': 0,
            'pending_approval': 0,
            'approved': 0
        }
        
        pending['needs_action'] = len(list((self.vault_path / 'Needs_Action').glob('*.md')))
        pending['pending_approval'] = len(list((self.vault_path / 'Pending_Approval').glob('*.md')))
        pending['approved'] = len(list((self.vault_path / 'Approved').glob('*.md')))
        
        return pending
    
    def _create_briefing_content(
        self,
        date: datetime,
        day_name: str,
        completed_tasks: Dict,
        activity_summary: Dict,
        pending_items: Dict
    ) -> str:
        """Create briefing markdown content."""
        
        date_str = date.strftime('%Y-%m-%d')
        
        # Build completed tasks list
        tasks_list = ''
        if completed_tasks['files']:
            for task in completed_tasks['files'][-10:]:  # Last 10 tasks
                tasks_list += f'- [x] {task["name"]} ({task["time"]})\n'
        else:
            tasks_list = '*No tasks completed yet*\n'
        
        # Build activity summary
        activity_text = ''
        for action_type, count in activity_summary['by_type'].items():
            activity_text += f'- **{action_type.replace("_", " ").title()}:** {count}\n'
        
        if not activity_text:
            activity_text = '*No activity logged*\n'
        
        content = f'''---
generated: {datetime.now().isoformat()}
date: {date_str}
day: {day_name}
period: {date_str} 00:00 to {date_str} 23:59
---

# Daily Briefing - {day_name}, {date_str}

## Executive Summary

Good morning! Here's your AI Employee daily briefing.

---

## Completed Tasks (Today)

**Total:** {completed_tasks['total']} tasks

{tasks_list}

---

## Activity Summary

**Total Actions:** {activity_summary['total_actions']}

{activity_text}

---

## Current Status

| Category | Count |
|----------|-------|
| Needs Action | {pending_items['needs_action']} |
| Pending Approval | {pending_items['pending_approval']} |
| Approved (Ready) | {pending_items['approved']} |

---

## Priorities for Today

1. Review pending approvals in `/Pending_Approval`
2. Process items in `/Needs_Action`
3. Execute approved actions in `/Approved`

---

## Notes

Add your notes, priorities, or focus areas for today:

---

*Generated by AI Employee Daily Briefing v0.1 (Silver Tier)*
'''
        
        return content


def main():
    """Main entry point for daily briefing generator."""
    if len(sys.argv) < 2:
        print('Usage: python daily_briefing.py <vault_path>')
        print('')
        print('Example:')
        print('  python daily_briefing.py "./AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create generator
    generator = DailyBriefing(vault_path)
    
    print('=' * 50)
    print('AI Employee - Daily Briefing Generator')
    print('=' * 50)
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Vault: {vault_path}')
    print('')
    
    # Generate briefing
    generator.generate_briefing()
    
    print('')
    print('=' * 50)
    print('Briefing complete!')
    print('=' * 50)


if __name__ == '__main__':
    main()
