from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Static files
@app.route('/')
def index():
    """Mini app interface"""
    return open('index.html', 'r', encoding='utf-8').read(), 200, {'Content-Type': 'text/html; charset=utf-8'}

ORDERS_FILE = 'orders.json'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')

# Kuchaytirilgan tovarlar bo'limi
PRODUCTS = {
    "categories": [
        "🍎 Meva", "🥗 Sabzavot", "💧 Ichimliklar", 
        "🥛 Sut Mahsuloti", "🍞 Non", "🍰 Shirinlik",
        "🥜 Asinolar", "🍦 Muzlavka", "🍖 Gosh Mahsuloti",
        "🐟 Baliq", "🧂 Ziravorlar", "🍵 Choylar"
    ],
    "products": [
        # MEVA (12 ta)
        {"id": 1, "name": "Olma (kg)", "category": "🍎 Meva", "price": 8000, "image": "https://images.unsplash.com/photo-1560806887-1295c1a9f632?w=300&h=300&fit=crop", "description": "Sho'rta, shirinli olma"},
        {"id": 2, "name": "Banan (kg)", "category": "🍎 Meva", "price": 6000, "image": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop", "description": "Yangi, sariq banan"},
        {"id": 3, "name": "Apelsin (kg)", "category": "🍎 Meva", "price": 9000, "image": "https://images.unsplash.com/photo-1611080626919-30979dba3c82?w=300&h=300&fit=crop", "description": "Sho'rta apelsin"},
        {"id": 4, "name": "Qizil uzum (kg)", "category": "🍎 Meva", "price": 18000, "image": "https://images.unsplash.com/photo-1576684179506-ca7da12d8259?w=300&h=300&fit=crop", "description": "Sho't, shirinli uzum"},
        {"id": 5, "name": "Limon (kg)", "category": "🍎 Meva", "price": 7000, "image": "https://images.unsplash.com/photo-1566201686209-51ce8a1e92dc?w=300&h=300&fit=crop", "description": "Sho'rta, tursh limon"},
        {"id": 6, "name": "Ananas (dona)", "category": "🍎 Meva", "price": 12000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi ananas"},
        {"id": 7, "name": "Qo'l o'rmonlari (kg)", "category": "🍎 Meva", "price": 25000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Yangi qo'l o'rmonlari"},
        {"id": 8, "name": "Shaftoli (kg)", "category": "🍎 Meva", "price": 11000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sho'rta shaftoli"},
        {"id": 9, "name": "Olxo'ri (kg)", "category": "🍎 Meva", "price": 14000, "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=300&fit=crop", "description": "Sho'rta olxo'ri"},
        {"id": 10, "name": "Pomegranate (dona)", "category": "🍎 Meva", "price": 15000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Yangi pomegranate"},
        {"id": 11, "name": "Nok (kg)", "category": "🍎 Meva", "price": 10000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sho'rta, shirinli nok"},
        {"id": 12, "name": "Qora ko'k (kg)", "category": "🍎 Meva", "price": 22000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Yangi qora ko'k"},

        # SABZAVOT (12 ta)
        {"id": 13, "name": "Pomidor (kg)", "category": "🥗 Sabzavot", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi, qizil pomidor"},
        {"id": 14, "name": "Salat (dona)", "category": "🥗 Sabzavot", "price": 3500, "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&h=300&fit=crop", "description": "Yangi, yashil salat"},
        {"id": 15, "name": "Bodring (kg)", "category": "🥗 Sabzavot", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi bodring"},
        {"id": 16, "name": "Sabzavot karvorti (dona)", "category": "🥗 Sabzavot", "price": 7000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi karvorti"},
        {"id": 17, "name": "Soğan (kg)", "category": "🥗 Sabzavot", "price": 2500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Qizil soğan"},
        {"id": 18, "name": "Sarmsaq (kg)", "category": "🥗 Sabzavot", "price": 8000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi sarmsaq"},
        {"id": 19, "name": "Bibir (kg)", "category": "🥗 Sabzavot", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Qizil bibir"},
        {"id": 20, "name": "Patates (kg)", "category": "🥗 Sabzavot", "price": 2000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi patates"},
        {"id": 21, "name": "Kapusta (dona)", "category": "🥗 Sabzavot", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi kapusta"},
        {"id": 22, "name": "Qizil lobiya (kg)", "category": "🥗 Sabzavot", "price": 9000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Quritilgan lobiya"},
        {"id": 23, "name": "Piyoz (kg)", "category": "🥗 Sabzavot", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sariq piyoz"},
        {"id": 24, "name": "Buqun o't (to'ppi)", "category": "🥗 Sabzavot", "price": 1500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi buqun o't"},

        # ICHIMLIKLAR (10 ta)
        {"id": 25, "name": "Toza suv 1.5L", "category": "💧 Ichimliklar", "price": 2500, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300&h=300&fit=crop", "description": "Toza, shirin suv"},
        {"id": 26, "name": "Sprite 0.5L", "category": "💧 Ichimliklar", "price": 3500, "image": "https://images.unsplash.com/photo-1554866585-e1dd5a36d1ef?w=300&h=300&fit=crop", "description": "Sprite ichimlik"},
        {"id": 27, "name": "Cola 0.5L", "category": "💧 Ichimliklar", "price": 3500, "image": "https://images.unsplash.com/photo-1554789867-42ec9804ff21?w=300&h=300&fit=crop", "description": "Cola ichimlik"},
        {"id": 28, "name": "Apelsin shira 1L", "category": "💧 Ichimliklar", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Natural shira"},
        {"id": 29, "name": "Alma shira 1L", "category": "💧 Ichimliklar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Natural alma shira"},
        {"id": 30, "name": "Qora choy 100g", "category": "💧 Ichimliklar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi choy"},
        {"id": 31, "name": "Yashil choy 100g", "category": "💧 Ichimliklar", "price": 12000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi yashil choy"},
        {"id": 32, "name": "Qahva 500g", "category": "💧 Ichimliklar", "price": 25000, "image": "https://images.unsplash.com/photo-1559056099-641a0ac8b3f7?w=300&h=300&fit=crop", "description": "Yangi qahva"},
        {"id": 33, "name": "Kakao 200g", "category": "💧 Ichimliklar", "price": 15000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi kakao"},
        {"id": 34, "name": "Kompot 1L", "category": "💧 Ichimliklar", "price": 5500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi kompot"},

        # SUT MAHSULOTI (10 ta)
        {"id": 35, "name": "Sut 1L", "category": "🥛 Sut Mahsuloti", "price": 9000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi, sof sut"},
        {"id": 36, "name": "Yoqurt 500ml", "category": "🥛 Sut Mahsuloti", "price": 6000, "image": "https://images.unsplash.com/photo-1488477181946-6428a0291840?w=300&h=300&fit=crop", "description": "Yangi yoqurt"},
        {"id": 37, "name": "Tvorog 500g", "category": "🥛 Sut Mahsuloti", "price": 14000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Yangi tvorog"},
        {"id": 38, "name": "Pishloq 500g", "category": "🥛 Sut Mahsuloti", "price": 22000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Yangi pishloq"},
        {"id": 39, "name": "Qaymoq 250ml", "category": "🥛 Sut Mahsuloti", "price": 8000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi qaymoq"},
        {"id": 40, "name": "Smetana 200g", "category": "🥛 Sut Mahsuloti", "price": 7500, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi smetana"},
        {"id": 41, "name": "Qutab (kg)", "category": "🥛 Sut Mahsuloti", "price": 16000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi qutab"},
        {"id": 42, "name": "Mozzarella 250g", "category": "🥛 Sut Mahsuloti", "price": 18000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Yangi mozzarella"},
        {"id": 43, "name": "Ayran 500ml", "category": "🥛 Sut Mahsuloti", "price": 5000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi ayran"},
        {"id": 44, "name": "Katyk 500ml", "category": "🥛 Sut Mahsuloti", "price": 6500, "image": "https://images.unsplash.com/photo-1488477181946-6428a0291840?w=300&h=300&fit=crop", "description": "Yangi katyk"},

        # NON (8 ta)
        {"id": 45, "name": "Oq non (kg)", "category": "🍞 Non", "price": 4000, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300&h=300&fit=crop", "description": "Yangi oq non"},
        {"id": 46, "name": "Qora non (kg)", "category": "🍞 Non", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi qora non"},
        {"id": 47, "name": "Lavash", "category": "🍞 Non", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi lavash"},
        {"id": 48, "name": "Somsa (6 dona)", "category": "🍞 Non", "price": 12000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi somsa"},
        {"id": 49, "name": "Puri (kg)", "category": "🍞 Non", "price": 6000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi puri"},
        {"id": 50, "name": "Tandoor non", "category": "🍞 Non", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi tandoor non"},
        {"id": 51, "name": "Boqal (dona)", "category": "🍞 Non", "price": 2500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi boqal"},
        {"id": 52, "name": "Turshi non (dona)", "category": "🍞 Non", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi turshi non"},

        # SHIRINLIK (10 ta)
        {"id": 53, "name": "Shokolad 100g", "category": "🍰 Shirinlik", "price": 8000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Qorali shokolad"},
        {"id": 54, "name": "Keks (6 dona)", "category": "🍰 Shirinlik", "price": 6000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Yangi keks"},
        {"id": 55, "name": "Tort (kg)", "category": "🍰 Shirinlik", "price": 35000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Yangi tort"},
        {"id": 56, "name": "Cookies 200g", "category": "🍰 Shirinlik", "price": 5000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Yangi cookies"},
        {"id": 57, "name": "Pirozhki (6 dona)", "category": "🍰 Shirinlik", "price": 8000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Yangi pirozhki"},
        {"id": 58, "name": "Halva 300g", "category": "🍰 Shirinlik", "price": 9000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi halva"},
        {"id": 59, "name": "Marmelad 200g", "category": "🍰 Shirinlik", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi marmelad"},
        {"id": 60, "name": "Caramel 100g", "category": "🍰 Shirinlik", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi caramel"},
        {"id": 61, "name": "Pastilas 150g", "category": "🍰 Shirinlik", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi pastilas"},
        {"id": 62, "name": "Chay qo'l 100g", "category": "🍰 Shirinlik", "price": 5500, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Yangi chay qo'li"},

        # ASINOLAR (8 ta)
        {"id": 63, "name": "Badаm (kg)", "category": "🥜 Asinolar", "price": 45000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi badam"},
        {"id": 64, "name": "Yoqoli (kg)", "category": "🥜 Asinolar", "price": 22000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi yoqoli"},
        {"id": 65, "name": "Fistiq (kg)", "category": "🥜 Asinolar", "price": 35000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi fistiq"},
        {"id": 66, "name": "Semiz (kg)", "category": "🥜 Asinolar", "price": 28000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi semiz"},
        {"id": 67, "name": "Valnuts (kg)", "category": "🥜 Asinolar", "price": 40000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi valnuts"},
        {"id": 68, "name": "Uruk (kg)", "category": "🥜 Asinolar", "price": 18000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi uruk"},
        {"id": 69, "name": "Sunflower seeds (kg)", "category": "🥜 Asinolar", "price": 12000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi seeds"},
        {"id": 70, "name": "Pumpkin seeds (kg)", "category": "🥜 Asinolar", "price": 20000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Yangi pumpkin seeds"},

        # MUZLAVKA (6 ta)
        {"id": 71, "name": "Qaymoq muzlavka", "category": "🍦 Muzlavka", "price": 8000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Yangi qaymoq muzlavka"},
        {"id": 72, "name": "Chocolate muzlavka", "category": "🍦 Muzlavka", "price": 8500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Yangi chocolate muzlavka"},
        {"id": 73, "name": "Qovun muzlavka", "category": "🍦 Muzlavka", "price": 7500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Yangi qovun muzlavka"},
        {"id": 74, "name": "Olma muzlavka", "category": "🍦 Muzlavka", "price": 7000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Yangi olma muzlavka"},
        {"id": 75, "name": "Nol qalora (diet)", "category": "🍦 Muzlavka", "price": 6500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Diet muzlavka"},
        {"id": 76, "name": "Dondurma", "category": "🍦 Muzlavka", "price": 5000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Yangi dondurma"},

        # GOSH MAHSULOTI (8 ta)
        {"id": 77, "name": "Tovuq ko'ksa (kg)", "category": "🍖 Gosh Mahsuloti", "price": 28000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi tovuq ko'ksa"},
        {"id": 78, "name": "Tovuq (kg)", "category": "🍖 Gosh Mahsuloti", "price": 32000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi tovuq"},
        {"id": 79, "name": "Goʻsht (kg)", "category": "🍖 Gosh Mahsuloti", "price": 45000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi qo'y go'shti"},
        {"id": 80, "name": "Kolbasa (kg)", "category": "🍖 Gosh Mahsuloti", "price": 35000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi kolbasa"},
        {"id": 81, "name": "Sosiskа (kg)", "category": "🍖 Gosh Mahsuloti", "price": 28000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi sosiska"},
        {"id": 82, "name": "Jambo (kg)", "category": "🍖 Gosh Mahsuloti", "price": 32000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi jambo"},
        {"id": 83, "name": "Baqalava go'shti (kg)", "category": "🍖 Gosh Mahsuloti", "price": 38000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi baqalava"},
        {"id": 84, "name": "Qavatdan (kg)", "category": "🍖 Gosh Mahsuloti", "price": 55000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi qavatdan"},

        # BALIQ (6 ta)
        {"id": 85, "name": "Shom baliq (kg)", "category": "🐟 Baliq", "price": 42000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi shom baliq"},
        {"id": 86, "name": "Losos (kg)", "category": "🐟 Baliq", "price": 65000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi losos"},
        {"id": 87, "name": "Karp (kg)", "category": "🐟 Baliq", "price": 38000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi karp"},
        {"id": 88, "name": "Sudak (kg)", "category": "🐟 Baliq", "price": 48000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi sudak"},
        {"id": 89, "name": "Calamari (kg)", "category": "🐟 Baliq", "price": 55000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi calamari"},
        {"id": 90, "name": "Krevetka (kg)", "category": "🐟 Baliq", "price": 72000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi krevetka"},

        # ZIRAVORLAR (8 ta)
        {"id": 91, "name": "Tuz (kg)", "category": "🧂 Ziravorlar", "price": 2000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Toza tuz"},
        {"id": 92, "name": "Qora murch (100g)", "category": "🧂 Ziravorlar", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi qora murch"},
        {"id": 93, "name": "Red murch (100g)", "category": "🧂 Ziravorlar", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi red murch"},
        {"id": 94, "name": "Barchka (100g)", "category": "🧂 Ziravorlar", "price": 6000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi barchka"},
        {"id": 95, "name": "Gil (100g)", "category": "🧂 Ziravorlar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi gil"},
        {"id": 96, "name": "Koriandor (100g)", "category": "🧂 Ziravorlar", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi koriandor"},
        {"id": 97, "name": "Sarmasak qo'l (100g)", "category": "🧂 Ziravorlar", "price": 5500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi sarmasak qo'li"},
        {"id": 98, "name": "Kumush (100g)", "category": "🧂 Ziravorlar", "price": 7000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi kumush"},

        # CHOYLAR (8 ta)
        {"id": 99, "name": "Qora choy (100g)", "category": "🍵 Choylar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi qora choy"},
        {"id": 100, "name": "Yashil choy (100g)", "category": "🍵 Choylar", "price": 12000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi yashil choy"},
        {"id": 101, "name": "Oolong choy (100g)", "category": "🍵 Choylar", "price": 15000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi oolong choy"},
        {"id": 102, "name": "Menta choy (50g)", "category": "🍵 Choylar", "price": 6000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi menta choy"},
        {"id": 103, "name": "Rose choy (50g)", "category": "🍵 Choylar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi rose choy"},
        {"id": 104, "name": "Ginger choy (100g)", "category": "🍵 Choylar", "price": 10000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi ginger choy"},
        {"id": 105, "name": "Chamomile (50g)", "category": "🍵 Choylar", "price": 7000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi chamomile"},
        {"id": 106, "name": "Hibiscus (100g)", "category": "🍵 Choylar", "price": 9000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Yangi hibiscus"}
    ]
}

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def send_to_telegram(order_id, user_name, phone, location, items, total, user_id):
    """Buyurtmani Telegram botga yuborish"""
    items_text = ""
    item_count = 0
    for product_id, item in items.items():
        items_text += f"\n• {item['name']} x{item['quantity']} = {item['price'] * item['quantity']:,} so'm"
        item_count += item['quantity']
    
    message = f"""
🛍️ <b>YANGI BUYURTMA!</b>

📋 <b>ID:</b> #{order_id}
👤 <b>Foydalanuvchi:</b> {user_name}
🆔 <b>Telegram ID:</b> {user_id}
📱 <b>Telefon:</b> {phone}
📍 <b>Lokatsiya:</b> {location}

<b>Tovarlar:</b> {items_text}

📦 <b>Jami tovarlar:</b> {item_count} dona
💰 <b>Jami narx:</b> {total:,} so'm

⏰ <b>Vaqti:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔗 <b>Telegram Username:</b> @{user_name}
    """
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram xato: {e}")
        return False

@app.route('/api/products', methods=['GET'])
def get_products():
    """Barcha tovarlarni olish"""
    try:
        return jsonify(PRODUCTS), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Yangi buyurtma yaratish"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'user_name', 'phone', 'location', 'items', 'total']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Barcha maydonlarni to'ldiring"}), 400
        
        orders = load_orders()
        order_id = len(orders) + 1
        
        order = {
            "order_id": order_id,
            "user_id": data['user_id'],
            "user_name": data['user_name'],
            "phone": data['phone'],
            "location": data['location'],
            "items": data['items'],
            "total": data['total'],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        orders.append(order)
        save_orders(orders)
        
        send_to_telegram(order_id, data['user_name'], data['phone'], 
                        data['location'], data['items'], data['total'], data['user_id'])
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "message": "Buyurtma qabul qilindi"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    """Barcha buyurtmalarni olish (admin uchun)"""
    orders = load_orders()
    return jsonify({"orders": orders, "total": len(orders)})

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Buyurtma ma'lumotini olish"""
    orders = load_orders()
    for order in orders:
        if order['order_id'] == order_id:
            return jsonify(order)
    return jsonify({"error": "Buyurtma topilmadi"}), 404

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Buyurtma statusini o'zgartirish"""
    try:
        data = request.get_json()
        orders = load_orders()
        
        for order in orders:
            if order['order_id'] == order_id:
                order['status'] = data.get('status', order['status'])
                order['updated_at'] = datetime.now().isoformat()
                save_orders(orders)
                return jsonify({"success": True, "order": order})
        
        return jsonify({"error": "Buyurtma topilmadi"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Statistika olish"""
    orders = load_orders()
    total_orders = len(orders)
    total_revenue = sum(order['total'] for order in orders)
    pending_orders = len([o for o in orders if o['status'] == 'pending'])
    completed_orders = len([o for o in orders if o['status'] == 'completed'])
    
    return jsonify({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "average_order": total_revenue // total_orders if total_orders > 0 else 0
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Server ishlayotganini tekshirish"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 SuperMarket Mini App Server ishga tushdi!")
    print(f"📍 http://localhost:{port}")
    print("🤖 Telegramga buyurtmalar yo'natiladi...")
    app.run(debug=False, port=port, host='0.0.0.0')
