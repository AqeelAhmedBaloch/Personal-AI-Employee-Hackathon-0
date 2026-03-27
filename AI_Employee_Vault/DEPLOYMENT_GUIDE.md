# 🚀 PLATINUM TIER - 24/7 DEPLOYMENT GUIDE

**Document:** Personal AI Employee Hackathon 0 Deployment  
**Purpose:** Dashboard ko 24/7 run karne ke liye deploy karna  
**Date:** March 27, 2026

---

## 📋 **DEPLOYMENT OPTIONS**

### **Option 1: Oracle Cloud Free Tier (RECOMMENDED)** ⭐

**Best For:** 24/7 always-on deployment  
**Cost:** FREE (Always Free tier)  
**Setup Time:** 30-45 minutes

#### **Resources:**
- **Compute:** 2 OCPU ARM Ampere A1
- **RAM:** 12 GB
- **Storage:** 200 GB
- **Network:** 10 Mbps

#### **Steps:**

**1. Oracle Cloud Account Setup:**
```bash
# 1. Visit: https://www.oracle.com/cloud/free/
# 2. Sign up for free account
# 3. Verify email and phone
# 4. Add credit card (for verification only)
```

**2. Create VM Instance:**
```bash
# Oracle Cloud Console mein:
# 1. Compute → Instances → Create Instance
# 2. Choose: Ubuntu 22.04
# 3. Shape: VM.Standard.A1.Flex (2 OCPU, 12GB RAM)
# 4. Add SSH key
# 5. Create
```

**3. Deploy Dashboard:**
```bash
# SSH into VM
ssh -i your_key.pem ubuntu@<your-vm-ip>

# Install Python & dependencies
sudo apt update
sudo apt install python3 python3-pip -y

# Clone your project
git clone <your-repo-url>
cd Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard

# Install requirements
pip3 install flask flask-cors python-dotenv

# Start with systemd (24/7)
sudo nano /etc/systemd/system/ai-dashboard.service
```

**4. Create Systemd Service:**
```ini
[Unit]
Description=AI Employee Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**5. Enable & Start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-dashboard
sudo systemctl start ai-dashboard
sudo systemctl status ai-dashboard
```

**6. Configure Firewall:**
```bash
sudo ufw allow 5000/tcp
sudo ufw enable
```

**7. Access Dashboard:**
```
http://<your-vm-ip>:5000
```

---

### **Option 2: AWS Free Tier** ☁️

**Best For:** AWS familiarity  
**Cost:** FREE for 12 months  
**Setup Time:** 30 minutes

#### **Resources:**
- **EC2:** t2.micro or t3.micro
- **RAM:** 1 GB
- **Storage:** 30 GB

#### **Quick Setup:**
```bash
# 1. AWS Console → EC2 → Launch Instance
# 2. AMI: Ubuntu 22.04
# 3. Instance: t2.micro (Free tier eligible)
# 4. Add SSH key
# 5. Security Group: Allow port 5000
# 6. Launch

# SSH and deploy
ssh -i your_key.pem ubuntu@<ec2-ip>
# Follow same steps as Oracle Cloud
```

---

### **Option 3: Google Cloud Free Tier** 🌐

**Best For:** GCP integration  
**Cost:** FREE for 12 months ($300 credit)  
**Setup Time:** 30 minutes

#### **Quick Setup:**
```bash
# 1. GCP Console → Compute Engine → VM Instances
# 2. Create Instance
# 3. Machine type: e2-micro (Free tier)
# 4. Boot disk: Ubuntu 22.04
# 5. Firewall: Allow HTTP (port 5000)
# 6. Create

# SSH and deploy via GCP Console
```

---

### **Option 4: Azure Free Tier** 💙

**Best For:** Microsoft ecosystem  
**Cost:** FREE for 12 months ($200 credit)  
**Setup Time:** 30 minutes

#### **Quick Setup:**
```bash
# 1. Azure Portal → Virtual Machines → Create
# 2. Image: Ubuntu 22.04
# 3. Size: B1s (Free tier eligible)
# 4. Add SSH key
# 5. Networking: Allow port 5000
# 6. Create

# SSH and deploy
```

---

### **Option 5: Local Deployment (Your PC)** 🖥️

**Best For:** Testing, not 24/7  
**Cost:** FREE  
**Setup Time:** 5 minutes

