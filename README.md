# 🛒 SuperMarket Mini App - Telegram Bot

Telegram mini app uchun professional e-commerce magazin. 106 ta tovar, Render.com deploy.

## ⚡ QUICK START (2 min)

### Local Testing:
```bash
cd supermarket
pip install -r requirements.txt
python run.py
```

Server: http://localhost:5000

### Production (Render):
```bash
git push origin main
# Render auto-deploy
```

API URL: https://supermarket-mini-app.onrender.com/api

✅ **106 ta tovar** - 12 ta kategoriyada
✅ **Real vaqtda Telegram integration** - Bot orqali buyurtmalar
✅ **Rasm bilan tovarlar** - Unsplash integratsiyasi
✅ **Savat tizimi** - Qo'shish, ayirish, ko'paytirish
✅ **Qidiruv** - Tovarlarni nomi bo'yicha topish
✅ **Responsive design** - Barcha telefonlarda ishlaydi
✅ **Orders tracking** - Barcha buyurtmalarni saqlash
✅ **Admin panel API** - /api/orders dan ko'rishish

---

## 🚀 Joylashtirish (Render.com)

### 1️⃣ GitHub ga upload qiling

```bash
git init
git add .
git commit -m "SuperMarket Mini App"
git remote add origin https://github.com/YOUR_USERNAME/supermarket.git
git push -u origin main
```

### 2️⃣ Render.com da yangi web service yaratish

1. https://render.com ga kiring va login qiling
2. "New +" bosing, "Web Service" tanlang
3. GitHub repositoriyangizni tanlang
4. Quyidagi ma'lumotlarni kiriting:

```
Name: supermarket-mini-app
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

5. Environment Variables qo'shing:
```
TELEGRAM_BOT_TOKEN = YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID = YOUR_CHAT_ID
PORT = 5000
```

### 3️⃣ Deploy qiling
"Create Web Service" bosing. Render 2-3 daqiqada deploy qiladi.

---

## 🤖 Telegram Bot Setup

### Bot Token olish (@BotFather orqali):

1. Telegram da @BotFather ga yozing
2. `/newbot` yozing
3. Bot nomini kiriting: `SuperMarket`
4. Bot usernameni kiriting: `@your_supermarket_bot`
5. Token olyapsiz (simplex: `123456:ABCDEFGH...`)

### Chat ID olish:

1. Botga `/start` yozing
2. Render logslarini ko'rib, sizning user IDni toping
3. Yoki: https://api.telegram.org/botYOUR_TOKEN/getUpdates
   - `"id": 123456789` - bu sizning Chat ID

### Telegram Mini App qo'shish:

1. @BotFather ga `/mybots` yozing
2. Botingizni tanlang
3. "Bot Settings" → "Menu Button"
4. URL kiriting: `https://your-render-app.onrender.com`

---

## 💻 Local Development

### Setup:

```bash
# 1. Python 3.8+ o'rnatish
python --version

# 2. Venv yaratish
python -m venv venv

# 3. Venv aktivlashtirish
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Dependencies o'rnatish
pip install -r requirements.txt

# 5. .env fayl yaratish
cp .env.example .env
# .env faylga token va chat IDni kiriting

# 6. Server ishga tushirish
python app.py
```

Server http://localhost:5000 da ishga tushadi

### Testing:

- Frontend: http://localhost:5000
- Products API: http://localhost:5000/api/products
- Orders API: http://localhost:5000/api/orders
- Health check: http://localhost:5000/health

---

## 📁 Fayllar Tuzilishi

```
supermarket/
├── app.py                 # Flask backend (106 tovar, bot integration)
├── index.html            # Frontend (Telegram mini app)
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku/Render deployment
├── render.yaml          # Render konfiguratsiyasi
├── .env.example         # Environment variables template
├── orders.json          # Buyurtmalarni saqlash (auto-created)
└── README.md           # Bu fayl
```

---

## 🔧 API Endpoints

### GET `/api/products`
Barcha tovarlarni olish
```json
{
  "categories": ["🍎 Meva", "🥗 Sabzavot", ...],
  "products": [
    {
      "id": 1,
      "name": "Olma (kg)",
      "category": "🍎 Meva",
      "price": 8000,
      "image": "https://...",
      "description": "Sho'rta, shirinli olma"
    }
  ]
}
```

### POST `/api/orders`
Buyurtma yaratish
```json
{
  "user_id": 12345,
  "user_name": "Amir",
  "phone": "+998901234567",
  "location": "Tashkent, 5-qo'rg'on",
  "items": {
    "1": {"quantity": 2, "name": "Olma", "price": 8000}
  },
  "total": 16000
}
```

### GET `/api/orders`
Barcha buyurtmalarni olish (admin)

### GET `/api/orders/:id`
Buyurtma ma'lumotini olish

### PUT `/api/orders/:id/status`
Buyurtma statusini yangilash

---

## 🎨 Tovarlarni Qo'shish/O'zgartirish

`app.py` faylida `PRODUCTS` dictionary ga yangi tovarlar qo'shing:

```python
{
    "id": 107,
    "name": "Yangi Tovar",
    "category": "🍎 Meva",
    "price": 15000,
    "image": "https://images.unsplash.com/photo-xxx?w=300&h=300&fit=crop",
    "description": "Tavsifi"
}
```

---

## 📊 Statistika

`GET /api/stats`

```json
{
  "total_orders": 45,
  "total_revenue": 1250000,
  "pending_orders": 12,
  "completed_orders": 33,
  "average_order": 27777
}
```

---

## ⚙️ Render Setting va Troubleshooting

### Port Error:
```
ERROR: Port 5000 already in use
```
Yechim: `PORT=8000 python app.py`

### CORS Error:
Render app URL: `https://supermarket-mini-app.onrender.com`
Frontend URL: `https://supermarket-mini-app.onrender.com`

### Bot not sending messages:
- Token to'g'rimi? @BotFather dan qayta oling
- Chat ID to'g'rimi? https://api.telegram.org/botTOKEN/getUpdates tekshiring

### Deploy Failed:
1. `requirements.txt` barcha dependency'larni o'z ichiga oladimi?
2. `app.py` uchun syntax error bor mi?
3. Render logs ko'ring: Dashboard → Logs

---

## 📱 Telegram Mini App Qo'shish

### Menu Button orqali:
1. @BotFather → `/mybots` → Botingiz
2. "Bot Settings" → "Menu Button" → "Web App"
3. URL: `https://supermarket-mini-app.onrender.com`
4. Text: `🛒 Magazin`

### Deep Linking:
```
https://t.me/YOUR_BOT_USERNAME?startapp=menu
```

---

## 💡 Tips

1. **Orders saqlash**: `orders.json` serverda saqlanadi. Render restart qilinsa ham orders yo'q bo'lmaydi (persist storage emas uchun)
2. **Rasm linklarini yangilash**: `app.py` dagi image URL larni o'zingizning CDN ga o'zgartirishingiz mumkin
3. **Tovarlar kategoriyasi**: Emoji bilan nom berish qolipiga amal qiling (masalan: "🍎 Meva")
4. **Bot responsiveness**: Render free plan 0 xotira bo'lishi mumkin. Paid plan olishni tavsiya qilamiz

---

## 📄 License

Open Source - Erkin foydalaning!

---

## 👨‍💻 Support

Savollar bo'lsa, Telegram: @YOURNAME

**Happy selling! 🛒✨**
