# 🚀 AI Employee - Complete Running Guide

**Date:** March 2, 2026  
**Version:** 1.0

---

## ⚠️ **IMPORTANT: HTML Dashboard Sirf DISPLAY Hai!**

### ❌ **HTML File Open Karne Se Yeh NAHI Hoga:**

```
❌ Gmail auto-reply automatically start NAHI hoga
❌ LinkedIn post automatically publish NAHI hogi
❌ File watcher automatically run NAHI hoga
❌ Orchestrator automatically start NAHI hoga
```

### ✅ **HTML Dashboard Kya Hai:**

```
✅ Yeh sirf ek DISPLAY hai (jaise TV screen)
✅ Real-time status dikhta hai
✅ Logs dikhte hain
✅ Buttons hain (lekin backend connect nahi hai)
✅ Aap ko Python scripts alag se run karni hongi
```

---

## 🎯 **COMPLETE SETUP - 3 Steps:**

### **Step 1: Start All Services (Ek Hi Click Mein)**

**File:** `AI_Employee_Vault/start-all.bat`

**Kaise Run Karein:**
1. `AI_Employee_Vault` folder open karein
2. **`start-all.bat`** par double-click karein
3. Sab kuch automatically start ho jayega!

**Kya Hoga:**
```
✅ File Watcher start hoga (Drop_Folder monitor karega)
✅ Gmail Watcher start hoga (har 60 seconds mein check karega)
✅ Orchestrator start hoga (har 30 seconds mein coordinate karega)
✅ AI Dashboard browser mein open hoga
```

---

### **Step 2: LinkedIn Task Check Karein**

**Task Scheduler already setup hai!**

**Check kaise karein:**
```bash
# PowerShell mein:
Get-ScheduledTask -TaskName "LinkedIn Daily Post 12PM"
```

**Expected Output:**
```
TaskName : LinkedIn Daily Post 12PM
State    : Ready
Next Run : 03-Mar-2026 12:00:00 PM
```

---

### **Step 3: Dashboard Mein Sab Kuch Dekhein**

**Dashboard automatically open ho jayega!**

**URL:**
```
file:///E:/Hackathon-Q4/Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard/ai-dashboard.html
```

**Kya dikhega:**
- ✅ Live system status
- ✅ Real-time logs
- ✅ Process flow visualization
- ✅ Activity feed
- ✅ Metrics (pending tasks, completed, etc.)

---

## 📋 **MANUAL METHOD (Agar Batch File Na Chal Jaye):**

### **Terminal 1: File Watcher**
```bash
cd E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python watchers/filesystem_watcher.py . Drop_Folder
```

### **Terminal 2: Gmail Watcher**
```bash
cd E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py 60
```

### **Terminal 3: Orchestrator**
```bash
cd E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python orchestrator.py . --dev-mode --interval 30
```

### **Browser: Dashboard**
```
Double-click: AI_Employee_Vault/dashboard/ai-dashboard.html
```

---

## 🛑 **STOP Kaise Karein:**

### **Option 1: Batch File (Easy)**
```
Double-click: stop-all.bat
```

### **Option 2: Manual**
```bash
# Task Manager open karein (Ctrl+Shift+Esc)
# Python processes dhund kar end karein
```

### **Option 3: Command**
```bash
taskkill /F /IM python.exe
```

---

## ✅ **DAILY ROUTINE:**

### **Subah (9:00 AM):**
1. **Run:** `start-all.bat`
2. **Check:** Dashboard open ho gaya
3. **Verify:** Teenon processes chal rahe hain

### **Dophar (12:00 PM):**
- **Automatic:** LinkedIn post publish hogi
- **Check:** Dashboard mein log dikhega

### **Shaam (6:00 PM):**
1. **Run:** `stop-all.bat` (agar band karna ho)
2. **Ya:** Chhor dein (background mein chalta rahega)

---

## 🔧 **TROUBLESHOOTING:**

