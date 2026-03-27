# 🚀 Complete Setup Guide - Personal AI Employee Hackathon-0

**Last Updated:** March 27, 2026  
**Author:** AI Assistant  
**Difficulty:** Beginner-Friendly

---

## 📋 **Table of Contents**

1. [Quick Start (3 Steps)](#quick-start)
2. [Gmail Auto-Reply Setup](#gmail-setup)
3. [Dashboard Run Karna](#dashboard-run)
4. [Full System Start](#full-system)
5. [Testing & Verification](#testing)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 **Quick Start** <a name="quick-start"></a>

Agar aap **jaldi se system start karna chahte hain**, toh yeh 3 steps follow karein:

### **Step 1: Gmail Credentials Verify Karein**

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
```

File check karein: `mcp_servers\email_mcp\.env`

```
GMAIL_EMAIL_ADDRESS=aqeelwork2026@gmail.com
GMAIL_APP_PASSWORD=hucpshwlcyxmvzgs
```

✅ **Already configured hai!** Aap directly Step 2 pe ja sakte hain.

---

### **Step 2: Dashboard Start Karein**

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
python app.py
```

Ya phir batch file run karein:

```bash
start.bat
```

**Dashboard open hoga:** http://localhost:5000

---

### **Step 3: Gmail Watcher Start Karein**

Dashboard mein **"Start Gmail Watcher"** button click karein, ya terminal mein:

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py
```

---

## 📧 **Gmail Auto-Reply Setup** <a name="gmail-setup"></a>

### **Kya Yeh Kaam Karta Hai?**

Jab bhi koi email aayega:
1. ✅ System detect karega (har 60 seconds mein check)
2. ✅ Email content analyze karega
3. ✅ Appropriate template select karega
4. ✅ Auto reply bhej dega
5. ✅ Log save karega

---

### **Configuration Verify Karna**

Already configured hai, lekin verify karna ho toh:

```bash
# .env file check karein
notepad e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\email_mcp\.env
```

**Expected content:**
```env
GMAIL_EMAIL_ADDRESS=aqeelwork2026@gmail.com
GMAIL_APP_PASSWORD=hucpshwlcyxmvzgs
DRY_RUN=false
```

---

### **Gmail App Password Kaise Generate Karein?**

Agar password change karna ho:

1. **Google Account Settings** mein jayein: https://myaccount.google.com/
2. **Security** tab click karein
3. **2-Step Verification** enable karein (agar nahi hai)
4. **App Passwords** section mein jayein: https://myaccount.google.com/apppasswords
5. **Mail** select karein aur **Windows Computer** select karein
6. **Generate** click karein
7. 16-character password copy karein (spaces ke bina)
8. `.env` file mein paste karein

---

### **Reply Templates**

System yeh templates use karta hai:

| Template | Keywords | Reply |
|----------|----------|-------|
| **invoice_inquiry** | invoice, billing, payment | Invoice response |
| **meeting_request** | meeting, call, schedule, appointment | Meeting availability |
| **support_ticket** | support, help, issue, problem, error | Support acknowledgment |
| **general_inquiry** | (default) | General thank you |

---

## 🖥️ **Dashboard Run Karna** <a name="dashboard-run"></a>

### **Method 1: Direct Python Command**

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
python app.py
```

**Output:**
```
============================================================
🤖 AI Employee Dashboard Backend Server
============================================================
📁 Vault Path: e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
📧 Gmail Watcher: ...\gmail_auto_reply_watcher.py
📊 Logs: e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs
============================================================
🌐 Dashboard URL: http://localhost:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**Browser mein open karein:** http://localhost:5000

---

### **Method 2: Batch File**

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
start.bat
```

---

### **Dashboard Features**

| Feature | Description |
|---------|-------------|
| **📊 Metrics** | Pending tasks, completed tasks, emails replied |
| **⚙️ Process Flow** | Live status of all watchers |
| **💻 Live Logs** | Real-time activity feed |
| **🎮 Controls** | Start/Stop Gmail, File Watcher, Orchestrator |
| **📧 Email Sender** | Manual email bhejne ke liye |

---

## 🔥 **Full System Start** <a name="full-system"></a>

### **All-in-One Start Script**

Agar **saare components ek saath start karna hain**:

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
start-all.bat
```

**Yeh start karega:**
- ✅ Gmail Auto-Reply Watcher
- ✅ File System Watcher
- ✅ Orchestrator
- ✅ Dashboard

---

### **Individual Components Start Karna**

#### **1. Gmail Auto-Reply Watcher**
```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py
```

#### **2. File System Watcher**
```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python watchers\filesystem_watcher.py
```

#### **3. Orchestrator**
```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python orchestrator.py . --dev-mode --interval 30
```

#### **4. Dashboard**
```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
python app.py
```

---

## ✅ **Testing & Verification** <a name="testing"></a>

### **Test 1: Email Auto-Reply**

1. **Gmail Watcher start karein:**
   ```bash
   python gmail_auto_reply_watcher.py
   ```

2. **Test email bhejein:**
   - Kisi dusre email se `aqeelwork2026@gmail.com` pe email bhejein
   - Subject: "Test Email"
   - Body: "Hello, this is a test"

3. **Verify karein:**
   - Terminal mein dekhein: `✅ Auto-reply sent to: ...`
   - Check logs: `AI_Employee_Vault\Logs\gmail_auto_reply.log`
   - Check CSV: `AI_Employee_Vault\Logs\auto_reply_log.csv`

---

### **Test 2: File Watcher**

1. **File Watcher start karein:**
   ```bash
   python watchers\filesystem_watcher.py
   ```

2. **Drop_Folder mein file daalein:**
   ```bash
   # New file create karein
   echo "Test content" > AI_Employee_Vault\Drop_Folder\test.txt
   ```

3. **Verify karein:**
   - Check `Inbox/` - file copy hoga
   - Check `Needs_Action/` - action file create hoga
   - Check `Plans/` - plan generate hoga

---

### **Test 3: Dashboard**

1. **Dashboard start karein:**
   ```bash
   cd dashboard
   python app.py
   ```

2. **Browser mein open karein:** http://localhost:5000

3. **Verify karein:**
   - ✅ Metrics show ho rahe hain
   - ✅ Process flow dikh raha hai
   - ✅ Live logs update ho rahe hain
   - ✅ Buttons kaam kar rahe hain

---

## 🐛 **Troubleshooting** <a name="troubleshooting"></a>

### **Problem 1: Gmail Credentials Error**

**Error:**
```
Gmail credentials not configured
```

**Solution:**
```bash
# .env file verify karein
notepad AI_Employee_Vault\mcp_servers\email_mcp\.env

# Ensure yeh lines hain:
GMAIL_EMAIL_ADDRESS=aqeelwork2026@gmail.com
GMAIL_APP_PASSWORD=hucpshwlcyxmvzgs
```

---

### **Problem 2: Dashboard Port Already in Use**

**Error:**
```
OSError: [WinError 10048] Only one usage of each socket address is normally permitted
```

**Solution:**
```bash
# Port 5000 pe running process dhundhein
netstat -ano | findstr :5000

# Process kill karein (PID replace karein)
taskkill /PID <PID> /F

# Ya phir different port use karein
python app.py --port 5001
```

---

### **Problem 3: Python Modules Missing**

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Dashboard requirements install karein
cd AI_Employee_Vault\dashboard
pip install -r requirements.txt

# Main requirements install karein
cd AI_Employee_Vault
pip install -r requirements.txt
```

---

### **Problem 4: Gmail IMAP Error**

**Error:**
```
imaplib.IMAP4.error: b'[AUTHENTICATION FAILED]'
```

**Solution:**
1. **App Password verify karein** - 16 characters, no spaces
2. **2-Step Verification enable karein** - https://myaccount.google.com/security
3. **Less Secure Apps** - Ab kaam nahi karte, App Password hi use karein

---

### **Problem 5: Auto-Reply Nahi Bhej Raha**

**Checklist:**
- ✅ Gmail Watcher running hai?
- ✅ `.env` file mein credentials sahi hain?
- ✅ Email unread hai? (pehle se read emails skip hote hain)
- ✅ Logs check karein: `Logs\gmail_auto_reply.log`

**Debug Mode:**
```bash
# Manual test karein
python -c "from dotenv import load_dotenv; import os; load_dotenv('mcp_servers/email_mcp/.env'); print(os.getenv('GMAIL_EMAIL_ADDRESS'))"
```

---

## 📊 **System Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    EMAIL SENDER                        │
│                  (External Gmail User)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              GMAIL AUTO-REPLY WATCHER                   │
│         (Checks every 60 seconds for new emails)        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              EMAIL ANALYZER                             │
│         (Determines template based on content)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AUTO-REPLY SENDER                          │
│         (Sends reply using Gmail SMTP)                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LOGGING SYSTEM                             │
│         (Saves to CSV and log files)                    │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              DASHBOARD (Flask App)                      │
│         (Real-time monitoring & control)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 **Quick Commands Reference**

| Command | Description |
|---------|-------------|
| `python gmail_auto_reply_watcher.py` | Start Gmail monitoring |
| `python watchers\filesystem_watcher.py` | Start file monitoring |
| `python orchestrator.py . --dev-mode` | Start orchestrator |
| `cd dashboard && python app.py` | Start dashboard |
| `start-all.bat` | Start all components |
| `stop-all.bat` | Stop all components |

---

## 📞 **Support & Resources**

| Resource | Link |
|----------|------|
| **Main Documentation** | `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` |
| **Project Status** | `PROJECT_STATUS.md` |
| **Gmail Setup Guide** | `GMAIL_SETUP_GUIDE.md` |
| **Dashboard README** | `dashboard\README.md` |

---

## ✅ **Completion Checklist**

- [ ] ✅ Gmail credentials configured
- [ ] ✅ Dashboard running (http://localhost:5000)
- [ ] ✅ Gmail Watcher running
- [ ] ✅ Test email bheja aur auto-reply receive hua
- [ ] ✅ Logs verify kiye
- [ ] ✅ Dashboard controls test kiye

---

**🎉 Congratulations! Aapka Personal AI Employee ab kaam kar raha hai!**

Agar koi problem ho toh **Troubleshooting** section check karein ya logs review karein.
