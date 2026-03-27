#!/usr/bin/env python3
"""
Claim-by-Move Rule Implementation

Platinum Tier - Prevents double-work between Cloud and Local agents.

Rule: First agent to move item from /Needs_Action to /In_Progress/<agent>/ owns it.
Other agents must ignore claimed items.
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import json


class ClaimManager:
    """
    Manages task claiming between Cloud and Local agents.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize Claim Manager.
        
        Args:
            vault_path: Path to Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.done = self.vault_path / 'Done'
        
        # Agent type: 'cloud_agent' or 'local_agent'
        self.agent_type = self._detect_agent_type()
        
        # Ensure directories exist
        self.in_progress.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)
        
        # Agent-specific folder
        self.agent_folder = self.in_progress / self.agent_type
        self.agent_folder.mkdir(parents=True, exist_ok=True)
    
    def _detect_agent_type(self) -> str:
        """Detect if running as cloud or local agent."""
        # Check for environment marker
        cloud_marker = Path(__file__).parent.parent / 'Cloud_Agent'
        if cloud_marker.exists():
            return 'cloud_agent'
        
        local_marker = Path(__file__).parent.parent / 'Local_Agent'
        if local_marker.exists():
            return 'local_agent'
        
        # Default to local
        return 'local_agent'
    
    def get_available_tasks(self) -> List[Path]:
        """
        Get list of unclaimed tasks in Needs_Action.
        
        Returns:
            List of file paths that can be claimed
        """
        available = []
        
        # Check all subfolders in Needs_Action
        for folder in ['cloud', 'local', 'shared']:
            folder_path = self.needs_action / folder
            if not folder_path.exists():
                continue
            
            for file_path in folder_path.glob('*.md'):
                # Check if already claimed
                if not self.is_claimed(file_path):
                    # Check if this agent type can access this folder
                    if self._can_access_folder(folder):
                        available.append(file_path)
        
        return available
    
    def _can_access_folder(self, folder: str) -> bool:
        """
        Check if agent type can access folder.
        
        Args:
            folder: Folder name (cloud, local, shared)
        
        Returns:
            True if agent can access
        """
        if folder == 'shared':
            return True  # Both agents can access shared
        
        if folder == 'cloud' and self.agent_type == 'cloud_agent':
            return True
        
        if folder == 'local' and self.agent_type == 'local_agent':
            return True
        
        return False
    
    def is_claimed(self, file_path: Path) -> bool:
        """
        Check if a task file is already claimed.
        
        Args:
            file_path: Path to task file
        
        Returns:
            True if claimed by any agent
        """
        # Check if file exists in any In_Progress subfolder
        for agent_folder in self.in_progress.iterdir():
            if agent_folder.is_dir():
                claimed_file = agent_folder / file_path.name
                if claimed_file.exists():
                    return True
        
        # Check if file exists in Needs_Action (not yet moved)
        if file_path.exists():
            return False
        
        # File not found anywhere - might be completed
        return True
    
    def claim_task(self, file_path: Path) -> Optional[Path]:
        """
        Claim a task by moving it to In_Progress/<agent>/.
        
        Args:
            file_path: Path to task file in Needs_Action
        
        Returns:
            Path to claimed file, or None if already claimed
        """
        # Check if already claimed
        if self.is_claimed(file_path):
            print(f"Task already claimed: {file_path.name}")
            return None
        
        # Move to agent's In_Progress folder
        dest_path = self.agent_folder / file_path.name
        
        try:
            shutil.move(str(file_path), str(dest_path))
            print(f"Claimed task: {file_path.name} → {self.agent_type}/")
            
            # Add claim metadata
            self._add_claim_metadata(dest_path)
            
            return dest_path
            
        except Exception as e:
            print(f"Error claiming task: {e}")
            return None
    
    def _add_claim_metadata(self, file_path: Path) -> None:
        """
        Add claim metadata to task file.
        
        Args:
            file_path: Path to claimed file
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Add claim comment
            claim_info = f"""---
claimed_by: {self.agent_type}
claimed_at: {datetime.now().isoformat()}
status: in_progress
---
"""
            # Insert after existing frontmatter or at beginning
            if content.startswith('---'):
                # Find end of existing frontmatter
                end_frontmatter = content.find('---', 3) + 3
                new_content = content[:end_frontmatter] + f"\n# Claimed by {self.agent_type} at {datetime.now().isoformat()}\n" + content[end_frontmatter:]
            else:
                new_content = claim_info + content
            
            file_path.write_text(new_content, encoding='utf-8')
            
        except Exception as e:
            print(f"Error adding claim metadata: {e}")
    
    def complete_task(self, file_path: Path, move_to_done: bool = True) -> bool:
        """
        Mark task as complete.
        
        Args:
            file_path: Path to task file in In_Progress
            move_to_done: Whether to move to Done folder
        
        Returns:
            True if successful
        """
        try:
            # Add completion metadata
            content = file_path.read_text(encoding='utf-8')
            
            completion_info = f"""
