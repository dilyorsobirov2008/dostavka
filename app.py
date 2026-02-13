#!/usr/bin/env python3
"""
🛒 Supermarket Mini App - Backend (Threading Fixed)
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import random
import string

load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '7351189083')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'tasamnodostavkabot')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://dostavka-intc.onrender.com')
PORT = int(os.getenv('PORT', '8000'))

# Flask App
app = Flask(__name__)
CORS(app)

# Products Database
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

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'status': '✅ Bot ishlamoqda!',
        'service': 'Supermarket API v2.0',
        'miniApp': MINI_APP_URL
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
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
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()

        # Get fields
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
        order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

        # Build items list
        items_list = '\n'.join([
            f"  • {item['name']} × {item['quantity']} = {item['price'] * item['quantity']:,} so'm"
            for item in items
        ])

        # Build message
        admin_message = f"""
<b>📦 YANGI BUYURTMA #{order_id}</b>

<b>👤 Foydalanuvchi:</b> {user_name}
<b>📱 Telefon:</b> <code>{phone}</code>
<b>📍 Manzil:</b> <code>{address}</code>

{f'<b>📝 Izoh:</b> {notes}' if notes else ''}

<b>📋 Tafsilotlar:</b>
{items_list}

<b>💰 Narx:</b> {total_price:,} so'm
<b>🚚 Dostavka:</b> 25,000 so'm
<b>💵 JAMI:</b> {total_price + 25000:,} so'm
        """

        logger.info(f'✅ Order #{order_id} created: {user_name}')

        # Send admin notification
        try:
            import requests
            telegram_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            requests.post(telegram_url, json={
                'chat_id': ADMIN_CHAT_ID,
                'text': admin_message,
                'parse_mode': 'HTML'
            }, timeout=10)
        except Exception as e:
            logger.warning(f'Could not send notification: {str(e)}')

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

# ==================== MAIN ====================

if __name__ == '__main__':
    logger.info(f"""
╔════════════════════════════════════════════════════╗
║     🛒 SUPERMARKET BOT - SIMPLE & STABLE          ║
╠════════════════════════════════════════════════════╣
║ 🤖 Bot: @{BOT_USERNAME}                            ║
║ 📱 URL: {MINI_APP_URL[:40]}... ║
║ 🔗 Port: {PORT}                                        ║
║ 📦 Products: {sum(len(items) for items in PRODUCTS.values())} dona                              ║
║ ✅ Status: Ready                                  ║
╚════════════════════════════════════════════════════╝
    """)

    # Run Flask
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True
    )
