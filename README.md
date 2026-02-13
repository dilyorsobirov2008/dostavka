# 🛒 Telegram Supermarket Mini App

Professional Telegram Mini App supermarket loyihasi - Python (Flask) backend va React frontend bilan.

## ✨ Xususiyatlar

- 🎨 **Zamonaviy dizayn** - Telegram UI/UX standartlariga mos
- 📱 **To'liq responsive** - Barcha qurilmalarda ishlaydi
- 🛒 **Savat tizimi** - Mahsulotlarni qo'shish, o'zgartirish, o'chirish
- 🔍 **Qidiruv va filtr** - Mahsulotlarni tez topish
- 📦 **6+ kategoriya** - Mevalar, sut, go'sht, ichimliklar va h.k.
- 💬 **Telegram integratsiyasi** - Bot orqali buyurtma qabul qilish
- ⚡ **Tez va samarali** - Flask + React + Vite

## 📁 Loyiha strukturasi

```
telegram-supermarket/
├── app.py                 # Flask backend server
├── bot.py                 # Telegram bot
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables namunasi
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Asosiy komponent
│   │   ├── App.css       # Asosiy CSS
│   │   ├── main.jsx      # Entry point
│   │   ├── components/
│   │   │   ├── ProductCard.jsx    # Mahsulot kartasi
│   │   │   └── CartModal.jsx      # Savat modal oynasi
│   │   └── utils/
│   │       └── api.js    # API funksiyalar
│   ├── package.json      # Node dependencies
│   ├── vite.config.js    # Vite config
│   └── index.html        # HTML template
└── README.md             # Bu fayl
```

## 🚀 Ishga tushirish (Lokal)

### 1. Repository ni clone qiling

```bash
git clone <repository-url>
cd telegram-supermarket
```

### 2. Backend ni sozlang

```bash
# Virtual environment yarating
python -m venv venv

# Virtual environment ni faollashtiring
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Dependencies ni o'rnating
pip install -r requirements.txt
```

### 3. Environment variables ni sozlang

```bash
# .env faylini yarating
cp .env.example .env

# .env faylini tahrirlang va quyidagilarni kiriting:
# BOT_TOKEN=your_bot_token_from_botfather
# ADMIN_CHAT_ID=your_telegram_chat_id
```

**Bot token olish:**
1. Telegram da @BotFather ga /start yuboring
2. /newbot buyrug'ini yuboring
3. Bot nomini va username ni kiriting
4. Token ni oling va .env ga qo'shing

**Chat ID olish:**
1. @userinfobot ga /start yuboring
2. O'z ID ingizni oling va .env ga qo'shing

### 4. Backend ni ishga tushiring

```bash
python app.py
```

Backend http://localhost:5000 da ishga tushadi.

### 5. Frontend ni sozlang

Yangi terminal oching:

```bash
cd frontend

# Node packages ni o'rnating
npm install

# .env faylini yarating
cp .env.example .env

# Development server ni ishga tushiring
npm run dev
```

Frontend http://localhost:3000 da ishga tushadi.

### 6. Telegram botni ishga tushiring

Yangi terminal oching:

```bash
# Virtual environment ni faollashtiring
source venv/bin/activate  # yoki Windows: venv\Scripts\activate

# Botni ishga tushiring
python bot.py
```

## 🌐 Production ga deploy qilish

### 1. Frontend ni build qiling

```bash
cd frontend
npm run build
```

Build qilingan fayllar `frontend/dist` papkasida bo'ladi.

### 2. Backend va frontend ni hosting ga yuklang

**Tavsiya etiladigan hostinglar:**
- **Backend:** Heroku, Railway, Render, PythonAnywhere
- **Frontend:** Vercel, Netlify, GitHub Pages

### 3. Telegram botda Web App URL ni o'rnating

```bash
# .env faylidagi WEB_APP_URL ni yangilang
WEB_APP_URL=https://your-deployed-frontend-url.com
```

### 4. BotFather orqali Web App ni ulang

1. @BotFather ga o'ting
2. /setmenubutton buyrug'ini yuboring
3. O'z botingizni tanlang
4. "Send URL" ni bosing
5. Frontend URL ini kiriting

## 📱 Foydalanish

1. **Botni oching:** Telegram da o'z botingizga /start yuboring
2. **Ilova ochiladi:** "🛒 Supermarketni ochish" tugmasini bosing
3. **Mahsulot tanlang:** Kategoriyalardan mahsulot tanlang
4. **Savatga qo'shing:** "+" tugmasini bosing
5. **Buyurtma bering:** Savatni ochib, ma'lumotlarni kiriting
6. **Tasdiqlang:** Admin botga buyurtma kelib tushadi

## 🛠️ API Endpoints

### Products

**GET** `/api/products`
- Barcha mahsulotlarni qaytaradi
- Query params: `category`, `search`

**GET** `/api/categories`
- Barcha kategoriyalarni qaytaradi

### Orders

**POST** `/api/order`
- Yangi buyurtma yaratadi
- Body:
```json
{
  "items": [...],
  "customer": {
    "name": "Ism",
    "phone": "+998901234567",
    "address": "Manzil"
  },
  "total": 150000
}
```

## 🎨 Dizaynni sozlash

CSS faylni tahrirlang: `frontend/src/App.css`

Telegram ranglarini o'zgartirish uchun CSS variables:
```css
:root {
  --tg-theme-bg-color: #ffffff;
  --tg-theme-button-color: #2481cc;
  /* va hokazo... */
}
```

## 📦 Mahsulotlar qo'shish

`app.py` faylidagi `PRODUCTS` ro'yxatiga yangi mahsulot qo'shing:

```python
{
    "id": 21,
    "name": "Yangi mahsulot",
    "price": 10000,
    "category": "kategoriya_id",
    "image": "🍎",
    "unit": "kg"
}
```

## 🔧 Muammolarni bartaraf qilish

### Backend ishlamayapti
- Virtual environment faollashtirilganini tekshiring
- Barcha dependencies o'rnatilganini tekshiring: `pip install -r requirements.txt`
- .env fayli to'g'ri sozlanganini tekshiring

### Frontend yuklanmayapti
- Node packages o'rnatilganini tekshiring: `npm install`
- Backend ishlab turganini tekshiring
- Browser console da xatolarni tekshiring

### Buyurtma Telegram botga kelmayapti
- BOT_TOKEN to'g'ri ekanligini tekshiring
- ADMIN_CHAT_ID to'g'ri ekanligini tekshiring
- Backend loglarini ko'ring

## 📝 Litsenziya

MIT License - o'zingiz xohlagancha ishlatishingiz mumkin!

## 🤝 Yordam

Savollar bo'lsa, Issue ochishingiz mumkin yoki Pull Request yuboring!

## 🎯 Keyingi qadamlar

- [ ] To'lov tizimi (Click, Payme)
- [ ] Mahsulot rasmlari
- [ ] Buyurtmalar tarixi
- [ ] Mahsulot reytingi
- [ ] Push bildirishnomalar
- [ ] Admin panel

---

**Yaratilgan:** 2026-yil
**Texnologiyalar:** Python, Flask, React, Vite, Telegram Bot API
