#!/usr/bin/env python3
"""
Plan Generator

Generates Plan.md files for action items in Needs_Action folder.
Creates step-by-step checklists for Qwen Code to follow.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class PlanGenerator:
    """
    Generates Plan.md files for action items.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the plan generator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        
        # Ensure Plans folder exists
        self.plans.mkdir(parents=True, exist_ok=True)
        
        # Action type to steps mapping
        self.action_templates = self._load_action_templates()
    
    def _load_action_templates(self) -> Dict[str, List[str]]:
        """Load action templates for different action types."""
        return {
            'file_drop': [
                'Review file contents and understand purpose',
                'Categorize file (document, invoice, receipt, etc.)',
                'Extract key information (dates, amounts, names)',
                'Determine required action',
                'Execute action or request approval',
                'Log action and move to Done'
            ],
            'email': [
                'Read email content and identify sender',
                'Check if sender is in contacts',
                'Identify email type (inquiry, invoice, urgent, etc.)',
                'Draft appropriate response',
                'Check if response requires approval',
                'Send email or request approval',
                'Archive email and log action'
            ],
            'whatsapp': [
                'Read message and identify sender',
                'Check for keywords (urgent, invoice, payment, help)',
                'Determine message priority',
                'Draft appropriate response',
                'Check if response requires approval',
                'Send message or request approval',
                'Log conversation'
            ],
            'payment': [
                'Identify payment details (amount, recipient, reference)',
                'Verify payment against invoices',
                'Check payment threshold (auto-approve < $50)',
                'Create approval request if needed',
                'Process payment after approval',
                'Log transaction in accounting',
                'Move to Done'
            ],
            'invoice': [
                'Identify client details',
                'Calculate amount based on rates',
                'Generate invoice PDF',
                'Review invoice for accuracy',
                'Send invoice via email (requires approval)',
                'Log transaction',
                'Move to Done'
            ],
            'social_media': [
                'Identify platform (LinkedIn, Twitter, Facebook)',
                'Review content for posting',
                'Check content against company guidelines',
                'Schedule post or request approval',
                'Post content after approval',
                'Log post and engagement',
                'Move to Done'
            ],
            'default': [
                'Review action item details',
                'Identify required steps',
                'Check Company Handbook for rules',
                'Determine if approval is needed',
                'Execute action or create approval request',
                'Log action taken',
                'Move to Done when complete'
            ]
        }
    
    def generate_plan(self, action_file: Path) -> Optional[Path]:
        """
        Generate a Plan.md file for an action item.
        
        Args:
            action_file: Path to the action file
            
        Returns:
            Path to the created Plan.md file, or None if failed
        """
        try:
            # Read action file
            content = action_file.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = self._extract_metadata(content)
            action_type = metadata.get('type', 'default')
            
            # Get steps for this action type
            steps = self.action_templates.get(
                action_type, 
                self.action_templates['default']
            )
            
            # Generate plan content
            plan_content = self._create_plan_content(
                action_file=action_file,
                metadata=metadata,
                steps=steps
            )
            
            # Create Plan.md file
            plan_filename = f'PLAN_{action_file.stem}.md'
            plan_path = self.plans / plan_filename
            
            plan_path.write_text(plan_content, encoding='utf-8')
            
            print(f'[OK] Plan created: {plan_filename}')
            return plan_path
            
        except Exception as e:
            print(f'[ERROR] Error creating plan: {e}')
            return None
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from action file frontmatter."""
        metadata = {}
        lines = content.split('\n')
        in_frontmatter = False
        
        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
        
        return metadata
    
    def _create_plan_content(
        self, 
        action_file: Path, 
        metadata: Dict[str, str],
        steps: List[str]
    ) -> str:
        """Create the Plan.md content."""
        
        action_type = metadata.get('type', 'unknown')
        priority = metadata.get('priority', 'normal')
        created = metadata.get('created', datetime.now().isoformat())
        
        # Build steps checklist
        steps_checklist = '\n'.join([f'- [ ] {step}' for step in steps])
        
        # Determine approval needed
        approval_needed = self._check_approval_needed(metadata)
        approval_section = ''
        if approval_needed:
            approval_section = f'''
## Approval Required

⚠️ This action requires human approval before proceeding.

**To Approve:**
1. Review the action details above
2. Move this file to `/Approved` folder
3. Orchestrator will execute the action

**To Reject:**
1. Move this file to `/Rejected` folder
2. Add reason for rejection in notes

'''
        
        content = f'''---
type: plan
action_type: {action_type}
priority: {priority}
created: {created}
status: pending
source_file: {action_file.name}
---

# Action Plan: {action_file.stem}

## Overview

**Action Type:** {action_type}
**Priority:** {priority}
**Created:** {created}
**Status:** Pending

## Objective

Complete the action item from `{action_file.name}` following Company Handbook rules.

## Steps

{steps_checklist}
{approval_section}
## Notes

Add notes, observations, or issues here:

---

## Audit Trail

| Timestamp | Action | Status |
|-----------|--------|--------|
| {datetime.now().isoformat()} | Plan created | Pending |

---

*Generated by AI Employee Plan Generator v0.2 (Silver Tier)*
'''
        
        return content
    
    def _check_approval_needed(self, metadata: Dict[str, str]) -> bool:
        """Check if action requires approval."""
        action_type = metadata.get('type', '')
        
        # These action types always need approval
        approval_types = ['payment', 'email_send', 'social_post']
        
        if action_type in approval_types:
            return True
        
        # Check amount for payments
        if 'amount' in metadata:
            try:
                amount = float(metadata['amount'])
                if amount >= 100:  # Payments >= $100 need approval
                    return True
            except ValueError:
                pass
        
        return False
    
    def process_all_pending(self) -> int:
        """
        Process all action files in Needs_Action folder.
        
        Returns:
            Number of plans created
        """
        plans_created = 0
        
        for action_file in self.needs_action.glob('*.md'):
            # Skip if already has a plan
            plan_filename = f'PLAN_{action_file.stem}.md'
            plan_path = self.plans / plan_filename
            
            if plan_path.exists():
                print(f'[SKIP] Plan already exists: {plan_filename}')
                continue
            
            # Generate plan
            if self.generate_plan(action_file):
                plans_created += 1
        
        return plans_created


def main():
    """Main entry point for plan generator."""
    if len(sys.argv) < 2:
        print('Usage: python plan_generator.py <vault_path>')
        print('')
        print('Example:')
        print('  python plan_generator.py "./AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create generator
    generator = PlanGenerator(vault_path)
    
    # Process all pending action files
    print('=' * 50)
    print('Plan Generator - Silver Tier')
    print('=' * 50)
    print(f'Vault: {vault_path}')
    print('')
    
    plans_created = generator.process_all_pending()
    
    print('')
    print('=' * 50)
    print(f'Plans created: {plans_created}')
    print('=' * 50)


if __name__ == '__main__':
    main()
