#!/usr/bin/env python3
"""
Orchestrator

Master process that monitors the AI Employee vault folders and
triggers Qwen Code to process pending actions.

The orchestrator:
1. Watches /Needs_Action for new action files
2. Triggers Qwen Code to process pending items
3. Generates Plan.md files for action items
4. Monitors /Approved for approved actions to execute
5. Updates Dashboard.md with current status
6. Manages logging and audit trails

Usage:
    python orchestrator.py /path/to/vault [--dev-mode]
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import time

# Import Plan Generator
from plan_generator import PlanGenerator


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.

    Coordinates between watchers, Qwen Code, and action execution.
    """
    
    def __init__(self, vault_path: str, dev_mode: bool = True):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            dev_mode: If True, run in development mode (dry-run for actions)
        """
        self.vault_path = Path(vault_path)
        self.dev_mode = dev_mode
        
        # Core folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.logs = self.vault_path / 'Logs'
        self.inbox = self.vault_path / 'Inbox'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure all folders exist
        for folder in [self.needs_action, self.done, self.plans, 
                       self.pending_approval, self.approved, self.rejected,
                       self.logs, self.inbox]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Initialize Plan Generator
        self.plan_generator = PlanGenerator(str(vault_path))
        
        self.logger.info(f'Orchestrator initialized')
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Dev mode: {dev_mode}')
        
        # Track processed files
        self.processed_files: set = set()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('Orchestrator')
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
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def run(self, check_interval: int = 30) -> None:
        """
        Main orchestration loop.
        
        Args:
            check_interval: Seconds between checks (default: 30)
        """
        self.logger.info('Starting Orchestrator')
        self.logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                self._run_cycle()
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise
    
    def _run_cycle(self) -> None:
        """Run a single orchestration cycle."""
        try:
            # Check for pending actions
            pending_count = self._count_pending()

            if pending_count > 0:
                self.logger.info(f'Found {pending_count} pending item(s)')
                
                # Generate plans for new action files
                plans_created = self._generate_plans()
                if plans_created > 0:
                    self.logger.info(f'Generated {plans_created} new plan(s)')

                # Trigger Qwen Code to process
                self._trigger_qwen()
            
            # Check for approved actions
            approved_files = list(self.approved.glob('*.md'))
            if approved_files:
                self.logger.info(f'Found {len(approved_files)} approved action(s)')
                self._process_approved(approved_files)
            
            # Check for rejected actions
            rejected_files = list(self.rejected.glob('*.md'))
            if rejected_files:
                self.logger.info(f'Found {len(rejected_files)} rejected action(s)')
                self._process_rejected(rejected_files)
            
            # Update dashboard
            self._update_dashboard()
            
        except Exception as e:
            self.logger.error(f'Error in cycle: {e}', exc_info=True)
    
    def _count_pending(self) -> int:
        """Count pending items in Needs_Action."""
        return len(list(self.needs_action.glob('*.md')))

    def _generate_plans(self) -> int:
        """
        Generate Plan.md files for action files without plans.
        
        Returns:
            Number of plans created
        """
        try:
            plans_created = 0
            
            for action_file in self.needs_action.glob('*.md'):
                # Skip if already has a plan
                plan_filename = f'PLAN_{action_file.stem}.md'
                plan_path = self.plans / plan_filename
                
                if plan_path.exists():
                    continue
                
                # Generate plan
                if self.plan_generator.generate_plan(action_file):
                    plans_created += 1
            
            return plans_created
            
        except Exception as e:
            self.logger.error(f'Error generating plans: {e}')
            return 0

    def _trigger_qwen(self) -> None:
        """
        Trigger Qwen Code to process pending items.
        
        In a full implementation, this would call Qwen Code API
        or run qwen-code CLI with appropriate prompts.
        """
        self.logger.info('Triggering Qwen Code processing...')
        
        if self.dev_mode:
            self.logger.info('[DEV MODE] Would trigger Qwen Code')
            self.logger.info('[DEV MODE] Run manually: qwen -c "Process /Needs_Action folder"')
            return
        
        # Full implementation would:
        # 1. Build prompt with pending files
        # 2. Call Qwen Code API or CLI
        # 3. Parse response and create Plan.md files
        # 4. Log the interaction
        
        try:
            # Example: Run qwen-code CLI
            cmd = [
                'qwen',
                '-c',
                f'Process all files in {self.needs_action}. '
                f'Create plans in {self.plans}. '
                f'Require approval for sensitive actions. '
                f'Follow Company_Handbook.md rules.'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            self.logger.info(f'Qwen Code exit code: {result.returncode}')
            
            if result.stdout:
                self.logger.info(f'Qwen output: {result.stdout[:500]}...')
            
        except subprocess.TimeoutExpired:
            self.logger.error('Qwen Code processing timed out')
        except FileNotFoundError:
            self.logger.error('qwen command not found. Install Qwen Code.')
        except Exception as e:
            self.logger.error(f'Error triggering Qwen: {e}')
    
    def _process_approved(self, files: List[Path]) -> None:
        """
        Process approved action files.
        
        Args:
            files: List of approved file paths
        """
        for file_path in files:
            try:
                self.logger.info(f'Processing approved: {file_path.name}')
                
                # Read the file
                content = file_path.read_text()
                
                # Parse frontmatter to determine action type
                action_type = self._extract_frontmatter_value(content, 'action_type')
                
                if self.dev_mode:
                    self.logger.info(f'[DEV MODE] Would execute: {action_type or "unknown"}')
                else:
                    # Execute the action based on type
                    self._execute_action(file_path, content)
                
                # Move to Done
                dest = self.done / file_path.name
                shutil.move(str(file_path), str(dest))
                self.logger.info(f'Moved to Done: {dest.name}')
                
                # Log the action
                self._log_action(file_path.name, action_type, 'approved_executed')
                
            except Exception as e:
                self.logger.error(f'Error processing approved file {file_path.name}: {e}')
    
    def _process_rejected(self, files: List[Path]) -> None:
        """
        Process rejected action files.
        
        Args:
            files: List of rejected file paths
        """
        for file_path in files:
            try:
                self.logger.info(f'Processing rejected: {file_path.name}')
                
                # Log the rejection
                content = file_path.read_text()
                action_type = self._extract_frontmatter_value(content, 'action_type')
                self._log_action(file_path.name, action_type, 'rejected')
                
                # Move to Done (rejected items also go to Done for audit)
                dest = self.done / f'REJECTED_{file_path.name}'
                shutil.move(str(file_path), str(dest))
                self.logger.info(f'Moved to Done: {dest.name}')
                
            except Exception as e:
                self.logger.error(f'Error processing rejected file {file_path.name}: {e}')
    
    def _execute_action(self, file_path: Path, content: str) -> None:
        """
        Execute an approved action.
        
        Args:
            file_path: Path to the action file
            content: File content
        """
        action_type = self._extract_frontmatter_value(content, 'action_type')
        
        if action_type == 'send_email':
            self._execute_send_email(content)
        elif action_type == 'payment':
            self._execute_payment(content)
        elif action_type == 'file_move':
            self._execute_file_move(content)
        else:
            self.logger.warning(f'Unknown action type: {action_type}')
    
    def _execute_send_email(self, content: str) -> None:
        """Execute email send action."""
        # Extract email details from content
        to = self._extract_frontmatter_value(content, 'to')
        subject = self._extract_frontmatter_value(content, 'subject')
        
        self.logger.info(f'Would send email to {to} with subject: {subject}')
        # Full implementation would call email MCP server
    
    def _execute_payment(self, content: str) -> None:
        """Execute payment action."""
        amount = self._extract_frontmatter_value(content, 'amount')
        recipient = self._extract_frontmatter_value(content, 'recipient')
        
        self.logger.info(f'Would process payment: ${amount} to {recipient}')
        # Full implementation would call payment MCP server
    
    def _execute_file_move(self, content: str) -> None:
        """Execute file move action."""
        source = self._extract_frontmatter_value(content, 'source')
        dest = self._extract_frontmatter_value(content, 'destination')
        
        if source and dest:
            src_path = Path(source)
            dst_path = Path(dest)
            if src_path.exists():
                shutil.move(str(src_path), str(dst_path))
                self.logger.info(f'Moved {source} to {dest}')
    
    def _update_dashboard(self) -> None:
        """Update the Dashboard.md with current status."""
        try:
            # Count items in each folder
            needs_action_count = len(list(self.needs_action.glob('*.md')))
            pending_approval_count = len(list(self.pending_approval.glob('*.md')))
            done_today = len([
                f for f in self.done.glob('*.md')
                if self._is_today(f)
            ])

            # Get recent activity
            recent = self._get_recent_activity()

            # Update dashboard
            if self.dashboard.exists():
                # FIX: Explicitly use UTF-8 encoding
                content = self.dashboard.read_text(encoding='utf-8')

                # Update timestamp
                content = self._update_yaml_value(
                    content, 'last_updated', datetime.now().isoformat()
                )

                # Update stats (simple string replacement for Bronze tier)
                content = self._replace_dashboard_value(
                    content, 'Pending Tasks', str(needs_action_count)
                )
                content = self._replace_dashboard_value(
                    content, 'Awaiting Approval', str(pending_approval_count)
                )
                content = self._replace_dashboard_value(
                    content, 'Completed Today', str(done_today)
                )

                # Update folder counts
                content = self._replace_dashboard_value(
                    content, '/Needs_Action', str(needs_action_count),
                    context='| /Needs_Action |'
                )
                content = self._replace_dashboard_value(
                    content, '/Pending_Approval', str(pending_approval_count),
                    context='| /Pending_Approval |'
                )

                self.dashboard.write_text(content, encoding='utf-8')
                self.logger.debug('Dashboard updated')
            
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def _get_recent_activity(self) -> List[Dict[str, str]]:
        """Get recent activity from Done folder."""
        activity = []
        done_files = sorted(
            self.done.glob('*.md'),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:5]  # Last 5 items
        
        for file_path in done_files:
            activity.append({
                'file': file_path.name,
                'time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        
        return activity
    
    def _log_action(self, filename: str, action_type: str, status: str) -> None:
        """
        Log an action to the audit log.
        
        Args:
            filename: Name of the action file
            action_type: Type of action
            status: Action status
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'file': filename,
            'action_type': action_type or 'unknown',
            'status': status,
            'actor': 'orchestrator'
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.json'

        # Read existing logs or create new
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                logs = []
        else:
            logs = []

        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')
    
    @staticmethod
    def _extract_frontmatter_value(content: str, key: str) -> Optional[str]:
        """Extract a value from YAML frontmatter."""
        lines = content.split('\n')
        in_frontmatter = False
        
        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter and line.startswith(f'{key}:'):
                value = line.split(':', 1)[1].strip().strip('"\'')
                return value
        
        return None
    
    @staticmethod
    def _update_yaml_value(content: str, key: str, value: str) -> str:
        """Update a YAML frontmatter value."""
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if line.startswith(f'{key}:'):
                new_lines.append(f'{key}: {value}')
            else:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    @staticmethod
    def _replace_dashboard_value(content: str, label: str, value: str, 
                                  context: str = None) -> str:
        """Replace a value in the dashboard."""
        if context:
            # Replace within specific context
            old_pattern = f'{context} {value}'
            new_pattern = f'{context} {value}'
            if context in content:
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if context in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            parts[-2] = f' {value} '
                            line = '|'.join(parts)
                    new_lines.append(line)
                return '\n'.join(new_lines)
        
        return content
    
    @staticmethod
    def _is_today(file_path: Path) -> bool:
        """Check if file was modified today."""
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.date() == datetime.now().date()


def main():
    """Main entry point for the orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='AI Employee Orchestrator'
    )
    parser.add_argument(
        'vault_path',
        help='Path to the Obsidian vault root'
    )
    parser.add_argument(
        '--dev-mode',
        action='store_true',
        default=True,  # Default to dev mode for safety
        help='Run in development mode (dry-run for actions)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Validate vault path
    if not Path(args.vault_path).exists():
        print(f'Error: Vault path does not exist: {args.vault_path}')
        sys.exit(1)
    
    # Create and run orchestrator
    orchestrator = Orchestrator(args.vault_path, dev_mode=args.dev_mode)
    orchestrator.run(check_interval=args.interval)


if __name__ == '__main__':
    main()
