from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
import requests
import shutil  # Nusxa olish uchun qo'shimcha
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

# To'g'irlangan mahsulotlar bo'limi
PRODUCTS = {
    "categories": [
        "🍎 Mevalar", "🥗 Sabzavotlar", "💧 Ichimliklar", 
        "🥛 Sut mahsulotlari", "🍞 Non mahsulotlari", "🍰 Shirinliklar",
        "🥜 Yong'oqlar", "🍦 Muzqaymoqlar", "🍖 Go'sht mahsulotlari",
        "🐟 Baliqlar", "🧂 Ziravorlar", "🍵 Choylar"
    ],
    "products": [
        # MEVALAR
        {"id": 1, "name": "Olma (kg)", "category": "🍎 Mevalar", "price": 8000, "image": "https://suret.pics/uploads/posts/2023-09/1695307331_1.jpg", "description": "Sershira va qarsildoq olma"},
        {"id": 2, "name": "Banan (kg)", "category": "🍎 Mevalar", "price": 6000, "image": "https://cdn.uza.uz/2023/12/27/06/14/chabCEPpOd5GaPbqOWXE7Wez6X1E4dsR_front.jpg", "description": "Yangi keltirilgan banan"},
        {"id": 3, "name": "Apelsin (kg)", "category": "🍎 Mevalar", "price": 9000, "image": "https://images.unsplash.com/photo-1611080626919-30979dba3c82?w=300&h=300&fit=crop", "description": "S vitamini bilan boy apelsin"},
        {"id": 4, "name": "Qizil uzum (kg)", "category": "🍎 Mevalar", "price": 18000, "image": "https://images.unsplash.com/photo-1576684179506-ca7da12d8259?w=300&h=300&fit=crop", "description": "Shirin va sershira uzum"},
        {"id": 5, "name": "Limon (kg)", "category": "🍎 Mevalar", "price": 7000, "image": "https://images.unsplash.com/photo-1566201686209-51ce8a1e92dc?w=300&h=300&fit=crop", "description": "Yangi uzilgan limon"},
        {"id": 6, "name": "Ananas (dona)", "category": "🍎 Mevalar", "price": 12000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Ekzotik ananas"},
        {"id": 7, "name": "Qulupnay (kg)", "category": "🍎 Mevalar", "price": 25000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Yangi va shirin qulupnay"},
        {"id": 8, "name": "Shaftoli (kg)", "category": "🍎 Mevalar", "price": 11000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Mayin shaftoli"},
        {"id": 9, "name": "Olxo'ri (kg)", "category": "🍎 Mevalar", "price": 14000, "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=300&fit=crop", "description": "Sershira olxo'ri"},
        {"id": 10, "name": "Anor (dona)", "category": "🍎 Mevalar", "price": 15000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Qizil va shirin anor"},
        {"id": 11, "name": "Nok (kg)", "category": "🍎 Mevalar", "price": 10000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yumshoq va shirin nok"},
        {"id": 12, "name": "Chernika (kg)", "category": "🍎 Mevalar", "price": 22000, "image": "https://images.unsplash.com/photo-1585183732519-e21cc028cb29?w=300&h=300&fit=crop", "description": "Foydali chernika mevasi"},

        # SABZAVOTLAR
        {"id": 13, "name": "Pomidor (kg)", "category": "🥗 Sabzavotlar", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Qizil va pishgan pomidor"},
        {"id": 14, "name": "Salat bargi (dona)", "category": "🥗 Sabzavotlar", "price": 3500, "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&h=300&fit=crop", "description": "Yangi va barra salat bargi"},
        {"id": 15, "name": "Bodring (kg)", "category": "🥗 Sabzavotlar", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Karsildoq bodring"},
        {"id": 16, "name": "Baqlajon (kg)", "category": "🥗 Sabzavotlar", "price": 7000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi baqlajonlar"},
        {"id": 17, "name": "Qizil piyoz (kg)", "category": "🥗 Sabzavotlar", "price": 2500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Salatlar uchun qizil piyoz"},
        {"id": 18, "name": "Sarimsoqpiyoz (kg)", "category": "🥗 Sabzavotlar", "price": 8000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "O'tkir ta'mli sarimsoqpiyoz"},
        {"id": 19, "name": "Bolgar qalampiri (kg)", "category": "🥗 Sabzavotlar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Shirin bolgar qalampiri"},
        {"id": 20, "name": "Kartoshka (kg)", "category": "🥗 Sabzavotlar", "price": 2000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sifatli kartoshka"},
        {"id": 21, "name": "Karam (dona)", "category": "🥗 Sabzavotlar", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Oq karam"},
        {"id": 22, "name": "Qizil lobiya (kg)", "category": "🥗 Sabzavotlar", "price": 9000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Saralangan qizil lobiya"},
        {"id": 23, "name": "Piyoz (kg)", "category": "🥗 Sabzavotlar", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sariq piyoz"},
        {"id": 24, "name": "Ko'katlar (bog')", "category": "🥗 Sabzavotlar", "price": 1500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi uzilgan ko'katlar"},

        # ICHIMLIKLAR
        {"id": 25, "name": "Gazsiz suv 1.5L", "category": "💧 Ichimliklar", "price": 2500, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300&h=300&fit=crop", "description": "Toza ichimlik suvi"},
        {"id": 26, "name": "Sprite 0.5L", "category": "💧 Ichimliklar", "price": 3500, "image": "https://images.unsplash.com/photo-1554866585-e1dd5a36d1ef?w=300&h=300&fit=crop", "description": "Limonli gazlangan ichimlik"},
        {"id": 27, "name": "Coca-Cola 0.5L", "category": "💧 Ichimliklar", "price": 3500, "image": "https://images.unsplash.com/photo-1554789867-42ec9804ff21?w=300&h=300&fit=crop", "description": "Klassik gazlangan ichimlik"},
        {"id": 28, "name": "Pepsi 1L", "category": "💧 Ichimliklar", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Gazlangan ichimlik"},
        {"id": 29, "name": "Olma sharbati 1L", "category": "💧 Ichimliklar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Tabiiy olma sharbati"},
        {"id": 30, "name": "Qora choy 100g", "category": "💧 Ichimliklar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Sifatli qora choy"},
        {"id": 31, "name": "Yashil choy 100g", "category": "💧 Ichimliklar", "price": 12000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Saralangan yashil choy"},
        {"id": 32, "name": "Qahva 500g", "category": "💧 Ichimliklar", "price": 25000, "image": "https://images.unsplash.com/photo-1559056099-641a0ac8b3f7?w=300&h=300&fit=crop", "description": "Tabiiy maydalangan qahva"},
        {"id": 33, "name": "Kakao 200g", "category": "💧 Ichimliklar", "price": 15000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Mazali kakao kukuni"},
        {"id": 34, "name": "Kompot 1L", "category": "💧 Ichimliklar", "price": 5500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Uy sharoitida tayyorlangan kompot"},

        # SUT MAHSULOTLARI
        {"id": 35, "name": "Sut 1L", "category": "🥛 Sut mahsulotlari", "price": 9000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi va toza sut"},
        {"id": 36, "name": "Yogurt 500ml", "category": "🥛 Sut mahsulotlari", "price": 6000, "image": "https://images.unsplash.com/photo-1488477181946-6428a0291840?w=300&h=300&fit=crop", "description": "Mevali yogurt"},
        {"id": 37, "name": "Tvorog 500g", "category": "🥛 Sut mahsulotlari", "price": 14000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Yumshoq tvorog"},
        {"id": 38, "name": "Pishloq 500g", "category": "🥛 Sut mahsulotlari", "price": 22000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Golland pishlog'i"},
        {"id": 39, "name": "Qaymoq 250ml", "category": "🥛 Sut mahsulotlari", "price": 8000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yog'li qaymoq"},
        {"id": 40, "name": "Smetana 200g", "category": "🥛 Sut mahsulotlari", "price": 7500, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Yangi smetana"},
        {"id": 41, "name": "Qurt (kg)", "category": "🥛 Sut mahsulotlari", "price": 16000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sho'r qurt"},
        {"id": 42, "name": "Mozzarella 250g", "category": "🥛 Sut mahsulotlari", "price": 18000, "image": "https://images.unsplash.com/photo-1589985643862-3c1a6218e2d6?w=300&h=300&fit=crop", "description": "Pitsa uchun mozzarella"},
        {"id": 43, "name": "Ayron 500ml", "category": "🥛 Sut mahsulotlari", "price": 5000, "image": "https://images.unsplash.com/photo-1550592154-17ccbf17eaf3?w=300&h=300&fit=crop", "description": "Chanqoqbosti ayron"},
        {"id": 44, "name": "Qatiq 500ml", "category": "🥛 Sut mahsulotlari", "price": 6500, "image": "https://images.unsplash.com/photo-1488477181946-6428a0291840?w=300&h=300&fit=crop", "description": "Xonadon qatig'i"},

        # NON MAHSULOTLARI
        {"id": 45, "name": "Oq non (buxanka)", "category": "🍞 Non mahsulotlari", "price": 4000, "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300&h=300&fit=crop", "description": "Issiq oq non"},
        {"id": 46, "name": "Qora non (kg)", "category": "🍞 Non mahsulotlari", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Parhezbop qora non"},
        {"id": 47, "name": "Lavash xamiri", "category": "🍞 Non mahsulotlari", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yupqa lavash xamiri"},
        {"id": 48, "name": "Somsa xamiri (6 dona)", "category": "🍞 Non mahsulotlari", "price": 12000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Tayyor qatlama xamir"},
        {"id": 49, "name": "Patir non", "category": "🍞 Non mahsulotlari", "price": 6000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yog'li patir non"},
        {"id": 50, "name": "Tandir non", "category": "🍞 Non mahsulotlari", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Issiq tandir non"},
        {"id": 51, "name": "Bulochka (dona)", "category": "🍞 Non mahsulotlari", "price": 2500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Shirin bulochka"},
        {"id": 52, "name": "Parhez non (dona)", "category": "🍞 Non mahsulotlari", "price": 3000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Suli noni"},

        # SHIRINLIKLAR
        {"id": 53, "name": "Shokolad 100g", "category": "🍰 Shirinliklar", "price": 8000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Sutli shokolad"},
        {"id": 54, "name": "Keks (6 dona)", "category": "🍰 Shirinliklar", "price": 6000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Mayizli kekslar"},
        {"id": 55, "name": "Tort (kg)", "category": "🍰 Shirinliklar", "price": 35000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Bayramona shokoladli tort"},
        {"id": 56, "name": "Pechenye 200g", "category": "🍰 Shirinliklar", "price": 5000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Qarsildoq pechenyelar"},
        {"id": 57, "name": "Pirojniy (6 dona)", "category": "🍰 Shirinliklar", "price": 8000, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Mevali pirojniylar"},
        {"id": 58, "name": "Halvo 300g", "category": "🍰 Shirinliklar", "price": 9000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Kunjutli halvo"},
        {"id": 59, "name": "Marmelad 200g", "category": "🍰 Shirinliklar", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Turli rangli marmeladlar"},
        {"id": 60, "name": "Karamel 100g", "category": "🍰 Shirinliklar", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Shirin karamellar"},
        {"id": 61, "name": "Pastila 150g", "category": "🍰 Shirinliklar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Olma pastilasi"},
        {"id": 62, "name": "Chak-chak 100g", "category": "🍰 Shirinliklar", "price": 5500, "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=300&fit=crop", "description": "Asalli chak-chak"},

        # YONG'OQLAR
        {"id": 63, "name": "Bodom (kg)", "category": "🥜 Yong'oqlar", "price": 45000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Pishgan shirin bodom"},
        {"id": 64, "name": "Yeryong'oq (kg)", "category": "🥜 Yong'oqlar", "price": 22000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Tozalangan yeryong'oq"},
        {"id": 65, "name": "Pista (kg)", "category": "🥜 Yong'oqlar", "price": 35000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Eron pistasi"},
        {"id": 66, "name": "Keshyu (kg)", "category": "🥜 Yong'oqlar", "price": 28000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Tuzlangan keshyu"},
        {"id": 67, "name": "Yong'oq (kg)", "category": "🥜 Yong'oqlar", "price": 40000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Tozalangan yong'oq mag'zi"},
        {"id": 68, "name": "Turshak (kg)", "category": "🥜 Yong'oqlar", "price": 18000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Quritilgan o'rik (turshak)"},
        {"id": 69, "name": "Pista (kg)", "category": "🥜 Yong'oqlar", "price": 12000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Kungaboqar pistasi"},
        {"id": 70, "name": "Qovoq urug'i (kg)", "category": "🥜 Yong'oqlar", "price": 20000, "image": "https://images.unsplash.com/photo-1585706781021-99000a51b93c?w=300&h=300&fit=crop", "description": "Tozalangan qovoq urug'i"},

        # MUZQAYMOQLAR
        {"id": 71, "name": "Qaymoqli muzqaymoq", "category": "🍦 Muzqaymoqlar", "price": 8000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Klassik qaymoqli muzqaymoq"},
        {"id": 72, "name": "Shokoladli muzqaymoq", "category": "🍦 Muzqaymoqlar", "price": 8500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Shokoladli va muzli"},
        {"id": 73, "name": "Qovunli muzqaymoq", "category": "🍦 Muzqaymoqlar", "price": 7500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Xushbo'y qovunli"},
        {"id": 74, "name": "Olmal muzqaymoq", "category": "🍦 Muzqaymoqlar", "price": 7000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Muzlatilgan olma sharbati"},
        {"id": 75, "name": "Dietik muzqaymoq", "category": "🍦 Muzqaymoqlar", "price": 6500, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Shakarsiz muzqaymoq"},
        {"id": 76, "name": "Dondurma", "category": "🍦 Muzqaymoqlar", "price": 5000, "image": "https://images.unsplash.com/photo-1563805042-7684c019e157?w=300&h=300&fit=crop", "description": "Turkcha dondurma"},

        # GO'SHT MAHSULOTLARI
        {"id": 77, "name": "Tovuq lahm (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 28000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi tovuq lahmi"},
        {"id": 78, "name": "Tovuq (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 32000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Butun tovuq"},
        {"id": 79, "name": "Qo'y go'shti (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 45000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yangi qo'y go'shti"},
        {"id": 80, "name": "Kolbasa (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 35000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Halol kolbasa mahsuloti"},
        {"id": 81, "name": "Sosiska (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 28000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Sifatli sosiskalar"},
        {"id": 82, "name": "Dudlangan go'sht (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 32000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Dudlangan mol go'shti"},
        {"id": 83, "name": "Mol go'shti (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 38000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Yumshoq mol go'shti"},
        {"id": 84, "name": "Qiyma (kg)", "category": "🍖 Go'sht mahsulotlari", "price": 55000, "image": "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=300&h=300&fit=crop", "description": "Uy qiymasi"},

        # BALIQLAR
        {"id": 85, "name": "Sazan baliq (kg)", "category": "🐟 Baliqlar", "price": 42000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi tutilgan sazan"},
        {"id": 86, "name": "Losos (kg)", "category": "🐟 Baliqlar", "price": 65000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Sifatli losos balig'i"},
        {"id": 87, "name": "Karp (kg)", "category": "🐟 Baliqlar", "price": 38000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Tirik karp balig'i"},
        {"id": 88, "name": "Sudak (kg)", "category": "🐟 Baliqlar", "price": 48000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Saralangan sudak balig'i"},
        {"id": 89, "name": "Kalmar (kg)", "category": "🐟 Baliqlar", "price": 55000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yangi muzlatilgan kalmar"},
        {"id": 90, "name": "Krevetka (kg)", "category": "🐟 Baliqlar", "price": 72000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yirik krevetkalar"},

        # ZIRAVORLAR
        {"id": 91, "name": "Osh tuzi (kg)", "category": "🧂 Ziravorlar", "price": 2000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Yodlangan osh tuzi"},
        {"id": 92, "name": "Qora murch (100g)", "category": "🧂 Ziravorlar", "price": 5000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Maydalangan qora murch"},
        {"id": 93, "name": "Qizil murch (100g)", "category": "🧂 Ziravorlar", "price": 3500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Achchiq qizil murch"},
        {"id": 94, "name": "Zira (100g)", "category": "🧂 Ziravorlar", "price": 6000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Xushbo'y zira"},
        {"id": 95, "name": "Kashnich urug'i (100g)", "category": "🧂 Ziravorlar", "price": 4000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Maydalangan kashnich"},
        {"id": 96, "name": "Zarchava (100g)", "category": "🧂 Ziravorlar", "price": 4500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Tabiiy zarchava"},
        {"id": 97, "name": "Sarimsoq kukuni (100g)", "category": "🧂 Ziravorlar", "price": 5500, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Quritilgan sarimsoq"},
        {"id": 98, "name": "Murch donachalari (100g)", "category": "🧂 Ziravorlar", "price": 7000, "image": "https://images.unsplash.com/photo-1599599810694-b5ac4dd33120?w=300&h=300&fit=crop", "description": "Butun murch donalari"},

        # CHOYLAR
        {"id": 99, "name": "Qora choy (100g)", "category": "🍵 Choylar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Hindiston qora choyi"},
        {"id": 100, "name": "Yashil choy (100g)", "category": "🍵 Choylar", "price": 12000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Xitoy yashil choyi"},
        {"id": 101, "name": "Oolong choyi (100g)", "category": "🍵 Choylar", "price": 15000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Sifatli oolong choyi"},
        {"id": 102, "name": "Yalpizli choy (50g)", "category": "🍵 Choylar", "price": 6000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Tinchlantiruvchi yalpizli choy"},
        {"id": 103, "name": "Namatak choyi (50g)", "category": "🍵 Choylar", "price": 8000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Vitaminli namatak"},
        {"id": 104, "name": "Zanjabil choyi (100g)", "category": "🍵 Choylar", "price": 10000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Isituvchi zanjabil choyi"},
        {"id": 105, "name": "Moychechak choyi (50g)", "category": "🍵 Choylar", "price": 7000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Tabiiy moychechak choyi"},
        {"id": 106, "name": "Karkade choyi (100g)", "category": "🍵 Choylar", "price": 9000, "image": "https://images.unsplash.com/photo-1597318345206-61f3ee1edbf2?w=300&h=300&fit=crop", "description": "Qizil karkade choyi"}
    ]
}

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    # Qo'shimcha: Har safar saqlashdan oldin zaxira nusxa yaratish
    if os.path.exists(ORDERS_FILE):
        if not os.path.exists('backups'): os.makedirs('backups')
        shutil.copy(ORDERS_FILE, f'backups/orders_backup_{datetime.now().strftime("%Y%m%d")}.json')
        
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

# --- QO'SHIMCHA FUNKSIYALAR ---

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Mahsulotlarni nomi yoki kategoriyasi bo'yicha qidirish"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    
    filtered = PRODUCTS['products']
    if category:
        filtered = [p for p in filtered if p['category'] == category]
    if query:
        filtered = [p for p in filtered if query in p['name'].lower()]
        
    return jsonify({"products": filtered, "count": len(filtered)})

def validate_total(items):
    """Xavfsizlik: Frontenddan kelgan narxni bazadagi bilan tekshirish"""
    real_total = 0
    for p_id, item in items.items():
        original = next((p for p in PRODUCTS['products'] if str(p['id']) == str(p_id)), None)
        if original:
            real_total += original['price'] * item['quantity']
    return real_total

# -----------------------------

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
        
        # Qo'shimcha: Narxni tekshirish
        server_total = validate_total(data['items'])
        
        orders = load_orders()
        order_id = len(orders) + 1
        
        order = {
            "order_id": order_id,
            "user_id": data['user_id'],
            "user_name": data['user_name'],
            "phone": data['phone'],
            "location": data['location'],
            "items": data['items'],
            "total": server_total, # Serverda hisoblangan narxni saqlaymiz
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        orders.append(order)
        save_orders(orders)
        
        send_to_telegram(order_id, data['user_name'], data['phone'], 
                        data['location'], data['items'], server_total, data['user_id'])
        
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
