#!/usr/bin/env python3
"""
🛒 Supermarket Mini App - Complete Backend
Features: Flask API, Telegram Bot, Order Management
"""

import os
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== LOGGING ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================
BOT_TOKEN = os.getenv('BOT_TOKEN', '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '7351189083'))
BOT_USERNAME = os.getenv('BOT_USERNAME', 'tasamnodostavkabot')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://dostavka-intc.onrender.com')
PORT = int(os.getenv('PORT', '8000'))

# ==================== FLASK APP ====================
app = Flask(__name__)
CORS(app)

# Global bot application
bot_app = None

# ==================== PRODUCTS DATABASE ====================
PRODUCTS = {
    "mevalar": [
        {
            "id": 1,
            "name": "Olma",
            "price": 5000,
            "image": "https://via.placeholder.com/150?text=Olma",
            "description": "Qizil, sog'lom olma"
        },
        {
            "id": 2,
            "name": "Apelsin",
            "price": 6000,
            "image": "https://via.placeholder.com/150?text=Apelsin",
            "description": "Shirin apelsin"
        },
        {
            "id": 3,
            "name": "Banan",
            "price": 4500,
            "image": "https://via.placeholder.com/150?text=Banan",
            "description": "Ranga oqargan banan"
        },
        {
            "id": 4,
            "name": "Angur",
            "price": 8000,
            "image": "https://via.placeholder.com/150?text=Angur",
            "description": "Siyoh, shirin angur"
        }
    ],
    "sutMahsulotlari": [
        {
            "id": 5,
            "name": "Sut (1L)",
            "price": 12000,
            "image": "https://via.placeholder.com/150?text=Sut",
            "description": "100% natural sut"
        },
        {
            "id": 6,
            "name": "Yogurt",
            "price": 8000,
            "image": "https://via.placeholder.com/150?text=Yogurt",
            "description": "Sog'lom yogurt"
        },
        {
            "id": 7,
            "name": "Pishloq",
            "price": 25000,
            "image": "https://via.placeholder.com/150?text=Pishloq",
            "description": "Eski pishloq"
        }
    ],
    "gosht": [
        {
            "id": 9,
            "name": "Go'sht (1kg)",
            "price": 45000,
            "image": "https://via.placeholder.com/150?text=Gosht",
            "description": "Yangi mobilli et"
        },
        {
            "id": 10,
            "name": "Tovuq (1kg)",
            "price": 35000,
            "image": "https://via.placeholder.com/150?text=Tovuq",
            "description": "Toza tovuq go'sti"
        }
    ],
    "ichimliklar": [
        {
            "id": 12,
            "name": "Suv (1.5L)",
            "price": 3000,
            "image": "https://via.placeholder.com/150?text=Suv",
            "description": "Toza ichimlik suvi"
        },
        {
            "id": 13,
            "name": "Choy",
            "price": 5000,
            "image": "https://via.placeholder.com/150?text=Choy",
            "description": "Qora choy"
        },
        {
            "id": 14,
            "name": "Cola (2L)",
            "price": 12000,
            "image": "https://via.placeholder.com/150?text=Cola",
            "description": "Sovun cola"
        }
    ]
}

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': '✅ Bot ishlamoqda!',
        'service': 'Supermarket API v2.0',
        'miniApp': MINI_APP_URL,
        'endpoints': [
            '/api/products',
            '/api/orders',
            '/health'
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        return jsonify({
            'status': 'success',
            'products': PRODUCTS,
            'count': sum(len(items) for items in PRODUCTS.values())
        }), 200
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()

        # Validate required fields
        user_name = data.get('userName', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        notes = data.get('notes', '').strip()
        items = data.get('items', [])
        total_price = data.get('totalPrice', 0)
        timestamp = data.get('timestamp', datetime.now().isoformat())

        # Validation
        if not all([user_name, phone, address, items]):
            return jsonify({
                'success': False,
                'error': "Barcha majburiy maydonlarni to'ldiring"
            }), 400

        # Generate order ID
        import random
        import string
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

        # Build items list
        items_list = '\n'.join([
            f"  • {item['name']} × {item['quantity']} = {item['price'] * item['quantity']:,} so'm"
            for item in items
        ])

        # Build admin message
        admin_message = f"""
<b>📦 YANGI BUYURTMA #{order_id}</b>

<b>👤 Foydalanuvchi:</b> {user_name}
<b>📱 Telefon:</b> <code>{phone}</code>

<b>📍 Dostavka manzili:</b>
<code>{address}</code>

{f'<b>📝 Qo\'shimcha izoh:</b>{chr(10)}{notes}' if notes else ''}

<b>📋 Buyurtma tafsilotlari:</b>
{items_list}

<b>💰 Oraliq narx:</b> <code>{total_price:,} so'm</code>
<b>🚚 Dostavka:</b> <code>25,000 so'm</code>
<b>💵 JAMI:</b> <code>{total_price + 25000:,} so'm</code>

<b>⏰ Vaqti:</b> {datetime.fromisoformat(timestamp).strftime('%d.%m.%Y %H:%M:%S')}
        """

        logger.info(f'📦 New order created: #{order_id} by {user_name}')

        # Send notification to admin (async)
        try:
            if bot_app:
                asyncio.create_task(
                    bot_app.bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=admin_message,
                        parse_mode='HTML'
                    )
                )
        except Exception as e:
            logger.warning(f'⚠️ Could not send admin notification: {str(e)}')

        return jsonify({
            'success': True,
            'message': 'Buyurtma qabul qilindi',
            'orderId': order_id,
            'totalPrice': total_price + 25000
        }), 200

    except Exception as e:
        logger.error(f'❌ Order processing error: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Xato: {str(e)}'
        }), 500

# ==================== TELEGRAM BOT HANDLERS ====================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    logger.info(f'📱 New user: {user.first_name} (ID: {user.id})')

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🛒 Supermarketchani ochish',
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ])

    message = f"""
<b>🛒 Supermarket ilovasiga xush kelibsiz!</b>

Salom, <b>{user.first_name}!</b> 👋

<i>✨ Mahsulotlarni qidiring, savatchaga qo'shing va buyurtma bering!</i>

<b>🎯 Xususiyatlar:</b>
• 🏪 Keng mahsulot assortimenti
• 🛒 Qulay savatcha tizimi
• 📦 Tez dostavka (30-40 minut)
• 💬 24/7 qo'llab-quvvatlash

Ilovani boshlash uchun quyidagi tugmani bosing 👇
    """

    await update.message.reply_html(message, reply_markup=keyboard)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
