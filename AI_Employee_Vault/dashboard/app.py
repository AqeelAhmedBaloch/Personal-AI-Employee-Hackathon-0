#!/usr/bin/env python3
"""
AI Employee Dashboard - Web Interface

Simple web dashboard to:
- View system status
- Change credentials (Gmail, LinkedIn)
- Manual controls (start/stop watchers)
- View logs
- Post to LinkedIn manually
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv, set_key

app = Flask(__name__)

# Paths
VAULT_PATH = Path(__file__).parent.parent
MCP_PATH = VAULT_PATH / 'mcp_servers'
EMAIL_MCP_PATH = MCP_PATH / 'email_mcp'
LINKEDIN_MCP_PATH = MCP_PATH / 'linkedin_mcp'
LOGS_PATH = VAULT_PATH / 'Logs'

# Environment files
EMAIL_ENV = EMAIL_MCP_PATH / '.env'
LINKEDIN_ENV = LINKEDIN_MCP_PATH / '.env'


def get_system_status():
    """Get current system status."""
    status = {
        'watchers': {
            'file_watcher': False,
            'gmail_watcher': False,
            'whatsapp_watcher': False,
        },
        'orchestrator': False,
        'linkedin_auto_post': False,
    }
    
    # Check running processes
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        if 'python.exe' in result.stdout:
            status['orchestrator'] = True
    except:
        pass
    
    return status


def get_credentials(env_file):
    """Get credentials from .env file."""
    if not env_file.exists():
        return {}
    
    load_dotenv(env_file)
    creds = {}
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                creds[key] = value
    
    return creds


def save_credentials(env_file, new_creds):
    """Save credentials to .env file."""
    env_file.parent.mkdir(parents=True, exist_ok=True)
    
    for key, value in new_creds.items():
        set_key(str(env_file), key, value)
    
    return True


def get_recent_logs(log_file, lines=50):
    """Get recent log entries."""
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            return all_lines[-lines:]
    except:
        return []


@app.route('/')
def dashboard():
    """Main dashboard."""
    status = get_system_status()
    
    # Get credential status (not actual values for security)
    email_configured = EMAIL_ENV.exists()
    linkedin_configured = LINKEDIN_ENV.exists()
    
    # Get recent logs
    orchestrator_logs = get_recent_logs(LOGS_PATH / 'orchestrator_{}.log'.format(datetime.now().strftime('%Y%m%d')))
    gmail_logs = get_recent_logs(LOGS_PATH / 'gmail_auto_reply.log')
    linkedin_logs = get_recent_logs(LINKEDIN_MCP_PATH / 'linkedin_auto_post.log')
    
    return render_template('dashboard.html',
                         status=status,
                         email_configured=email_configured,
                         linkedin_configured=linkedin_configured,
                         orchestrator_logs=orchestrator_logs,
                         gmail_logs=gmail_logs,
                         linkedin_logs=linkedin_logs,
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/credentials')
def credentials():
    """Credentials management page."""
    email_creds = get_credentials(EMAIL_ENV) if EMAIL_ENV.exists() else {}
    linkedin_creds = get_credentials(LINKEDIN_ENV) if LINKEDIN_ENV.exists() else {}
    
    return render_template('credentials.html',
                         email_creds=email_creds,
                         linkedin_creds=linkedin_creds)


@app.route('/update_email', methods=['POST'])
def update_email():
    """Update Gmail credentials."""
    new_creds = {
        'GMAIL_EMAIL_ADDRESS': request.form.get('email', ''),
        'GMAIL_APP_PASSWORD': request.form.get('password', ''),
        'DRY_RUN': request.form.get('dry_run', 'true')
    }
    
    save_credentials(EMAIL_ENV, new_creds)
    
    return jsonify({'success': True, 'message': 'Gmail credentials updated!'})


@app.route('/update_linkedin', methods=['POST'])
def update_linkedin():
    """Update LinkedIn credentials."""
    new_creds = {
        'LINKEDIN_EMAIL': request.form.get('email', ''),
        'LINKEDIN_PASSWORD': request.form.get('password', ''),
        'LINKEDIN_CLIENT_ID': request.form.get('client_id', ''),
        'LINKEDIN_CLIENT_SECRET': request.form.get('client_secret', ''),
        'LINKEDIN_ACCESS_TOKEN': request.form.get('access_token', ''),
        'DRY_RUN': request.form.get('dry_run', 'true')
    }
    
    save_credentials(LINKEDIN_ENV, new_creds)
    
    return jsonify({'success': True, 'message': 'LinkedIn credentials updated!'})


@app.route('/controls')
def controls():
    """Manual controls page."""
    return render_template('controls.html')


@app.route('/start_watcher', methods=['POST'])
def start_watcher():
    """Start a watcher."""
    watcher_type = request.form.get('type')
    
    try:
        if watcher_type == 'file':
            subprocess.Popen(['python', 'watchers/filesystem_watcher.py', '.', './Drop_Folder'],
                           cwd=str(VAULT_PATH))
        elif watcher_type == 'gmail':
            subprocess.Popen(['python', 'watchers/gmail_watcher.py', '.'],
                           cwd=str(VAULT_PATH))
        elif watcher_type == 'orchestrator':
            subprocess.Popen(['python', 'orchestrator.py', '.', '--dev-mode'],
                           cwd=str(VAULT_PATH))
        
        return jsonify({'success': True, 'message': f'{watcher_type} watcher started!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/stop_all', methods=['POST'])
def stop_all():
    """Stop all Python processes."""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True)
        return jsonify({'success': True, 'message': 'All processes stopped!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/post_linkedin', methods=['POST'])
def post_linkedin():
    """Post to LinkedIn now."""
    post_type = request.form.get('post_type', 'general')

    try:
        # Use the new simple daily post script
        result = subprocess.run(
            ['python', 'mcp_servers/linkedin_mcp/linkedin_simple_daily_post.py'],
            cwd=str(VAULT_PATH),
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Post published to LinkedIn!'})
        else:
            return jsonify({'success': False, 'message': result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'message': 'Posting timed out'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/linkedin_task_status')
def linkedin_task_status():
    """Get LinkedIn Task Scheduler status."""
    try:
        result = subprocess.run(
            ['schtasks', '/Query', '/TN', 'LinkedIn Daily Post 12PM', '/FO', 'LIST'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Parse the output
            lines = result.stdout.strip().split('\n')
            status = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    status[key.strip()] = value.strip()
            
            return jsonify({'success': True, 'task': status})
        else:
            return jsonify({'success': False, 'message': 'Task not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/run_linkedin_task_now', methods=['POST'])
def run_linkedin_task_now():
    """Run LinkedIn task immediately."""
    try:
        subprocess.run(
            ['schtasks', '/Run', '/TN', 'LinkedIn Daily Post 12PM'],
            capture_output=True,
            text=True
        )
        return jsonify({'success': True, 'message': 'LinkedIn task started!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/logs')
def logs():
    """Logs viewer page."""
    log_files = list(LOGS_PATH.glob('*.log'))
    log_files.extend(LINKEDIN_MCP_PATH.glob('*.log'))
    
    return render_template('logs.html', log_files=log_files)


@app.route('/view_log/<path:log_file>')
def view_log(log_file):
    """View specific log file."""
    full_path = Path(log_file)
    
    if not full_path.exists():
        return jsonify({'error': 'File not found'})
    
    content = get_recent_logs(full_path, lines=200)
    
    return jsonify({'content': ''.join(content)})


@app.route('/refresh_status')
def refresh_status():
    """Refresh system status."""
    status = get_system_status()
    return jsonify(status)


if __name__ == '__main__':
    # Create templates directory
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print('=' * 60)
    print('AI Employee Dashboard')
    print('=' * 60)
    print('')
    print('Open in browser:')
    print('http://localhost:5000')
    print('')
    print('Press Ctrl+C to stop')
    print('=' * 60)
    
    app.run(debug=True, port=5000)
