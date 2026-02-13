# 🚀 Render.com ga 5 daqiqada deploy

## 1. Render.com ga kiring
[render.com](https://render.com) → GitHub bilan login

## 2. Web Service yarating
**New +** → **Web Service** → Repository ni ulang

## 3. Sozlamalar
```
Name: supermarket-api
Region: Singapore
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
Instance Type: Free
```

## 4. Environment Variables
```
BOT_TOKEN = 1234567890:ABC... (o'zingizniki)
ADMIN_CHAT_ID = 123456789 (o'zingizniki)
FLASK_ENV = production
```

## 5. Deploy!
**Create Web Service** → 3-5 daqiqa kutish

## ✅ Tayyor!
Backend URL: `https://supermarket-api.onrender.com`

## 6. Frontend (Vercel)
1. [vercel.com](https://vercel.com) → New Project
2. Repository → Import
3. Root Directory: `frontend`
4. Environment Variable:
   ```
   VITE_API_URL = https://supermarket-api.onrender.com
   ```
5. Deploy

## 7. BotFather sozlash
```
@BotFather
/setmenubutton
→ Botni tanlang
→ Send URL → https://your-frontend.vercel.app
```

## 8. Bot ishga tushirish
**Render** → **New +** → **Background Worker**
```
Name: supermarket-bot
Build: pip install -r requirements.txt
Start: python bot.py
Environment Variables: (yuqoridagidek)
```

✅ TAYYOR! Test qiling: Telegram botga `/start`

---

**Batafsil:** `RENDER_DEPLOY.md` ni o'qing
