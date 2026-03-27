# 🚀 Quick Reference - Personal AI Employee

**Banaya Gaya:** March 27, 2026  
**Purpose:** One-page reference guide

---

## ⚡ Quick Start (2 Options)

### **Option 1: One-Click Start (Recommended)**

```bash
# AI_Employee_Vault folder mein jayein aur yeh run karein:
QUICK_START_SYSTEM.bat
```

**Yeh automatically:**
- ✅ Gmail Watcher start karega
- ✅ Dashboard start karega  
- ✅ Browser mein http://localhost:5000 khol dega

---

### **Option 2: Manual Start**

```bash
# Terminal 1 - Gmail Watcher
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py

# Terminal 2 - Dashboard
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
python app.py
```

---

## 📧 Auto-Reply Test Karna

1. **System start karein** (upar diye gaye methods se)

2. **Test email bhejein:**
   - Kisi dusre email se (Gmail, Yahoo, etc.)
   - To: `aqeelwork2026@gmail.com`
   - Subject: `Test Email`
   - Body: `Hello, testing auto-reply`

3. **Verify karein:**
   - Gmail Watcher terminal mein: `✅ Auto-reply sent to: ...`
   - Dashboard pe logs update honge
   - Aapko reply email milega

---

## 📁 Important Files & Folders

| Path | Purpose |
|------|---------|
| `AI_Employee_Vault\` | Main project folder |
| `AI_Employee_Vault\Drop_Folder\` | Yahan files daalein for processing |
| `AI_Employee_Vault\Inbox\` | Processed files yahan copy honge |
| `AI_Employee_Vault\Needs_Action\` | Pending tasks |
| `AI_Employee_Vault\Logs\` | All activity logs |
| `AI_Employee_Vault\dashboard\` | Web dashboard |
| `mcp_servers\email_mcp\.env` | Gmail credentials |

---

## 🎮 Dashboard Controls

**URL:** http://localhost:5000

| Button | Action |
|--------|--------|
| **Start Gmail Watcher** | Auto-reply system start |
| **Stop Gmail Watcher** | Auto-reply system stop |
| **Start File Watcher** | File monitoring start |
| **Start Orchestrator** | Main coordinator start |
| **Send Email** | Manual email bhejne ke liye |

---

## 🛑 System Stop Karna

### **Method 1: Taskkill (All at Once)**
```bash
taskkill /F /FI "WINDOWTITLE eq Gmail*"
taskkill /F /FI "WINDOWTITLE eq AI Employee*"
```

### **Method 2: Manual (Ctrl+C)**
1. Gmail Watcher window mein jayein → **Ctrl+C**
2. Dashboard window mein jayein → **Ctrl+C**

---

## 📊 Logs Check Karna

| Log File | Purpose |
|----------|---------|
| `Logs\gmail_auto_reply.log` | Gmail activity |
| `Logs\auto_reply_log.csv` | Email replies CSV |
| `Logs\dashboard_activity.json` | Dashboard actions |
| `Logs\watcher.log` | File watcher logs |

---

## 🔧 Common Commands

```bash
# Gmail Watcher akela start karna
python gmail_auto_reply_watcher.py

# File Watcher akela start karna
python watchers\filesystem_watcher.py

# Orchestrator start karna
python orchestrator.py . --dev-mode --interval 30

# Dashboard start karna
cd dashboard && python app.py

# All components start karna
start-all.bat

# All components stop karna
stop-all.bat
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **Dashboard nahi khul raha** | Browser mein http://localhost:5000 manually type karein |
| **Port 5000 already in use** | `netstat -ano \| findstr :5000` → Process kill karein |
| **Gmail credentials error** | `mcp_servers\email_mcp\.env` check karein |
| **Auto-reply nahi aa raha** | Logs check karein: `Logs\gmail_auto_reply.log` |
| **Module not found error** | `pip install -r requirements.txt` run karein |

---

## 📞 Help & Documentation

| Document | Location |
|----------|----------|
| **Complete Setup Guide** | `COMPLETE_SETUP_GUIDE.md` |
| **Project Status** | `PROJECT_STATUS.md` |
| **Main README** | `README.md` |
| **Gmail Setup** | `GMAIL_SETUP_GUIDE.md` |

---

## ✅ System Check Checklist

Har baar start karne se pehle verify karein:

- [ ] Python installed hai? (`python --version`)
- [ ] `.env` file mein credentials hain?
- [ ] Port 5000 free hai?
- [ ] Internet connection active hai?

---

## 🎯 Expected Behavior

Jab system properly chal raha ho:

1. ✅ **Gmail Watcher** terminal mein: `Checking Gmail...` every 60s
2. ✅ **Dashboard** http://localhost:5000 pe load ho raha ho
3. ✅ **Live Logs** update ho rahe hon
4. ✅ **Metrics** show ho rahe hon (pending tasks, emails replied, etc.)

---

## 📧 Test Email Templates

Aap in subjects se test kar sakte hain:

| Subject | Expected Reply |
|---------|---------------|
| `Invoice Question` | Invoice inquiry template |
| `Meeting Request` | Meeting availability template |
| `Need Help` | Support ticket template |
| `Hello` | General inquiry template |

---

**🎉 You're all set! Happy automating!**
