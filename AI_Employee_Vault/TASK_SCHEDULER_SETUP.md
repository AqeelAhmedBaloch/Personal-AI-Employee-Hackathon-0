# 📅 Task Scheduler Setup Guide

## Weekly CEO Briefing - Every Monday at 8:00 AM

### Step 1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### Step 2: Create Basic Task
1. Click **Action** → **Create Basic Task**
2. Name: `CEO Briefing - Monday 8AM`
3. Description: `Generate weekly CEO briefing report`
4. Click **Next**

### Step 3: Set Trigger
1. Select **Weekly**
2. Click **Next**
3. Check **Monday**
4. Set time: **8:00 AM**
5. Recur every: **1** weeks
6. Click **Next**

### Step 4: Set Action
1. Select **Start a program**
2. Click **Next**
3. Program/script: `python`
4. Add arguments: 
   ```
   "E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\ceo_briefing.py" "E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault"
   ```
5. Start in:
   ```
   E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
   ```
6. Click **Next**

### Step 5: Finish
1. Check **Open Properties** before clicking Finish
2. Click **Finish**

### Step 6: Advanced Settings
In Properties dialog:
1. **General** tab:
   - ☑ Run whether user is logged on or not
   - ☑ Run with highest privileges
   
2. **Conditions** tab:
   - ☐ Start the task only if computer is on AC power (uncheck for laptop)
   - ☑ Wake the computer to run this task (optional)
   
3. **Settings** tab:
   - ☑ Allow task to be run on demand
   - ☑ If task fails, restart every: **5 minutes**
   - Attempt to restart: **3** times
   - ☑ Stop task if runs longer than: **1 hour**

4. Click **OK**
5. Enter your Windows password if prompted

---

## Test the Task

1. Find your task in Task Scheduler Library
2. Right-click → **Run**
3. Check `/Briefings` folder for output

---

## LinkedIn Daily Post - Already Configured

The LinkedIn Daily Post task is already configured for 12:00 PM daily.

To verify:
1. Open Task Scheduler
2. Look for: **LinkedIn Daily Post 12PM**
3. Should show trigger: **Daily at 12:00 PM**

---

## All Scheduled Tasks

| Task | Schedule | Script | Status |
|------|----------|--------|--------|
| LinkedIn Daily Post | Daily 12:00 PM | `linkedin_daily_auto_post.py` | ✅ Configured |
| CEO Briefing | Monday 8:00 AM | `ceo_briefing.py` | ⏳ Setup Required |
| Daily Briefing | Daily 8:00 AM | `daily_briefing.py` | ⏳ Optional |

---

## Troubleshooting

### Task doesn't run
- Check **History** tab in Task Scheduler
- Verify Python is in PATH
- Check user permissions

### Task runs but script fails
- Verify file paths are absolute
- Check Python version (`python --version`)
- Review script logs in `/Logs` folder

### Task runs but no output
- Check working directory in task properties
- Verify vault path is correct
- Look for Python errors in Event Viewer

---

## Export Task (Backup)

To backup your task configuration:
1. Right-click task
2. **Export...**
3. Save as `.xml` file
4. Store in safe location

---

## Import Task (Restore)

To restore from backup:
1. **Action** → **Import Task List**
2. Select `.xml` file
3. Review settings
4. Click **OK**

---

*Guide for Personal AI Employee Hackathon-0*
