#!/usr/bin/env python3
"""
AI Employee Dashboard Backend Server

Provides real-time API for the dashboard:
- Start/Stop Gmail Watcher
- Get email activity logs
- Send manual emails
- Get system status
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import threading
import json
import os
from pathlib import Path
from datetime import datetime
import queue
import time

app = Flask(__name__, static_folder='.', static_path='')
CORS(app)

# Global variables
gmail_watcher_process = None
activity_log = queue.Queue(maxsize=100)
system_status = {
    'gmail_watcher': False,
    'file_watcher': False,
    'orchestrator': False,
    'last_email_check': None,
    'emails_processed_today': 0,
    'auto_replies_sent_today': 0
}

# Paths
VAULT_PATH = Path(__file__).parent.parent
LOGS_PATH = VAULT_PATH / 'Logs'
GMAIL_WATCHER_SCRIPT = VAULT_PATH / 'gmail_auto_reply_watcher.py'


def log_activity(activity_type: str, message: str, details: dict = None):
    """Log activity for dashboard"""
    activity_log.put({
        'timestamp': datetime.now().isoformat(),
        'type': activity_type,
        'message': message,
        'details': details or {}
    })
    
    # Also log to file
    log_file = LOGS_PATH / 'dashboard_activity.json'
    try:
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'message': message,
            'details': details or {}
        })
        
        # Keep last 100 entries
        logs = logs[-100:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error writing to log file: {e}")


def monitor_gmail_watcher():
    """Monitor Gmail watcher process and log activity"""
    global system_status
    
    while system_status['gmail_watcher']:
        try:
            # Check if process is running
            if gmail_watcher_process and gmail_watcher_process.poll() is not None:
                system_status['gmail_watcher'] = False
                log_activity('error', 'Gmail Watcher stopped unexpectedly', {
                    'return_code': gmail_watcher_process.returncode
                })
                break
            
            # Read Gmail auto-reply log
            gmail_log_file = LOGS_PATH / 'gmail_auto_reply.log'
            if gmail_log_file.exists():
                try:
                    with open(gmail_log_file, 'r') as f:
                        lines = f.readlines()
                        # Get last 10 lines
                        for line in lines[-10:]:
                            if 'INFO' in line:
                                if 'New email from' in line:
                                    email_from = line.split('from: ')[-1].strip()
                                    log_activity('email_received', f'New email received from {email_from}', {
                                        'from': email_from
                                    })
                                    system_status['emails_processed_today'] += 1
                                elif 'Auto-reply sent' in line:
                                    email_to = line.split('to: ')[-1].strip()
                                    log_activity('auto_reply_sent', f'Auto-reply sent to {email_to}', {
                                        'to': email_to
                                    })
                                    system_status['auto_replies_sent_today'] += 1
                                elif 'Found' in line and 'unread' in line:
                                    count = line.split('Found ')[-1].split(' unread')[0]
                                    log_activity('info', f'Checked Gmail - {count} unread emails')
                    
                    system_status['last_email_check'] = datetime.now().isoformat()
                except Exception as e:
                    print(f"Error reading Gmail log: {e}")
            
            time.sleep(5)  # Check every 5 seconds
            
        except Exception as e:
            print(f"Monitor error: {e}")
            time.sleep(5)


@app.route('/')
def serve_dashboard():
    """Serve the dashboard HTML file"""
    return send_from_directory('.', 'ai-dashboard.html')


@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify(system_status)


@app.route('/api/activity', methods=['GET'])
def get_activity():
    """Get recent activity logs"""
    logs = []
    while not activity_log.empty():
        logs.append(activity_log.get())
    
    # Return last 50 activities
    return jsonify(logs[-50:])


@app.route('/api/gmail/start', methods=['POST'])
def start_gmail_watcher():
    """Start Gmail Watcher"""
    global gmail_watcher_process, system_status
    
    if system_status['gmail_watcher']:
        return jsonify({'success': False, 'message': 'Already running'})
    
    try:
        # Start Gmail watcher
        gmail_watcher_process = subprocess.Popen(
            ['python', str(GMAIL_WATCHER_SCRIPT), '60'],
            cwd=str(VAULT_PATH),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        system_status['gmail_watcher'] = True
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_gmail_watcher, daemon=True)
        monitor_thread.start()
        
        log_activity('success', 'Gmail Watcher started', {
            'pid': gmail_watcher_process.pid
        })
        
        return jsonify({'success': True, 'message': 'Gmail Watcher started'})
        
    except Exception as e:
        log_activity('error', f'Failed to start Gmail Watcher: {str(e)}')
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/gmail/stop', methods=['POST'])
def stop_gmail_watcher():
    """Stop Gmail Watcher"""
    global gmail_watcher_process, system_status
    
    if not system_status['gmail_watcher']:
        return jsonify({'success': False, 'message': 'Not running'})
    
    try:
        gmail_watcher_process.terminate()
        gmail_watcher_process.wait(timeout=5)
        system_status['gmail_watcher'] = False
        
        log_activity('info', 'Gmail Watcher stopped')
        
        return jsonify({'success': True, 'message': 'Gmail Watcher stopped'})
        
    except Exception as e:
        log_activity('error', f'Failed to stop Gmail Watcher: {str(e)}')
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/email/send', methods=['POST'])
def send_email():
    """Send manual email"""
    data = request.json
    
    if not data or 'to' not in data or 'subject' not in data or 'body' not in data:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        # Import Gmail libraries
        import smtplib
        from email.mime.text import MIMEText
        from dotenv import load_dotenv
        
        # Load credentials
        env_path = VAULT_PATH / 'mcp_servers' / 'email_mcp' / '.env'
        load_dotenv(env_path)
        
        email_address = os.getenv('GMAIL_EMAIL_ADDRESS')
        app_password = os.getenv('GMAIL_APP_PASSWORD', '').replace(' ', '')
        
        if not email_address or not app_password:
            return jsonify({'success': False, 'message': 'Email credentials not configured'})
        
        # Create message
        msg = MIMEText(data['body'], 'plain')
        msg['From'] = email_address
        msg['To'] = data['to']
        msg['Subject'] = data['subject']
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, app_password)
        server.send_message(msg)
        server.quit()
        
        log_activity('email_sent', f'Manual email sent to {data["to"]}', {
            'to': data['to'],
            'subject': data['subject']
        })
        
        return jsonify({'success': True, 'message': 'Email sent successfully'})
        
    except Exception as e:
        log_activity('error', f'Failed to send email: {str(e)}')
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/orchestrator/start', methods=['POST'])
def start_orchestrator():
    """Start Orchestrator"""
    try:
        orchestrator_script = VAULT_PATH / 'orchestrator.py'
        subprocess.Popen(
            ['python', str(orchestrator_script), '.', '--dev-mode', '--interval', '30'],
            cwd=str(VAULT_PATH),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        system_status['orchestrator'] = True
        log_activity('success', 'Orchestrator started')
        
        return jsonify({'success': True, 'message': 'Orchestrator started'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/file-watcher/start', methods=['POST'])
def start_file_watcher():
    """Start File Watcher"""
    try:
        file_watcher_script = VAULT_PATH / 'watchers' / 'filesystem_watcher.py'
        subprocess.Popen(
            ['python', str(file_watcher_script), '.', 'Drop_Folder'],
            cwd=str(VAULT_PATH),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        system_status['file_watcher'] = True
        log_activity('success', 'File Watcher started')
        
        return jsonify({'success': True, 'message': 'File Watcher started'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    print("=" * 60)
    print("🤖 AI Employee Dashboard Backend Server")
    print("=" * 60)
    print(f"📁 Vault Path: {VAULT_PATH}")
    print(f"📧 Gmail Watcher: {GMAIL_WATCHER_SCRIPT}")
    print(f"📊 Logs: {LOGS_PATH}")
    print("=" * 60)
    print("🌐 Dashboard URL: http://localhost:5000")
    print("=" * 60)
    
    # Ensure logs directory exists
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Start server
    app.run(debug=True, port=5000, host='0.0.0.0')
