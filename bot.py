import os
import sys
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# .env faylini yuklash
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL', 'http://localhost:3000')

# Token tekshirish
if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    print("❌ XATOLIK: BOT_TOKEN topilmadi!")
    print("📝 .env faylida BOT_TOKEN ni to'ldiring:")
    print("   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
    sys.exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot start komandasi"""
    try:
        logger.info(f"Start komandasi: {update.effective_user.first_name}")
        
        keyboard = [
            [KeyboardButton(
                text="🛒 Supermarketni ochish",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "🛒 <b>Supermarket Mini App</b>ga xush kelibsiz!\n\n"
            "Quyidagi tugmani bosib, mahsulotlarni ko'ring va buyurtma bering:\n\n"
            "📱 <i>Tugmani bosing va ilova ochiladi</i>",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info("✅ Start komandasi muvaffaqiyatli yuborildi")
        
    except Exception as e:
        logger.error(f"❌ Start komandasi xatosi: {e}")
        await update.message.reply_text(
            "Kechirasiz, xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam komandasi"""
    try:
        logger.info(f"Help komandasi: {update.effective_user.first_name}")
        
        await update.message.reply_text(
            "📱 <b>Bot haqida:</b>\n\n"
            "Bu bot orqali siz supermarketdan mahsulotlarni buyurtma qilishingiz mumkin.\n\n"
            "🛒 Mahsulotlar ko'rish uchun \"Supermarketni ochish\" tugmasini bosing.\n"
            "📦 Savatga mahsulotlarni qo'shing.\n"
            "✅ Buyurtma bering va biz sizga yetkazamiz!\n\n"
            "♻️ /start - Botni qayta ishga tushirish",
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"❌ Help komandasi xatosi: {e}")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test komandasi - bot ishlayotganini tekshirish"""
    try:
        user = update.effective_user
        username = user.username if user.username else "yo'q"
        
        message = (
            f"✅ Bot ishlayapti!\n\n"
            f"👤 Sizning ma'lumotlaringiz:\n"
            f"├ ID: {user.id}\n"
            f"├ Ism: {user.first_name}\n"
            f"├ Username: @{username}\n"
            f"└ Bot Version: 1.0\n\n"
            f"🌐 Web App URL: {WEB_APP_URL}"
        )
        
        await update.message.reply_text(message)
        logger.info(f"✅ Test komandasi: {user.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Test komandasi xatosi: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha xabarlarga javob berish"""
    try:
        await update.message.reply_text(
            "👋 Salom! Men supermarket boti.\n\n"
            "Buyurtma berish uchun /start ni bosing."
        )
    except Exception as e:
        logger.error(f"❌ Echo xatosi: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatolarni handle qilish"""
    logger.error(f"❌ Update xatolik keltirib chiqardi: {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring yoki /start ni bosing."
            )
    except:
        pass

def main():
    """Botni ishga tushirish"""
    print("\n" + "="*50)
    print("🤖 TELEGRAM SUPERMARKET BOT")
    print("="*50)
    
    # Token tekshirish
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN topilmadi!")
        return
    
    print(f"✅ Token: {BOT_TOKEN[:10]}...")
    print(f"🌐 Web App URL: {WEB_APP_URL}")
    print(f"📡 Polling rejimi: Faol")
    print("="*50 + "\n")
    
    try:
        # Application yaratish
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Komandalarni qo'shish
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("test", test_command))
        
        # Barcha xabarlarga javob berish
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot muvaffaqiyatli ishga tushdi!")
        print("📝 Telegram da botga /start yuboring\n")
        print("🛑 To'xtatish uchun: Ctrl+C\n")
        
        # Botni ishga tushirish
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Bot ishga tushmadi: {e}")
        print(f"\n❌ XATOLIK: {e}\n")
        print("📋 Tekshirish ro'yxati:")
        print("  1. BOT_TOKEN to'g'ri kiritilganmi?")
        print("  2. Internet aloqa bormi?")
        print("  3. Python packages o'rnatilganmi?")
        print("     pip install -r requirements.txt")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot to'xtatildi")
        sys.exit(0)