# Completed by {self.agent_type} at {datetime.now().isoformat()}
status: completed
completed_at: {datetime.now().isoformat()}
"""
            
            # Append completion info
            new_content = content + completion_info
            file_path.write_text(new_content, encoding='utf-8')
            
            # Move to Done if requested
            if move_to_done:
                dest_path = self.done / file_path.name
                shutil.move(str(file_path), str(dest_path))
                print(f"Task completed: {file_path.name} → Done/")
            
            return True
            
        except Exception as e:
            print(f"Error completing task: {e}")
            return False
    
    def release_task(self, file_path: Path) -> bool:
        """
        Release a claimed task (e.g., if agent can't handle it).
        
        Args:
            file_path: Path to task file in In_Progress
        
        Returns:
            True if successful
        """
        try:
            # Move back to Needs_Action/shared
            dest_path = self.needs_action / 'shared' / file_path.name
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove claim metadata
            content = file_path.read_text(encoding='utf-8')
            # Remove claim-related lines
            lines = content.split('\n')
            filtered_lines = [line for line in lines if not any(
                keyword in line.lower() 
                for keyword in ['claimed_by', 'claimed_at', 'status: in_progress']
            )]
            clean_content = '\n'.join(filtered_lines)
            file_path.write_text(clean_content, encoding='utf-8')
            
            # Move
            shutil.move(str(file_path), str(dest_path))
            print(f"Released task: {file_path.name} → shared/")
            
            return True
            
        except Exception as e:
            print(f"Error releasing task: {e}")
            return False
    
    def get_agent_stats(self) -> Dict:
        """
        Get statistics for current agent.
        
        Returns:
            Dictionary with agent stats
        """
        # Count tasks in different states
        in_progress_count = len(list(self.agent_folder.glob('*.md')))
        done_count = len(list(self.done.glob('*.md')))
        available_count = len(self.get_available_tasks())
        
        return {
            'agent_type': self.agent_type,
            'in_progress': in_progress_count,
            'completed': done_count,
            'available': available_count,
            'timestamp': datetime.now().isoformat()
        }


def main():
    """Test claim manager."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python claim_manager.py <vault_path>")
        print("")
        print("Commands:")
        print("  python claim_manager.py <vault_path> status")
        print("  python claim_manager.py <vault_path> claim <file>")
        print("  python claim_manager.py <vault_path> complete <file>")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) > 2 else 'status'
    
    claim_mgr = ClaimManager(str(vault_path))
    
    if command == 'status':
        stats = claim_mgr.get_agent_stats()
        print(f"\n=== {claim_mgr.agent_type} Status ===")
        print(f"In Progress: {stats['in_progress']}")
        print(f"Completed: {stats['completed']}")
        print(f"Available: {stats['available']}")
        print()
    
    elif command == 'claim':
        if len(sys.argv) < 4:
            print("Error: Specify file to claim")
            sys.exit(1)
        
        file_name = sys.argv[3]
        
        # Find file in Needs_Action
        file_path = None
        for folder in ['cloud', 'local', 'shared']:
            test_path = claim_mgr.needs_action / folder / file_name
            if test_path.exists():
                file_path = test_path
                break
        
        if not file_path:
            print(f"File not found: {file_name}")
            sys.exit(1)
        
        result = claim_mgr.claim_task(file_path)
        if result:
            print(f"✓ Claimed: {file_name}")
        else:
            print(f"✗ Already claimed: {file_name}")
    
    elif command == 'complete':
        if len(sys.argv) < 4:
            print("Error: Specify file to complete")
            sys.exit(1)
        
        file_name = sys.argv[3]
        file_path = claim_mgr.agent_folder / file_name
        
        if not file_path.exists():
            print(f"File not found in In_Progress: {file_name}")
            sys.exit(1)
        
        result = claim_mgr.complete_task(file_path)
        if result:
            print(f"✓ Completed: {file_name}")
        else:
            print(f"✗ Error completing: {file_name}")


if __name__ == '__main__':
    main()
