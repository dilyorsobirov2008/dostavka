require('dotenv').config();
const { Telegraf } = require('telegraf');
const express = require('express');
const path = require('path');

// Bot tokeni va admin chat ID
const BOT_TOKEN = '8516821604:AAEW4IT9CXtB6R9hcoeRcnsJygCVzQ-IhOo';
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID || '123456789'; // Bu yerga o'zingizning Telegram ID'ni qo'ying
const BOT_USERNAME = 'supermarket_shop_bot';

// Server sozlamalari
const PORT = process.env.PORT || 8000;
const MINI_APP_URL = process.env.MINI_APP_URL || 'https://your-render-frontend-url.onrender.com';

const bot = new Telegraf(BOT_TOKEN);
const app = express();

app.use(express.json());
app.use(express.static('public'));

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ 
    status: 'Bot is running! ✅',
    botUsername: BOT_USERNAME,
    timestamp: new Date().toISOString()
  });
});

// Health check untuk uptime robot
app.get('/health', (req, res) => {
  res.json({ status: 'OK' });
});

// Mini App havolasi bilan /start
bot.start((ctx) => {
  console.log(`📱 New user: ${ctx.from.first_name} (ID: ${ctx.from.id})`);
  
  ctx.replyWithHTML(`
    <b>🛒 Supermarket ilovasiga xush kelibsiz!</b>

    <i>Mahsulotlarni qidiring, savatchaga qo'shing va buyurtma bering.</i>

    Ilovani ochish uchun quyidagi tugmani bosing:
  `, {
    reply_markup: {
      inline_keyboard: [[
        {
          text: '🛒 Supermarketchani ochish',
          web_app: {
            url: MINI_APP_URL
          }
        }
      ]]
    }
  });
});

// Buyurtmalarni qabul qilish API
app.post('/api/orders', async (req, res) => {
  try {
    const {
      userId,
      userName,
      phone,
      address,
      notes,
      items,
      totalPrice,
      timestamp
    } = req.body;

    console.log('📦 New order received:', {
      userName,
      phone,
      itemsCount: items?.length,
      totalPrice
    });

    // Validation
    if (!userName || !phone || !address || !items || items.length === 0) {
      return res.status(400).json({ 
        error: 'Barcha maydonlar to\'ldirilishi kerak' 
      });
    }

    // Buyurtma raqamini generatsiya qilish
    const orderId = Math.random().toString(36).substr(2, 9).toUpperCase();

    // Buyurtma xabarini tayyorlash
    const itemsList = items
      .map(item => `  • ${item.name} × ${item.quantity} = ${(item.price * item.quantity).toLocaleString()} so'm`)
      .join('\n');

    const adminMessage = `
<b>📦 YANGI BUYURTMA #${orderId}</b>

<b>👤 Foydalanuvchi:</b> ${userName}
<b>📱 Telefon:</b> <code>${phone}</code>
<b>🆔 User ID:</b> <code>${userId || 'N/A'}</code>

<b>📍 Dostavka manzili:</b>
<code>${address}</code>

${notes ? `<b>📝 Qo'shimcha izoh:</b>\n${notes}` : ''}

<b>📋 Buyurtma tafsilotlari:</b>
${itemsList}

<b>💰 Oraliq narx:</b> <code>${(totalPrice).toLocaleString()} so'm</code>
<b>🚚 Dostavka:</b> <code>25,000 so'm</code>
<b>💵 JAMI:</b> <code>${(totalPrice + 25000).toLocaleString()} so'm</code>

<b>⏰ Vaqti:</b> ${new Date(timestamp).toLocaleString('uz-UZ')}
    `;

    // Admin'ga xabar yuborish
    try {
      await bot.telegram.sendMessage(ADMIN_CHAT_ID, adminMessage, {
        parse_mode: 'HTML'
      });
      console.log(`✅ Admin message sent for order #${orderId}`);
    } catch (error) {
      console.error('❌ Failed to send admin message:', error.message);
    }

    // Foydalanuvchiga tasdiqlash yuborish (agar kerak bo'lsa)
    if (userId) {
      try {
        const userMessage = `
✅ <b>Buyurtmangiz qabul qilindi!</b>

Siz bilan tez orada bog'lanib, dostavka vaqtini keltiramiz.

<b>Buyurtma raqami:</b> #${orderId}
<b>Jami:</b> ${(totalPrice + 25000).toLocaleString()} so'm

Rahmat! 🙏
        `;
        await bot.telegram.sendMessage(userId, userMessage, {
          parse_mode: 'HTML'
        });
      } catch (error) {
        console.log('User confirmation message failed (ok):', error.message);
      }
    }

    res.json({ 
      success: true, 
      message: 'Buyurtma qabul qilindi',
      orderId: orderId,
      totalPrice: totalPrice + 25000
    });

  } catch (error) {
    console.error('❌ Order processing error:', error);
    res.status(500).json({ 
      error: error.message,
      success: false
    });
  }
});

// Webhook endpoint (Render'da kerak)
const WEBHOOK_URL = `${process.env.RENDER_EXTERNAL_URL || 'https://your-app-name.onrender.com'}/webhook`;

app.post('/webhook', (req, res) => {
  bot.handleUpdate(req.body, res);
});

// Bot bilan bog'lash
bot.catch((err, ctx) => {
  console.error('❌ Bot error:', err);
});

// Server ishga tushirish
app.listen(PORT, async () => {
  console.log(`
╔════════════════════════════════════════════════════╗
║     🛒 SUPERMARKET BOT SERVER STARTED ✅           ║
╠════════════════════════════════════════════════════╣
║ 🔗 Server Port: ${PORT}                                 ║
║ 🤖 Bot Username: @${BOT_USERNAME}                    ║
║ 📱 Mini App URL: ${MINI_APP_URL.substring(0, 40)}... ║
║ 🌍 Webhook: ${WEBHOOK_URL.substring(0, 40)}... ║
╚════════════════════════════════════════════════════╝
  `);

  // Webhook'ni o'rnatish
  if (process.env.NODE_ENV === 'production') {
    try {
      await bot.telegram.setWebhook(WEBHOOK_URL);
      console.log('✅ Webhook set successfully');
    } catch (error) {
      console.error('⚠️ Webhook setup error:', error.message);
    }
  } else {
    // Local development - polling
    console.log('🔄 Running in polling mode (development)');
    bot.launch();
  }
});

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

module.exports = { bot, app };
