# 🚀 Dashboard Setup Guide - Real-Time Email Activity

## ✨ Features

Jab aap dashboard run karenge, yeh automatically:

1. **✅ Auto-Start Services:**
   - Gmail Watcher (auto-reply)
   - File Watcher (Drop_Folder monitoring)
   - Orchestrator (task coordination)

2. **📧 Real-Time Email Tracking:**
   - Jab email aata hai → Dashboard pe show hota hai
   - Jab auto-reply bheja jata hai → Live update
   - Email count aur reply count real-time

3. **📊 Live Status:**
   - Kaunse services chal rahe hain
   - Aaj kitne emails process huye
   - Kitne auto-replies bheje gaye

---

## 📋 Setup Steps

### **Step 1: Install Dependencies**

```bash
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard

# Install Flask backend
pip install flask flask-cors python-dotenv
```

### **Step 2: Run Dashboard**

**Option A: Batch File (Recommended)**

```bash
# Double-click karein
start-dashboard.bat
```

**Option B: Manual Command**

```bash
cd AI_Employee_Vault/dashboard
python app.py
```

### **Step 3: Dashboard Open Hoga**

Browser mein automatically open hoga:
```
http://localhost:5000
```

---

## 🎯 Kya Hoga Jab Dashboard Run Hoga?

### **1. Backend Server Start Hoga**

```
============================================
🤖 AI Employee Dashboard Backend Server
============================================
📁 Vault Path: e:\...\AI_Employee_Vault
📧 Gmail Watcher: ...\gmail_auto_reply_watcher.py
📊 Logs: ...\Logs
============================================
🌐 Dashboard URL: http://localhost:5000
============================================
```

### **2. Services Auto-Start Hongge**

Dashboard terminal mein dekhenge:

```
[12:00:00] 🚀 Connecting to backend server...
[12:00:01] ✅ Connected to backend server!
[12:00:02] 🔄 Auto-starting services...
[12:00:03] 📧 Starting Gmail Watcher...
[12:00:04] ✅ Gmail Watcher started!
[12:00:05] 📁 Starting File Watcher...
[12:00:06] ✅ File Watcher started!
[12:00:07] 🎯 Starting Orchestrator...
[12:00:08] ✅ Orchestrator started!
[12:00:09] ✅ All services started automatically!
```

### **3. Real-Time Activity Show Hogi**

Jab bhi:

**Email Aata Hai:**
```
[12:05:00] 📧 New email received from client@example.com
```

**Auto Reply Bheja Jata Hai:**
```
[12:05:03] ✅ Auto-reply sent to client@example.com
```

**Gmail Check Hota Hai:**
```
[12:06:00] 📧 Gmail: Checking for new emails...
[12:06:02] ℹ️ Checked Gmail - 2 unread emails
```

---

## 📊 Dashboard Features

### **Live Status Cards**

| Status | Shows |
|--------|-------|
| 📧 Gmail Watcher | 🟢 Running / 🔴 Stopped |
| 📁 File Watcher | 🟢 Running / 🔴 Stopped |
| 🎯 Orchestrator | 🟢 Running / 🔴 Stopped |

### **Email Counters**

- **Emails Processed Today:** Total emails received
- **Auto-Replies Sent Today:** Total replies bheje gaye

### **Activity Terminal**

Real-time scroll hoti hai:
- Email receive
- Auto-reply sent
- File detected
- Service status

---

## 🧪 Test Karein

### **Test Email Bhejein:**

1. `aqeelwork2026@gmail.com` par email bhejein
2. Subject: `Test Email for Auto-Reply`
3. 60 seconds mein dashboard pe dekhenge:

```
[12:30:00] 📧 New email received from your-email@gmail.com
[12:30:03] ✅ Auto-reply sent to your-email@gmail.com
```

### **Manual Email Bhejein:**

Dashboard pe "Send Email" button click kar ke test email bhej sakte hain.

---

## ⚙️ API Endpoints

Backend yeh APIs provide karta hai:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Current system status |
| `/api/activity` | GET | Recent activity logs |
| `/api/gmail/start` | POST | Start Gmail Watcher |
| `/api/gmail/stop` | POST | Stop Gmail Watcher |
| `/api/email/send` | POST | Send manual email |
| `/api/orchestrator/start` | POST | Start Orchestrator |
| `/api/file-watcher/start` | POST | Start File Watcher |

---

## 🛠️ Troubleshooting

### **Problem: Backend start nahi ho raha**

**Solution:**
```bash
# Dependencies reinstall karein
pip uninstall flask flask-cors python-dotenv
pip install flask flask-cors python-dotenv

# Phir try karein
python app.py
```

### **Problem: Dashboard pe "Backend not available" aa raha hai**

**Solution:**
1. Check karein backend terminal chal raha hai ya nahi
2. `http://localhost:5000` open karein
3. Backend terminal mein errors check karein

### **Problem: Auto-start kaam nahi kar raha**

**Solution:**
1. Dashboard pe manually "Start Gmail Watcher" button click karein
2. Check karein `.env` file mein credentials configured hain
3. Logs check karein: `Logs/gmail_auto_reply.log`

---

## 📝 Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. Dashboard Run Karein                                │
│     → start-dashboard.bat                               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  2. Backend Server Start Hota Hai                       │
│     → Flask server on port 5000                         │
│     → Dashboard opens in browser                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  3. Services Auto-Start Hoti Hain                       │
│     → Gmail Watcher (auto-reply)                        │
│     → File Watcher (Drop_Folder)                        │
│     → Orchestrator (coordination)                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  4. Real-Time Activity Show Hoti Hai                    │
│     → Email aata hai → Dashboard pe dikhta hai          │
│     → Auto-reply jata hai → Update hota hai             │
│     → Status har 3 seconds mein update                  │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Quick Start Command

```bash
# Seedha run karein
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
start-dashboard.bat
```

**Bas! Dashboard chal pada aur sab services auto-start ho gaye!** 🎉

---

## 🎯 Next Steps

1. **Dashboard open karein** → `http://localhost:5000`
2. **Test email bhejein** → `aqeelwork2026@gmail.com`
3. **Activity dekhein** → Real-time updates terminal mein
4. **Enjoy karein!** → Apna AI Employee kaam kar raha hai!

---

**Happy Automating! 🚀**
