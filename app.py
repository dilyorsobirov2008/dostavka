from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Telegram Bot Token (o'zingiznikini kiriting)
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', 'YOUR_ADMIN_CHAT_ID')

# Mahsulotlar ma'lumotlar bazasi
PRODUCTS = [
    # Mevalar
    {"id": 1, "name": "Olma", "price": 15000, "category": "mevalar", "image": "🍎", "unit": "kg"},
    {"id": 2, "name": "Banan", "price": 25000, "category": "mevalar", "image": "🍌", "unit": "kg"},
    {"id": 3, "name": "Apelsin", "price": 20000, "category": "mevalar", "image": "🍊", "unit": "kg"},
    {"id": 4, "name": "Uzum", "price": 30000, "category": "mevalar", "image": "🍇", "unit": "kg"},
    
    # Sut mahsulotlari
    {"id": 5, "name": "Sut", "price": 12000, "category": "sut", "image": "🥛", "unit": "L"},
    {"id": 6, "name": "Qatiq", "price": 8000, "category": "sut", "image": "🥤", "unit": "dona"},
    {"id": 7, "name": "Tvorog", "price": 18000, "category": "sut", "image": "🧈", "unit": "kg"},
    {"id": 8, "name": "Pishloq", "price": 45000, "category": "sut", "image": "🧀", "unit": "kg"},
    
    # Go'sht mahsulotlari
    {"id": 9, "name": "Mol go'shti", "price": 85000, "category": "gosht", "image": "🥩", "unit": "kg"},
    {"id": 10, "name": "Tovuq go'shti", "price": 35000, "category": "gosht", "image": "🍗", "unit": "kg"},
    {"id": 11, "name": "Kolbasa", "price": 55000, "category": "gosht", "image": "🌭", "unit": "kg"},
    
    # Ichimliklar
    {"id": 12, "name": "Cola", "price": 8000, "category": "ichimlik", "image": "🥤", "unit": "dona"},
    {"id": 13, "name": "Suv", "price": 3000, "category": "ichimlik", "image": "💧", "unit": "dona"},
    {"id": 14, "name": "Sharbat", "price": 12000, "category": "ichimlik", "image": "🧃", "unit": "dona"},
    
    # Non mahsulotlari
    {"id": 15, "name": "Non", "price": 2500, "category": "non", "image": "🍞", "unit": "dona"},
    {"id": 16, "name": "Lavash", "price": 3500, "category": "non", "image": "🫓", "unit": "dona"},
    
    # Sabzavotlar
    {"id": 17, "name": "Pomidor", "price": 12000, "category": "sabzavot", "image": "🍅", "unit": "kg"},
    {"id": 18, "name": "Bodring", "price": 8000, "category": "sabzavot", "image": "🥒", "unit": "kg"},
    {"id": 19, "name": "Kartoshka", "price": 5000, "category": "sabzavot", "image": "🥔", "unit": "kg"},
    {"id": 20, "name": "Piyoz", "price": 4000, "category": "sabzavot", "image": "🧅", "unit": "kg"},
]

CATEGORIES = [
    {"id": "mevalar", "name": "Mevalar", "icon": "🍎"},
    {"id": "sut", "name": "Sut mahsulotlari", "icon": "🥛"},
    {"id": "gosht", "name": "Go'sht", "icon": "🥩"},
    {"id": "ichimlik", "name": "Ichimliklar", "icon": "🥤"},
    {"id": "non", "name": "Non mahsulotlari", "icon": "🍞"},
    {"id": "sabzavot", "name": "Sabzavotlar", "icon": "🥗"},
]

@app.route('/', methods=['GET'])
def home():
    """Asosiy sahifa"""
    return jsonify({
        "status": "ok",
        "message": "Telegram Supermarket API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "products": "/api/products",
            "categories": "/api/categories",
            "order": "/api/order"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Server holatini tekshirish - Render.com uchun muhim"""
    return jsonify({
        "status": "ok", 
        "message": "Server ishlamoqda",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """Barcha mahsulotlarni qaytarish"""
    category = request.args.get('category')
    search = request.args.get('search', '').lower()
    
    filtered_products = PRODUCTS
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search:
        filtered_products = [p for p in filtered_products if search in p['name'].lower()]
    
    return jsonify(filtered_products)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Barcha kategoriyalarni qaytarish"""
    return jsonify(CATEGORIES)

@app.route('/api/order', methods=['POST'])
def create_order():
    """Yangi buyurtma yaratish"""
    try:
        data = request.json
        
        # Ma'lumotlarni tekshirish
        if not data.get('items') or not data.get('customer'):
            return jsonify({"error": "To'liq ma'lumot kiritilmagan"}), 400
        
        # Buyurtma ma'lumotlari
        customer = data['customer']
        items = data['items']
        total = data.get('total', 0)
        
        # Telegram botga xabar yuborish
        message = f"""
🛒 <b>YANGI BUYURTMA!</b>

👤 <b>Mijoz:</b>
├ Ism: {customer.get('name', 'Noma\'lum')}
├ Telefon: {customer.get('phone', 'Noma\'lum')}
└ Manzil: {customer.get('address', 'Noma\'lum')}

📦 <b>Mahsulotlar:</b>
"""
        
        for item in items:
            product = next((p for p in PRODUCTS if p['id'] == item['id']), None)
            if product:
                message += f"├ {product['image']} {product['name']}\n"
                message += f"│  └ {item['quantity']} {product['unit']} × {product['price']:,} so'm = {item['quantity'] * product['price']:,} so'm\n"
        
        message += f"""
💰 <b>Jami summa:</b> {total:,} so'm

⏰ <b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Telegram API orqali yuborish
        send_telegram_message(message)
        
        return jsonify({
            "success": True,
            "message": "Buyurtma muvaffaqiyatli qabul qilindi!"
        })
        
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        return jsonify({"error": "Buyurtma yuborishda xatolik yuz berdi"}), 500

def send_telegram_message(message):
    """Telegram botga xabar yuborish"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Telegram xabar yuborishda xatolik: {str(e)}")
        return None

if __name__ == '__main__':
    # Render.com uchun PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    
    # Production yoki development rejimini aniqlash
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Server ishga tushmoqda...")
    print(f"📡 Port: {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌐 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
