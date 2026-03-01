# LinkedIn Daily Auto-Post - Setup Guide

## 🎯 Goal
```
Rozana 9 AM automatic LinkedIn par AI post publish ho
```

---

## 📋 **Setup Steps:**

---

### **Step 1: LinkedIn API Credentials (30 minutes)**

1. **Open:** https://www.linkedin.com/developers/
2. **Sign In:** aqeelwork2026@gmail.com
3. **Create App:** https://www.linkedin.com/developers/apps
4. **Get Credentials:**
   - Client ID
   - Client Secret
   - Access Token (generate via OAuth)

---

### **Step 2: Configure .env File (2 minutes)**

**File Location:**
```
D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp\.env
```

**Add This:**
```env
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_ACCESS_TOKEN=your_access_token_here
```

**Save**

---

### **Step 3: Test Script (1 minute)**

**Command:**
```bash
cd D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp
python linkedin_daily_auto_post.py
```

**Expected Output:**
```
============================================================
LinkedIn Daily AI Auto-Post
============================================================

Day X: Posting to LinkedIn...

============================================================
Status: success
Message: Post published successfully!

✅ Daily AI post published!
```

---

### **Step 4: Windows Task Scheduler Setup (5 minutes)**

#### **Option A: Manual Setup**

1. **Open Task Scheduler:**
   - Press `Windows + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create Basic Task:**
   - Right-click "Task Scheduler Library"
   - Select: "Create Basic Task"

3. **Name:**
   ```
   Name: LinkedIn Daily AI Post
   Description: Posts daily AI content to LinkedIn at 9 AM
   ```

4. **Trigger:**
   ```
   Select: Daily
   Start: 9:00:00 AM
   Recur: Every 1 day
   ```

5. **Action:**
   ```
   Select: Start a program
   Program/script: D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp\run_daily_post.bat
   Start in: D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp
   ```

6. **Finish**

7. **Properties Setup:**
   - Right-click task → Properties
   - ✅ "Run whether user is logged on or not"
   - ✅ "Run with highest privileges"
   - Settings tab:
     - ✅ "Allow task to be run on demand"
     - ✅ "Run task as soon as possible after scheduled start"
     - ✅ "Stop task if it runs longer than: 1 hour"

8. **OK** → Enter password

---

#### **Option B: Automatic Setup (Run This Command)**

**PowerShell (Admin) mein yeh run karein:**

```powershell
$taskName = "LinkedIn Daily AI Post"
$scriptPath = "D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp\run_daily_post.bat"
$startTime = "09:00"

# Create task action
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create daily trigger at 9 AM
$trigger = New-ScheduledTaskTrigger -Daily -At $startTime

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Posts daily AI content to LinkedIn automatically at 9 AM every day"
```

---

### **Step 5: Verify Task (1 minute)**

**Check Task:**
```powershell
Get-ScheduledTask -TaskName "LinkedIn Daily AI Post"
```

**Expected Output:**
```
TaskPath                                    : \
TaskName                                    : LinkedIn Daily AI Post
State                                       : Ready
```

**Test Run:**
```powershell
Start-ScheduledTask -TaskName "LinkedIn Daily AI Post"
```

**Check History:**
```powershell
Get-ScheduledTaskInfo -TaskName "LinkedIn Daily AI Post"
```

---

## ✅ **Done!**

**Ab kya hoga:**
```
✅ Rozana 9 AM automatic post publish hoga
✅ 30 days of unique AI content
✅ No manual intervention needed
✅ Full audit trail in logs
```

---

## 📊 **Content Schedule:**

| Day | Topic | Example |
|-----|-------|---------|
| 1 | AI Transformation | AI is transforming work |
| 2 | AI Facts | Did you know AI can... |
| 3 | Monday Motivation | Automation quote |
| 4 | AI Tips | Start small with automation |
| 5 | Success Story | This week AI saved... |
| 6 | Tech Education | What is MCP? |
| 7 | Sunday Learning | AI terms |
| ... | ... | ... |
| 30 | Month Review | 30 days summary |

---

## 🔧 **Maintenance:**

### **Monthly:**
- ✅ Check task is running
- ✅ Verify posts are publishing
- ✅ Review access token expiry (60 days)

### **Token Refresh (Every 60 days):**
1. Generate new access token
2. Update .env file
3. Done!

---

## 📝 **Log Files:**

**Location:**
```
D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\linkedin_auto_post.log
```

**Content:**
```
2026-03-01 09:00:00 - Post published successfully
2026-03-02 09:00:00 - Post published successfully
...
```

---

## 🎯 **Quick Commands:**

### **Test Post Manually:**
```bash
cd D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\linkedin_mcp
python linkedin_daily_auto_post.py
```

### **Check Task Status:**
```powershell
Get-ScheduledTask -TaskName "LinkedIn Daily AI Post" | Select-Object TaskName, State
```

### **Run Task Now:**
```powershell
Start-ScheduledTask -TaskName "LinkedIn Daily AI Post"
```

### **View Task History:**
```powershell
Get-ScheduledTaskInfo -TaskName "LinkedIn Daily AI Post"
```

---

## ⚠️ **Troubleshooting:**

### **Task Not Running:**
```powershell
# Check if task exists
Get-ScheduledTask -TaskName "LinkedIn Daily AI Post"

# Check last run result
Get-ScheduledTaskInfo -TaskName "LinkedIn Daily AI Post" | Select-Object LastRunTime, LastTaskResult
```

### **Post Failed:**
```bash
# Check .env credentials
# Test manually
python linkedin_daily_auto_post.py
```

### **Token Expired:**
```bash
# Generate new token from LinkedIn Developer Dashboard
# Update .env file
# Task will work automatically
```

---

## 🏆 **Complete Setup Time:**

```
Step 1: API Credentials    - 30 minutes
Step 2: Configure .env     - 2 minutes
Step 3: Test Script        - 1 minute
Step 4: Task Scheduler     - 5 minutes
Step 5: Verify             - 1 minute
─────────────────────────────────────
TOTAL:                     ~40 minutes (one-time)
```

**After Setup:**
```
Daily Time: 0 minutes (fully automatic!)
```

---

## ✅ **Ready to Start!**

**Next Step:** LinkedIn Developer Account banayein!

Link: https://www.linkedin.com/developers/
