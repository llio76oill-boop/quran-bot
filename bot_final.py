#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلغرام متقدم لإرسال آيات قصيرة من القرآن الكريم إلى قناة
Advanced Quran Telegram Bot - Sends random Quranic verses to a channel every 15 minutes
"""

import os
import logging
import random
import requests
import asyncio
import threading
from datetime import datetime
from typing import Optional, Dict, List
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('quran_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# الثوابت
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
QURAN_API_URL = "https://api.alquran.cloud/v1"
PORT = int(os.getenv('PORT', 8000))

# قاموس أسماء السور بالعربية
SURAH_NAMES_AR = {
    1: "الفاتحة", 2: "البقرة", 3: "آل عمران", 4: "النساء", 5: "المائدة",
    6: "الأنعام", 7: "الأعراف", 8: "الأنفال", 9: "التوبة", 10: "يونس",
    11: "هود", 12: "يوسف", 13: "الرعد", 14: "إبراهيم", 15: "الحجر",
    16: "النحل", 17: "الإسراء", 18: "الكهف", 19: "مريم", 20: "طه",
    21: "الأنبياء", 22: "الحج", 23: "المؤمنون", 24: "النور", 25: "الفرقان",
    26: "الشعراء", 27: "النمل", 28: "القصص", 29: "العنكبوت", 30: "الروم",
    31: "لقمان", 32: "السجدة", 33: "الأحزاب", 34: "سبأ", 35: "فاطر",
    36: "يس", 37: "الصافات", 38: "ص", 39: "الزمر", 40: "غافر",
    41: "فصلت", 42: "الشورى", 43: "الزخرف", 44: "الدخان", 45: "الجاثية",
    46: "الأحقاف", 47: "محمد", 48: "الفتح", 49: "الحجرات", 50: "ق",
    51: "الذاريات", 52: "الطور", 53: "النجم", 54: "القمر", 55: "الرحمن",
    56: "الواقعة", 57: "الحديد", 58: "المجادلة", 59: "الحشر", 60: "الممتحنة",
    61: "الصف", 62: "الجمعة", 63: "المنافقون", 64: "التغابن", 65: "الطلاق",
    66: "التحريم", 67: "الملك", 68: "القلم", 69: "الحاقة", 70: "المعارج",
    71: "نوح", 72: "الجن", 73: "المزمل", 74: "المدثر", 75: "القيامة",
    76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "الناشئات", 80: "عبس",
    81: "التكوير", 82: "الإنفطار", 83: "المطففين", 84: "الانشقاق", 85: "البروج",
    86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
    91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
    96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
    101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
    106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
    111: "المسد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"
}

# ============================================================
# Web Server البسيط (لـ Render.com)
# ============================================================

class HealthCheckHandler(BaseHTTPRequestHandler):
    """معالج طلبات صحة البوت"""
    
    def do_GET(self):
        """معالج طلبات GET"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """تعطيل السجلات الافتراضية"""
        pass

def start_web_server():
    """بدء web server بسيط"""
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
        logger.info(f"✅ بدء Web Server على المنفذ {PORT}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ خطأ في Web Server: {e}")

# ============================================================
# فئة API القرآن الكريم
# ============================================================

class QuranAPI:
    """فئة للتعامل مع API القرآن الكريم"""
    
    def __init__(self):
        self.base_url = QURAN_API_URL
        self.surahs = []
        self.load_surahs()
    
    def load_surahs(self):
        """تحميل قائمة السور"""
        try:
            response = requests.get(f"{self.base_url}/surah", timeout=10)
            if response.status_code == 200:
                self.surahs = response.json()['data']
                logger.info(f"✅ تم تحميل معلومات {len(self.surahs)} سورة")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل السور: {e}")
    
    def get_random_verse(self) -> Optional[Dict]:
        """الحصول على آية عشوائية"""
        try:
            surah_num = random.randint(1, 114)
            response = requests.get(f"{self.base_url}/surah/{surah_num}", timeout=10)
            
            if response.status_code == 200:
                surah_data = response.json()['data']
                ayahs = surah_data['ayahs']
                random_ayah = random.choice(ayahs)
                
                # الحصول على اسم السورة بالعربية
                surah_name_ar = SURAH_NAMES_AR.get(surah_num, surah_data['englishName'])
                
                return {
                    'surah': surah_data['englishName'],
                    'surah_ar': surah_name_ar,
                    'surah_number': surah_num,
                    'ayah_number': random_ayah['numberInSurah'],
                    'text': random_ayah['text'],
                    'full_reference': f"{surah_data['englishName']} {random_ayah['numberInSurah']}"
                }
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على آية: {e}")
        
        return None
    
    def search_verses(self, keyword: str) -> Optional[List[Dict]]:
        """البحث عن آيات تحتوي على كلمة معينة"""
        try:
            response = requests.get(f"{self.base_url}/search/{keyword}", timeout=10)
            if response.status_code == 200:
                return response.json()['data']['matches']
        except Exception as e:
            logger.error(f"❌ خطأ في البحث: {e}")
        
        return None
    
    def get_surah_verses(self, surah_num: int) -> Optional[Dict]:
        """الحصول على آيات سورة معينة"""
        try:
            if 1 <= surah_num <= 114:
                response = requests.get(f"{self.base_url}/surah/{surah_num}", timeout=10)
                if response.status_code == 200:
                    return response.json()['data']
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على السورة: {e}")
        
        return None

# ============================================================
# فئة البوت الرئيسية
# ============================================================

class QuranBot:
    """فئة البوت الرئيسية"""
    
    def __init__(self, token: str, channel_id: str):
        self.token = token
        self.channel_id = channel_id
        self.quran_api = QuranAPI()
        self.verse_count = 0
        self.last_verse = None
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.running = True
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        """إرسال رسالة عبر Telegram API"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                logger.error(f"❌ فشل الإرسال: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الرسالة: {e}")
            return False
    
    def format_verse_message(self, verse: Dict) -> str:
        """تنسيق رسالة الآية بتنسيق جميل"""
        # استخدام القوس المزخرف
        formatted_text = f"﴿{verse['text']}﴾"
        
        return f"""{formatted_text}

{verse['surah_ar']} - {verse['ayah_number']}

قناة آية كل 15 دقيقة"""
    
    async def send_verse_to_channel(self):
        """إرسال آية إلى القناة"""
        try:
            if not self.channel_id:
                logger.warning("⚠️ معرف القناة غير محدد")
                return
            
            verse = self.quran_api.get_random_verse()
            if not verse:
                logger.error("❌ فشل في الحصول على آية")
                return
            
            # تجنب إرسال نفس الآية مرتين متتاليتين
            if self.last_verse and self.last_verse == verse['full_reference']:
                verse = self.quran_api.get_random_verse()
            
            message = self.format_verse_message(verse)
            
            # إرسال الرسالة إلى القناة
            if self.send_message(self.channel_id, message):
                self.last_verse = verse['full_reference']
                self.verse_count += 1
                logger.info(f"✅ تم إرسال الآية #{self.verse_count}: {verse['full_reference']} إلى القناة")
            else:
                logger.error("❌ فشل في إرسال الآية")
        
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الآية إلى القناة: {e}")
    
    async def periodic_sender(self):
        """مهمة دورية لإرسال الآيات"""
        logger.info("✅ بدء المهمة الدورية لإرسال الآيات")
        
        # إرسال الآية الأولى فوراً
        await self.send_verse_to_channel()
        
        while self.running:
            try:
                # انتظر 15 دقيقة
                await asyncio.sleep(15 * 60)
                
                if self.running:
                    await self.send_verse_to_channel()
            except asyncio.CancelledError:
                logger.info("🛑 تم إيقاف المهمة الدورية")
                break
            except Exception as e:
                logger.error(f"❌ خطأ في المهمة الدورية: {e}")
                await asyncio.sleep(5)
    
    async def run(self):
        """تشغيل البوت"""
        logger.info("=" * 60)
        logger.info("🤖 بدء تشغيل بوت القرآن الكريم")
        logger.info("=" * 60)
        logger.info(f"📱 البوت: @aya_Quraanbot")
        logger.info(f"📢 القناة: {self.channel_id}")
        logger.info(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # التحقق من البيانات المطلوبة
        if not self.token or not self.channel_id:
            logger.error("❌ خطأ: TELEGRAM_TOKEN أو CHANNEL_ID غير محدد")
            return
        
        # اختبار الاتصال بـ Telegram
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                bot_info = response.json()['result']
                logger.info(f"✅ تم الاتصال بـ Telegram: {bot_info['username']}")
            else:
                logger.error(f"❌ فشل الاتصال بـ Telegram: {response.text}")
                return
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال بـ Telegram: {e}")
            return
        
        logger.info("✅ تم جدولة إرسال الآيات (كل 15 دقيقة)")
        logger.info("✅ البوت جاهز للعمل!")
        logger.info("=" * 60)
        
        # بدء المهمة الدورية
        periodic_task = asyncio.create_task(self.periodic_sender())
        
        try:
            # الاستمرار في التشغيل
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("🛑 تم إيقاف البوت بواسطة المستخدم")
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
        finally:
            self.running = False
            periodic_task.cancel()
            try:
                await periodic_task
            except asyncio.CancelledError:
                pass
            logger.info("🛑 تم إيقاف البوت")

# ============================================================
# الدالة الرئيسية
# ============================================================

async def main():
    """الدالة الرئيسية"""
    # بدء Web Server في thread منفصل
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    # بدء البوت
    bot = QuranBot(TELEGRAM_TOKEN, CHANNEL_ID)
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")
    except Exception as e:
        logger.error(f"❌ خطأ حرج: {e}")
