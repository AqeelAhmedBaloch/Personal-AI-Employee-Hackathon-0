# AI Employee - Quick Start Guide 🚀

## Step-by-Step Instructions (Roman Urdu Mein)

---

## 🔹 Step 1: Run File Ko Execute Karein

**Sab se pehle:**
1. `AI_Employee_Vault` folder open karein
2. **`run.bat`** file par double-click karein

Yeh file automatically:
- ✅ Python check karegi
- ✅ Required packages install karegi
- ✅ Saare folders create karegi
- ✅ File Watcher start karegi
- ✅ Orchestrator start karegi
- ✅ Drop_Folder open kar degi

---

## 🔹 Step 2: Do Terminal Windows Khulengi

Jab `run.bat` run hoga, to **do alag terminal windows** khulengi:

### Window 1: File Watcher 📁
```
AI Employee - File Watcher
```
- Yeh `Drop_Folder` ko monitor karti hai
- Jab bhi koi nayi file ayegi, detect karegi

### Window 2: Orchestrator 🎯
```
AI Employee - Orchestrator
```
- Yeh check karta hai ke kaunse actions pending hain
- Har 30 seconds mein check karta hai

**⚠️ Dono windows ko KHULA CHHOD DEIN!** (band na karein)

---

## 🔹 Step 3: Test File Drop Karein

Ab aap test kar sakte hain:

**Option A:** Koi bhi file `Drop_Folder` mein copy/paste karein

**Option B:** Command prompt mein likhein:
```bash
echo "Mera pehla AI Employee test" > Drop_Folder\test.txt
```

---

## 🔹 Step 4: Result Check Karein

### Check karein ke file process hui ya nahi:

1. **Needs_Action folder check karein:**
   ```
   AI_Employee_Vault\Needs_Action\
   ```
   Yahan aap ko `FILE_test_*.md` jaisi file dikhai degi.

2. **Inbox folder check karein:**
   ```
   AI_Employee_Vault\Inbox\
   ```
   Yahan aap ki original file copy ho gayi hogi.

3. **Logs check karein:**
   ```
   AI_Employee_Vault\Logs\
   ```
   Yahan watcher aur orchestrator ki logs hongi.

---

## 🔹 Step 5: Obsidian Mein Dashboard Dekhein 📊

1. **Obsidian open karein**
2. **Open Folder as Vault** select karein
3. `AI_Employee_Vault` folder select karein
4. **`Dashboard.md`** file open karein

Yahan aap dekh sakte hain:
- Pending tasks kitne hain
- Aaj kitne tasks complete huye
- Recent activity kya hai

---

## 🔹 Step 6: Qwen Code Se Process Karein 🤖

Agar aap ne **Qwen Code** install kiya hai:

```bash
cd D:\Q4-Hackathon\Personal-AI-Employee-Hackathon-0\AI_Employee_Vault
qwen -c "Process all files in Needs_Action folder. Follow Company_Handbook.md rules."
```

**Agar Qwen Code nahi hai:**
- Aap manually bhi files process kar sakte hain
- `Needs_Action` folder se files open karein
- Khud decide karein ke kya action lena hai
- File ko `Done` folder mein move kar dein

---

## 🔹 Step 7: Services Ko Stop Karein 🛑

Jab aap kaam khatam kar lein:

**Option A:** `stop.bat` run karein
```
AI_Employee_Vault\stop.bat
```

**Option B:** Dono terminal windows manually band kar dein (X button)

---

## 📋 Quick Reference

| Kaam | Kaise Karein |
|------|-------------|
| **Start** | `run.bat` par double-click |
| **Stop** | `stop.bat` par double-click |
| **Test** | `Drop_Folder` mein file daalein |
| **Check** | `Needs_Action` folder dekhein |
| **Dashboard** | Obsidian mein `Dashboard.md` open karein |
| **Process** | `qwen -c "Process Needs_Action"` |

---

## ❗ Common Problems

### Problem: "Python not found"
**Solution:** Python install karein from [python.org](https://python.org)

### Problem: "Qwen Code not found"
**Solution:** Koi baat nahi! Aap manually bhi files process kar sakte hain

### Problem: "File process nahi hui"
**Solution:** 
1. Check karein ke dono terminal windows chal rahi hain
2. Logs check karein: `Logs\` folder
3. `run.bat` dobara run karein

---

## 📞 Help Chahiye?

Agar koi problem ho to:
1. `Logs\` folder mein error logs check karein
2. Terminal windows mein error messages dekhein
3. Mujhe batayein, main help karunga!

---

*Happy Automating! 🎉*
