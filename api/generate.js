export default async function handler(req, res) {
  const PIXELDRAIN_API_KEY = process.env.PIXELDRAIN_API_KEY;
  const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
  const TELEGRAM_USER_ID = process.env.TELEGRAM_USER_ID;

  // اختبار فقط: ملف صوت وهمي
  const sessionUrl = "https://pixeldrain.com/u/placeholder_session_id";

  // إرسال إلى تليجرام
  const telegramApiUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const message = `🧠 جلسة جديدة تم توليدها تلقائيًا\n💊 التأثير: هلوسة واقعية + ترددات Theta\n⏱️ المدة: 42 دقيقة\n🎧 الصيغة: FLAC (48kHz, 24bit)\n🔗 رابط التحميل: ${sessionUrl}`;

  try {
    await fetch(telegramApiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: TELEGRAM_USER_ID,
        text: message
      })
    });

    res.status(200).json({ status: "✅ Session message sent!", link: sessionUrl });
  } catch (err) {
    console.error("❌ Telegram Error:", err);
    res.status(500).json({ error: "Telegram send failed" });
  }
}
