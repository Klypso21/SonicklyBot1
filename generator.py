import os
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import requests
from datetime import datetime

# --- الإعدادات العامة ---
DURATION_MINUTES = 42
DURATION_MS = DURATION_MINUTES * 60 * 1000
SAMPLE_RATE = 48000
FILENAME = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.flac"

# --- توليد binaural beat: left = 200Hz, right = 204Hz (يعطيك 4Hz فرق - Theta) ---
def generate_binaural_beat(duration_ms, base_freq=200, beat_freq=4):
    left = Sine(base_freq).to_audio_segment(duration=duration_ms)
    right = Sine(base_freq + beat_freq).to_audio_segment(duration=duration_ms)
    return left, right

# --- توليد pink noise (ضجيج مهلوس مريح للأذن) ---
def generate_pink_noise(duration_ms, volume_db=-30):
    samples = np.random.normal(0, 1, int(SAMPLE_RATE * DURATION_MINUTES))
    audio = AudioSegment(
        samples.astype(np.float32).tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=4,
        channels=1
    ).apply_gain(volume_db)
    return audio

# --- دمج كل العناصر ---
def generate_full_session():
    left, right = generate_binaural_beat(DURATION_MS)
    pink_noise = generate_pink_noise(DURATION_MS)

    # Mix left + noise
    left = left.overlay(pink_noise - 5)
    right = right.overlay(pink_noise - 5)

    # Combine to stereo
    session = AudioSegment.from_mono_audiosegments(left, right)
    return session

# --- توليد وتصدير الجلسة ---
print("🧠 توليد الجلسة...")
session = generate_full_session()
session.export(FILENAME, format="flac")
print(f"✅ تم تصدير الجلسة: {FILENAME}")

# --- رفع الجلسة إلى Pixeldrain ---
PIXELDRAIN_API_KEY = os.getenv("PIXELDRAIN_API_KEY")
with open(FILENAME, 'rb') as f:
    upload = requests.post(
        'https://pixeldrain.com/api/file',
        files={'file': f},
        auth=(PIXELDRAIN_API_KEY, '')
    )

if upload.status_code == 200:
    file_id = upload.json()['id']
    link = f"https://pixeldrain.com/u/{file_id}"
    print(f"✅ تم رفع الجلسة: {link}")

    # --- إرسال إلى تيليجرام ---
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_user_id = os.getenv("TELEGRAM_USER_ID")
    text = f"""🧠 جلسة جديدة تم توليدها تلقائيًا
💊 التأثير: هلوسة واقعية + ترددات Theta
⏱️ المدة: {DURATION_MINUTES} دقيقة
🎧 الصيغة: FLAC (48kHz, 24bit)
🔗 رابط التحميل: {link}""".strip()
