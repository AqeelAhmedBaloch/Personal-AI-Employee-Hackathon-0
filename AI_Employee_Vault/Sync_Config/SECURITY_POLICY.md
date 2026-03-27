# 🔒 PLATINUM TIER - SECURITY POLICY

**Version:** 1.0  
**Date:** March 27, 2026  
**Classification:** CRITICAL

---

## ⚠️ **CRITICAL SECURITY RULES**

### **Rule #1: Secrets NEVER Sync**

**The following MUST NEVER sync to cloud:**

1. **Environment Files**
   - `.env`
   - `.env.local`
   - `.env.production`
   - `*.env`

2. **Credentials**
   - `credentials.json` (Google OAuth)
   - `service_account.json`
   - `banking_credentials.json`
   - `payment_tokens.json`

3. **Session Files**
   - `whatsapp_session/`
   - `browser_profile/`
   - `chrome_profile/`
   - `*.session`
   - `*.session-journal`

4. **Keys & Certificates**
   - `*.pem`
   - `*.key`
   - `*.crt`
   - `*.p12`

5. **OAuth Tokens**
   - `oauth_tokens.json`
   - `tokens/`
   - `auth/`

---

## 🏗️ **ARCHITECTURE SECURITY**

### **Cloud Agent (Oracle/AWS VM)**

**HAS ACCESS TO:**
- ✅ Email drafts (Gmail API - send disabled)
- ✅ Social media drafts (LinkedIn, Facebook, Twitter - post disabled)
- ✅ Finance data (read-only)
- ✅ Public documentation

**DOES NOT HAVE:**
- ❌ WhatsApp session
- ❌ Banking credentials
- ❌ Payment tokens
- ❌ Final send/post permissions
- ❌ OAuth credentials for sensitive services

**Cloud Agent Capabilities:**
```python
# CAN DO:
- Read emails
- Draft email replies
- Read social media feeds
- Draft social posts
- Monitor transactions
- Create analysis reports
- Write to /Updates/ folder

# CANNOT DO:
- Send emails (draft only)
- Post to social media (draft only)
- Make payments (draft only)
- Access WhatsApp
- Access banking
- Execute final actions
```

---

### **Local Agent (Your Machine)**

**HAS ACCESS TO:**
- ✅ All cloud drafts
- ✅ WhatsApp session
- ✅ Banking credentials
- ✅ Payment tokens
- ✅ Final send/post permissions
- ✅ Approval workflow

**Local Agent Capabilities:**
```python
# CAN DO:
- Review cloud drafts
- Approve/reject actions
- Send final emails
- Post to social media
- Make payments
- Access WhatsApp
- Execute final actions via MCP
- Write to Dashboard.md

# MUST DO:
- Review all sensitive actions
- Log all final actions
- Maintain audit trail
```

---

## 📁 **FOLDER SECURITY CLASSIFICATION**

### **Public (Safe to Sync)**

| Folder | Sync | Reason |
|--------|------|--------|
| `Needs_Action/cloud/` | ✅ Yes | Cloud-drafted items only |
| `Needs_Action/shared/` | ✅ Yes | Non-sensitive tasks |
| `Plans/` | ✅ Yes | Action plans (no secrets) |
| `Pending_Approval/` | ✅ Yes | Approval requests |
| `Approved/` | ✅ Yes | Approved actions |
| `Done/` | ✅ Yes | Completed tasks |
| `Updates/` | ✅ Yes | Cloud→Local updates |
| `Signals/` | ✅ Yes | Cloud→Local signals |
| `In_Progress/cloud_agent/` | ✅ Yes | Cloud work items |
| `In_Progress/local_agent/` | ✅ Yes | Local work items |

---

### **Private (Local Only - NEVER Sync)**

| Folder | Sync | Reason |
|--------|------|--------|
| `Needs_Action/local/` | ❌ No | May contain sensitive local tasks |
| `Accounting/` | ❌ No | Financial data |
| `Logs/` | ❌ No | May contain sensitive info |
| `Local_Agent/.env` | ❌ No | Secrets |
| `Local_Agent/credentials.json` | ❌ No | OAuth credentials |
| `Local_Agent/whatsapp_session/` | ❌ No | WhatsApp session |
| `Local_Agent/banking_credentials/` | ❌ No | Banking secrets |

---

## 🔐 **CREDENTIAL MANAGEMENT**

### **Cloud VM Credentials**

```bash
# Cloud VM .env file (ORACLE/AWS VM)
# Location: /home/ubuntu/ai_employee/Cloud_Agent/.env

# Gmail (READ-ONLY, no send permission)
GMAIL_CLIENT_ID=xxx
GMAIL_CLIENT_SECRET=xxx
GMAIL_SCOPES=gmail.readonly,gmail.compose

# Social Media (DRAFT-ONLY, no post permission)
LINKEDIN_CLIENT_ID=xxx
LINKEDIN_SCOPES=w_member_social,r_basicprofile

# Database (if using)
DB_HOST=localhost
DB_USER=cloud_agent
DB_PASSWORD=xxx

# NO BANKING CREDENTIALS
# NO WHATSAPP SESSION
# NO PAYMENT TOKENS
```

---

### **Local Machine Credentials**

