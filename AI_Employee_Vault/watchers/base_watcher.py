"""
Base Watcher Module

Abstract base class for all watcher scripts in the Personal AI Employee Hackathon-0 system.
All watchers follow the same pattern: monitor inputs and create actionable
files in the Needs_Action folder.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all Personal AI Employee Hackathon-0 watchers.
    
    Watchers are long-running processes that monitor external inputs
    (email, WhatsApp, files, etc.) and create action files when new
    items are detected.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.check_interval = check_interval
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Track processed items to avoid duplicates
        self.processed_ids: set = set()
        
        self.logger.info(f'{self.__class__.__name__} initialized')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {check_interval}s')
    
    def _setup_logging(self) -> None:
        """Set up logging to both file and console."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'watcher_{self.__class__.__name__.lower()}.log'
        
        # Create logger
        self.logger = logging.getLogger(self.__class__.__name__)
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
    
    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new items to process.
        
        Returns:
            List of new items that need processing
            
        This method must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create an action file in the Needs_Action folder.
        
        Args:
            item: The item to create an action file for
            
        Returns:
            Path to the created file, or None if creation failed
            
        This method must be implemented by subclasses.
        """
        pass
    
    def run(self) -> None:
        """
        Main run loop for the watcher.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        
                    for item in items:
                        filepath = self.create_action_file(item)
                        if filepath:
                            self.logger.info(f'Created action file: {filepath.name}')
                    
                except Exception as e:
                    self.logger.error(f'Error processing items: {e}', exc_info=True)
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}', exc_info=True)
            raise
    
    def generate_frontmatter(self, item_type: str, **kwargs) -> str:
        """
        Generate YAML frontmatter for action files.
        
        Args:
            item_type: Type of item (email, whatsapp, file_drop, etc.)
            **kwargs: Additional metadata fields
            
        Returns:
            Formatted YAML frontmatter string
        """
        lines = ['---', f'type: {item_type}']
        
        # Add timestamp
        lines.append(f'created: {datetime.now().isoformat()}')
        
        # Add status
        lines.append('status: pending')
        
        # Add priority (default: normal)
        priority = kwargs.pop('priority', 'normal')
        lines.append(f'priority: {priority}')
        
        # Add remaining kwargs
        for key, value in kwargs.items():
            # Escape special characters in values
            if isinstance(value, str):
                value = value.replace('"', '\\"').replace('\n', ' ')
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
        
        lines.append('---')
        return '\n'.join(lines)
    
    def get_unique_filename(self, prefix: str, extension: str = '.md') -> Path:
        """
        Generate a unique filename in the Needs_Action folder.
        
        Args:
            prefix: Filename prefix
            extension: File extension (default: .md)
            
        Returns:
            Path to a unique filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{prefix}_{timestamp}{extension}'
        filepath = self.needs_action / filename
        
        # Ensure uniqueness
        counter = 0
        while filepath.exists():
            counter += 1
            filename = f'{prefix}_{timestamp}_{counter}{extension}'
            filepath = self.needs_action / filename
        
        return filepath
