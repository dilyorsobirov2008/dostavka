# 🐍 Python Telegram Bot - Render.com Deploy Guide

## 📦 Kerakli Fayllar

GitHub repository'da quyidagilar bo'lishi kerak:

```
backend/
├── bot.py                ✅ Python bot kodi
├── requirements.txt      ✅ Python dependencies
├── Procfile              ✅ Render uchun
├── .env                  ✅ Environment variables
└── .gitignore            ✅ .env'ni git'ga qo'yma
```

---

## 🚀 Render.com'ga Deploy Qilish

### 1️⃣ GitHub'ga Push Qiling

```bash
# Repository'ni clone/create qiling
git add bot.py requirements.txt Procfile .env .gitignore
git commit -m "Python Telegram Bot - Ready for Render"
git push origin main
```

### 2️⃣ Render Dashboard'da Service Yaratish

```
1. Dashboard → New Web Service
2. Repository ulang: supermarket-mini-app
3. Build Command: pip install -r requirements.txt
4. Start Command: gunicorn -w 1 -b 0.0.0.0:$PORT bot:app
5. Environment: Python
6. Python Version: 3.11 (yoki 3.12)
```

### 3️⃣ Environment Variables'ni O'rnatish

Render Settings → Environment:

```
BOT_TOKEN=8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo
ADMIN_CHAT_ID=YOUR_TELEGRAM_ID
BOT_USERNAME=supermarket_shop_bot
MINI_APP_URL=https://your-supermarket-frontend.onrender.com
PORT=8000
```

### 4️⃣ Deploy Qiling

```
"Create Web Service" tugmasini bosing
Deploy bo'lishini kutib turing (2-5 minut)
✅ Service active bo'lgandan keyin, URL ohasiz
```

---

## 📋 Lokal'da Test Qilish

### 1. Virtual Environment Yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 2. Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

### 3. Bot'ni Ishga Tushirish

```bash
python bot.py
```

### 4. Server Tekshirish

```bash
curl http://localhost:8000/
# Output: {"status": "Bot is running! ✅", ...}
```

---

## 🧪 Order API Test Qilish

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 123456789,
    "userName": "Test User",
    "phone": "+998901234567",
    "address": "Test Address, Tashkent",
    "notes": "Test order",
    "items": [
      {"id": 1, "name": "Olma", "price": 5000, "quantity": 2}
    ],
    "totalPrice": 10000,
    "timestamp": "2024-02-13T12:00:00Z"
  }'
```

---

## ✅ Deploy Checklist

- [ ] `bot.py` faylini yaratdim
- [ ] `requirements.txt` faylini yaratdim
- [ ] `Procfile` faylini yaratdim
- [ ] `.env` faylini yaratdim
- [ ] Barcha fayllarni GitHub'ga push qildim
- [ ] Render'da Web Service yaratdim
- [ ] Environment variables'ni o'rnatdim
- [ ] Deploy bo'ldi va URL ohdim
- [ ] BotFather'da Mini App URL o'rnatdim
- [ ] Bot /start'da Mini App tugmasini ko'rsatadi
- [ ] Order API test qilindi

---

## 🔧 Muammolar va Yechim

### ❌ "ModuleNotFoundError: No module named 'telegram'"

**Yechim:**
```bash
pip install -r requirements.txt
```

### ❌ "BOT_TOKEN is not defined"

**Yechim:**
- `.env` faylini tekshiring
- Render Environment tab'da o'rnatilganini tekshiring
- Bot'ni restart qiling

### ❌ "Port 8000 already in use"

**Yechim:**
```bash
# Boshqa port ishlatish
PORT=8001 python bot.py
```

### ❌ "Gunicorn error"

**Yechim:**
```bash
# Procfile tekshiring
# web: gunicorn -w 1 -b 0.0.0.0:$PORT bot:app
```

---

## 🎯 Frontend Sozlamasi

Frontend `.env.local` faylida:

```
VITE_API_URL=https://your-supermarket-bot.onrender.com
```

Order yuborishda:

```javascript
const response = await fetch(`${apiUrl}/api/orders`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(orderData)
});
```

---

## 📊 Monitoring

### Logs'ni Ko'rish

```
Render Dashboard → Web Service → Logs
```

### Health Check

```
https://your-supermarket-bot.onrender.com/health
```

### Uptime Robot Qo'shish

```
https://uptimerobot.com
Monitor: https://your-supermarket-bot.onrender.com/health
```

---

## 🎉 Tayyor!

Python bot'ingiz Render'da live! 🚀

Agar savollar bo'lsa, logs'ni ko'rib, error'ni toping va tuzating.
