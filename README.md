# 🛒 Telegram Mini App Supermarket Ilovasi

Telegram platformasida ishlaydigan to'liq supermarket ilovasi. Mahsulotlarni katalogdan tanlash, savatchaga qo'shish va buyurtma berish imkoniyati.

---

## 📦 Texnik Stack

**Frontend:**
- React 18
- Vite
- CSS3 (Telegram TMA UI uslubida)
- @telegram-apps/sdk

**Backend:**
- Node.js
- Express
- Telegraf (Telegram Bot API)
- MongoDB (ixtiyoriy, uchun ma'lumotlarni saqlash)

---

## 🚀 O'rnatish va Ishga Tushirish

### Frontend Setup

```bash
# 1. Frontend papkasiga o'tish
cd frontend

# 2. Modullarni o'rnatish
npm install

# 3. Development serverini ishga tushirish
npm run dev
# http://localhost:5173 ochilib ishga tushradi
```

### Backend Setup

```bash
# 1. Backend papkasiga o'tish
cd backend

# 2. Modullarni o'rnatish
npm install

# 3. .env faylini tayyorlash
cp .env.example .env
# Va quyidagilarni to'ldiring:
# - BOT_TOKEN (BotFather'dan olingan)
# - ADMIN_CHAT_ID (admin'ning chat ID'si)
# - MINI_APP_URL (frontend URL'i)

# 4. Botni ishga tushirish
npm run dev
# Polling rejimida dastlab sinovdan o'tkazish uchun:
# .env'da: USE_POLLING=true qilib qo'ying
```

---

## 🔑 Telegram Bot Tayyorlash

### 1. BotFather'dan Bot Yaratish

```
/start → @BotFather'ga yozing
/newbot → yangi bot yaratish
Botga nom bering (masalan: SupermarketBot)
Username bering (masalan: supermarket_shop_bot)
Token olib qo'ying (va .env'ga qo'ying)
```

### 2. Mini App URL'ni O'rnatish

```
@BotFather → /setmenubutton
Bot tanlash → Token yozish
URL: https://yourdomain.com (o'z domeni)
Tugma matni: 🛒 Supermarketchani ochish
```

### 3. Admin Chat ID Olish

```
# Bot'ga /start yozing
# Consoleda olib qo'ying:
console.log(ctx.message.chat.id)
```

---

## 📁 Papka Struktura Tushuntirish

```
supermarket-tma/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.jsx          ← Asosiy komponenta
│   │   │   ├── Category.jsx     ← Kategoriya filtrasi
│   │   │   ├── Cart.jsx         ← Savatcha
│   │   │   ├── Checkout.jsx     ← Buyurtma shakli
│   │   │   └── Header.jsx       ← Yuqori qism
│   │   ├── App.css              ← Barcha stillar
│   │   ├── main.jsx             ← Kirish nuqtasi
│   │   └── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── bot.js                   ← Asosiy bot kodi
│   ├── handlers/
│   │   ├── orderHandler.js
│   │   └── notificationHandler.js
│   ├── package.json
│   ├── .env.example
│   └── .env                     ← Muhim ma'lumotlar (git'ga qo'ymang!)
│
└── README.md
```

---

## 🎨 Xususiyatlar va Funksiyalar

### ✅ Amalga Oshirilgan

- **Katalog Tizimi**: 4 ta kategoriya (Mevalar, Sut mahsulotlari, Go'sht, Ichimliklar)
- **Savatcha**: Mahsulotlarni qo'shish, o'chirish, miqdorni o'zgartirish
- **Buyurtma Shakli**: Foydalanuvchi ma'lumotlarini so'rash
- **Admin Bildirishnomasi**: Bot orqali admin'ga habar yuborish
- **Responsive Dizayn**: Barcha qurilmalarda yaxshi ko'rinadi
- **Telegram UI**: Telegramning o'ziga o'xshash uslubi

### 🔄 Keyin Qo'shish Mumkin

- **To'lov**: Stripe / Click / Payme integratsiyasi
- **Reyting Tizimi**: Mahsulotlarni baholash
- **Favoritlar**: Sevimli mahsulotlarni saqlash
- **Order History**: Oldingi buyurtmalarni ko'rish
- **Push Bildirishnomalar**: Buyurtma statusini kuzatish
- **Database**: MongoDB orqali ma'lumotlarni saqlash

---

## 🔗 API Endpointlari

### POST `/api/orders`

Yangi buyurtma yaratish

**Request:**
```json
{
  "userId": 123456789,
  "userName": "Ali Aliev",
  "phone": "+998901234567",
  "address": "Tashkent, Mirzo Ulugbek ko'chasi 25",
  "notes": "Pintig'iga qo'ng'iroq qiling",
  "items": [
    {
      "id": 1,
      "name": "Olma",
      "price": 5000,
      "quantity": 2
    }
  ],
  "totalPrice": 35000,
  "timestamp": "2024-02-13T10:30:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Buyurtma qabul qilindi",
  "orderId": "ORD123456"
}
```

---

## 🛠️ Muhim JavaScript Snippets

### Telegram SDK Ishlatish

```javascript
import { initializeApp } from '@telegram-apps/sdk';

const tmaSDK = initializeApp();
const user = tmaSDK.initDataUnsafe?.user;

console.log(`Foydalanuvchi: ${user.first_name}`);
```

### Haptic Feedback (Titreshtirish)

```javascript
import { useHapticFeedback } from '@telegram-apps/sdk';

const haptic = useHapticFeedback();

// Tugma bosilganda
haptic.impactOccurred('light');
```

### Main Button

```javascript
const mainButton = tmaSDK.mainButton;
mainButton.setText('Buyurtmani yuborish');
mainButton.onClick(() => {
  // Buyurtmani yuborish logikasi
});
mainButton.show();
```

---

## 🐛 Tez-tez Muammolar va Yechim

### Problem: "BOT_TOKEN is not defined"
**Yechim:** .env faylini tekshiring va `npm install dotenv` qo'ling

### Problem: "Cannot GET /api/orders"
**Yechim:** Backend serverini ishga tushirgansiz mi? `npm run dev` ishlatib ko'ring

### Problem: Mini App yuklanmayapti
**Yechim:** 
- Frontend URL'i to'g'ri bo'lishini tekshiring
- HTTPS ishlatayotganingizni tekshiring (HTTP Telegram'da ishlamaydi)

### Problem: Bot habar yubormiayapti
**Yechim:**
- ADMIN_CHAT_ID to'g'ri bo'lishini tekshiring
- Bot'ni guruhga qo'shib, admin qilib qo'ying

---

## 📱 Deployment (Production)

### Frontend (Vercel/Netlify)

```bash
# 1. Vercel o'rnatish
npm install -g vercel

# 2. Deploy qilish
vercel --prod

# 3. URL olib, BotFather'da Mini App URL qo'ying
```

### Backend (Heroku/Railway)

```bash
# 1. Heroku'da yangi app yaratish
heroku create supermarket-bot

# 2. Environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMIN_CHAT_ID=your_id

# 3. Push qilish
git push heroku main
```

---

## 💡 Muhim Maslahatlar

1. **Security**: Foydalanuvchi ma'lumotlarini validate qiling
2. **Error Handling**: Barcha APIlar uchun try-catch ishlatip qo'ying
3. **Testing**: Polling rejimida local'da sinovdan o'tkazing
4. **Rate Limiting**: Spamga qarshi himoya qo'ying
5. **Logging**: Barcha buyurtmalarni database'ga saqlang

---

## 📞 Qo'shimcha Yordam

- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Mini Apps**: https://core.telegram.org/bots/webapps
- **Telegraf Docs**: https://telegraf.js.org

---

## 📄 Litsenziya

MIT License - Erkin ishlatish mumkin ✅

**Muvaffaq bo'lishlaringizni tilayman! 🚀**
