# 🧪 Gmail Auto-Reply Test Guide

## ✅ Quick Test (2 Minutes)

### **Step 1: Test Email Bhejein**

1. Apne **dusre email** se (e.g., Gmail, Yahoo, Outlook) email bhejein:
   - **To:** `aqeelwork2026@gmail.com`
   - **Subject:** `Test Auto Reply`
   - **Body:** `Yeh mera test email hai. Please reply karein.`

2. **Send** par click karein

---

### **Step 2: Wait Karein (30-60 Seconds)**

Gmail watcher har 60 seconds mein check karta hai.

---

### **Step 3: Check Karein**

#### **A) Apne Inbox Mein Check Karein:**

1. **Open:** https://mail.google.com
2. **Login:** `aqeelwork2026@gmail.com`
3. **Sent folder** check karein
4. Aap ko **auto-reply email** dikhai dega

#### **B) Logs Check Karein:**

```bash
# Latest logs dekhein
powershell -Command "Get-Content 'E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\gmail_auto_reply.log' -Tail 20"
```

**Expected Output:**
```
INFO - New email from: Your Name <your@email.com>
INFO - Subject: Test Auto Reply
INFO - Processing email from Your Name
INFO - Auto-reply sent to: Your Name
INFO - Template used: default
```

#### **C) CSV Log File Check Karein:**

```bash
# CSV log file open karein
notepad E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\auto_reply_log.csv
```

**Expected Content:**
```csv
timestamp,to,subject,template,status
2026-03-02T10:35:00,your@email.com,"Test Auto Reply",default,success
```

---

## 📋 **Test Templates**

### **Template 1: Invoice Test**
```
To: aqeelwork2026@gmail.com
Subject: Invoice Payment Question
Body: Hi, I have a question about my invoice. When will it be processed?
```
**Expected Reply:** `invoice_inquiry` template

---

### **Template 2: Meeting Request Test**
```
To: aqeelwork2026@gmail.com
Subject: Meeting Request - Next Week
Body: Can we schedule a meeting next week to discuss the project?
```
**Expected Reply:** `meeting_request` template

---

### **Template 3: Support Test**
```
To: aqeelwork2026@gmail.com
Subject: Help Needed - Issue with Account
Body: I'm having an issue with my account. Can you help?
```
**Expected Reply:** `support_ticket` template

---

### **Template 4: General Test**
```
To: aqeelwork2026@gmail.com
Subject: Hello
Body: Just testing the auto-reply system.
```
**Expected Reply:** `default` template

---

## 🔍 **Troubleshooting**

### **Problem: Auto-Reply Nahi Aaya**

**Check:**
1. Watcher run kar raha hai? → Logs check karein
2. Email unread hai? → Gmail mein check karein
3. Credentials sahi hain? → .env file verify karein

### **Problem: Error in Logs**

```bash
# Latest errors dekhein
powershell -Command "Get-Content 'E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\gmail_auto_reply.log' | Select-String 'ERROR'"
```

### **Problem: Watcher Stop Hai**

```bash
# Restart karein
cd E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py 60
```

---

## 📊 **Quick Status Check**

```bash
# Watcher process check karein
tasklist | findstr python

# Latest logs check karein
powershell -Command "Get-Content 'E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\gmail_auto_reply.log' -Tail 10"

# CSV log check karein
powershell -Command "Get-Content 'E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\Logs\auto_reply_log.csv'"
```

---

## ✅ **Success Indicators**

| Check | Expected Result |
|-------|-----------------|
| **Gmail Sent Folder** | Auto-reply email dikhai dega |
| **Logs** | "Auto-reply sent" message |
| **CSV Log** | New entry with timestamp |
| **Recipient Inbox** | Reply email received |

---

*Happy Testing! 🎉*
