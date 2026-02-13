@echo off
chcp 65001 > nul

echo ========================================
echo 🚀 Telegram Supermarket Mini App
echo ========================================
echo.

REM .env faylini tekshirish
if not exist .env (
    echo ⚠️  .env fayli topilmadi. Namunadan yaratilmoqda...
    copy .env.example .env
    echo ✅ .env fayli yaratildi. Iltimos, BOT_TOKEN va ADMIN_CHAT_ID ni kiriting.
    echo.
    pause
)

REM Virtual environment yaratish
if not exist venv (
    echo 📦 Virtual environment yaratilmoqda...
    python -m venv venv
)

REM Virtual environment ni faollashtirish
echo 🔧 Virtual environment faollashtirilmoqda...
call venv\Scripts\activate.bat

REM Dependencies o'rnatish
echo 📦 Python dependencies o'rnatilmoqda...
pip install -r requirements.txt

REM Frontend dependencies
if not exist frontend\node_modules (
    echo 📦 Frontend dependencies o'rnatilmoqda...
    cd frontend
    call npm install
    cd ..
)

REM Frontend .env
if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
)

echo.
echo ✅ Barcha dependencies o'rnatildi!
echo.
echo 📱 Botni ishga tushirish uchun:
echo    python bot.py
echo.
echo 🖥️  Backend serverni ishga tushirish uchun:
echo    python app.py
echo.
echo 🎨 Frontend serverni ishga tushirish uchun:
echo    cd frontend ^&^& npm run dev
echo.
echo 💡 Maslahat: 3 ta terminal oching va har birida bitta komandani ishga tushiring
echo.
pause
