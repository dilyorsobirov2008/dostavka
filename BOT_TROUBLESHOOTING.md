# 🔧 Bot Muammolarini Hal Qilish

## ❌ Bot javob bermayapti?

### 1-QADAM: .env faylini tekshiring

**.env fayli mavjudmi?**
```bash
# Loyiha papkasida .env faylini tekshiring
ls -la | grep .env
```

Agar yo'q bo'lsa:
```bash
cp .env.example .env
```

**.env faylini oching va to'ldiring:**
```bash
nano .env
# yoki
notepad .env  # Windows
```

**.env fayli ichida:**
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_CHAT_ID=123456789
WEB_APP_URL=http://localhost:3000
```

### 2-QADAM: Bot Token to'g'rimi?

**Token olish:**
1. Telegram da @BotFather ga o'ting
2. `/newbot` yuboring (yangi bot uchun)
   YOKI
   `/mybots` → botingiz → "API Token" → token ni ko'chiring
3. Token formatini tekshiring: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

**Token test qilish:**
```bash
# Terminal da (Linux/Mac)
curl https://api.telegram.org/bot<TOKEN>/getMe

# Browser da
https://api.telegram.org/bot<TOKEN>/getMe
```

Javob:
```json
{
  "ok": true,
  "result": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "Supermarket Bot",
    ...
  }
}
```

Agar `"ok": false` bo'lsa → token noto'g'ri!

### 3-QADAM: Dependencies o'rnatilganmi?

```bash
# Virtual environment ni faollashtiring
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies ni o'rnating
pip install -r requirements.txt

# Maxsus tekshirish
pip install python-telegram-bot==21.0 python-dotenv
```

### 4-QADAM: Botni to'g'ri ishga tushirish

```bash
# Terminal 1: Backend (majburiy emas, lekin tavsiya)
python app.py

# Terminal 2: Bot
python bot.py
```

**Bot ishga tushishi kerak:**
```
==================================================
🤖 TELEGRAM SUPERMARKET BOT
==================================================
✅ Token: 1234567890...
🌐 Web App URL: http://localhost:3000
📡 Polling rejimi: Faol
==================================================

✅ Bot muvaffaqiyatli ishga tushdi!
📝 Telegram da botga /start yuboring

🛑 To'xtatish uchun: Ctrl+C
```

### 5-QADAM: Telegram da test qiling

Telegram da:
1. O'z botingizni toping (search orqali)
2. `/start` yuboring
3. "🛒 Supermarketni ochish" tugmasi paydo bo'lishi kerak

**Agar tugma yo'q bo'lsa:**
1. `/test` yuboring → Bot javob beradimi?
2. Istalgan matn yuboring → Bot javob beradimi?

---

## 🔍 Batafsil Diagnostika

### Test 1: Bot ishlayaptimi?

```bash
python bot.py
```

**Kutilgan natija:**
```
✅ Bot muvaffaqiyatli ishga tushdi!
```

**Xatolar:**

#### "BOT_TOKEN topilmadi!"
→ .env faylida `BOT_TOKEN=...` qo'shing

#### "Invalid token"
→ Token noto'g'ri. @BotFather dan qayta oling

#### "Conflict: terminated by other getUpdates request"
→ Bot boshqa joyda ishlab turibdi. O'sha joyni to'xtating yoki:
```bash
# Webhook ni o'chirish
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

#### "NetworkError" / "Connection refused"
→ Internet aloqangizni tekshiring

### Test 2: Manual test

```bash
# Bot ma'lumotlarini olish
curl https://api.telegram.org/bot<TOKEN>/getMe

# Xabar yuborish test
curl -X POST https://api.telegram.org/bot<TOKEN>/sendMessage \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "<CHAT_ID>", "text": "Test xabar"}'
```

### Test 3: Logs ni tekshirish

Bot ishga tushganda:
```
2024-02-13 10:30:00 - telegram.ext.Application - INFO - Application started
2024-02-13 10:30:01 - __main__ - INFO - Start komandasi: Foydalanuvchi
```

Xatolar:
```
ERROR - Bot ishga tushmadi: [Unauthorized] ...
```

---

## 🐛 Tez-tez uchraydigan xatolar

### 1. "python: command not found"
```bash
# Python o'rnatilganligini tekshiring
python --version
# yoki
python3 --version

# Agar yo'q bo'lsa, o'rnating:
# https://python.org/downloads
```

### 2. "No module named 'telegram'"
```bash
pip install python-telegram-bot==21.0
```

### 3. "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### 4. ".env file not found"
```bash
cp .env.example .env
nano .env  # to'ldiring
```

### 5. Bot webhook rejimida
```bash
# Webhook ni o'chirish
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook

# Bot qayta ishga tushirish
python bot.py
```

---

## ✅ To'liq Test Rejasi

### 1. Environment tekshirish
```bash
# Python versiya (3.8+)
python --version

# pip mavjudmi?
pip --version

# Virtual environment faolmi?
which python  # /path/to/venv/bin/python bo'lishi kerak
```

### 2. Dependencies tekshirish
```bash
pip list | grep telegram
# python-telegram-bot 21.0 ko'rinishi kerak

pip list | grep dotenv
# python-dotenv 1.0.0 ko'rinishi kerak
```

### 3. .env tekshirish
```bash
cat .env
# BOT_TOKEN=... ko'rinishi kerak
# ADMIN_CHAT_ID=... ko'rinishi kerak
```

### 4. Token test
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
# {"ok": true, ...} qaytishi kerak
```

### 5. Bot test
```bash
python bot.py
# ✅ Bot muvaffaqiyatli ishga tushdi!
```

### 6. Telegram test
- `/start` → Tugma paydo bo'ladi
- `/test` → Bot ma'lumotlari qaytadi
- `/help` → Yordam xabari keladi

---

## 🆘 Hali ham ishlamayaptimi?

### Debug rejimi

`bot.py` da logging darajasini o'zgartiring:

```python
logging.basicConfig(
    level=logging.DEBUG  # INFO dan DEBUG ga
)
```

### Minimal test bot

`test_bot.py` yarating:
```python
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "sizning_tokeningiz"

async def start(update: Update, context):
    await update.message.reply_text("Bot ishlayapti! ✅")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot ishga tushdi...")
app.run_polling()
```

Test:
```bash
python test_bot.py
```

Telegram da `/start` → "Bot ishlayapti! ✅" kelishi kerak.

Agar bu ishlamasa:
1. ✅ Python to'g'ri o'rnatilgan
2. ✅ python-telegram-bot to'g'ri o'rnatilgan
3. ❌ Token noto'g'ri → @BotFather dan qayta oling
4. ❌ Internet aloqa yo'q → Wi-Fi/LAN tekshiring

---

## 📞 Yordam

Agar muammo hal bo'lmasa:

1. **Bot log larini saqlab oling:**
   ```bash
   python bot.py > bot_logs.txt 2>&1
   ```

2. **Muammo tavsifini yozing:**
   - Qanday xatolik?
   - Qaysi qadamda to'xtayapti?
   - Xatolik xabari?

3. **Quyidagilarni yuklang:**
   - bot_logs.txt
   - .env.example (tokenlariz yo'q!)
   - requirements.txt

---

**Omad!** 🚀
