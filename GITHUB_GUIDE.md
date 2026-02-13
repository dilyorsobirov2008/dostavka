# 📦 GitHub ga yuklash qo'llanmasi

## 🎯 1-QADAM: GitHub Repository yaratish

### A. GitHub.com ga kiring
1. [GitHub.com](https://github.com) ga o'ting
2. Login qiling (yoki Sign Up)

### B. Yangi Repository yarating
1. O'ng yuqoridagi **"+"** belgisini bosing
2. **"New repository"** ni tanlang
3. Sozlamalar:
   ```
   Repository name: telegram-supermarket
   Description: Telegram Mini App - Professional Supermarket
   Public yoki Private: tanlang
   ❌ README.md qo'shmang (bizda allaqachon bor)
   ❌ .gitignore qo'shmang (bizda allaqachon bor)
   ```
4. **"Create repository"** ni bosing

### C. Repository URL ni oling
Misol: `https://github.com/username/telegram-supermarket.git`

---

## 🚀 2-QADAM: Loyihani GitHub ga yuklash

### Terminal ochib, loyiha papkasiga o'ting:

```bash
cd telegram-supermarket
```

### Git ni sozlash (agar birinchi marta bo'lsa):

```bash
# Git username ni o'rnatish
git config --global user.name "Ismingiz"

# Git email ni o'rnatish
git config --global user.email "email@example.com"
```

### Loyihani Git repository ga aylantirish:

```bash
# Git repository ni boshlash
git init

# Barcha fayllarni qo'shish
git add .

# Birinchi commit
git commit -m "Initial commit: Telegram Supermarket Mini App"

# Main branch ni o'rnatish
git branch -M main

# Remote repository ni qo'shish (URL ni o'zingizniki bilan almashtiring)
git remote add origin https://github.com/username/telegram-supermarket.git

# GitHub ga yuklash
git push -u origin main
```

---

## 🔐 3-QADAM: GitHub Authentication

Agar parol so'ralsa:

### Variant A: Personal Access Token (Tavsiya etiladi)

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **"Generate new token"** → **"Generate new token (classic)"**
3. Sozlamalar:
   ```
   Note: Telegram Supermarket Token
   Expiration: 90 days (yoki No expiration)
   Scopes: ✅ repo (barcha repo checkboxlar)
   ```
4. **"Generate token"** → Token ni ko'chiring (ESDA QOLDIRASIZ!)
5. Git push da username so'rasa: GitHub username
6. Password so'rasa: Token ni kiriting (parol emas!)

### Variant B: GitHub CLI (Oson)

```bash
# GitHub CLI o'rnatish
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# Login qilish
gh auth login

# Repository yaratish va yuklash
gh repo create telegram-supermarket --public --source=. --push
```

---

## 🔄 4-QADAM: Keyingi o'zgarishlarni yuklash

Loyihada o'zgarish qilganingizdan keyin:

```bash
# O'zgarishlarni ko'rish
git status

# Barcha o'zgarishlarni qo'shish
git add .

# Commit qilish
git commit -m "O'zgarishlar tavsifi"

# GitHub ga yuklash
git push
```

### Commit message misollari:
```bash
git commit -m "Add: Yangi mahsulotlar qo'shildi"
git commit -m "Fix: Savat xatosi tuzatildi"
git commit -m "Update: Dizayn yangilandi"
git commit -m "Feature: To'lov tizimi qo'shildi"
```

---

## 📋 5-QADAM: .gitignore tekshirish

`.gitignore` faylingiz mavjud va quyidagilar ichida bo'lishi kerak:

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# Node
node_modules/
.env.local

# Build
frontend/dist/
```

Bu fayllar GitHub ga yuklanmaydi (to'g'ri).

---

## 🔒 6-QADAM: Environment Variables xavfsizligi

**MUHIM:** `.env` fayli GitHub ga yuklanmasligi kerak!

### Tekshirish:
```bash
cat .gitignore | grep .env
```

Agar `.env` ko'rinmasa, qo'shing:
```bash
echo ".env" >> .gitignore
```

### GitHub Secrets sozlash (Render uchun):

GitHub repository → **Settings** → **Secrets and variables** → **Actions**

**New repository secret**:
```
Name: BOT_TOKEN
Value: 1234567890:ABC...

Name: ADMIN_CHAT_ID
Value: 123456789
```

---

## 🌿 7-QADAM: Branches bilan ishlash (Optional)

### Development branch yaratish:
```bash
# Yangi branch yaratish
git checkout -b development

# O'zgarishlar qilish...

# Commit va push
git add .
git commit -m "Dev: yangi feature"
git push origin development
```

### Main ga merge qilish:
```bash
# Main ga qaytish
git checkout main

# Development dan merge
git merge development

# GitHub ga yuklash
git push
```

---

## 🔄 8-QADAM: Repository ni clone qilish (boshqa kompyuterda)

```bash
# Repository ni clone qilish
git clone https://github.com/username/telegram-supermarket.git

# Papkaga o'tish
cd telegram-supermarket

# .env faylini yaratish
cp .env.example .env
# .env ni to'ldiring!

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..
```

---

## 🎯 9-QADAM: Render.com bilan bog'lash

### Render.com da:
1. **New Web Service**
2. **Connect to GitHub** → Repository ni tanlang
3. Render avtomatik code o'zgarishlarni deploy qiladi!

### Auto Deploy:
Har safar `git push` qilganingizda, Render avtomatik yangi versiyani deploy qiladi.

---

## 💡 10-QADAM: Foydali Git komandalar

```bash
# Oxirgi commitni bekor qilish
git reset --soft HEAD~1

# O'zgarishlarni bekor qilish
git checkout -- .

# Remote repository URL ni ko'rish
git remote -v

# Remote ni o'zgartirish
git remote set-url origin https://github.com/newuser/telegram-supermarket.git

# Loglarni ko'rish
git log --oneline

# Branch larni ko'rish
git branch -a

# Pull (GitHub dan yangilanishlarni olish)
git pull origin main
```

---

## 🆘 Muammolar va yechimlar

### 1. "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/username/telegram-supermarket.git
```

### 2. "failed to push some refs"
```bash
# GitHub dagi o'zgarishlarni olish
git pull origin main --rebase

# Qayta yuklash
git push origin main
```

### 3. "Authentication failed"
- Personal Access Token ishlatayapsizmi?
- Token ni to'g'ri ko'chirgansizmi?
- Token `repo` permissions ga egami?

### 4. ".env fayli GitHub da ko'rinib qoldi"

```bash
# .env ni history dan o'chirish
git rm --cached .env
git commit -m "Remove .env from tracking"
git push

# GitHub repository → Settings → Options → Danger Zone
# "Change visibility" yoki "Delete repository" (agar token ochiq bo'lsa)
# Telegram bot tokenni o'zgartiring! (@BotFather /revoke)
```

---

## ✅ Tayyor!

GitHub repository: `https://github.com/username/telegram-supermarket`

**Keyingi qadam:** Render.com ga deploy qilish!

---

## 📚 Qo'shimcha manbalar

- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub CLI](https://cli.github.com)

---

**Savol bo'lsa:** Issue ochishingiz mumkin yoki Pull Request yuboring!
