# 🚀 Production ga Deploy qilish qo'llanmasi

## 1. Frontend - Vercel (Tavsiya etiladi)

### A. Vercel orqali deploy

1. [Vercel](https://vercel.com) ga kiring (GitHub akkaunt bilan)
2. "New Project" ni bosing
3. Repository ni tanlang yoki import qiling
4. Sozlamalar:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Environment Variables qo'shing:
   - `VITE_API_URL` = Backend URL (masalan: `https://your-backend.herokuapp.com`)
6. "Deploy" ni bosing

### B. Netlify orqali deploy

1. [Netlify](https://netlify.com) ga kiring
2. "Add new site" → "Import an existing project"
3. Repository ni ulang
4. Sozlamalar:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
5. Environment variables: `VITE_API_URL`
6. Deploy qiling

---

## 2. Backend - Heroku

### A. Heroku Setup

```bash
# Heroku CLI o'rnating
# https://devcenter.heroku.com/articles/heroku-cli

# Login qiling
heroku login

# App yarating
heroku create your-supermarket-api

# Config vars qo'shing
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set ADMIN_CHAT_ID=your_chat_id
```

### B. Procfile yarating

Loyiha asosiy papkasida `Procfile` yarating:

```
web: python app.py
```

### C. Deploy qiling

```bash
git add .
git commit -m "Production deploy"
git push heroku main
```

---

## 3. Backend - Railway

1. [Railway](https://railway.app) ga kiring
2. "New Project" → "Deploy from GitHub repo"
3. Repository ni tanlang
4. Variables qo'shing:
   - `BOT_TOKEN`
   - `ADMIN_CHAT_ID`
5. Deploy command: `python app.py`

---

## 4. Backend - Render

1. [Render](https://render.com) ga kiring
2. "New +" → "Web Service"
3. Repository ni ulang
4. Sozlamalar:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Environment Variables qo'shing
6. "Create Web Service"

---

## 5. Bot konfiguratsiyasi

Deploy qilgandan so'ng:

### A. BotFather sozlamalari

```
1. @BotFather ga o'ting
2. /setmenubutton
3. Botingizni tanlang
4. "Send URL" → Frontend URL ni kiriting
   Masalan: https://supermarket.vercel.app
```

### B. Bot ishga tushirish

**Variant 1: Lokal server (test uchun)**
```bash
python bot.py
```

**Variant 2: Cloud server**
- Heroku, Railway yoki Render da alohida dyno/service yarating
- `Procfile` ga qo'shing: `bot: python bot.py`

**Variant 3: PythonAnywhere**
1. PythonAnywhere ga file upload qiling
2. "Always-on task" yarating: `python /home/username/bot.py`

---

## 6. CORS sozlamalari

Agar frontend bilan backend turli domenlarda bo'lsa, `app.py` da CORS ni to'g'ri sozlang:

```python
from flask_cors import CORS

CORS(app, origins=[
    'https://your-frontend.vercel.app',
    'http://localhost:3000'  # Development uchun
])
```

---

## 7. SSL/HTTPS

Telegram Mini App uchun HTTPS majburiy!

- Vercel, Netlify, Heroku - avtomatik HTTPS
- Custom domain uchun: Let's Encrypt SSL

---

## 8. Environment Variables to'liq ro'yxati

### Backend (.env)
```
BOT_TOKEN=123456:ABC-DEF...
ADMIN_CHAT_ID=123456789
WEB_APP_URL=https://your-frontend.vercel.app
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend.herokuapp.com
```

---

## 9. Deploy checklist

- [ ] Backend deploy qilindi va ishlayapti
- [ ] Frontend deploy qilindi va ishlayapti
- [ ] CORS to'g'ri sozlangan
- [ ] Environment variables to'liq kiritilgan
- [ ] HTTPS ishlayapti
- [ ] BotFather da Web App URL o'rnatilgan
- [ ] Bot ishga tushirilgan
- [ ] Test buyurtma muvaffaqiyatli yuborildi

---

## 10. Monitoring va Logs

### Heroku
```bash
heroku logs --tail
```

### Vercel
Dashboard → Deployments → Logs

### Render
Dashboard → Logs tab

---

## 🆘 Muammolar va yechimlar

### CORS xatosi
- Backend `CORS()` to'g'ri sozlanganini tekshiring
- Frontend URL ni whitelist ga qo'shing

### 502 Bad Gateway
- Backend serveri ishlab turganini tekshiring
- Environment variables to'g'ri kiritilganini tekshiring

### Bot javob bermayapti
- BOT_TOKEN to'g'ri ekanligini tekshiring
- Bot webhook emas, polling rejimida ekanligini tekshiring

---

**Qo'shimcha yordam:** README.md faylini o'qing
