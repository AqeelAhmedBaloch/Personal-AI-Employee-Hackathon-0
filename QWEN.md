# Personal AI Employee Hackathon 0

## Project Overview

This is a **hackathon project** for building a "Digital FTE" (Full-Time Equivalent) — an autonomous AI employee that manages personal and business affairs 24/7. The architecture is **local-first, agent-driven, and human-in-the-loop**.

### Core Concept

The AI Employee uses:
- **Claude Code** as the reasoning engine and executor
- **Obsidian** (Markdown) as the dashboard and long-term memory
- **Python Watcher scripts** as sensors (monitoring Gmail, WhatsApp, filesystems)
- **MCP (Model Context Protocol) servers** as hands for external actions

### Architecture: Perception → Reasoning → Action

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Perception    │────▶│   Reasoning     │────▶│     Action      │
│   (Watchers)    │     │  (Claude Code)  │     │   (MCP Servers) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
  - Gmail Watcher         - Reads vault           - Email MCP
  - WhatsApp Watcher      - Creates Plan.md       - Browser MCP
  - File Watcher          - Ralph Wiggum loop     - Payment MCP
  - Finance Watcher       - Human-in-loop         - Calendar MCP
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Watchers** | Python scripts monitoring inputs, creating `.md` files in `/Needs_Action` |
| **Ralph Wiggum Loop** | Stop hook keeping Claude working until tasks complete |
| **Human-in-the-Loop** | Sensitive actions require approval via file movement |
| **CEO Briefing** | Autonomous weekly business audit with revenue/bottleneck reports |
| **Tiered Progression** | Bronze → Silver → Gold → Platinum achievement levels |

## Project Structure

```
Personal-AI-Employee-Hackathon-0/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main documentation
├── skills-lock.json          # Skill dependencies
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/  # Browser automation skill
│           ├── SKILL.md
│           ├── scripts/
│           │   ├── mcp-client.py      # MCP client for browser control
│           │   ├── start-server.sh    # Start Playwright MCP server
│           │   ├── stop-server.sh     # Stop Playwright MCP server
│           │   └── verify.py          # Server verification
│           └── references/
│               └── playwright-tools.md
└── .git/
```

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |
| GitHub Desktop | Latest | Version control |

## Building & Running

### Start Playwright MCP Server (for browser automation)

```bash
# Start the browser automation server
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Verify it's running
python3 .qwen/skills/browsing-with-playwright/scripts/verify.py

# Stop when done
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
```

### Typical Workflow

1. **Set up Obsidian Vault** with folders: `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`, `/Pending_Approval`
2. **Create Dashboard.md** and `Company_Handbook.md` in vault root
3. **Run Watcher scripts** (Gmail, WhatsApp, File monitoring)
4. **Trigger Claude Code** to process `/Needs_Action` folder
5. **Review approval requests** in `/Pending_Approval`
6. **Move approved files** to `/Approved` for execution

### Ralph Wiggum Loop (Autonomous Task Completion)

```bash
# Start a Ralph loop for autonomous processing
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

## Development Conventions

### File Naming Patterns

| Pattern | Purpose |
|---------|---------|
| `*_watcher.py` | Python scripts monitoring external inputs |
| `*_mcp.py` | MCP server implementations |
| `*.md` in `/Needs_Action/` | Actionable items for Claude |
| `Plan.md` | Claude-generated task breakdown |
| `APPROVAL_*.md` | Human approval requests |

### Human-in-the-Loop Pattern

For sensitive actions (payments, sending messages):

1. Claude creates `APPROVAL_*.md` in `/Pending_Approval/`
2. User reviews and moves file to `/Approved/` or `/Rejected/`
3. Orchestrator executes approved actions via MCP

### Watcher Script Template

```python
from base_watcher import BaseWatcher

class MyWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Return list of new items to process
        pass
    
    def create_action_file(self, item) -> Path:
        # Create .md file in Needs_Action folder
        pass
```

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hrs | Obsidian vault, 1 watcher, basic Claude integration |
| **Silver** | 20-30 hrs | 2+ watchers, MCP server, approval workflow, scheduling |
| **Gold** | 40+ hrs | Full integration, Odoo accounting, multiple MCPs, Ralph loop |
| **Platinum** | 60+ hrs | Cloud deployment, work-zone specialization, A2A upgrade |

## Available Skills

- **browsing-with-playwright**: Browser automation via Playwright MCP
  - Navigate websites, fill forms, click elements
  - Take screenshots, extract data
  - Use for web scraping, UI testing, form submission

## Resources

- **Main Documentation**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Wednesday Research Meetings**: Zoom link in main doc (Wed 10:00 PM)
- **Ralph Wiggum Plugin**: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum

## Notes

- This is an **intermediate-level project** requiring CLI comfort and API familiarity
- All AI functionality should be implemented as [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Security rule: Never sync secrets (.env, tokens, WhatsApp sessions, banking credentials)
