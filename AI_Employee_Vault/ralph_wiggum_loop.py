#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Autonomous Task Completion

Implements the "Ralph Wiggum" pattern: a stop hook that keeps Claude/Qwen Code
working autonomously until a task is complete.

How it works:
1. Orchestrator creates state file with prompt
2. AI works on task
3. AI tries to exit
4. Stop hook checks: Is task file in /Done?
5. YES → Allow exit (complete)
6. NO → Block exit, re-inject prompt (loop continues)
7. Repeat until complete or max iterations

Usage:
    python ralph_wiggum_loop.py /path/to/vault --prompt "Process all files" --max-iterations 10
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import logging
import time
import argparse
import shutil


class RalphWiggumLoop:
    """
    Ralph Wiggum Loop for autonomous AI task completion.
    
    This loop keeps the AI agent working until:
    - Task is marked complete (file moved to /Done)
    - Max iterations reached
    - Completion promise detected in output
    """
    
    def __init__(
        self,
        vault_path: str,
        prompt: str,
        max_iterations: int = 10,
        completion_promise: str = "TASK_COMPLETE",
        ai_command: str = "claude"
    ):
        """
        Initialize Ralph Wiggum Loop.
        
        Args:
            vault_path: Path to Obsidian vault
            prompt: Initial task prompt for AI
            max_iterations: Maximum loop iterations before giving up
            completion_promise: Special token AI outputs when done
            ai_command: Command to run AI (e.g., 'claude', 'qwen')
        """
        self.vault_path = Path(vault_path)
        self.prompt = prompt
        self.max_iterations = max_iterations
        self.completion_promise = completion_promise
        self.ai_command = ai_command
        
        # State folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.state_file = self.vault_path / '.ralph_state.json'
        self.log_file = self.vault_path / 'Logs' / f'ralph_loop_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        # Ensure logs folder exists
        self.vault_path.joinpath('Logs').mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # State tracking
        self.current_iteration = 0
        self.task_complete = False
        self.last_output = ""
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        self.logger = logging.getLogger('RalphWiggumLoop')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _save_state(self) -> None:
        """Save current loop state to file."""
        state = {
            'iteration': self.current_iteration,
            'prompt': self.prompt,
            'task_complete': self.task_complete,
            'last_output': self.last_output,
            'started_at': datetime.now().isoformat()
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_state(self) -> Optional[dict]:
        """Load previous state if exists."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return None
    
    def _check_task_completion(self) -> bool:
        """
        Check if task is complete by looking for files in /Done.
        
        Returns:
            True if task appears complete, False otherwise
        """
        # Check if any files were moved to /Done
        done_files = list(self.done.glob('*.md'))
        if done_files:
            self.logger.info(f"Found {len(done_files)} files in /Done - task may be complete")
            return True
        
        # Check if Needs_Action is empty (all processed)
        needs_action_files = list(self.needs_action.glob('*.md'))
        if not needs_action_files:
            self.logger.info("No files in /Needs_Action - all tasks processed")
            return True
        
        return False
    
    def _check_completion_promise(self, output: str) -> bool:
        """
        Check if AI output contains completion promise.
        
        Args:
            output: AI's last output
            
        Returns:
            True if completion promise detected
        """
        # Check for completion promise token
        if f"<promise>{self.completion_promise}</promise>" in output:
            self.logger.info(f"Completion promise detected: {self.completion_promise}")
            return True
        
        # Also check for plain text
        if self.completion_promise in output:
            self.logger.info(f"Completion text detected: {self.completion_promise}")
            return True
        
        return False
    
    def _run_ai(self, prompt: str) -> str:
        """
        Run AI agent with given prompt.
        
        Args:
            prompt: Prompt to send to AI
            
        Returns:
            AI's output
        """
        self.logger.info(f"Running AI with prompt: {prompt[:100]}...")
        
        try:
            # Run AI command with timeout
            result = subprocess.run(
                [self.ai_command, prompt],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout per iteration
                cwd=str(self.vault_path)
            )
            
            output = result.stdout + result.stderr
            self.logger.info(f"AI output length: {len(output)} chars")
            
            return output
            
        except subprocess.TimeoutExpired:
            self.logger.warning("AI command timed out after 5 minutes")
            return "ERROR: Timeout expired"
        except Exception as e:
            self.logger.error(f"Error running AI: {e}")
            return f"ERROR: {str(e)}"
    
    def _build_continuation_prompt(self, previous_output: str) -> str:
        """
        Build continuation prompt that includes previous output.
        
        Args:
            previous_output: AI's previous output
            
        Returns:
            New prompt that continues the conversation
        """
        return f"""{self.prompt}

---
PREVIOUS ATTEMPT OUTPUT:
{previous_output}

Continue working on the task. Review what was done and what still needs to be done.
If the task is complete, output: <promise>{self.completion_promise}</promise>
"""
    
    def run(self) -> bool:
        """
        Run the Ralph Wiggum Loop.
        
        Returns:
            True if task completed successfully, False otherwise
        """
        self.logger.info("=" * 60)
        self.logger.info("RALPH WIGGUM LOOP - Starting Autonomous Task Completion")
        self.logger.info("=" * 60)
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Prompt: {self.prompt[:100]}...")
        self.logger.info(f"Max iterations: {self.max_iterations}")
        self.logger.info(f"Completion promise: {self.completion_promise}")
        self.logger.info("=" * 60)
        
        # Load previous state if exists
        previous_state = self._load_state()
        if previous_state:
            self.logger.info(f"Resuming from iteration {previous_state.get('iteration', 0)}")
            self.current_iteration = previous_state.get('iteration', 0)
            self.last_output = previous_state.get('last_output', '')
        
        # Main loop
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            
            self.logger.info("-" * 40)
            self.logger.info(f"ITERATION {self.current_iteration}/{self.max_iterations}")
            self.logger.info("-" * 40)
            
            # Build prompt
            if self.current_iteration == 1:
                current_prompt = self.prompt
            else:
                current_prompt = self._build_continuation_prompt(self.last_output)
            
            # Run AI
            output = self._run_ai(current_prompt)
            self.last_output = output
            
            # Save state
            self._save_state()
            
            # Check completion conditions
            if self._check_completion_promise(output):
                self.logger.info("✓ Task completed (completion promise detected)")
                self.task_complete = True
                break
            
            if self._check_task_completion():
                self.logger.info("✓ Task completed (files processed)")
                self.task_complete = True
                break
            
            self.logger.info(f"Iteration {self.current_iteration} complete, continuing...")
            
            # Small delay between iterations
            time.sleep(2)
        
        # Final status
        if self.task_complete:
            self.logger.info("=" * 60)
            self.logger.info("✓ RALPH WIGGUM LOOP - TASK COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 60)
            # Clean up state file
            if self.state_file.exists():
                self.state_file.unlink()
            return True
        else:
            self.logger.warning("=" * 60)
            self.logger.warning("✗ RALPH WIGGUM LOOP - MAX ITERATIONS REACHED")
            self.logger.warning("=" * 60)
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Ralph Wiggum Loop - Autonomous AI Task Completion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python ralph_wiggum_loop.py ./vault --prompt "Process all files in Needs_Action"
  
  # With max iterations
  python ralph_wiggum_loop.py ./vault --prompt "Reply to all emails" --max-iterations 5
  
  # With completion promise
  python ralph_wiggum_loop.py ./vault --prompt "Generate invoice" --completion-promise "INVOICE_SENT"
        """
    )
    
    parser.add_argument(
        'vault_path',
        help='Path to Obsidian vault'
    )
    parser.add_argument(
        '--prompt', '-p',
        required=True,
        help='Task prompt for AI'
    )
    parser.add_argument(
        '--max-iterations', '-m',
        type=int,
        default=10,
        help='Maximum loop iterations (default: 10)'
    )
    parser.add_argument(
        '--completion-promise', '-c',
        default='TASK_COMPLETE',
        help='Completion promise token (default: TASK_COMPLETE)'
    )
    parser.add_argument(
        '--ai-command', '-a',
        default='claude',
        help='AI command to run (default: claude)'
    )
    
    args = parser.parse_args()
    
    # Create and run loop
    loop = RalphWiggumLoop(
        vault_path=args.vault_path,
        prompt=args.prompt,
        max_iterations=args.max_iterations,
        completion_promise=args.completion_promise,
        ai_command=args.ai_command
    )
    
    success = loop.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
