# ⚡ Tezkor Boshlash (5 daqiqa)

## 1️⃣ Telegram Bot yarating (1 daqiqa)

1. Telegram da **@BotFather** ni oching
2. `/newbot` yuboring
3. Bot nomini kiriting: `Supermarket`
4. Username kiriting: `my_supermarket_bot` (unikal bo'lishi kerak)
5. **Token**ni saqlab oling (masalan: `123456:ABC-DEF...`)

## 2️⃣ Chat ID ni oling (30 soniya)

1. **@userinfobot** ni oching
2. `/start` yuboring
3. **ID** raqamingizni saqlab oling (masalan: `123456789`)

## 3️⃣ Loyihani o'rnating (2 daqiqa)

### Linux / Mac:
```bash
./setup.sh
```

### Windows:
```cmd
setup.bat
```

Yoki qo'lda:
```bash
# Python dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

## 4️⃣ Konfiguratsiya (1 daqiqa)

### .env faylini yarating va to'ldiring:

```bash
BOT_TOKEN=sizning_bot_tokeningiz
ADMIN_CHAT_ID=sizning_chat_id
WEB_APP_URL=http://localhost:3000
```

### frontend/.env faylini yarating:

```bash
VITE_API_URL=http://localhost:5000
```

## 5️⃣ Ishga tushiring (30 soniya)

**3 ta terminal oching:**

### Terminal 1 - Backend:
```bash
python app.py
```
✅ http://localhost:5000 da ishga tushadi

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```
✅ http://localhost:3000 da ishga tushadi

### Terminal 3 - Bot:
```bash
python bot.py
```
✅ Bot ishga tushadi

## 6️⃣ Testlash (30 soniya)

1. Telegram da o'z botingizga `/start` yuboring
2. "🛒 Supermarketni ochish" tugmasini bosing
3. Ilova ochiladi! 🎉

---

## 🔥 Agar nimadir ishlamasa:

### Backend ishlamayapti?
```bash
# Virtual environment faollashtirilganini tekshiring
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies ni qayta o'rnating
pip install -r requirements.txt

# Serverni qayta ishga tushiring
python app.py
```

### Frontend yuklanmayapti?
```bash
cd frontend

# Dependencies ni qayta o'rnating
npm install

# Cache ni tozalang
rm -rf node_modules/.vite

# Qayta ishga tushiring
npm run dev
```

### Bot javob bermayapti?
1. .env da BOT_TOKEN to'g'ri ekanligini tekshiring
2. Botni qayta ishga tushiring: `python bot.py`
3. Telegram da `/start` ni qayta yuboring

---

## 🎯 Keyingi qadamlar

✅ Lokal testdan so'ng → [DEPLOY.md](DEPLOY.md) ni o'qing
✅ Dizaynni o'zgartirish → [frontend/src/App.css](frontend/src/App.css)
✅ Mahsulot qo'shish → [app.py](app.py) dagi `PRODUCTS` ro'yxati

---

**Yordam kerakmi?** README.md ni to'liq o'qing yoki Issue oching!
