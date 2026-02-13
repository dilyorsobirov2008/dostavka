# 🚀 Yangi Bot Setup Guide - HTML/JS + Python + AI Images

## 📦 Kerakli Fayllar

```
supermarket-bot-new/
├── app.py                    ← Python Backend (AI + Bot)
├── index.html                ← Frontend (HTML/CSS/JS)
├── requirements.txt          ← Python dependencies
├── Procfile                  ← Render deployment
├── .env                      ← Environment variables
└── .gitignore
```

---

## 🎯 Features

✅ **HTML/CSS/JavaScript Frontend**
- Responsive design
- Telegram Mini App compatible
- Offline-first

✅ **Python Backend**
- Flask API
- Telegram Bot integration
- Order management

✅ **AI Product Images** (Optional)
- Hugging Face Stable Diffusion API
- Automatic image generation
- Fallback placeholder images

---

## 🔧 Lokal Setup (Development)

### 1️⃣ Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

### 2️⃣ Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

### 3️⃣ .env Faylini Tayyorlash

```bash
cp .env-template .env
```

`.env` da quyidagilarni kiritish:
```
BOT_TOKEN=8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo
ADMIN_CHAT_ID=7351189083
BOT_USERNAME=tasamnodostavkabot
MINI_APP_URL=http://localhost:8000
PORT=8000
```

### 4️⃣ Bot'ni Ishga Tushirish

```bash
python app.py
```

Server ishlab ketadi: `http://localhost:8000`

### 5️⃣ Test Qilish

```bash
# Browser'da
http://localhost:8000/index.html

# API test
curl http://localhost:8000/api/products

# Bot test
Telegram @tasamnodostavkabot'ga /start yozing
```

---

## 🌐 Render'da Deploy

### Step 1: GitHub'ga Push Qiling

```bash
git add app.py index.html requirements.txt Procfile .env
git commit -m "New bot with AI images"
git push origin main
```

### Step 2: Render'da Web Service Yaratish

```
1. Render.com → New Web Service
2. GitHub repository ulang
3. Build Command: pip install -r requirements.txt
4. Start Command: gunicorn -w 1 -b 0.0.0.0:$PORT app:app
5. Environment: Python 3.11
```

### Step 3: Environment Variables

```
BOT_TOKEN=8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo
ADMIN_CHAT_ID=7351189083
BOT_USERNAME=tasamnodostavkabot
MINI_APP_URL=https://your-service.onrender.com
PORT=8000
HF_API_TOKEN=(optional)
```

### Step 4: Deploy

```
"Create Web Service" → Deploy
```

---

## 🤖 Telegram Bot Setup

### BotFather'da

```
@BotFather'ga:

/setmenubutton
→ tasamnodostavkabot
→ URL: https://your-service.onrender.com/index.html
→ Text: 🛒 Supermarketchani ochish
```

---

## 📊 API Endpoints

### GET Requests

```
GET /                          → Status
GET /health                    → Health check
GET /api/products              → Barcha mahsulotlar
GET /api/products/<category>   → Kategoriya mahsulotlari
```

### POST Requests

```
POST /api/orders
Body: {
  "userName": "Ali",
  "phone": "+998901234567",
  "address": "Tashkent, 123",
  "notes": "...",
  "items": [...],
  "totalPrice": 50000,
  "timestamp": "2024-02-13T12:00:00Z"
}
```

---

## 🎨 AI Product Images

### Hugging Face API Ishlatish

1. **Token Olish**:
   - https://huggingface.co/settings/tokens
   - New token yaratish

2. **.env'da Qo'shish**:
   ```
   HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
   ```

3. **Avtomatik Rasm Generatsiyasi**:
   - Backend avtomat ravishda rasmlari generatsiya qiladi
   - Fallback: Placeholder rasmlari

---

## 🧪 Testing Checklist

- [ ] Lokal'da bot ishlamoqda
- [ ] HTML/JS interface ishlaydi
- [ ] API endpoints javob beraydi
- [ ] Buyurtma test qilindi
- [ ] Admin Telegram'da xabar oldi
- [ ] Render'ga deploy qilindi
- [ ] Bot Telegram'da /start beraydi
- [ ] Mini App yuklanadi
- [ ] Buyurtma production'da ishlaydi

---

## 🛠️ Troubleshooting

### Bot "Not Found" deyapti

```
1. Render logs'ni ko'ring
2. Environment variables tekshiring
3. PORT = 8000 bo'lishini tekshiring
```

### Mini App yuklanmayapti

```
1. MINI_APP_URL tekshirish
2. index.html API_URL o'rnatish
3. CORS enabled (flask-cors)
```

### AI Rasmlari generatsiya qilinmayapti

```
1. HF_API_TOKEN kiritish (optional)
2. Placeholder rasmlari ishlatiladi (default)
```

---

## 📱 Production Checklist

- [ ] .env secure qilingan (.gitignore)
- [ ] HTTPS URL ishlatilgan
- [ ] CORS sozlanmagan
- [ ] Error logging enabled
- [ ] Rate limiting qo'shilgan
- [ ] Database backup plan
- [ ] Uptime monitoring (UptimeRobot)

---

## 📈 Keyin Qo'shish Mumkin

- [ ] Database (MongoDB/PostgreSQL)
- [ ] User authentication
- [ ] Order history
- [ ] Real-time notifications
- [ ] Payment integration
- [ ] Admin dashboard
- [ ] Analytics

---

## 🎉 Tayyor!

Bot 100% setup va ishga tushirish uchun tayyor! 🚀

Test qiling va feedback bering! 📝
