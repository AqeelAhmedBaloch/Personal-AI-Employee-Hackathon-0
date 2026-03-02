# Gmail App Password Setup Guide

## Step 1: Google Account Mein Jayein

1. Apne Google Account mein login karein: https://myaccount.google.com/
2. **Security** tab par click karein

## Step 2: 2-Step Verification Enable Karein

Agar already enabled hai to skip karein:

1. **Security** → **2-Step Verification** par click karein
2. **Get Started** par click karein
3. Phone number enter karein
4. Verification code enter karein
5. **Turn On** par click karein

## Step 3: App Password Generate Karein

1. **Security** → **2-Step Verification** par jayein
2. Neeche scroll karein → **App passwords** par click karein
3. **App** select karein: **Mail**
4. **Device** select karein: **Other (Custom name)**
5. Custom name enter karein: `AI Employee System`
6. **Generate** par click karein

## Step 4: Password Copy Karein

Aap ko 16-character ka password milega, jaise:
```
abcd efgh ijkl mnop
```

Isay copy kar lein (spaces ke bina): `abcdefghijklmnop`

## Step 5: .env File Mein Save Karein

`.env` file create/edit karein:

```bash
# AI_Employee_Vault/mcp_servers/email_mcp/.env
GMAIL_EMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
DRY_RUN=true
```

## ✅ Done!

Ab Gmail watcher run kar sakte hain!
