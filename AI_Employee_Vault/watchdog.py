#!/usr/bin/env python3
"""
Watchdog Process - Health Monitor

Monitors and auto-restarts critical AI Employee processes.
Ensures 24/7 operation by detecting crashes and restarting services.

Features:
- Process health monitoring
- Auto-restart on crash
- Human notification on restart
- Resource usage tracking
- Graceful shutdown

Usage:
    python watchdog.py
"""

import sys
import os
import json
import subprocess
import time
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import psutil


class Watchdog:
    """
    Watchdog Process Health Monitor.
    
    Monitors critical processes and restarts them if they crash.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize Watchdog.
        
        Args:
            vault_path: Path to Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logs_folder = self.vault_path / 'Logs'
        self.state_file = self.vault_path / '.watchdog_state.json'
        self.pid_file = self.vault_path / '.watchdog.pid'
        
        # Ensure folders exist
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self._setup_logging()
        
        # Process definitions
        self.processes = self._get_process_definitions()
        
        # Track running processes
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self.restart_counts: Dict[str, int] = {}
        self.max_restarts_per_hour = 5  # Prevent restart loops
        
        # Save PID
        self.pid_file.write_text(str(os.getpid()))
        
        # Handle shutdown signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("Watchdog initialized")
        self.logger.info(f"Monitoring {len(self.processes)} processes")
        
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_file = self.logs_folder / f'watchdog_{datetime.now().strftime("%Y%m%d")}.log'
        
        self.logger = logging.getLogger('Watchdog')
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
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _get_process_definitions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get definitions of processes to monitor.
        
        Returns:
            Dictionary of process configurations
        """
        return {
            'orchestrator': {
                'command': ['python', 'orchestrator.py', '.', '--dev-mode'],
                'description': 'Main Orchestrator',
                'restart_delay': 5,
                'check_interval': 30,
            },
            'file_watcher': {
                'command': ['python', 'watchers/filesystem_watcher.py', '.', 'Drop_Folder'],
                'description': 'File System Watcher',
                'restart_delay': 3,
                'check_interval': 10,
            },
            'gmail_watcher': {
                'command': ['python', 'gmail_auto_reply_watcher.py', '60'],
                'description': 'Gmail Auto-Reply Watcher',
                'restart_delay': 10,
                'check_interval': 60,
            },
        }
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)
    
    def _start_process(self, name: str) -> Optional[subprocess.Popen]:
        """
        Start a monitored process.
        
        Args:
            name: Process name
            
        Returns:
            Process handle if successful, None otherwise
        """
        if name not in self.processes:
            self.logger.error(f"Unknown process: {name}")
            return None
        
        config = self.processes[name]
        
        try:
            self.logger.info(f"Starting {config['description']}...")
            
            # Create log file for this process
            process_log = self.logs_folder / f'{name}_{datetime.now().strftime("%Y%m%d")}.log'
            
            # Start process
            proc = subprocess.Popen(
                config['command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(self.vault_path),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
            )
            
            self.logger.info(f"✓ {config['description']} started (PID: {proc.pid})")
            
            # Log to file
            self._log_event('process_start', {
                'name': name,
                'pid': proc.pid,
                'command': ' '.join(config['command'])
            })
            
            return proc
            
        except Exception as e:
            self.logger.error(f"Failed to start {config['description']}: {e}")
            self._log_event('process_start_failed', {
                'name': name,
                'error': str(e)
            })
            return None
    
    def _check_process_health(self, name: str, proc: subprocess.Popen) -> bool:
        """
        Check if a process is healthy.
        
        Args:
            name: Process name
            proc: Process handle
            
        Returns:
            True if healthy, False if needs restart
        """
        # Check if process is running
        if proc.poll() is not None:
            # Process exited
            return_code = proc.returncode
            self.logger.warning(f"{name} exited with code {return_code}")
            return False
        
        # Check if process is responsive (optional: check CPU/memory)
        try:
            ps_proc = psutil.Process(proc.pid)
            cpu_percent = ps_proc.cpu_percent(interval=1)
            memory_percent = ps_proc.memory_percent()
            
            # Log resource usage
            if cpu_percent > 90:
                self.logger.warning(f"{name} using high CPU: {cpu_percent}%")
            if memory_percent > 80:
                self.logger.warning(f"{name} using high memory: {memory_percent}%")
                
        except psutil.NoSuchProcess:
            self.logger.warning(f"{name} process not found in psutil")
            return False
        
        return True
    
    def _should_restart(self, name: str) -> bool:
        """
        Check if process should be restarted (rate limiting).
        
        Args:
            name: Process name
            
        Returns:
            True if restart is allowed
        """
        if name not in self.restart_counts:
            self.restart_counts[name] = 0
        
        # Reset count if more than an hour since last restart
        # (simplified: just check count for now)
        if self.restart_counts[name] >= self.max_restarts_per_hour:
            self.logger.warning(f"{name} restarted {self.restart_counts[name]} times this hour. Not restarting.")
            return False
        
        return True
    
    def _notify_human(self, event: str, details: Dict) -> None:
        """
        Notify human about important events.
        
        Args:
            event: Event type
            details: Event details
        """
        # For now, just log. Could be extended to send email/SMS.
        self.logger.info(f"HUMAN NOTIFICATION: {event} - {details}")
        
        # Write to notification file
        notification_file = self.vault_path / 'Needs_Action' / f'WATCHDOG_{event}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        content = f"""---
type: watchdog_notification
event: {event}
timestamp: {datetime.now().isoformat()}
---

# Watchdog Notification

## Event: {event}

{json.dumps(details, indent=2)}

---

*Generated by Watchdog Process Monitor*
"""
        
        try:
            notification_file.parent.mkdir(parents=True, exist_ok=True)
            notification_file.write_text(content, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Could not write notification: {e}")
    
    def _log_event(self, event_type: str, details: Dict) -> None:
        """Log event to JSON log file."""
        log_file = self.logs_folder / f'watchdog_events_{datetime.now().strftime("%Y%m")}.json'
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details
        }
        
        events = []
        if log_file.exists():
            try:
                events = json.loads(log_file.read_text())
            except:
                events = []
        
        events.append(event)
        log_file.write_text(json.dumps(events, indent=2))
    
    def _save_state(self) -> None:
        """Save current watchdog state."""
        state = {
            'timestamp': datetime.now().isoformat(),
            'running_processes': list(self.running_processes.keys()),
            'restart_counts': self.restart_counts,
            'uptime': datetime.now().isoformat()
        }
        
        self.state_file.write_text(json.dumps(state, indent=2))
    
    def start_all(self) -> None:
        """Start all monitored processes."""
        self.logger.info("Starting all monitored processes...")
        
        for name in self.processes:
            proc = self._start_process(name)
            if proc:
                self.running_processes[name] = proc
                self.restart_counts[name] = 0
        
        self._save_state()
        self.logger.info("All processes started")
    
    def stop_all(self) -> None:
        """Stop all monitored processes."""
        self.logger.info("Stopping all processes...")
        
        for name, proc in self.running_processes.items():
            try:
                proc.terminate()
                proc.wait(timeout=5)
                self.logger.info(f"✓ {name} stopped")
            except Exception as e:
                self.logger.error(f"Error stopping {name}: {e}")
                proc.kill()
        
        self.running_processes.clear()
        self._save_state()
    
    def shutdown(self) -> None:
        """Graceful shutdown."""
        self.logger.info("Watchdog shutting down...")
        self.stop_all()
        
        # Remove PID file
        if self.pid_file.exists():
            self.pid_file.unlink()
        
        self.logger.info("Watchdog stopped")
    
    def run(self) -> None:
        """
        Main watchdog loop.
        
        Monitors processes and restarts as needed.
        """
        self.logger.info("=" * 60)
        self.logger.info("WATCHDOG PROCESS MONITOR - Starting")
        self.logger.info("=" * 60)
        
        # Start all processes
        self.start_all()
        
        # Main monitoring loop
        check_interval = 10  # Check every 10 seconds
        last_check = {name: 0 for name in self.processes}
        
        try:
            while True:
                current_time = time.time()
                
                for name, proc in list(self.running_processes.items()):
                    config = self.processes[name]
                    
                    # Check if it's time to check this process
                    if current_time - last_check[name] < config['check_interval']:
                        continue
                    
                    last_check[name] = current_time
                    
                    # Check process health
                    if not self._check_process_health(name, proc):
                        self.logger.warning(f"{config['description']} unhealthy, attempting restart...")
                        
                        # Check restart limit
                        if not self._should_restart(name):
                            self._notify_human('restart_limit_reached', {
                                'process': name,
                                'max_restarts': self.max_restarts_per_hour
                            })
                            continue
                        
                        # Restart process
                        proc.terminate()
                        try:
                            proc.wait(timeout=5)
                        except:
                            proc.kill()
                        
                        time.sleep(config['restart_delay'])
                        
                        new_proc = self._start_process(name)
                        if new_proc:
                            self.running_processes[name] = new_proc
                            self.restart_counts[name] = self.restart_counts.get(name, 0) + 1
                            
                            self._notify_human('process_restarted', {
                                'process': name,
                                'restart_count': self.restart_counts[name]
                            })
                        else:
                            self.logger.error(f"Failed to restart {name}")
                            del self.running_processes[name]
                
                # Save state periodically
                self._save_state()
                
                # Sleep
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        except Exception as e:
            self.logger.error(f"Watchdog error: {e}")
        finally:
            self.shutdown()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        vault_path = '.'
    else:
        vault_path = sys.argv[1]
    
    vault_path = Path(vault_path).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create watchdog
    watchdog = Watchdog(str(vault_path))
    
    print("=" * 60)
    print('🐕 Watchdog Process Monitor')
    print('=' * 60)
    print(f'Vault: {vault_path}')
    print(f'Monitoring: {len(watchdog.processes)} processes')
    print('')
    print('Press Ctrl+C to stop')
    print('')
    
    # Run watchdog
    watchdog.run()


if __name__ == '__main__':
    main()
