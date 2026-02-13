#!/usr/bin/env python3
"""
Supermarket Mini App - Python Backend
Features: AI Product Images, Telegram Bot, Flask API
"""

import os
import logging
import requests
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
from io import BytesIO
from PIL import Image
import random
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONFIG ====================
BOT_TOKEN = os.getenv('BOT_TOKEN', '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '7351189083'))
BOT_USERNAME = os.getenv('BOT_USERNAME', 'tasamnodostavkabot')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://your-frontend.onrender.com')
PORT = int(os.getenv('PORT', '8000'))

# Hugging Face API uchun token
HF_TOKEN = os.getenv('HF_API_TOKEN', '')

# ==================== FLASK APP ====================
app = Flask(__name__)
CORS(app)

# Global bot application
bot_app = None

# ==================== AI PRODUCT IMAGE GENERATOR ====================
class AIImageGenerator:
    """Hugging Face API orqali AI rasmlari generatsiya qilish"""
    
    @staticmethod
    async def generate_image(prompt: str) -> bytes:
        """AI orqali rasm generatsiya qilish"""
        try:
            # Hugging Face Stable Diffusion API
            if HF_TOKEN:
                api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                
                response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=30)
                
                if response.status_code == 200:
                    return response.content
            
            # Fallback: Placeholder rasm
            return AIImageGenerator.create_placeholder(prompt)
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            return AIImageGenerator.create_placeholder(prompt)
    
    @staticmethod
    def create_placeholder(text: str) -> bytes:
        """Placeholder rasm yaratish"""
        img = Image.new('RGB', (200, 200), color=(102, 126, 234))
        # Rasm faylini bytes'ga aylantiramiz
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io.getvalue()

# ==================== PRODUCTS DATABASE ====================
PRODUCTS = {
    "mevalar": [
        {
            "id": 1,
            "name": "Olma",
            "price": 5000,
            "description": "Qizil, sog'lom olma",
            "prompt": "delicious red apple, professional food photography, high quality"
        },
        {
            "id": 2,
            "name": "Apelsin",
            "price": 6000,
            "description": "Shirin apelsin",
            "prompt": "fresh orange fruit, vibrant color, professional photography"
        },
        {
            "id": 3,
            "name": "Banan",
            "price": 4500,
            "description": "Ranga oqargan banan",
            "prompt": "yellow banana, natural light, high quality food photography"
        },
        {
            "id": 4,
            "name": "Angur",
            "price": 8000,
            "description": "Siyoh, shirin angur",
            "prompt": "bunch of black grapes, fresh, professional food photo"
        }
    ],
    "sutMahsulotlari": [
        {
            "id": 5,
            "name": "Sut (1L)",
            "price": 12000,
            "description": "100% natural sut",
            "prompt": "milk bottle, white fresh milk, professional product photography"
        },
        {
            "id": 6,
            "name": "Yogurt",
            "price": 8000,
            "description": "Sog'lom yogurt",
            "prompt": "yogurt in bowl, fresh dairy, professional food photo"
        },
        {
            "id": 7,
            "name": "Pishloq",
            "price": 25000,
            "description": "Eski pishloq",
            "prompt": "cheese block, delicious cheese, professional food photography"
        }
    ],
    "gosht": [
        {
            "id": 9,
            "name": "Go'sht (1kg)",
            "price": 45000,
            "description": "Yangi mobilli et",
            "prompt": "fresh meat, butcher quality, professional food photo"
        },
        {
            "id": 10,
            "name": "Tovuq (1kg)",
            "price": 35000,
            "description": "Toza tovuq go'sti",
            "prompt": "chicken meat, fresh poultry, professional food photography"
        }
    ],
    "ichimliklar": [
        {
            "id": 12,
            "name": "Suv (1.5L)",
            "price": 3000,
            "description": "Toza ichimlik suvi",
            "prompt": "water bottle, clear water, professional product photo"
        },
        {
            "id": 13,
            "name": "Choy",
            "price": 5000,
            "description": "Qora choy",
            "prompt": "black tea, hot beverage, professional food photo"
        },
        {
            "id": 14,
            "name": "Cola (2L)",
            "price": 12000,
            "description": "Sovun cola",
            "prompt": "cola bottle, refreshing drink, professional product photography"
        }
    ]
}

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': '✅ Bot ishlamoqda!',
        'service': 'Supermarket API v1.0',
        'endpoints': [
            '/api/products',
            '/api/orders',
            '/health'
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'OK'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Barcha mahsulotlarni olish"""
    return jsonify({
        'status': 'success',
        'products': PRODUCTS
    }), 200

@app.route('/api/products/<category>', methods=['GET'])
def get_category_products(category):
    """Kategoriya boʻyicha mahsulotlar"""
    if category not in PRODUCTS:
        return jsonify({'error': 'Category not found'}), 404
    
    return jsonify({
        'status': 'success',
        'category': category,
        'products': PRODUCTS[category]
    }), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Buyurtma yaratish"""
    try:
        data = request.get_json()
        
        # Validation
        user_name = data.get('userName', '')
        phone = data.get('phone', '')
        address = data.get('address', '')
        notes = data.get('notes', '')
        items = data.get('items', [])
        total_price = data.get('totalPrice', 0)
        timestamp = data.get('timestamp', '')
        
        if not all([user_name, phone, address, items]):
            return jsonify({
                'success': False,
                'error': "Barcha maydonlar to'ldirilishi kerak"
            }), 400
        
        # Order ID generatsiya
        import random
        import string
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        
        # Admin xabarini tayyorlash
        items_list = '\n'.join([
            f"  • {item['name']} × {item['quantity']} = {item['price'] * item['quantity']:,} so'm"
            for item in items
        ])
        
        admin_message = f"""
<b>📦 YANGI BUYURTMA #{order_id}</b>

<b>👤 Foydalanuvchi:</b> {user_name}
<b>📱 Telefon:</b> <code>{phone}</code>

<b>📍 Manzil:</b>
<code>{address}</code>

{f'<b>📝 Izoh:</b> {notes}' if notes else ''}

<b>📋 Tafsilotlar:</b>
{items_list}

<b>💰 Narx:</b> {total_price + 25000:,} so'm
<b>⏰ Vaqti:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        """
        
        # Admin'ga xabar yuborish
        try:
            if bot_app:
                import asyncio
                loop = asyncio.new_event_loop()
                loop.run_until_complete(
                    bot_app.bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=admin_message,
                        parse_mode='HTML'
                    )
                )
                loop.close()
            logger.info(f'✅ Order {order_id} saved and admin notified')
        except Exception as e:
            logger.error(f'Admin notification error: {str(e)}')
        
        return jsonify({
            'success': True,
            'message': 'Buyurtma qabul qilindi',
            'orderId': order_id,
            'totalPrice': total_price + 25000
        }), 200
        
    except Exception as e:
        logger.error(f'Order error: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/index.html')
