#!/usr/bin/env python3
"""
File System Watcher

Monitors a drop folder for new files and creates action files
in the Needs_Action folder. This is the Bronze tier watcher.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder
"""

import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder."""
    
    def __init__(self, watcher: 'FileSystemWatcher'):
        """
        Initialize the handler.
        
        Args:
            watcher: The parent FileSystemWatcher instance
        """
        super().__init__()
        self.watcher = watcher
    
    def on_created(self, event) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return
        
        self.watcher.logger.info(f'File created: {event.src_path}')
        self.watcher.process_file(Path(event.src_path))


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a new file is detected, it copies the file to the vault
    and creates a corresponding action file in Needs_Action.
    """
    
    def __init__(self, vault_path: str, drop_folder: str, check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            drop_folder: Path to the folder to monitor for new files
            check_interval: Seconds between checks (default: 5 for file watcher)
        """
        super().__init__(vault_path, check_interval)
        
        self.drop_folder = Path(drop_folder)
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Track processed files
        self.processed_files: set = set()
        
        self.logger.info(f'Drop folder: {self.drop_folder}')
    
    def check_for_updates(self) -> List[Path]:
        """
        Check for new files in the drop folder.
        
        Returns:
            List of new file paths to process
        """
        new_files = []
        
        try:
            for file_path in self.drop_folder.iterdir():
                if file_path.is_file() and file_path not in self.processed_files:
                    # Skip hidden files and temporary files
                    if file_path.name.startswith('.') or file_path.suffix == '.tmp':
                        continue
                    
                    new_files.append(file_path)
                    self.processed_files.add(file_path)
                    
        except Exception as e:
            self.logger.error(f'Error scanning drop folder: {e}')
        
        return new_files
    
    def create_action_file(self, file_path: Path) -> Optional[Path]:
        """
        Create an action file for a dropped file.
        
        Args:
            file_path: Path to the dropped file
            
        Returns:
            Path to the created action file, or None if failed
        """
        try:
            # Copy file to vault
            dest_path = self.vault_path / 'Inbox' / file_path.name
            shutil.copy2(file_path, dest_path)
            self.logger.info(f'Copied file to vault: {dest_path}')
            
            # Get file metadata
            file_stat = file_path.stat()
            file_size = file_stat.st_size
            
            # Generate frontmatter
            frontmatter = self.generate_frontmatter(
                item_type='file_drop',
                original_name=file_path.name,
                original_path=str(file_path),
                vault_path=str(dest_path),
                size=file_size,
                priority='normal'
            )
            
            # Create action file content
            content = f'''{frontmatter}

# File Drop for Processing

## File Information
- **Original Name:** {file_path.name}
- **Size:** {self._format_size(file_size)}
- **Detected:** {self._get_timestamp()}

## Suggested Actions
- [ ] Review file contents
- [ ] Categorize file
- [ ] Take appropriate action
- [ ] Move to /Done when complete

## Notes
Add your notes here...

'''

            # Write action file with UTF-8 encoding
            action_filepath = self.get_unique_filename(f'FILE_{file_path.stem}')
            action_filepath.write_text(content, encoding='utf-8')

            self.logger.info(f'Action file created: {action_filepath.name}')
            return action_filepath
            
        except Exception as e:
            self.logger.error(f'Error creating action file: {e}', exc_info=True)
            return None
    
    def process_file(self, file_path: Path) -> None:
        """
        Process a newly detected file (called by event handler).
        
        Args:
            file_path: Path to the new file
        """
        self.logger.info(f'Processing file: {file_path.name}')
        
        if file_path in self.processed_files:
            self.logger.debug(f'File already processed: {file_path.name}')
            return
        
        self.processed_files.add(file_path)
        self.create_action_file(file_path)
    
    def run_with_observer(self) -> None:
        """
        Run the watcher using the watchdog observer (real-time).
        
        This provides instant detection instead of polling.
        """
        self.logger.info('Starting FileSystemWatcher with real-time observer')
        
        event_handler = DropFolderHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        self.logger.info(f'Watching folder: {self.drop_folder}')
        self.logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                # Process any files that might have been added before observer started
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
                
                import time
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Stopping observer...')
            observer.stop()
        
        observer.join()
        self.logger.info('FileSystemWatcher stopped')
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in readable format."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    """Main entry point for the filesystem watcher."""
    if len(sys.argv) < 3:
        print('Usage: python filesystem_watcher.py <vault_path> <drop_folder>')
        print('')
        print('Arguments:')
        print('  vault_path    Path to the Obsidian vault root')
        print('  drop_folder   Path to the folder to monitor for new files')
        print('')
        print('Example:')
        print('  python filesystem_watcher.py "./AI_Employee_Vault" "./Drop_Folder"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2]
    
    # Validate paths
    if not Path(vault_path).exists():
        print(f'Error: Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    # Create watcher
    watcher = FileSystemWatcher(vault_path, drop_folder)
    
    # Run with real-time observer
    watcher.run_with_observer()


if __name__ == '__main__':
    main()