```bash
# Local .env file (YOUR LAPTOP)
# Location: AI_Employee_Vault/Local_Agent/.env

# Gmail (FULL ACCESS)
GMAIL_CLIENT_ID=xxx
GMAIL_CLIENT_SECRET=xxx
GMAIL_SCOPES=gmail.readonly,gmail.compose,gmail.send

# WhatsApp Session
WHATSAPP_SESSION_PATH=/path/to/session

# Banking
BANK_API_URL=xxx
BANK_API_TOKEN=xxx

# Payment Gateway
STRIPE_SECRET_KEY=xxx
PAYPAL_CLIENT_ID=xxx

# Social Media (FULL ACCESS)
LINKEDIN_ACCESS_TOKEN=xxx
FACEBOOK_ACCESS_TOKEN=xxx
TWITTER_API_KEY=xxx

# These NEVER sync to cloud!
```

---

## 🚨 **SECURITY AUDIT CHECKLIST**

### **Before Cloud Deployment:**

- [ ] Remove all `.env` files from sync
- [ ] Add `.gitignore` rules
- [ ] Verify no credentials in code
- [ ] Setup separate cloud/local credentials
- [ ] Document what syncs and what doesn't
- [ ] Test sync with dummy files
- [ ] Verify Logs folder excluded
- [ ] Verify Accounting folder excluded

---

### **Before Each Sync:**

- [ ] Scan for credential patterns
- [ ] Check for new .env files
- [ ] Verify no session files included
- [ ] Review Logs folder excluded
- [ ] Check for banking data

---

### **Weekly Security Review:**

- [ ] Review sync logs
- [ ] Check for accidental secret commits
- [ ] Rotate cloud credentials
- [ ] Review access logs
- [ ] Update .gitignore if needed
- [ ] Review conflict backups

---

## 🔍 **AUTOMATED SECURITY SCANNING**

### **Pre-Sync Scan Script**

```python
# sync_scanner.py
# Run before every sync operation

import os
import re
from pathlib import Path

SENSITIVE_PATTERNS = [
    r'password\s*=\s*["\'].*["\']',
    r'secret\s*=\s*["\'].*["\']',
    r'api_key\s*=\s*["\'].*["\']',
    r'token\s*=\s*["\'].*["\']',
    r'credential\s*=\s*["\'].*["\']',
    r'private_key\s*=\s*["\'].*["\']',
]

def scan_file(filepath):
    """Scan file for sensitive patterns."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    findings = []
    for pattern in SENSITIVE_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings.append({
                'file': filepath,
                'pattern': pattern,
                'matches': len(matches)
            })
    
    return findings

def scan_directory(directory):
    """Scan directory for sensitive files."""
    all_findings = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        if any(excluded in root for excluded in ['Logs', 'Accounting', 'session']):
            continue
        
        for file in files:
            # Skip .env files
            if file.endswith('.env') or 'credential' in file.lower():
                all_findings.append({
                    'file': os.path.join(root, file),
                    'issue': 'Sensitive file detected'
                })
                continue
            
            # Scan file content
            if file.endswith(('.py', '.js', '.json', '.md', '.txt')):
                findings = scan_file(os.path.join(root, file))
                all_findings.extend(findings)
    
    return all_findings

if __name__ == '__main__':
    vault_path = Path(__file__).parent.parent
    print(f"Scanning {vault_path}...")
    
    findings = scan_directory(vault_path)
    
    if findings:
        print(f"\n⚠️ SECURITY ALERT: {len(findings)} issues found!\n")
        for finding in findings:
            print(f"  File: {finding['file']}")
            if 'pattern' in finding:
                print(f"  Pattern: {finding['pattern']}")
            print()
        exit(1)
    else:
        print("✅ No security issues found. Safe to sync.")
        exit(0)
```

---

## 📋 **SECURITY INCIDENT RESPONSE**

### **If Secret Accidentally Synced:**

1. **IMMEDIATE ACTION:**
   - Stop sync process
   - Revoke compromised credentials
   - Change passwords
   - Notify team

2. **CONTAINMENT:**
   - Remove secret from cloud VM
   - Check cloud VM logs for unauthorized access
   - Review what was exposed

3. **RECOVERY:**
   - Generate new credentials
   - Update .gitignore
   - Re-sync clean vault
   - Document incident

4. **POST-MORTEM:**
   - Root cause analysis
   - Update security policy
   - Implement additional checks
   - Train team

---

## ✅ **SECURITY COMPLIANCE**

### **Platinum Tier Security Requirements:**

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Secrets never sync | ✅ | `.gitignore` configured |
| Separate cloud/local credentials | ✅ | Separate .env files |
| Cloud draft-only | ✅ | MCP servers configured |
| Local final approval | ✅ | Approval workflow |
| Audit logging | ✅ | Logs maintained |
| Security scanning | ✅ | Pre-sync scanner |
| Incident response | ✅ | Documented process |

---

## 🎓 **SECURITY TRAINING**

### **For Humans Using the System:**

1. **NEVER commit .env files**
2. **NEVER share credentials**
3. **NEVER disable security scanning**
4. **ALWAYS review approval requests**
5. **ALWAYS rotate credentials regularly**

---

**Security Policy Version:** 1.0  
**Last Updated:** March 27, 2026  
**Next Review:** April 3, 2026  
**Owner:** AI Employee Security Team

---

*This document is CRITICAL. Read and understand before deploying Platinum Tier.*
