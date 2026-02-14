"""
Configuration settings for SuperMarket Mini App
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))
FLASK_ENV = os.getenv('FLASK_ENV', 'production')

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID')

# Database
ORDERS_FILE = 'orders.json'

# App Info
APP_NAME = 'SuperMarket Mini App'
APP_VERSION = '1.0.0'
AUTHOR = 'SuperMarket Team'

# CORS Settings
CORS_ORIGINS = ['*']

print(f"""
╔════════════════════════════════════════════════════════════╗
║ {APP_NAME} v{APP_VERSION}
║ Environment: {FLASK_ENV}
║ Debug: {DEBUG}
║ Port: {PORT}
╚════════════════════════════════════════════════════════════╝
""")