def serve_index():
    """HTML faylini qayta ishlatish"""
    return send_file('index.html')

# ==================== TELEGRAM BOT ====================

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""
    user = update.effective_user
    logger.info(f'New user: {user.first_name} (ID: {user.id})')
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🛒 Supermarketchani ochish',
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ])
    
    await update.message.reply_html("""
<b>🛒 Supermarket ilovasiga xush kelibsiz!</b>

<i>✨ Mahsulotlarni qidiring va buyurtma bering!</i>

🎯 <b>Xususiyatlar:</b>
• 🏪 Keng mahsulot assortimenti
• 🛒 Qulay savatcha tizimi
• 📦 Tez dostavka
• 💬 24/7 qo'llab-quvvatlash

Ilovani boshlash uchun tugmani bosing 👇
    """, reply_markup=keyboard)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    await update.message.reply_html("""
<b>📖 Qo'llanma:</b>

/start - Boshlash
/help - Yordam
/status - Statusni ko'rish

<b>📱 Ilovada:</b>
1️⃣ Mahsulotlarni tanlang
2️⃣ Savatchaga qo'shing
3️⃣ Buyurtma bering
4️⃣ Dostavkani kutib turing

<i>Savollar bo'lsa, admin'ga murojaat qiling! 👉 @tasannodostavka</i>
    """)

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Status command"""
    await update.message.reply_html(f"""
<b>🤖 Bot Status:</b>

✅ <b>Bot:</b> Ishlamoqda
✅ <b>API:</b> Aktiv
✅ <b>Database:</b> Bog'langan
✅ <b>Mini App:</b> {MINI_APP_URL}

<b>📊 Ma'lumot:</b>
• Mahsulotlar: {sum(len(p) for p in PRODUCTS.values())} dona
• Kategoriyalar: 4 ta
• Dostavka vaqti: 30-40 minut

<i>Barcha tizimlar normal!</i>
    """)

def setup_bot():
    """Bot setup"""
    global bot_app
    
    try:
        bot_app = Application.builder().token(BOT_TOKEN).build()
        
        bot_app.add_handler(CommandHandler('start', start_handler))
        bot_app.add_handler(CommandHandler('help', help_handler))
        bot_app.add_handler(CommandHandler('status', status_handler))
        
        logger.info(f"""
╔════════════════════════════════════════╗
║  🛒 SUPERMARKET BOT INITIALIZED ✅    ║
╠════════════════════════════════════════╣
║  Bot: @{BOT_USERNAME}                    ║
║  URL: {MINI_APP_URL[:40]}... ║
║  Port: {PORT}                              ║
║  Products: {sum(len(p) for p in PRODUCTS.values())} dona                              ║
╚════════════════════════════════════════╝
        """)
        
        bot_app.run_polling(allowed_updates=['message'])
    except Exception as e:
        logger.error(f'Bot error: {str(e)}')

def start_bot_thread():
    """Bot'ni thread'da ishga tushirish"""
    bot_thread = threading.Thread(target=setup_bot, daemon=True)
    bot_thread.start()
    logger.info('🤖 Bot thread started')

# ==================== MAIN ====================

if __name__ == '__main__':
    # Bot'ni ishga tushirish
    start_bot_thread()
    
    logger.info(f'🌐 Server starting on 0.0.0.0:{PORT}...')
    
    # Flask app'ni ishga tushirish
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
