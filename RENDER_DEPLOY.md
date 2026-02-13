# 🚀 Render.com ga Deploy qilish

Bu qo'llanma Telegram Supermarket ilovasini Render.com ga deploy qilish jarayonini batafsil tushuntiradi.

---

## 📋 Boshlashdan oldin

✅ Render.com akkauntingiz bo'lishi kerak (GitHub orqali tez ro'yxatdan o'tishingiz mumkin)
✅ Telegram bot tokeningiz tayyor bo'lishi kerak (@BotFather dan)
✅ Admin chat ID ni bilishingiz kerak (@userinfobot dan)

---

## 🎯 1-QADAM: Backend (Flask API) ni Deploy qilish

### A. Render.com ga kiring

1. [Render.com](https://render.com) ga o'ting
2. GitHub akkaunt bilan kirish (yoki ro'yxatdan o'tish)

### B. Yangi Web Service yarating

1. Dashboard da **"New +"** tugmasini bosing
2. **"Web Service"** ni tanlang
3. **"Build and deploy from a Git repository"** → **"Next"**

### C. Repository ni ulang

**Variant 1: GitHub repository**
- Repository ni tanlang yoki ulang
- **"Connect"** ni bosing

**Variant 2: Manual (Git URL orqali)**
- Public repository URL sini kiriting
- **"Continue"** ni bosing

### D. Sozlamalarni kiriting

```
Name: telegram-supermarket-api (yoki o'zingiz xohlagan nom)
Region: Singapore (yoki eng yaqin region)
Branch: main
Root Directory: bo'sh qoldiring

Runtime: Python 3

Build Command:
pip install -r requirements.txt

Start Command:
python app.py
```

### E. Instance Type

- **Free** ni tanlang (test uchun)
- Yoki **Starter** ($7/oy) - production uchun

### F. Environment Variables qo'shing

**"Advanced"** bo'limini oching va quyidagilarni qo'shing:

```
Key: BOT_TOKEN
Value: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz (o'zingizniki)

Key: ADMIN_CHAT_ID
Value: 123456789 (o'zingizniki)

Key: FLASK_ENV
Value: production

Key: PORT
Value: 10000 (Render avtomatik beradi, lekin siz ham qo'shishingiz mumkin)
```

### G. Deploy qiling!

1. **"Create Web Service"** tugmasini bosing
2. Deploy jarayoni boshlanadi (3-5 daqiqa)
3. ✅ Deploy tayyor bo'lganda, URL olasiz: `https://telegram-supermarket-api.onrender.com`

---

## 🎨 2-QADAM: Frontend ni Deploy qilish

### Variant A: Vercel (Tavsiya etiladi - bepul va tez)

1. [Vercel](https://vercel.com) ga o'ting
2. **"Add New Project"**
3. Repository ni import qiling
4. Sozlamalar:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
5. Environment Variables:
   ```
   VITE_API_URL = https://telegram-supermarket-api.onrender.com
   ```
6. **"Deploy"** ni bosing

### Variant B: Netlify

1. [Netlify](https://netlify.com) ga o'ting
2. **"Add new site"** → **"Import an existing project"**
3. Repository ni ulang
4. Sozlamalar:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```
5. Environment variables:
   ```
   VITE_API_URL = https://telegram-supermarket-api.onrender.com
   ```
6. **"Deploy site"** ni bosing

### Variant C: Render (Agar frontend ham Render da bo'lishini xohlasangiz)

1. Render da **"New +"** → **"Static Site"**
2. Repository ni ulang
3. Sozlamalar:
   ```
   Name: telegram-supermarket-frontend
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: frontend/dist
   ```
4. Environment Variables:
   ```
   VITE_API_URL = https://telegram-supermarket-api.onrender.com
   ```
5. **"Create Static Site"**

---

## 🤖 3-QADAM: Telegram Bot ni sozlash

### A. BotFather da Web App URL ni o'rnatish

1. Telegram da **@BotFather** ga o'ting
2. Quyidagi komandalarni yuboring:

```
/setmenubutton
→ Botingizni tanlang
→ "Send URL" tugmasini bosing
→ Frontend URL ni kiriting:
   https://your-frontend-url.vercel.app
```

### B. Bot ni ishga tushirish

**Variant 1: Render da alohida service (Tavsiya etiladi)**

1. Render da yangi **"Background Worker"** yarating
2. Repository: xuddi web service bilan bir xil
3. Sozlamalar:
   ```
   Name: telegram-supermarket-bot
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```
4. Environment Variables (web service bilan bir xil):
   ```
   BOT_TOKEN=...
   ADMIN_CHAT_ID=...
   WEB_APP_URL=https://your-frontend-url.vercel.app
   ```
5. **"Create Background Worker"**

**Variant 2: Lokal kompyuterda (test uchun)**
```bash
python bot.py
```

**Variant 3: 24/7 bepul hosting (PythonAnywhere)**
1. [PythonAnywhere](https://pythonanywhere.com) ga ro'yxatdan o'ting
2. Files → Upload: `bot.py` va `requirements.txt`
3. Consoles → Bash:
   ```bash
   pip3 install --user -r requirements.txt
   ```
4. Tasks → Always-on task:
   ```
   python3 /home/yourusername/bot.py
   ```

---

## ✅ 4-QADAM: Test qilish

1. **Backend test:**
   - Brauzerda ochib ko'ring: `https://your-api.onrender.com/health`
   - Javob: `{"status": "ok", "message": "Server ishlamoqda"}`

2. **Frontend test:**
   - Frontend URL ni brauzerda oching
   - Mahsulotlar yuklanishi kerak

3. **Bot test:**
   - Telegram da botingizga `/start` yuboring
   - "🛒 Supermarketni ochish" tugmasini bosing
   - Ilova ochilishi kerak

4. **To'liq test:**
   - Mahsulot tanlang va savatga qo'shing
   - Buyurtma bering
   - Admin (siz) ga xabar kelishi kerak

---

## 🔧 Render.com da PORT sozlamalari

Render avtomatik ravishda `PORT` environment variable ni beradi. Bizning kodimiz:

```python
port = int(os.environ.get('PORT', 5000))
app.run(debug=False, host='0.0.0.0', port=port)
```

✅ Bu kod Render da avtomatik ishlaydi!

---

## 💡 Muhim eslatmalar

### 1. Free tier cheklovlari
- Render free plan: 750 soat/oy (bir ilova uchun)
- 15 daqiqa aktivlik bo'lmasa, service "sleep" rejimiga o'tadi
- Birinchi so'rovda uyg'onishi uchun 30-60 soniya kerak

### 2. Sleep rejimini oldini olish
**Render da "Keep Awake" xizmati:**
- Paid plan ga o'ting ($7/oy)
- Yoki [UptimeRobot](https://uptimerobot.com) ishlatib, har 5 daqiqada ping yuboring

### 3. CORS sozlamalari
`app.py` da frontend URL ni whitelist ga qo'shing:

```python
from flask_cors import CORS

CORS(app, origins=[
    'https://your-frontend.vercel.app',
    'http://localhost:3000'  # development uchun
])
```

### 4. HTTPS
✅ Render avtomatik HTTPS beradi
✅ Telegram Mini App uchun HTTPS majburiy

---

## 📊 Monitoring va Logs

### Logs ko'rish
1. Render dashboard ga o'ting
2. Service ni tanlang
3. **"Logs"** tab ni bosing
4. Real-time logs ko'rish

### Deploy History
- **"Events"** tab da barcha deploy tarixini ko'rish mumkin

---

## 🆘 Tez-tez uchraydigan muammolar

### 1. "Application failed to respond"
**Sabab:** PORT to'g'ri ishlatilmagan
**Yechim:** `app.py` da:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### 2. CORS xatosi
**Sabab:** Frontend URL whitelist da emas
**Yechim:** `app.py` da CORS sozlang

### 3. Bot javob bermayapti
**Sabab:** Bot service ishlamayapti yoki environment variables noto'g'ri
**Yechim:** 
- Logs ni tekshiring
- Environment variables ni qayta kiriting
- Service ni restart qiling

### 4. Deploy muvaffaqiyatsiz
**Sabab:** requirements.txt da xatolik
**Yechim:** Lokal da test qiling:
```bash
pip install -r requirements.txt
python app.py
```

---

## 🎉 Tayyor!

Backend: `https://your-api.onrender.com` ✅
Frontend: `https://your-frontend.vercel.app` ✅
Bot: Telegram da ishlayapti ✅

---

## 📞 Yordam

Agar qiyinchilik bo'lsa:
1. Render Logs ni tekshiring
2. Browser Console ni tekshiring (F12)
3. `python app.py` local da test qiling

**Muvaffaqiyat tilaklar!** 🚀
