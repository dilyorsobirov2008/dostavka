#!/bin/bash

echo "🚀 Telegram Supermarket Mini App - Ishga tushirish"
echo "=================================================="

# Ranglar
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# .env faylini tekshirish
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env fayli topilmadi. Namunadan yaratilmoqda...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env fayli yaratildi. Iltimos, BOT_TOKEN va ADMIN_CHAT_ID ni kiriting.${NC}"
    echo ""
    read -p "Davom etishni xohlaysizmi? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Virtual environment yaratish
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Virtual environment yaratilmoqda...${NC}"
    python3 -m venv venv
fi

# Virtual environment ni faollashtirish
echo -e "${GREEN}🔧 Virtual environment faollashtirilmoqda...${NC}"
source venv/bin/activate

# Dependencies o'rnatish
echo -e "${YELLOW}📦 Python dependencies o'rnatilmoqda...${NC}"
pip install -r requirements.txt

# Frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Frontend dependencies o'rnatilmoqda...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    cp frontend/.env.example frontend/.env
fi

echo ""
echo -e "${GREEN}✅ Barcha dependencies o'rnatildi!${NC}"
echo ""
echo "📱 Botni ishga tushirish uchun:"
echo "   python bot.py"
echo ""
echo "🖥️  Backend serverni ishga tushirish uchun:"
echo "   python app.py"
echo ""
echo "🎨 Frontend serverni ishga tushirish uchun:"
echo "   cd frontend && npm run dev"
echo ""
echo -e "${YELLOW}💡 Maslahat: 3 ta terminal oching va har birida bitta komandani ishga tushiring${NC}"
