# 🚀 Render.com'ga Deploy Qilish - To'liq Qo'llanma

## 📋 Tayyorlash

### 1️⃣ GitHub'da Repository Yaratish

```bash
# GitHub'ga login qiling va yangi repository yarating
# Repository nomi: supermarket-mini-app
```

### 2️⃣ Lokal Loyihangizni GitHub'ga Push Qilish

```bash
# Backend papkada
git init
git add .
git commit -m "Initial commit - Supermarket Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/supermarket-mini-app.git
git push -u origin main
```

---

## 🔧 Backend (Bot) - Render.com'ga Deploy

### Step 1: Render.com'da Login Qilish

1. **[render.com](https://render.com)** ochib, GitHub account bilan sign up qiling
2. Dashboard'ga o'ting
3. **"New +"** tugmasini bosing → **"Web Service"** tanlang

### Step 2: Repository'ni Ulang

```
1. "Connect a repository" bosing
2. GitHub account'ni approve qiling
3. supermarket-mini-app repository'ni tanlang
4. Branch: main
```

### Step 3: Service Sozlamalarini Kiritish

```
Name:                    supermarket-bot
Environment:             Node
Build Command:           npm install
Start Command:           npm start
Instance Type:           Free (yoki Paid)
```

### Step 4: Environment Variables'ni O'rnatish

Dashboard'da **"Environment"** bo'limiga o'ting va quyidagilarni qo'ying:

```
BOT_TOKEN = 8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo
ADMIN_CHAT_ID = 987654321              (O'zingizning Telegram ID)
BOT_USERNAME = supermarket_shop_bot
MINI_APP_URL = https://your-supermarket-frontend.onrender.com (Frontend URL keyinroq)
NODE_ENV = production
PORT = 8000
```

### Step 5: Deploy Qilish

```
"Create Web Service" tugmasini bosing
Render deploy qilishni boshlaidi (2-5 minut vaqt oladi)
✅ Deployment complete bo'lganidan keyin URL olasiz:
   https://supermarket-bot.onrender.com (tasodifiy nomi bo'ladi)
```

---

## 🎨 Frontend (React App) - Render.com'ga Deploy

### Step 1: Yangi Service Yaratish

```
1. Render Dashboard'ga o'ting
2. "New +" → "Static Site"
3. supermarket-mini-app repository'ni tanlang (agar bog'lamagan bo'lsangiz)
```

### Step 2: Build Sozlamalarini Kiritish

```
Name:                supermarket-frontend
Build Command:       npm run build
Publish Directory:   dist
```

### Step 3: Deploy Qilish

```
"Create Static Site" tugmasini bosing
Frontend deploy bo'lishini kutib turing
✅ Frontend URL ohasiz:
   https://supermarket-frontend.onrender.com
```

### Step 4: Environment File'ni Yangilash

Frontend'da `.env` faylni yangilang:

```env
VITE_API_URL=https://supermarket-bot.onrender.com
```

Yangi build deploy qiling:
```bash
git add .env
git commit -m "Update API URL for Render deployment"
git push origin main
```

---

## 🔗 BotFather'da Mini App URL'ni O'rnatish

Telegram'da @BotFather'ga yozing:

```
/setmenubutton
→ supermarket_shop_bot tanlang
→ URL: https://supermarket-frontend.onrender.com
→ Button text: 🛒 Supermarketchani ochish
```

---

## 🧪 Deployment'ni Test Qilish

### 1. Bot'ni Test Qilish

```
Telegram'da @supermarket_shop_bot'ga /start yozing
Mini App tugmasini bosing
Frontend yuklanishi kerak
```

### 2. API'ni Test Qilish

```bash
# Backend health check
curl https://supermarket-bot.onrender.com/health

# Output:
# {"status":"OK"}
```

### 3. Order Test Qilish

```javascript
// Browser Console'da
fetch('https://supermarket-bot.onrender.com/api/orders', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userId: 123456789,
    userName: 'Test User',
    phone: '+998901234567',
    address: 'Test Address',
    notes: 'Test note',
    items: [
      { id: 1, name: 'Test Product', price: 5000, quantity: 1 }
    ],
    totalPrice: 5000,
    timestamp: new Date().toISOString()
  })
})
.then(r => r.json())
.then(d => console.log(d))
```

---

## 📊 Render.com Sozlamalarini Monitoring Qilish

### Logs'ni Ko'rish

```
1. Render Dashboard
2. Serviceingizni tanlang
3. "Logs" bo'limiga o'ting
4. Real-time logs ko'rish mumkin
```

### Uptime Monitoring

Render Free plan'da:
- ⚠️ Service inaktiv bo'lsa 15 dakikada sleep rejimiga o'tadi
- ✅ Paid plan'da 24/7 ishlaydi

Uptime robot qo'shish:
```
1. https://uptimerobot.com dan login qiling
2. Monitoring qo'shish: https://supermarket-bot.onrender.com/health
3. Har 5 minutda monitor qiladi (service sleep rejimiga tushmasligi uchun)
```

---

## 🛠️ Keng Ishlatiladigan Muammolar va Yechim

### ❌ "Bot not responding"

**Yechim:**
```
1. Environment variables'ni tekshiring (BOT_TOKEN, ADMIN_CHAT_ID)
2. Deploy logs'ni ko'ring
3. Bot'ni restart qiling (Render Dashboard → Restart button)
```

### ❌ "CORS Error"

**Yechim:**
Backend `bot.js`'da CORS qo'shilgan:
```javascript
const cors = require('cors');
app.use(cors());
```

### ❌ "API 404 error"

**Yechim:**
- Frontend'da `VITE_API_URL` to'g'ri bo'lishini tekshiring
- Backend URL'i HTTPS bo'lishi kerak
- Trailing slash bo'lmasligi kerak

### ❌ "Frontend doesn't load"

**Yechim:**
```
1. Build command'ni tekshiring: npm run build
2. Publish directory: dist
3. Logs'da error ko'rish
```

---

## 📱 Mini App'ni Test Qilish (Telegram Desktop)

```
1. Telegram Desktop o'rnatish
2. Bot'ga /start yozing
3. 🛒 Tugmasini bosing
4. Mini App yuklanishi kerak
5. DevTools (F12) bilan debug qiling
```

---

## 💰 Render.com Pricing

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 750 compute hours/month, Sleep after 15min inactive |
| Starter | $7 | Unlimited compute hours |
| Standard | $25+ | High performance |

**Tavsiya:** Dastlab Free plan'da test qiling, keyin Starter plan'ga o'ting.

---

## 🔐 Production Security Checklist

- ✅ BOT_TOKEN `.env`'da saqlandi (git'ga qo'ymadi)
- ✅ HTTPS URL ishlatilgan (http emas)
- ✅ ADMIN_CHAT_ID maxfiy qo'shilgan
- ✅ Frontend va Backend CORS sozlangan
- ✅ Input validation qo'shilgan
- ✅ Error logging qo'shilgan

---

## 📞 Keyingi Qadamlar

1. **Database Qo'shish** - MongoDB Atlas (free tier)
2. **To'lov Tizimi** - Stripe/Click/Payme
3. **Real-time Updates** - Socket.io
4. **Push Notifications** - Firebase
5. **Analytics** - Google Analytics

---

## ✅ Deploy Checklist

- [ ] GitHub'da repository yaratildi
- [ ] Lokal kod GitHub'ga push qilindi
- [ ] Render.com'da Backend service yaratildi
- [ ] Render.com'da Frontend service yaratildi
- [ ] Environment variables o'rnatildi
- [ ] BotFather'da Mini App URL o'rnatildi
- [ ] Bot /start'da Mini App tugmasini ko'rsatadi
- [ ] Frontend Mini App'da yuklanadi
- [ ] Order API test qilindi
- [ ] Admin Telegram'da order xabari oladi

---

**Tabriklashlarim! 🎉 Mini app'ingiz live! 🚀**

Savollar bo'lsa, bu qo'llanmani qaytadan o'qib ko'ring yoki log'larni tekshiring.
