import os
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import requests
from datetime import datetime

DURATION_MINUTES = 42
DURATION_MS = DURATION_MINUTES * 60 * 1000
SAMPLE_RATE = 48000
FILENAME = f"/tmp/session_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.flac"

def generate_binaural_beat(duration_ms, base_freq=200, beat_freq=4):
    left = Sine(base_freq).to_audio_segment(duration=duration_ms)
    right = Sine(base_freq + beat_freq).to_audio_segment(duration=duration_ms)
    return left, right

def generate_pink_noise(duration_ms, volume_db=-30):
    samples = np.random.normal(0, 1, int(SAMPLE_RATE * DURATION_MINUTES))
    audio = AudioSegment(
        samples.astype(np.float32).tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=4,
        channels=1
    ).apply_gain(volume_db)
    return audio

def generate_full_session():
    left, right = generate_binaural_beat(DURATION_MS)
    pink_noise = generate_pink_noise(DURATION_MS)
    left = left.overlay(pink_noise - 5)
    right = right.overlay(pink_noise - 5)
    session = AudioSegment.from_mono_audiosegments(left, right)
    return session

def upload_to_pixeldrain(filepath):
    api_key = os.getenv("PIXELDRAIN_API_KEY")
    with open(filepath, 'rb') as f:
        response = requests.post(
            'https://pixeldrain.com/api/file',
            files={'file': f},
            auth=(api_key, '')
        )
    if response.status_code == 200:
        file_id = response.json()['id']
        return f"https://pixeldrain.com/u/{file_id}"
    else:
        raise Exception("❌ فشل في رفع الملف إلى Pixeldrain")

def send_to_telegram(link):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    user_id = os.getenv("TELEGRAM_USER_ID")
    text = f"""🧠 جلسة جديدة تم توليدها تلقائيًا
💊 التأثير: هلوسة واقعية + ترددات Theta
⏱️ المدة: {DURATION_MINUTES} دقيقة
🎧 الصيغة: FLAC (48kHz, 24bit)
🔗 رابط التحميل: {link}"""
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": user_id, "text": text}
    )

def handler(request):
    try:
        print("🔊 توليد الجلسة...")
        session = generate_full_session()
        session.export(FILENAME, format="flac")
        print("✅ تصدير الجلسة")

        print("⬆️ رفع إلى Pixeldrain...")
        link = upload_to_pixeldrain(FILENAME)
        print("📨 إرسال إلى تيليجرام...")
        send_to_telegram(link)

        return {
            "statusCode": 200,
            "body": f"✅ جلسة مرفوعة: {link}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"❌ خطأ: {str(e)}"
        }
