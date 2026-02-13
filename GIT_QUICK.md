# ⚡ Git Quick Commands

## 🚀 Birinchi marta GitHub ga yuklash

```bash
# 1. Loyiha papkasiga o'ting
cd telegram-supermarket

# 2. Git ni sozlash (birinchi marta)
git config --global user.name "Ismingiz"
git config --global user.email "email@example.com"

# 3. Git repository ga aylantirish
git init
git add .
git commit -m "Initial commit: Telegram Supermarket"

# 4. GitHub repository yarating va URL oling
# https://github.com → New repository → URL ni oling

# 5. Remote qo'shish (URL ni o'zingizniki bilan almashtiring)
git remote add origin https://github.com/username/telegram-supermarket.git

# 6. Main branch va push
git branch -M main
git push -u origin main
```

---

## 🔄 Keyingi o'zgarishlarni yuklash

```bash
# Oddiy 3 komanda:
git add .
git commit -m "O'zgarish tavsifi"
git push
```

---

## 🔐 GitHub Login

### Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token → ✅ repo
3. Token ni ko'chiring
4. Push da: username → username, password → token

### yoki GitHub CLI:
```bash
gh auth login
```

---

## 📦 Clone qilish (boshqa kompyuterda)

```bash
git clone https://github.com/username/telegram-supermarket.git
cd telegram-supermarket
cp .env.example .env
# .env ni to'ldiring!
```

---

## 💡 Foydali komandalar

```bash
# Status
git status

# Loglar
git log --oneline

# Pull (GitHub dan olish)
git pull

# Branch yaratish
git checkout -b feature-name

# Branch ga o'tish
git checkout main

# Remote URL
git remote -v
```

---

**Batafsil:** `GITHUB_GUIDE.md` ni o'qing
