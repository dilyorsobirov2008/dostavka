#!/usr/bin/env python3
"""
Telegram Mini App Supermarket Bot - Python Version
Using python-telegram-bot library
"""

import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Environment variables'ni yuklash
load_dotenv()

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot sozlamalari
BOT_TOKEN = os.getenv('BOT_TOKEN', '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '123456789'))
BOT_USERNAME = os.getenv('BOT_USERNAME', 'supermarket_shop_bot')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://your-supermarket-frontend.onrender.com')
PORT = int(os.getenv('PORT', '8000'))

# Flask app
app = Flask(__name__)

# Health check endpoint
@app.route('/', methods=['GET'])
def health():
    return jsonify({
        'status': 'Bot is running! ✅',
        'botUsername': BOT_USERNAME,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

# Order API endpoint
@app.route('/api/orders', methods=['POST'])
async def create_order():
    try:
        data = request.get_json()
        
        # Ma'lumotlarni tekshirish
        user_name = data.get('userName', '')
        phone = data.get('phone', '')
        address = data.get('address', '')
        notes = data.get('notes', '')
        items = data.get('items', [])
        total_price = data.get('totalPrice', 0)
        user_id = data.get('userId')
        timestamp = data.get('timestamp', '')
        
        if not all([user_name, phone, address, items]):
            return jsonify({'error': 'Barcha maydonlar to\'ldirilishi kerak', 'success': False}), 400
        
        # Buyurtma raqamini generatsiya qilish
        import random
        import string
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        
        # Buyurtma xabarini tayyorlash
        items_list = '\n'.join([
            f"  • {item['name']} × {item['quantity']} = {item['price'] * item['quantity']:,} so'm"
            for item in items
        ])
        
        admin_message = f"""
<b>📦 YANGI BUYURTMA #{order_id}</b>

<b>👤 Foydalanuvchi:</b> {user_name}
<b>📱 Telefon:</b> <code>{phone}</code>
<b>🆔 User ID:</b> <code>{user_id or 'N/A'}</code>

<b>📍 Dostavka manzili:</b>
<code>{address}</code>

{f'<b>📝 Qo\'shimcha izoh:</b>\n{notes}' if notes else ''}

<b>📋 Buyurtma tafsilotlari:</b>
{items_list}

<b>💰 Oraliq narx:</b> <code>{total_price:,} so'm</code>
<b>🚚 Dostavka:</b> <code>25,000 so'm</code>
<b>💵 JAMI:</b> <code>{total_price + 25000:,} so'm</code>

<b>⏰ Vaqti:</b> {datetime.fromisoformat(timestamp).strftime('%d.%m.%Y %H:%M:%S')}
        """
        
        logger.info(f'📦 New order received: {user_name}, Phone: {phone}, Items: {len(items)}')
        
        # Admin'ga xabar yuborish (async)
        try:
            # Bu yerda telegram bot'ga xabar yuboramiz
            # Lekin async context'da ishlashi uchun, bot instance kerak
            logger.info(f'✅ Order notification prepared for admin: {order_id}')
        except Exception as e:
            logger.error(f'❌ Failed to send admin message: {str(e)}')
        
        return jsonify({
            'success': True,
            'message': 'Buyurtma qabul qilindi',
            'orderId': order_id,
            'totalPrice': total_price + 25000
        }), 200
        
    except Exception as e:
        logger.error(f'❌ Order processing error: {str(e)}')
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

# Telegram Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = update.effective_user
    logger.info(f'📱 New user: {user.first_name} (ID: {user.id})')
    
    # Mini App button bilan xabar yuborish
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text='🛒 Supermarketchani ochish',
            web_app=WebAppInfo(url=MINI_APP_URL)
        )]
    ])
    
    message_text = """
<b>🛒 Supermarket ilovasiga xush kelibsiz!</b>

<i>Mahsulotlarni qidiring, savatchaga qo'shing va buyurtma bering.</i>

Ilovani ochish uchun quyidagi tugmani bosing:
    """
    
    await update.message.reply_html(message_text, reply_markup=keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = """
<b>Qo'llanma:</b>

/start - Boshlash
/help - Yordam
/orders - Buyurtmalarim

Ilovani http://localhost:3000 da sinab ko'rishingiz mumkin
    """
    await update.message.reply_html(help_text)

def main() -> None:
    """Main function - Bot ishga tushirish"""
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    
    logger.info(f"""
╔════════════════════════════════════════════════════╗
║     🛒 SUPERMARKET BOT STARTING UP... ⏳           ║
╠════════════════════════════════════════════════════╣
║ 🤖 Bot Username: @{BOT_USERNAME}                    ║
║ 📱 Mini App URL: {MINI_APP_URL[:40]}... ║
║ 🔗 Server Port: {PORT}                                  ║
║ 🐍 Python Version: Active                          ║
╚════════════════════════════════════════════════════╝
    """)
    
    # Polling ishga tushirish (development mode)
    application.run_polling()

if __name__ == '__main__':
    # Flask app'ni threaded mode'da ishga tushirish
    import threading
    
    # Bot'ni separate thread'da ishga tushirish
    bot_thread = threading.Thread(target=main, daemon=True)
    bot_thread.start()
    
    logger.info(f'🌐 Flask server starting on port {PORT}...')
    
    # Flask app'ni ishga tushirish
    app.run(host='0.0.0.0', port=PORT, debug=False)
