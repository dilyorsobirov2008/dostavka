#!/usr/bin/env python3
"""
Bot test skripti - botning ishlashini tekshirish
"""

import os
import sys
from dotenv import load_dotenv
import requests

print("\n" + "="*60)
print("🔍 TELEGRAM BOT TEST SKRIPTI")
print("="*60 + "\n")

# 1. .env faylini yuklash
print("📋 1. .env faylini tekshirish...")
if not os.path.exists('.env'):
    print("   ❌ .env fayli topilmadi!")
    print("   💡 .env.example dan .env yarating va to'ldiring")
    sys.exit(1)
else:
    print("   ✅ .env fayli mavjud")

load_dotenv()

# 2. BOT_TOKEN tekshirish
print("\n📋 2. BOT_TOKEN tekshirish...")
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print("   ❌ BOT_TOKEN topilmadi yoki bo'sh!")
    print("   💡 .env faylida BOT_TOKEN ni to'ldiring")
    sys.exit(1)
else:
    print(f"   ✅ BOT_TOKEN: {BOT_TOKEN[:10]}...")

# 3. Token validligini tekshirish
print("\n📋 3. Token validligini tekshirish...")
try:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if data.get('ok'):
        bot_info = data.get('result', {})
        print("   ✅ Token to'g'ri!")
        print(f"   🤖 Bot nomi: {bot_info.get('first_name')}")
        print(f"   🔗 Username: @{bot_info.get('username')}")
        print(f"   🆔 Bot ID: {bot_info.get('id')}")
    else:
        print(f"   ❌ Token noto'g'ri: {data.get('description')}")
        sys.exit(1)
        
except requests.exceptions.RequestException as e:
    print(f"   ❌ Internet aloqa xatosi: {e}")
    sys.exit(1)

# 4. ADMIN_CHAT_ID tekshirish
print("\n📋 4. ADMIN_CHAT_ID tekshirish...")
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == 'YOUR_ADMIN_CHAT_ID':
    print("   ⚠️  ADMIN_CHAT_ID topilmadi")
    print("   💡 @userinfobot ga /start yuboring va ID ni oling")
else:
    print(f"   ✅ ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")

# 5. WEB_APP_URL tekshirish
print("\n📋 5. WEB_APP_URL tekshirish...")
WEB_APP_URL = os.getenv('WEB_APP_URL', 'http://localhost:3000')
print(f"   ✅ WEB_APP_URL: {WEB_APP_URL}")

# 6. Python packages tekshirish
print("\n📋 6. Python packages tekshirish...")
try:
    import telegram
    print(f"   ✅ python-telegram-bot: {telegram.__version__}")
except ImportError:
    print("   ❌ python-telegram-bot o'rnatilmagan!")
    print("   💡 pip install python-telegram-bot==21.0")
    sys.exit(1)

# 7. Test xabar yuborish (agar ADMIN_CHAT_ID bo'lsa)
if ADMIN_CHAT_ID and ADMIN_CHAT_ID != 'YOUR_ADMIN_CHAT_ID':
    print("\n📋 7. Test xabar yuborish...")
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_CHAT_ID,
            "text": "✅ Bot test xabari - Bot to'g'ri sozlangan!"
        }
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if data.get('ok'):
            print("   ✅ Test xabar yuborildi!")
            print("   📱 Telegram da xabarni tekshiring")
        else:
            print(f"   ⚠️  Xabar yuborilmadi: {data.get('description')}")
            print("   💡 ADMIN_CHAT_ID to'g'ri ekanligini tekshiring")
            
    except Exception as e:
        print(f"   ⚠️  Xatolik: {e}")

# 8. Webhook holatini tekshirish
print("\n📋 8. Webhook holatini tekshirish...")
try:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url, timeout=10)
    data = response.json()
    
    webhook_url = data.get('result', {}).get('url', '')
    
    if webhook_url:
        print(f"   ⚠️  Webhook faol: {webhook_url}")
        print("   💡 Polling uchun webhook ni o'chirish kerak:")
        print(f"      curl https://api.telegram.org/bot{BOT_TOKEN[:15]}***/deleteWebhook")
    else:
        print("   ✅ Webhook o'chirilgan (polling rejimi)")
        
except Exception as e:
    print(f"   ⚠️  Tekshirish xatosi: {e}")

# Xulosa
print("\n" + "="*60)
print("📊 XULOSA")
print("="*60)

issues = []

if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    issues.append("❌ BOT_TOKEN noto'g'ri")

if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == 'YOUR_ADMIN_CHAT_ID':
    issues.append("⚠️  ADMIN_CHAT_ID sozlanmagan")

if issues:
    print("\n⚠️  Muammolar topildi:")
    for issue in issues:
        print(f"   {issue}")
    print("\n💡 Muammolarni hal qilish: BOT_TROUBLESHOOTING.md ni o'qing")
else:
    print("\n✅ Barcha tekshiruvlar muvaffaqiyatli!")
    print("\n🚀 Botni ishga tushirish:")
    print("   python bot.py")
    print("\n📱 Telegram da botingizga /start yuboring")

print("\n" + "="*60 + "\n")
