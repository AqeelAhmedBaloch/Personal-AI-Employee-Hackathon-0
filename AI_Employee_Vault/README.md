# Personal AI Employee Hackathon-0 - Bronze Tier

> **Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026**

A local-first, agent-driven Personal AI Employee Hackathon-0 system built with Qwen Code and Obsidian.

---

## 🚀 Quick Start (Sab Se Pehle Yeh Karein!)

**Sab se aasan tareeqa:**

1. **`STEP_BY_STEP.bat`** par double-click karein
2. Har step ke baad **Enter** dabayein
3. Yeh file aap ko guide karegi!

**Ya phir:**

1. **`run.bat`** par double-click karein
2. Sab kuch automatically start ho jayega!

---

## Overview

This Bronze Tier implementation provides the foundation for your Personal AI Employee Hackathon-0:

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ File System Watcher (monitors drop folder for new files)
- ✅ Orchestrator (coordinates between watchers and Qwen Code)
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ Human-in-the-loop approval workflow

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   File Watcher  │────▶│   Orchestrator  │────▶│   Qwen Code     │
│   (watchdog)    │     │   (coordinator) │     │   (reasoning)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Obsidian Vault │
                        │  - Dashboard.md │
                        │  - Handbook.md  │
                        └─────────────────┘
```

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.13+ | Watcher scripts & orchestration |
| Qwen Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Node.js | v24+ LTS | Future MCP servers |

## Installation

### 1. Install Python Dependencies

```bash
cd AI_Employee_Vault
pip install -r requirements.txt
```

### 2. Verify Qwen Code Installation

```bash
qwen --version
```

If not installed, follow the [Qwen Code installation guide](https://qwen.ai/).

### 3. Open Vault in Obsidian

Open the `AI_Employee_Vault` folder in Obsidian to view the dashboard and handbook.

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time status dashboard
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Business objectives
├── requirements.txt          # Python dependencies
├── orchestrator.py           # Main orchestration process
├── watchers/
│   ├── base_watcher.py       # Base class for all watchers
│   └── filesystem_watcher.py # File system watcher (Bronze tier)
├── Inbox/                    # Dropped files stored here
├── Needs_Action/             # Pending action files
├── Plans/                    # Qwen-generated plans
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions (move here to execute)
├── Rejected/                 # Rejected actions
├── Done/                     # Completed actions
├── Logs/                     # Audit logs
├── Accounting/               # Financial records
└── Briefings/                # CEO briefings
```

## Usage

### 🎯 Quick Method (Recommended!)

**Start karne ke liye:**

```bash
# Bas is file par double-click karein:
run.bat
```

**Stop karne ke liye:**

```bash
# Is file par double-click karein:
stop.bat
```

### Step-by-Step Method

The watcher monitors a drop folder for new files:

```bash
# Terminal 1: Start the file watcher
cd AI_Employee_Vault
python watchers/filesystem_watcher.py . ./Drop_Folder
```

This creates a `Drop_Folder` directory. Any file dropped there will trigger an action file.

### Start the Orchestrator

The orchestrator coordinates between watchers and Qwen Code:

```bash
# Terminal 2: Start the orchestrator
cd AI_Employee_Vault
python orchestrator.py . --dev-mode
```

**Dev Mode:** By default, runs in development mode (dry-run for external actions).

### Test the System

1. **Drop a file** into the `Drop_Folder`:
   ```bash
   echo "Test content" > Drop_Folder/test_document.txt
   ```

2. **Watcher detects** the file and creates an action file in `Needs_Action/`

3. **Review the action file** in `Needs_Action/FILE_test_document_*.md`

4. **Process with Qwen Code** (manual for Bronze tier):
   ```bash
   qwen -c "Process all files in Needs_Action folder. Follow Company_Handbook.md rules."
   ```

5. **Move to Done** after processing:
   ```bash
   mv Needs_Action/FILE_*.md Done/
   ```

### Human-in-the-Loop Approval

For sensitive actions, Qwen creates approval request files:

1. File appears in `Pending_Approval/`
2. Review the requested action
3. **To approve:** Move file to `Approved/`
4. **To reject:** Move file to `Rejected/`

The orchestrator automatically processes files in `Approved/`.

## Configuration

### Environment Variables

Create a `.env` file (never commit to git):

```bash
# .env - NEVER COMMIT
DEV_MODE=true
LOG_LEVEL=INFO
```

### Company Handbook

Edit `Company_Handbook.md` to customize:
- Communication rules
- Payment thresholds
- Escalation rules
- Security policies

### Dashboard

The `Dashboard.md` is automatically updated by the orchestrator with:
- Pending task counts
- Approval queue status
- Recent activity
- Revenue tracking

## Development Mode

By default, the system runs in **development mode**:

- All external actions are logged but not executed
- Extra verbose logging enabled
- Safe for testing and learning

To disable dev mode (for production use):

```bash
python orchestrator.py . --no-dev-mode
```

⚠️ **Warning:** Only disable dev mode after thorough testing!

## Logging

Logs are stored in `Logs/`:

- `orchestrator_YYYYMMDD.log` - Orchestrator activity
- `watcher_filesystemwatcher.log` - File watcher activity
- `YYYY-MM-DD.json` - Daily audit log (JSON format)

## Troubleshooting

### Watcher Not Detecting Files

1. Check the watcher is running: `ps aux | grep filesystem_watcher`
2. Verify drop folder path is correct
3. Check watcher logs: `Logs/watcher_filesystemwatcher.log`

### Orchestrator Not Processing

1. Ensure orchestrator is running
2. Check for Python errors in logs
3. Verify Qwen Code is installed: `qwen --version`

### Files Not Moving to Done

1. Check file permissions
2. Verify folder structure exists
3. Review orchestrator logs for errors

## Next Steps (Silver Tier)

After mastering Bronze tier, add:

1. **Gmail Watcher** - Monitor email inbox
2. **WhatsApp Watcher** - Monitor WhatsApp messages
3. **MCP Server** - Enable external actions (send emails, etc.)
4. **Scheduled Tasks** - Cron-based daily briefings
5. **Plan.md Generation** - Qwen creates detailed plans

## Security Notes

- Never store credentials in vault files
- Use environment variables for API keys
- Keep `.env` file out of version control
- Review all actions in dev mode before production
- Regularly rotate credentials

## Resources

- [Main Hackathon Document](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code Documentation](https://qwen.ai/)
- [Obsidian Documentation](https://help.obsidian.md)
- [Watchdog Documentation](https://pypi.org/project/watchdog/)

## License

This project is part of the Personal AI Employee Hackathon 0.

---

*Built with ❤️ for the Personal AI Employee Hackathon 0*