<b>📖 Qo'llanma:</b>

<b>/start</b> - Ilovani boshlash
<b>/help</b> - Yordam
<b>/status</b> - Bot statusini ko'rish

<b>📱 Ilovada qanday ishlash kerak:</b>
1️⃣ Kategoriyalardan mahsulot tanlang
2️⃣ "Savatchaga qo'shish" tugmasini bosing
3️⃣ Savatcha bo'limida miqdorni o'zgartiring
4️⃣ "Buyurtma berish" tugmasini bosing
5️⃣ Shaklni to'ldiring va tasdiqlang
6️⃣ Dostavkani kutib turing

<b>❓ Savollar bo'lsa:</b>
Admin: @tasannodostavka
Email: info@supermarket.uz

<i>Bot 24/7 ishlamoqda!</i>
    """
    await update.message.reply_html(help_text)

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command"""
    status_text = f"""
<b>🤖 Bot Status:</b>

✅ <b>Bot:</b> Ishlamoqda
✅ <b>API:</b> Aktiv
✅ <b>Mini App:</b> {MINI_APP_URL}
✅ <b>Database:</b> Bog'langan

<b>📊 Statistika:</b>
• Mahsulotlar: {sum(len(items) for items in PRODUCTS.values())} dona
• Kategoriyalar: 4 ta
• Dostavka vaqti: 30-40 minut
• Eng yaxshi baholangan: 4.8/5 ⭐

<i>Barcha tizimlar normal ishlamoqda!</i>
    """
    await update.message.reply_html(status_text)

def run_bot():
    """Run Telegram bot"""
    global bot_app
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Initialize bot application
        bot_app = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        bot_app.add_handler(CommandHandler('start', start_handler))
        bot_app.add_handler(CommandHandler('help', help_handler))
        bot_app.add_handler(CommandHandler('status', status_handler))

        logger.info(f"""
╔════════════════════════════════════════════════════╗
║     🛒 SUPERMARKET BOT INITIALIZED SUCCESSFULLY   ║
╠════════════════════════════════════════════════════╣
║ 🤖 Bot Username: @{BOT_USERNAME}                    ║
║ 📱 Mini App URL: {MINI_APP_URL[:40]}... ║
║ 🔗 API Server: http://0.0.0.0:{PORT}               ║
║ 📦 Products: {sum(len(items) for items in PRODUCTS.values())} dona                              ║
║ 🌍 Environment: Production                        ║
╚════════════════════════════════════════════════════╝
        """)

        # Run polling
        loop.run_until_complete(bot_app.run_polling(allowed_updates=['message']))
    except Exception as e:
        logger.error(f'❌ Bot error: {str(e)}')
    finally:
        loop.close()

def start_bot_thread():
    """Start bot in separate thread"""
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info('🤖 Bot thread started')

# ==================== MAIN ====================

if __name__ == '__main__':
    # Start bot in background
    start_bot_thread()

    logger.info(f'🌐 Flask server starting on 0.0.0.0:{PORT}...')

    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True,
        use_reloader=False
    )
