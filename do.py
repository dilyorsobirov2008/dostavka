import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

API_TOKEN = '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo' # Bot tokeningizni shu yerga qo'ying
WEB_APP_URL = 'https://dostavka-dun.vercel.app/' # Yuqoridagi HTML yuklangan manzil

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Mini App'ni ochuvchi tugma
    kb = [
        [InlineKeyboardButton(text="Magazinni ochish", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer("Xush kelibsiz! Magazinimizdan foydalanish uchun tugmani bosing:", reply_markup=keyboard)

@dp.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: types.Message):
    # Mini App'dan kelgan ma'lumotni tutib olish
    data = json.loads(message.web_app_data.data)
    product = data.get("item")
    price = data.get("price")
    
    await message.answer(f"Rahmat! Siz {product} sotib olmoqchisiz. \nNarxi: {price}$ \nTez orada operator bog'lanadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())