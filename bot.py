import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import asyncio
import os
from aiohttp import web

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokenini o'rnating
API_TOKEN = '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo'
WEB_APP_URL = 'https://dostavka-gamma.vercel.app/'  # Mini app URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Buyurtmalarni saqlash uchun (database o'rniga)
orders = {}

# --- PORT UCHUN QISM ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
# -----------------------

@dp.message(CommandStart())
async def start(message: types.Message):
    """Botning /start komandasiga javob"""
    user_name = message.from_user.first_name
    
    kb = [
        [InlineKeyboardButton(text="🛒 Magazinni ochish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    welcome_text = f"""
👋 Salom, {user_name}!

Xush kelibsiz "Dostavka" xizmatiga! 

📦 Biz sizga:
✅ Tez yetkazib berish (30-60 daqiqa)
✅ Sifatli tovarlar
✅ Qulay narxlar
✅ 24/7 qo'llab-quvvatlash

🛍️ Boshlanish uchun tugmani bosing va magazindan xohlagan tovarlarni tanlang!

Savollar bormi? /help komandasini yozing.
"""
    
    await message.answer(welcome_text, reply_markup=keyboard)

@dp.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: types.Message):
    """Mini app'dan kelgan buyurtmani qabul qilish va qayta ishlash"""
    try:
        # Mini app'dan kelgan ma'lumotni JSON formatidan o'qish
        data = json.loads(message.web_app_data.data)
        
        # Buyurtma ma'lumotlarini o'z ichiga olish
        items = data.get("items", [])
        total_items = data.get("totalItems", 0)
        total_price = data.get("totalPrice", 0)
        timestamp = data.get("timestamp", "")
        
        # Buyurtma ID yaratish
        order_id = f"ORD_{message.from_user.id}_{int(datetime.now().timestamp())}"
        
        # Buyurtmani saqlash
        orders[order_id] = {
            "user_id": message.from_user.id,
            "username": message.from_user.username or message.from_user.first_name,
            "items": items,
            "total_items": total_items,
            "total_price": total_price,
            "timestamp": timestamp,
            "status": "pending"  # pending, confirmed, delivered, cancelled
        }
        
        # Buyurtma tasdiqini tayyorlash
        confirmation_text = f"""
✅ BUYURTMA QABUL QILINDI!

📋 Buyurtma raqami: <code>{order_id}</code>

👤 Foydalanuvchi: {message.from_user.first_name} {message.from_user.last_name or ''}

📦 TOVARLAR RO'YXATI:
━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Tovarlarni ro'yxatga olish
        for idx, item in enumerate(items, 1):
            item_name = item.get('name', 'Noma\'lum')
            quantity = item.get('quantity', 0)
            subtotal = item.get('subtotal', 0)
            
            confirmation_text += f"""
{idx}. {item_name}
   └─ Miqdori: {quantity} ta
   └─ Narxi: {subtotal:,} so'm
"""
        
        # Umumiy ma'lumot qo'shish
        confirmation_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━
📊 JAMI:
   • Mahsulotlar: {total_items} ta
   • Umumiy narx: {total_price:,} so'm

⏰ Buyurtma vaqti: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✏️ Status: Jarayonda... (Operatordan kutilmoqda)

💡 KEYINGI QADAMLAR:
1️⃣ Operatorimiz sizga 5 daqiqa ichida bog'lanadi
2️⃣ Yetkazib berish manzilini tasdiqlaymiz
3️⃣ To'lovni amalga oshirasiz
4️⃣ 30-60 daqiqada tovarlar sizga yetadi! 📦

❓ Savollar bormi? /help komandasini yozing
🚀 Boshqa buyurtma berish uchun /start komandasini yozing
"""
        
        await message.answer(confirmation_text, parse_mode="HTML")
        
        # Admin raxbariyatiga xabar yuborish (test uchun o'z ID'izga)
        admin_notification = f"""
🔔 YANGI BUYURTMA!

📋 Buyurtma ID: <code>{order_id}</code>
👤 Foydalanuvchi: {message.from_user.first_name} (ID: {message.from_user.id})

📦 Tovarlar:
"""
        for item in items:
            admin_notification += f"\n• {item['name']} x{item['quantity']} = {item['subtotal']:,} so'm"
        
        admin_notification += f"\n\n💰 Jami: {total_price:,} so'm"
        
        logger.info(f"Yangi buyurtma: {order_id} - {message.from_user.first_name}")
        
        # Foydalanuvchiga qo'shimcha tugmalar ko'rsatish
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📞 Operator bilan aloqa", url="https://t.me/support_bot")],
            [InlineKeyboardButton(text="🔄 Yangi buyurtma berish", web_app=WebAppInfo(url=WEB_APP_URL))]
        ])
        
        await message.answer(
            "🎉 Buyurtmangiz muvaffaqiyatli qabul qilindi! Operator sizga tez orada bog'lanadi.",
            reply_markup=keyboard
        )
        
    except json.JSONDecodeError:
        await message.answer("❌ Xato: Ma'lumotni o'qiyolmadim. Qayta urinib ko'ring.")
    except Exception as e:
        logger.error(f"Xato: {str(e)}")
        await message.answer(f"❌ Xato: {str(e)}\n\nQayta urinib ko'ring yoki /help komandasini yozing.")

@dp.message(lambda message: message.text == "/help")
async def help_command(message: types.Message):
    """Yordam komandasiga javob"""
    help_text = """
📚 YORDAM VA MA'LUMOTLAR

🛍️ BUYURTMA BERISH:
1. /start komandasini yozing
2. "Magazinni ochish" tugmasini bosing
3. Xohlaganingiz tovarlarni tanlang
4. Savatchani to'ldiring
5. "Buyurtmani tasdiqlash" tugmasini bosing

💳 TO'LOV USULLARI:
• Naqd pul (yetkazib berishda)
• Click (/click_payment)
• Payme (/payme_payment)

📦 YETKAZIB BERISH:
• Vaqt: 30-60 daqiqa
• Narx: Buyurtma miqdoridan qarab
• Rajon: Tashkent shahrida

❓ SAVOLLAR:
/contact - Bog'lanish ma'lumotlari
/faq - Ko'p soraladigan savollar
/track - Buyurtmani kuzatish

🤝 MUAMMOLAR:
Agar muammo bo'lsa, operator bilan bog'laning:
📞 +998 90 XXX XX XX
💬 Telegram: @support_bot
"""
    await message.answer(help_text)

@dp.message(lambda message: message.text == "/contact")
async def contact_command(message: types.Message):
    """Bog'lanish ma'lumotlari"""
    contact_text = """
📞 BOG'LANISH MA'LUMOTLARI

☎️ TELEFON RAQAMLAR:
📱 +998 90 123 45 67 (Asosiy)
📱 +998 91 234 56 78 (Yedek)

💬 IJTIMOIY TARMOQLAR:
🔗 Telegram: @dostavka_uz
🔗 Instagram: @dostavka_tashkent
🔗 Facebook: /dostavka.uz

🕐 ISHCHI VAQTI:
⏰ 09:00 - 23:00 (Har kuni)

📍 MANZIL:
Tashkent shahar, Mirzo Ulug'bek tumani
Akademik Abdullayev ko'chasi, 23

📧 EMAIL:
info@dostavka.uz
support@dostavka.uz
"""
    await message.answer(contact_text)

@dp.message(lambda message: message.text == "/faq")
async def faq_command(message: types.Message):
    """Ko'p soraladigan savollar"""
    faq_text = """
❓ KO'P SORALADIGAN SAVOLLAR

🚀 Buyurtma berish qancha vaqt oladiadi?
→ Odatda 5-10 daqiqadir

📦 Yetkazib berish qancha vaqt oladiadi?
→ 30-60 daqiqa (geografik joylashuviga qarab)

💰 Minimum buyurtma narxi nechada?
→ Minimum 50,000 so'm

🚗 Yetkazib berish haqqi nechada?
→ 10,000 - 30,000 so'm (masofaga qarab)

❌ Buyurtmani bekor qilish mumkinmi?
→ Ha, 10 daqiqa ichida. Keyin emas

💯 Tovar sifatasiga kafolat bormi?
→ Ha, 100% kafolat bilan!

🔄 Qaytarish shartlari qanday?
→ 48 soat ichida, qo'l tegmagan holda

📱 Buyurtma holatini qanday o'rganaman?
→ /track komandasini yozing
"""
    await message.answer(faq_text)

@dp.message(lambda message: message.text == "/track")
async def track_command(message: types.Message):
    """Buyurtmani kuzatish"""
    user_orders = [order for order_id, order in orders.items() if order['user_id'] == message.from_user.id]
    
    if not user_orders:
        await message.answer("❌ Sizning buyurtmalaringiz topilmadi. /start komandasini yozing va yangi buyurtma bering.")
        return
    
    tracking_text = "📦 SIZNING BUYURTMALARINGIZ:\n\n"
    
    for order_id, order in orders.items():
        if order['user_id'] == message.from_user.id:
            status_emoji = {
                'pending': '⏳',
                'confirmed': '✅',
                'delivered': '🎉',
                'cancelled': '❌'
            }.get(order['status'], '?')
            
            tracking_text += f"""
{status_emoji} Buyurtma: {order_id}
   Narx: {order['total_price']:,} so'm
   Mahsulotlar: {order['total_items']} ta
   Status: {order['status']}
   Vaqti: {order['timestamp']}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    await message.answer(tracking_text)

@dp.message(lambda message: message.text)
async def echo_message(message: types.Message):
    """Boshqa xabarlar uchun javob"""
    await message.answer(
        "Meni tushunmadim. 🤔\n\n"
        "Quyidagi komandalari ishlating:\n"
        "/start - Asosiy bo'lim\n"
        "/help - Yordam\n"
        "/contact - Bog'lanish\n"
        "/faq - Ko'p soraladigan savollar\n"
        "/track - Buyurtmani kuzatish"
    )

async def main():
    """Botni ishga tushirish"""
    print("🤖 Bot ishga tushdi...")
    # Render uchun portni va botni parallel ishga tushiramiz
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_server()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
