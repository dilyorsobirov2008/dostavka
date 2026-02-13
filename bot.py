import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://your-domain.com')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot start komandasi"""
    keyboard = [
        [KeyboardButton(
            text="🛒 Supermarketni ochish",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🛒 <b>Supermarket Mini App</b>ga xush kelibsiz!\n\n"
        "Quyidagi tugmani bosib, mahsulotlarni ko'ring va buyurtma bering:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam komandasi"""
    await update.message.reply_text(
        "📱 <b>Bot haqida:</b>\n\n"
        "Bu bot orqali siz supermarketdan mahsulotlarni buyurtma qilishingiz mumkin.\n\n"
        "🛒 Mahsulotlar ko'rish uchun \"Supermarketni ochish\" tugmasini bosing.\n"
        "📦 Savatga mahsulotlarni qo'shing.\n"
        "✅ Buyurtma bering va biz sizga yetkazamiz!",
        parse_mode='HTML'
    )

def main():
    """Botni ishga tushirish"""
    print("🤖 Bot ishga tushmoqda...")
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Komandalarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    print("✅ Bot muvaffaqiyatli ishga tushdi!")
    print(f"🌐 Web App URL: {WEB_APP_URL}")
    
    # Botni ishga tushirish
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