#### **Setup:**
```bash
# 1. Keep your PC running 24/7
# 2. Set up static IP
# 3. Configure port forwarding (5000)
# 4. Use Windows Task Scheduler

# Create batch file: start-dashboard-service.bat
@echo off
cd /d "e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\dashboard"
python app.py
pause

# Task Scheduler mein add karein:
# 1. Task Scheduler open karein
# 2. Create Basic Task
# 3. Trigger: At startup
# 4. Action: Start program → select batch file
# 5. Finish
```

**⚠️ Limitations:**
- ❌ PC must stay on 24/7
- ❌ Internet must stay connected
- ❌ Not production-ready
- ❌ Dynamic IP issues

---

### **Option 6: Railway.app** 🚂

**Best For:** Easy deployment  
**Cost:** FREE tier available  
**Setup Time:** 15 minutes

#### **Setup:**
```bash
# 1. Visit: https://railway.app
# 2. Sign up with GitHub
# 3. New Project → Deploy from GitHub
# 4. Select your repo
# 5. Add environment variables
# 6. Deploy

# railway.json create karein:
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd AI_Employee_Vault/dashboard && python app.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

### **Option 7: Render.com** 📦

**Best For:** Simple web services  
**Cost:** FREE tier available  
**Setup Time:** 15 minutes

#### **Setup:**
```bash
# 1. Visit: https://render.com
# 2. Sign up
# 3. New → Web Service
# 4. Connect GitHub repo
# 5. Configure:
#    - Build: pip install -r requirements.txt
#    - Start: python AI_Employee_Vault/dashboard/app.py
# 6. Deploy
```

---

## 🎯 **RECOMMENDED: ORACLE CLOUD**

### **Complete Step-by-Step:**

#### **Phase 1: Account Setup (15 minutes)**
```bash
1. Visit: https://cloud.oracle.com
2. Click "Start for free"
3. Fill details:
   - Name, Email, Phone
   - Credit card (verification only)
4. Verify email and phone
5. Login to Oracle Cloud Console
```

#### **Phase 2: Create VM (10 minutes)**
```bash
1. Console → Compute → Instances
2. Create Instance
3. Configuration:
   - Name: ai-employee-dashboard
   - Compartment: Root compartment
   - Availability Domain: Any
   - Image: Ubuntu 22.04
   - Shape: VM.Standard.A1.Flex
   - OCPUs: 2
   - Memory: 12 GB
4. Networking:
   - VCN: Default
   - Subnet: Public
   - Assign public IPv4: Yes
5. SSH Keys:
   - Generate key pair
   - Download private key
6. Boot Volume: Default (50GB)
7. Click "Create"
```

#### **Phase 3: Connect & Deploy (15 minutes)**
```bash
# Windows PowerShell se connect:
ssh -i <path-to-key> ubuntu@<public-ip>

# Update system:
sudo apt update && sudo apt upgrade -y

# Install Python:
sudo apt install python3 python3-pip git -y

# Clone project:
cd /home/ubuntu
git clone <your-github-repo>
cd Personal-AI-Employee-Hackathon-0

# Install dependencies:
cd AI_Employee_Vault/dashboard
pip3 install -r requirements.txt

# Test run:
python3 app.py
# Should show: Running on http://0.0.0.0:5000
# Ctrl+C to stop
```

#### **Phase 4: Setup Systemd Service (10 minutes)**
```bash
# Create service file:
sudo nano /etc/systemd/system/ai-dashboard.service

# Add this content:
[Unit]
Description=AI Employee Dashboard Service
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=ai-dashboard

[Install]
WantedBy=multi-user.target

# Save (Ctrl+O, Enter, Ctrl+X)

# Enable and start:
sudo systemctl daemon-reload
sudo systemctl enable ai-dashboard
sudo systemctl start ai-dashboard
sudo systemctl status ai-dashboard
```

#### **Phase 5: Configure Firewall (5 minutes)**
```bash
# Oracle Cloud Console mein:
# 1. Networking → Virtual Cloud Networks
# 2. Click on your VCN
# 3. Security Lists → Default Security List
# 4. Add Ingress Rule:
#    - Source CIDR: 0.0.0.0/0
#    - Destination Port Range: 5000
#    - Description: AI Dashboard
# 5. Save