### **Problem: Python Not Found**
**Solution:**
```bash
# Python install karein: https://python.org
# Version: Python 3.13+
```

### **Problem: Gmail Credentials Error**
**Solution:**
```bash
# .env file check karein:
AI_Employee_Vault/mcp_servers/email_mcp/.env

# Yeh fields bharein:
GMAIL_EMAIL_ADDRESS=aqeelwork2026@gmail.com
GMAIL_APP_PASSWORD=your-app-password-here
```

### **Problem: LinkedIn Post Nahi Hui**
**Solution:**
```bash
# Task Scheduler check karein:
Get-ScheduledTask -TaskName "LinkedIn Daily Post 12PM"

# Manually run karein:
schtasks /Run /TN "LinkedIn Daily Post 12PM"
```

### **Problem: Dashboard Open Nahi Hua**
**Solution:**
```bash
# Directly browser mein open karein:
file:///E:/Hackathon-Q4/Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard/ai-dashboard.html
```

---

## 📊 **WHAT'S WORKING:**

| Feature | Status | How to Test |
|---------|--------|-------------|
| **File Watcher** | ✅ Working | Drop a file in `Drop_Folder/` |
| **Gmail Auto-Reply** | ✅ Working | Send email to aqeelwork2026@gmail.com |
| **LinkedIn Auto-Post** | ✅ Working | Wait for 12:00 PM or run task manually |
| **Orchestrator** | ✅ Working | Check logs in dashboard |
| **Dashboard** | ✅ Working | Open ai-dashboard.html |
| **Task Scheduler** | ✅ Working | Check in Windows Task Scheduler |

---

## 🎯 **QUICK COMMANDS:**

### **Start Everything:**
```bash
start-all.bat
```

### **Stop Everything:**
```bash
stop-all.bat
```

### **Check LinkedIn Task:**
```bash
schtasks /Query /TN "LinkedIn Daily Post 12PM"
```

### **Run LinkedIn Task Now:**
```bash
schtasks /Run /TN "LinkedIn Daily Post 12PM"
```

### **Check Python Processes:**
```bash
tasklist | findstr python
```

---

## 📝 **FOLDER STRUCTURE:**

```
AI_Employee_Vault/
├── start-all.bat          ← START HERE!
├── stop-all.bat           ← Stop all processes
├── dashboard/
│   ├── ai-dashboard.html  ← Beautiful AI dashboard
│   └── index.html         ← Simple dashboard
├── watchers/
│   ├── filesystem_watcher.py
│   └── gmail_auto_reply_watcher.py
├── orchestrator.py
├── Drop_Folder/           ← Files yahan daalein
├── Inbox/                 ← Files yahan copy hongi
├── Needs_Action/          ← Action files yahan bangege
├── Plans/                 ← Plans yahan bangege
└── Logs/                  ← Logs yahan save honge
```

---

## 🎉 **COMPLETE WORKFLOW:**

```
1. Run: start-all.bat
   ↓
2. File Watcher starts → Monitors Drop_Folder
   ↓
3. Gmail Watcher starts → Checks email every 60s
   ↓
4. Orchestrator starts → Coordinates everything every 30s
   ↓
5. Dashboard opens → Shows live status
   ↓
6. At 12:00 PM → LinkedIn post publishes automatically
   ↓
7. Everything logs to dashboard → You can see everything!
```

---

## ✅ **FINAL CHECKLIST:**

- [ ] Python 3.13+ installed
- [ ] Gmail credentials configured in `.env`
- [ ] Task Scheduler setup (LinkedIn Daily Post 12PM)
- [ ] `start-all.bat` run kiya
- [ ] Dashboard browser mein open hua
- [ ] Teenon processes chal rahe hain (check taskbar)

---

**Last Updated:** March 2, 2026 - 3:00 PM  
**Next Review:** Daily before starting

---

**🚀 Ready to start? Run `start-all.bat` now!**
