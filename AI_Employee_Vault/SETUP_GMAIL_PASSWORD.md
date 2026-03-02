# 🔐 Gmail App Password Setup - Quick Guide

## ❗ Error Kyun Aa Raha Hai?

```
Gmail credentials not configured
```

Yeh error is liye aa raha hai kyunki **GMAIL_APP_PASSWORD** khali hai!

---

## ✅ Solution: 3 Steps

### **Step 1: Google Account Mein Jayein**

**Direct Link:** https://myaccount.google.com/apppasswords

Ya phir:
1. https://myaccount.google.com/security par jayein
2. **2-Step Verification** enable karein (agar nahi hai)
3. **App passwords** par click karein

---

### **Step 2: App Password Generate Karein**

1. **App select karein:** `Mail`
2. **Device select karein:** `Other (Custom name)`
3. **Name enter karein:** `AI Employee`
4. **Generate button** par click karein

---

### **Step 3: Password Copy Kar Ke .env File Mein Paste Karein**

Aap ko 16-character password milega:
```
abcd efgh ijkl mnop
```

**❗ Important:** Spaces hata kar paste karein!

**Example:**
- Mila: `abcd efgh ijkl mnop`
- Paste karein: `abcdefghijklmnop`

---

## 📝 .env File Update Karein

**File Location:**
```
E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault\mcp_servers\email_mcp\.env
```

**Edit karein:**
```env
GMAIL_EMAIL_ADDRESS=aqeelwork2026@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop  # ← Yahan apna password paste karein
DRY_RUN=true
```

---

### **Step 4: Gmail Watcher Restart Karein**

```bash
# Purana process stop karein
taskkill /F /T /PID 6156

# Naya process start karein
cd E:\Hackathon-Q4\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
python gmail_auto_reply_watcher.py 60
```

---

## ✅ Verification

Logs check karein:
```
2026-03-02 - GmailAutoReplyWatcher - INFO - Connecting to Gmail IMAP...
2026-03-02 - GmailAutoReplyWatcher - INFO - Found 0 unread email(s)
```

Agar yeh dikhe to **successful** hai!

---

## ❗ Common Errors

| Error | Solution |
|-------|----------|
| `Invalid credentials` | Password mein spaces hain? Hata kar try karein |
| `2-Step Verification required` | Pehle 2FA enable karein |
| `App passwords not available` | Work/School account hai? Personal Gmail use karein |

---

## 📞 Help Chahiye?

Agar abhi bhi problem ho to:
1. Screenshot lein error ka
2. Mujhe batayein
3. Main help karunga!
