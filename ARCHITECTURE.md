TELEGRAM MINI APP SUPERMARKET - ARCHITECTURE DIAGRAM
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                      TELEGRAM USER (MOBILE/DESKTOP)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TELEGRAM BOT (@BotFather)                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ /start → 🛒 Supermarketchani ochish                                 │   │
│  │ Mini App Button → MINI_APP_URL ga yuborish                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
    ┌──────────────────────────────┐   ┌──────────────────────────┐
    │  FRONTEND (React + Vite)     │   │  BACKEND (Node.js)       │
    │  ┌──────────────────────────┐│   │  ┌──────────────────────┐│
    │  │ Header (Logo + Cart)     ││   │  │ Express Server       ││
    │  │ Category Filter          ││   │  │ POST /api/orders     ││
    │  │ Product Grid (4 col)     ││   │  │ Bot Handler (Telegraf)││
    │  │ Cart Sidebar             ││   │  │ Email/SMS Notif      ││
    │  │ Checkout Form            ││   │  │ Order Database       ││
    │  └──────────────────────────┘│   │  └──────────────────────┘│
    │                              │   │                          │
    │  @telegram-apps/sdk init     │   │  Bot Token: env var      │
    │  TMA UI Kit (Colors)         │   │  Admin ID: env var       │
    └──────────────────────────────┘   └──────────────────────────┘
                    │                         ▲
                    │ HTTP POST               │
                    │ /api/orders             │ Send Message
                    │ (Cart + User Data)      │
                    └─────────────────────────┘


COMPONENT TREE:
================================================================================

App
├── Header
│   ├── Logo
│   ├── Cart Badge (count)
│   └── Total Price Display
│
├── Category
│   ├── Category Buttons (Mevalar, Sut, Go'sht, Ichimliklar)
│   └── Search Input
│
├── ProductGrid
│   └── ProductCard × N
│       ├── Image
│       ├── Name
│       ├── Price
│       └── Add Button
│
├── Cart (Sidebar)
│   ├── Cart Header
│   ├── CartItems × N
│   │   ├── Item Image
│   │   ├── Item Name & Price
│   │   ├── Quantity Controls (±)
│   │   └── Remove Button
│   ├── Summary (Subtotal, Delivery, Total)
│   └── Checkout Button
│
└── Checkout (Modal)
    ├── User Info Form
    │   ├── Full Name Input
    │   ├── Phone Input
    │   └── Address TextArea
    ├── Order Summary
    │   └── Items List with Prices
    └── Submit Button


DATA FLOW:
================================================================================

1. USER SELECTS PRODUCT
   ProductCard → addToCart() → App State (cart array)

2. CART UPDATED
   Cart State → Display CartItems → Show Total

3. USER CLICKS CHECKOUT
   Checkout Form → Validates Input → POST /api/orders

4. ORDER SENT TO BACKEND
   Backend receives: {userId, userName, phone, address, items, totalPrice}

5. ADMIN NOTIFIED
   Bot sends message to ADMIN_CHAT_ID with order details

6. SUCCESS MESSAGE
   User sees confirmation, Cart clears


FOLDER STRUCTURE:
================================================================================

supermarket-tma/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.jsx                    ← Main App
│   │   │   ├── Header.jsx                 ← Top Bar
│   │   │   ├── Category.jsx               ← Category Filter
│   │   │   ├── ProductCard.jsx (in App)   ← Product Tile
│   │   │   ├── Cart.jsx                   ← Cart Sidebar
│   │   │   ├── Checkout.jsx               ← Order Form
│   │   │   └── Loading.jsx                ← Loading State
│   │   │
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   ├── Category.css
│   │   │   └── Checkout.css
│   │   │
│   │   ├── utils/
│   │   │   ├── api.js                     ← API calls
│   │   │   ├── tmaUtils.js                ← TMA SDK helpers
│   │   │   └── storage.js                 ← LocalStorage
│   │   │
│   │   ├── main.jsx
│   │   ├── App.jsx (COMBINED)
│   │   └── index.css
│   │
│   ├── public/
│   │   └── index.html
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── bot.js                             ← Main Bot Logic
│   │
│   ├── handlers/
│   │   ├── orderHandler.js                ← Process Orders
│   │   └── notificationHandler.js         ← Send Messages
│   │
│   ├── models/
│   │   ├── Order.js                       ← Order Schema
│   │   └── Product.js                     ← Product Schema
│   │
│   ├── package.json
│   ├── .env                               ← Secrets (git ignore!)
│   ├── .env.example                       ← Template
│   └── .gitignore
│
├── README.md
└── .gitignore


KEY FILES SUMMARY:
================================================================================

Frontend Files Created:
  ✓ App.jsx             - Main component with state management
  ✓ Category.jsx        - Category filtering
  ✓ Cart.jsx            - Shopping cart display
  ✓ Checkout.jsx        - Order form
  ✓ App.css             - All styling (Telegram UI Kit style)
  ✓ vite.config.js      - Vite configuration
  ✓ package.json        - Dependencies

Backend Files Created:
  ✓ bot.js              - Express + Telegraf main file
  ✓ .env.example        - Environment variables template
  ✓ package.json        - Node dependencies


DEPLOYMENT CHECKLIST:
================================================================================

Frontend:
  □ Build: npm run build
  □ Deploy to: Vercel, Netlify, or custom server
  □ Get HTTPS URL
  □ Update MINI_APP_URL in .env

Backend:
  □ Set environment variables (BOT_TOKEN, ADMIN_CHAT_ID, MINI_APP_URL)
  □ Deploy to: Heroku, Railway, or custom VPS
  □ Webhook URL: https://yourdomain.com/bot{BOT_TOKEN}
  □ Register webhook with Telegram

Bot Setup:
  □ Create bot with @BotFather
  □ Get BOT_TOKEN
  □ Set Menu Button with Mini App
  □ Get Admin's Chat ID
  □ Test in staging environment


SECURITY CONSIDERATIONS:
================================================================================

1. Input Validation
   - Validate all form inputs on frontend AND backend
   - Use regex for phone number validation
   
2. Rate Limiting
   - Limit API requests per user/IP
   - Prevent order spam

3. Environment Variables
   - Never commit .env file
   - Use .env.example as template
   - Rotate BOT_TOKEN if compromised

4. Data Privacy
   - Store only necessary user data
   - Hash sensitive information
   - GDPR compliance

5. HTTPS Only
   - Mini Apps MUST use HTTPS
   - Secure WebApp connection

================================================================================
