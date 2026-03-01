# 🤖 AI Employee Dashboard

Web-based control center for your AI Employee system.

---

## 🚀 **Quick Start**

### **Step 1: Install Requirements**

```bash
cd D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard
pip install -r requirements.txt
```

### **Step 2: Start Dashboard**

**Option A: Double-click**
```
start.bat
```

**Option B: Command line**
```bash
python app.py
```

### **Step 3: Open Browser**

```
http://localhost:5000
```

---

## 📊 **Features**

### **Dashboard**
- ✅ System status (watchers, orchestrator)
- ✅ Credential status (Gmail, LinkedIn)
- ✅ Recent logs viewer
- ✅ Auto-refresh every 10 seconds

### **Credentials Management**
- ✅ Update Gmail credentials
- ✅ Update LinkedIn credentials
- ✅ Dry run mode toggle
- ✅ Secure local storage

### **Manual Controls**
- ✅ Start/Stop watchers
- ✅ Post to LinkedIn now
- ✅ Emergency stop all

### **Logs Viewer**
- ✅ View all log files
- ✅ Real-time log updates
- ✅ Search functionality

---

## 🎯 **What You Can Do**

### **1. Monitor System**
```
Dashboard par dekh sakte hain:
- Kaun se watchers chal rahe hain
- Kaun se band hain
- Credentials configured hain ya nahi
```

### **2. Change Credentials**
```
Credentials page par:
- Gmail email/password change karein
- LinkedIn email/password change karein
- LinkedIn API credentials add karein
- Dry run mode enable/disable karein
```

### **3. Manual Controls**
```
Controls page par:
- File watcher start/stop karein
- Gmail watcher start/stop karein
- Orchestrator start/stop karein
- LinkedIn post manually karein
- Emergency stop all
```

### **4. View Logs**
```
Logs page par:
- Sab log files dekhein
- Recent errors check karein
- System activity track karein
```

---

## 📁 **File Structure**

```
dashboard/
├── app.py                  # Flask application
├── start.bat               # Quick start script
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── templates/
    ├── dashboard.html      # Main dashboard
    ├── credentials.html    # Credentials management
    ├── controls.html       # Manual controls
    └── logs.html           # Logs viewer
```

---

## 🔐 **Security**

```
✅ Credentials stored locally in .env files
✅ .env files in .gitignore (never commit)
✅ No external data transmission
✅ Local server only (localhost:5000)
✅ Password fields masked in UI
```

---

## ⚙️ **Configuration**

### **Gmail Credentials**

File: `mcp_servers/email_mcp/.env`

```env
GMAIL_EMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
DRY_RUN=true
```

### **LinkedIn Credentials**

File: `mcp_servers/linkedin_mcp/.env`

```env
LINKEDIN_EMAIL=your.email@gmail.com
LINKEDIN_PASSWORD=your-password
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret
LINKEDIN_ACCESS_TOKEN=your-access-token
DRY_RUN=true
```

---

## 🎨 **Screenshots**

### **Dashboard**
- System status at a glance
- Quick actions
- Recent logs

### **Credentials**
- Update Gmail settings
- Update LinkedIn settings
- API credentials

### **Controls**
- Start/Stop watchers
- Post to LinkedIn
- Emergency controls

### **Logs**
- View all log files
- Real-time updates
- Search and filter

---

## 🐛 **Troubleshooting**

### **Dashboard doesn't start**

```bash
# Check if port 5000 is available
netstat -ano | findstr :5000

# If occupied, change port in app.py
app.run(debug=True, port=5001)
```

### **Credentials not saving**

```bash
# Check .env file permissions
# Make sure file is not read-only
# Run as Administrator if needed
```

### **Watchers not starting**

```bash
# Check Python path
python --version

# Install required packages
pip install watchdog playwright
```

---

## 📞 **Support**

For issues or questions:
1. Check logs in Logs viewer
2. Review credentials configuration
3. Restart dashboard
4. Check system requirements

---

## 🏆 **Silver Tier Features**

✅ Dashboard implemented
✅ Credential management
✅ Manual controls
✅ Logs viewer
✅ Real-time status
✅ LinkedIn integration
✅ Gmail integration
✅ File watcher integration

---

**Enjoy your AI Employee Dashboard!** 🎉