# VM mein:
sudo ufw allow 5000/tcp
sudo ufw enable
```

#### **Phase 6: Access Dashboard**
```bash
# Browser mein open karein:
http://<your-vm-public-ip>:5000

# Example:
http://129.150.87.215:5000
```

---

## 📊 **DEPLOYMENT COMPARISON**

| Platform | Cost | Setup Time | Resources | 24/7 | Recommended |
|----------|------|------------|-----------|------|-------------|
| **Oracle Cloud** | FREE | 45 min | 2 OCPU, 12GB RAM | ✅ | ⭐⭐⭐⭐⭐ |
| **AWS Free Tier** | FREE (12 mo) | 30 min | 1 vCPU, 1GB RAM | ✅ | ⭐⭐⭐⭐ |
| **Google Cloud** | FREE (12 mo) | 30 min | 1 vCPU, 1GB RAM | ✅ | ⭐⭐⭐⭐ |
| **Azure** | FREE (12 mo) | 30 min | 1 vCPU, 1GB RAM | ✅ | ⭐⭐⭐⭐ |
| **Railway** | FREE | 15 min | 512MB RAM | ✅ | ⭐⭐⭐ |
| **Render** | FREE | 15 min | 512MB RAM | ✅ | ⭐⭐⭐ |
| **Local PC** | FREE | 5 min | Your PC specs | ❌ | ⭐⭐ |

---

## 🔧 **POST-DEPLOYMENT CHECKLIST**

### **After Deployment:**

- [ ] Dashboard accessible via public IP
- [ ] Systemd service running
- [ ] Auto-restart on failure enabled
- [ ] Firewall configured
- [ ] Logs accessible
- [ ] HTTPS configured (optional)
- [ ] Domain name configured (optional)

### **Monitoring:**

```bash
# Check service status
sudo systemctl status ai-dashboard

# View logs
sudo journalctl -u ai-dashboard -f

# Restart service
sudo systemctl restart ai-dashboard

# Stop service
sudo systemctl stop ai-dashboard

# Check resource usage
htop
```

---

## 🎯 **QUICK START: ORACLE CLOUD**

### **One-Command Deploy:**

```bash
# Yeh commands copy-paste karein Oracle Cloud VM mein:

# 1. Install dependencies
sudo apt update && sudo apt install python3 python3-pip git -y

# 2. Clone project
cd /home/ubuntu
git clone <YOUR_GITHUB_REPO_URL>
cd Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard

# 3. Install requirements
pip3 install -r requirements.txt

# 4. Create systemd service
sudo bash -c 'cat > /etc/systemd/system/ai-dashboard.service << EOF
[Unit]
Description=AI Employee Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Personal-AI-Employee-Hackathon-0/AI_Employee_Vault/dashboard
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

# 5. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ai-dashboard
sudo systemctl start ai-dashboard

# 6. Configure firewall
sudo ufw allow 5000/tcp

echo "✅ Dashboard deployed!"
echo "Access at: http://$(curl -s http://169.254.169.254/opc/v1/instance/metadata/public_ipv4):5000"
```

---

## 📝 **GIT REPO SETUP (For Deployment)**

### **GitHub Push:**

```bash
# Local machine par:
cd e:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0

# Initialize git (agar nahi hai)
git init
git add .
git commit -m "Initial commit - AI Employee Dashboard"

# GitHub repo create karein
# Phir:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### **.gitignore (Important!):**
```gitignore
# NEVER commit these:
.env
*.env
credentials.json
*.pem
*.key
session/
Logs/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
```

---

## 🎉 **RECOMMENDATION**

**For Hackathon Submission:**

**Best Option:** **Oracle Cloud Free Tier**

**Why:**
- ✅ 100% FREE (always free, not just 12 months)
- ✅ 24/7 always-on
- ✅ Professional deployment
- ✅ Real public IP
- ✅ Can share demo URL with judges
- ✅ Production-ready
- ✅ Impressive for judges

**Setup Time:** 45 minutes  
**Cost:** $0 (FREE)

---

## 🚀 **NEXT STEPS**

1. **Choose deployment platform** (Oracle Cloud recommended)
2. **Create account** (15 minutes)
3. **Setup VM** (10 minutes)
4. **Deploy dashboard** (15 minutes)
5. **Test access** (5 minutes)
6. **Share URL** for hackathon submission

---

**Ready to deploy?** Main step-by-step guide kar sakta hoon! 🚀
