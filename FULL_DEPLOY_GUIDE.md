# 🚀 GitHub + Render.com - To'liq Deploy

Bu qo'llanma loyihangizni GitHub ga yuklab, keyin Render.com ga deploy qilish jarayonini ko'rsatadi.

---

## 📦 QISM 1: GitHub ga yuklash (5 daqiqa)

### 1. GitHub da repository yarating
1. [GitHub.com](https://github.com) ga kiring
2. **New repository** tugmasini bosing
3. Sozlamalar:
   - **Name:** `telegram-supermarket`
   - **Public** yoki **Private** tanlang
   - ❌ README, .gitignore qo'shmang
4. **Create repository** → URL ni saqlab oling

### 2. Loyihani GitHub ga yuklang

Terminal ochib:

```bash
# Loyiha papkasiga o'ting
cd telegram-supermarket

# Git ni sozlang (birinchi marta)
git config --global user.name "Ismingiz"
git config --global user.email "email@example.com"

# Git repository yaratish
git init
git add .
git commit -m "Initial commit: Telegram Supermarket Mini App"

# Remote qo'shish (URL ni o'zingizniki bilan almashtiring!)
git branch -M main
git remote add origin https://github.com/USERNAME/telegram-supermarket.git

# GitHub ga yuklash
git push -u origin main
```

**Login:** GitHub username va Personal Access Token (parol emas!)

Token olish: GitHub → Settings → Developer settings → Personal access tokens → Generate new token → ✅ repo

✅ **GitHub da loyihangiz!**

---

## 🌐 QISM 2: Render.com da Backend (5 daqiqa)

### 1. Render.com ga kiring
[Render.com](https://render.com) → **Sign Up** yoki **Log In** (GitHub bilan)

### 2. Backend Web Service yaratish

1. Dashboard → **New +** → **Web Service**
2. **Connect to GitHub** → Repository ruxsat bering
3. **telegram-supermarket** ni tanlang → **Connect**
4. Sozlamalar:

```
Name: telegram-supermarket-api
Region: Singapore (yoki eng yaqin)
Branch: main
Root Directory: (bo'sh qoldiring)
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
python app.py

Instance Type: Free
```

5. **Environment Variables** qo'shing (Advanced tugmasini bosing):

```
BOT_TOKEN = 1234567890:ABCdef... (o'zingizniki)
ADMIN_CHAT_ID = 123456789 (o'zingizniki)
FLASK_ENV = production
```

6. **Create Web Service** → 3-5 daqiqa deploy bo'ladi

✅ Backend URL: `https://telegram-supermarket-api.onrender.com`

**Test:** Brauzerda ochib ko'ring → `{"status": "ok"}` ko'rinishi kerak

---

## 🎨 QISM 3: Vercel da Frontend (3 daqiqa)

### 1. Vercel ga kiring
[Vercel.com](https://vercel.com) → **Sign Up** (GitHub bilan)

### 2. Frontend deploy

1. **Add New Project** → **Import Git Repository**
2. **telegram-supermarket** ni tanlang → **Import**
3. Sozlamalar:

```
Framework Preset: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

4. **Environment Variables** qo'shing:

```
Name: VITE_API_URL
Value: https://telegram-supermarket-api.onrender.com
```

5. **Deploy** → 2-3 daqiqa

✅ Frontend URL: `https://telegram-supermarket.vercel.app`

**Test:** URL ni ochib mahsulotlar yuklanishini ko'ring

---

## 🤖 QISM 4: Telegram Bot (2 daqiqa)

### 1. BotFather da Web App sozlash

Telegram da:
```
@BotFather
/setmenubutton
→ Botingizni tanlang
→ "Send URL" → https://telegram-supermarket.vercel.app
```

### 2. Bot serverni ishga tushirish

**Variant A: Render.com (Tavsiya etiladi)**

1. Render → **New +** → **Background Worker**
2. Repository: `telegram-supermarket`
3. Sozlamalar:

```
Name: telegram-supermarket-bot
Branch: main
Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
python bot.py

Instance Type: Free
```

4. Environment Variables (Web Service bilan bir xil):
```
BOT_TOKEN = ...
ADMIN_CHAT_ID = ...
WEB_APP_URL = https://telegram-supermarket.vercel.app
```

5. **Create Background Worker**

**Variant B: Lokal kompyuter (test uchun)**
```bash
python bot.py
```

---

## ✅ QISM 5: Test qilish

### 1. Backend test
Brauzer: `https://telegram-supermarket-api.onrender.com/health`
```json
{"status": "ok", "message": "Server ishlamoqda"}
```

### 2. Frontend test
Brauzer: `https://telegram-supermarket.vercel.app`
- Mahsulotlar yuklanishi kerak
- Kategoriyalar ishlashi kerak

### 3. Bot test
Telegram:
1. Botingizga `/start` yuboring
2. "🛒 Supermarketni ochish" tugmasini bosing
3. Mini App ochilishi kerak
4. Mahsulot tanlang, buyurtma bering
5. Sizga (admin) xabar kelishi kerak

---

## 🔄 QISM 6: Yangilanishlarni deploy qilish

### Lokal da o'zgarish qiling:
```bash
# Masalan, app.py da yangi mahsulot qo'shish
nano app.py

# Git ga commit
git add .
git commit -m "Add: Yangi mahsulotlar qo'shildi"
git push
```

✅ **Avtomatik deploy:**
- GitHub ga push qilsangiz
- Render va Vercel avtomatik yangi versiyani deploy qiladi
- 2-3 daqiqada tayyor!

---

## 📊 Monitoring

### Render Logs
Dashboard → Service → **Logs** tab

### Vercel Logs  
Dashboard → Project → **Deployments** → Logs

### Telegram test
Bot orqali buyurtma yuborib test qiling

---

## 🆘 Muammolar

### Backend ishlamayapti
1. Render Logs ni tekshiring
2. Environment Variables to'g'ri kiritilganini tekshiring
3. Build va Start Commands to'g'ri ekanligini tekshiring

### Frontend yuklanmayapti
1. Vercel Logs ni tekshiring
2. VITE_API_URL to'g'ri ekanligini tekshiring
3. Browser Console (F12) ni tekshiring

### Bot javob bermayapti
1. Bot service ishlab turganini tekshiring (Render)
2. WEB_APP_URL to'g'ri ekanligini tekshiring
3. BotFather da Web App URL to'g'ri o'rnatilganini tekshiring

### CORS xatosi
`app.py` da:
```python
from flask_cors import CORS
CORS(app, origins=["https://telegram-supermarket.vercel.app"])
```

---

## 💡 Pro Tips

### 1. Custom Domain (Optional)
- Vercel: Settings → Domains → Add custom domain
- Render: Settings → Custom Domain

### 2. Auto Deploy
- Default: har push da avtomatik deploy
- O'chirish: Render/Vercel settings da

### 3. Environment Variables xavfsizligi
- `.env` faylini GitHub ga yuklamang! (.gitignore da bor)
- Token oshkor bo'lsa, darhol o'zgartiring!

### 4. Free Tier Limits
- **Render Free:** 750 soat/oy, 15 min sleep
- **Vercel Free:** 100 GB bandwidth/oy
- Production uchun: Paid plan ($7-20/oy)

---

## 📈 Keyingi qadamlar

- [ ] To'lov tizimi (Click, Payme, Stripe)
- [ ] Admin panel
- [ ] Buyurtmalar tarixi
- [ ] Mahsulot rasmlari
- [ ] Push bildirishnomalar
- [ ] Analytics

---

## 🎉 Tabriklayman!

Sizning Telegram Mini App loyihangiz professional tarzda deploy qilindi:

✅ Backend: Render.com
✅ Frontend: Vercel
✅ Bot: Render Background Worker
✅ GitHub: Version control
✅ Auto deploy: Push va tayyor!

**Omad!** 🚀
