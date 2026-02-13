require('dotenv').config();
const { Telegraf } = require('telegraf');
const express = require('express');

const BOT_TOKEN = process.env.BOT_TOKEN;
const ADMIN_CHAT_ID = process.env.ADMIN_CHAT_ID;
const BOT_USERNAME = process.env.BOT_USERNAME;

const bot = new Telegraf(BOT_TOKEN);
const app = express();

app.use(express.json());

// Mini App havolasi
bot.start((ctx) => {
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
            url: process.env.MINI_APP_URL || 'https://yourdomain.com'
          }
        }
      ]]
    }
  });
});

// Buyurtmalarni qabul qilish
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

    // Buyurtma xabarini tayyorlash
    const itemsList = items
      .map(item => `  • ${item.name} × ${item.quantity} = ${(item.price * item.quantity).toLocaleString()} so'm`)
      .join('\n');

    const message = `
<b>📦 YANGI BUYURTMA</b>

<b>👤 Foydalanuvchi:</b> ${userName}
<b>📱 Telefon:</b> <code>${phone}</code>
<b>🆔 User ID:</b> <code>${userId}</code>

<b>📍 Manzil:</b>
<code>${address}</code>

${notes ? `<b>📝 Qo'shimcha izoh:</b>\n${notes}` : ''}

<b>📋 Buyurtma tafsilotlari:</b>
${itemsList}

<b>💰 Jami narx:</b> <code>${totalPrice.toLocaleString()} so'm</code>

<b>⏰ Vaqti:</b> ${new Date(timestamp).toLocaleString('uz-UZ')}
    `;

    // Admin'ga xabar yuborish
    await bot.telegram.sendMessage(ADMIN_CHAT_ID, message, {
      parse_mode: 'HTML'
    });

    // Foydalanuvchiga tasdiqlash yuborish (agar kerak bo'lsa)
    if (userId) {
      await bot.telegram.sendMessage(userId, `
✅ <b>Buyurtmangiz qabul qilindi!</b>

Siz bilan tez orada bog'lanib, dostavka vaqtini keltiramiz.

Buyurtma raqami: <code>${Math.random().toString(36).substr(2, 9).toUpperCase()}</code>
Jami: ${totalPrice.toLocaleString()} so'm
      `, {
        parse_mode: 'HTML'
      });
    }

    res.json({ success: true, message: 'Buyurtma qabul qilindi' });
  } catch (error) {
    console.error('Xato:', error);
    res.status(500).json({ error: error.message });
  }
});

// Webhook orqali yangilanishlarni qabul qilish
app.post(`/bot${BOT_TOKEN}`, (req, res) => {
  bot.handleUpdate(req.body, res);
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK' });
});

// Server ishga tushirish
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Bot server ${PORT}-portda ishlayapti`);
});

// Polling orqali (local test uchun)
if (process.env.USE_POLLING === 'true') {
  bot.launch();
  console.log('🤖 Bot polling rejimida ishlayapti...');
}

module.exports = { bot, app };
