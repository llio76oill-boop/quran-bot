#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلغرام لإرسال آيات قصيرة من القرآن الكريم إلى قناة
Quran Telegram Bot - Sends random Quranic verses to a channel every 15 minutes
"""

import os
import logging
import random
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('quran_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# الثوابت
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')  # معرف القناة مثل: @channel_name أو -100123456789
QURAN_API_URL = "https://api.alquran.cloud/v1"
QURAN_EDITION = "ar.alafasy"  # النسخة العربية

# حالات المحادثة
WAITING_FOR_SURAH = 1

class QuranAPI:
    """فئة للتعامل مع API القرآن الكريم"""
    
    def __init__(self):
        self.base_url = QURAN_API_URL
        self.edition = QURAN_EDITION
        self.session = requests.Session()
        self.session.headers.update({'Accept-Encoding': 'gzip'})
        self.surah_info = None
        self._load_surah_info()
    
    def _load_surah_info(self):
        """تحميل معلومات السور"""
        try:
            response = self.session.get(f"{self.base_url}/surah")
            if response.status_code == 200:
                self.surah_info = response.json().get('data', [])
                logger.info(f"✅ تم تحميل معلومات {len(self.surah_info)} سورة")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل معلومات السور: {e}")
    
    def get_random_verse(self) -> Optional[Dict]:
        """الحصول على آية عشوائية من القرآن"""
        try:
            if not self.surah_info:
                self._load_surah_info()
            
            # اختيار سورة عشوائية (من 1 إلى 114)
            surah_number = random.randint(1, 114)
            
            # الحصول على عدد الآيات في السورة
            surah = next((s for s in self.surah_info if s['number'] == surah_number), None)
            if not surah:
                return None
            
            ayah_count = surah['numberOfAyahs']
            ayah_number = random.randint(1, ayah_count)
            
            # جلب الآية
            return self.get_verse(surah_number, ayah_number)
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على آية عشوائية: {e}")
            return None
    
    def get_verse(self, surah: int, ayah: int) -> Optional[Dict]:
        """الحصول على آية محددة"""
        try:
            url = f"{self.base_url}/ayah/{surah}:{ayah}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                return {
                    'surah': data.get('surah', {}).get('name', 'غير معروف'),
                    'surah_number': data.get('surah', {}).get('number', 0),
                    'ayah_number': data.get('numberInSurah', 0),
                    'text': data.get('text', ''),
                    'full_reference': f"{data.get('surah', {}).get('name', '')} {data.get('numberInSurah', '')}"
                }
            return None
        except Exception as e:
            logger.error(f"❌ خطأ في جلب الآية {surah}:{ayah}: {e}")
            return None
    
    def search_verses(self, keyword: str) -> List[Dict]:
        """البحث عن آيات تحتوي على كلمة محددة"""
        try:
            url = f"{self.base_url}/search/{keyword}/en"
            response = self.session.get(url)
            
            if response.status_code == 200:
                matches = response.json().get('data', {}).get('matches', [])
                results = []
                for match in matches[:5]:  # أول 5 نتائج
                    results.append({
                        'surah': match.get('surah', {}).get('name', ''),
                        'ayah': match.get('numberInSurah', ''),
                        'text': match.get('text', '')
                    })
                return results
            return []
        except Exception as e:
            logger.error(f"❌ خطأ في البحث: {e}")
            return []

class QuranBot:
    """فئة رئيسية لبوت القرآن"""
    
    def __init__(self):
        self.quran_api = QuranAPI()
        self.scheduler = BackgroundScheduler()
        self.channel_id = CHANNEL_ID
        self.app = None
        
        # تحميل تفضيلات المستخدمين
        self.user_preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict:
        """تحميل تفضيلات المستخدمين من ملف"""
        try:
            if os.path.exists('user_preferences.json'):
                with open('user_preferences.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل التفضيلات: {e}")
        return {}
    
    def _save_preferences(self):
        """حفظ تفضيلات المستخدمين"""
        try:
            with open('user_preferences.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ التفضيلات: {e}")
    
    def format_verse_message(self, verse: Dict) -> str:
        """تنسيق رسالة الآية"""
        if not verse:
            return "❌ عذراً، حدث خطأ في جلب الآية"
        
        message = f"""
📖 *{verse['full_reference']}*

{verse['text']}

_تم الإرسال: {datetime.now().strftime('%H:%M')} ⏰_
"""
        return message.strip()
    
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
            
            message = self.format_verse_message(verse)
            
            # إرسال الرسالة إلى القناة
            await self.app.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode="Markdown"
            )
            
            logger.info(f"✅ تم إرسال الآية: {verse['full_reference']} إلى القناة")
        
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الآية إلى القناة: {e}")
    
    def schedule_periodic_verses(self):
        """جدولة إرسال الآيات الدورية"""
        self.scheduler.add_job(
            func=lambda: self._run_async_job(self.send_verse_to_channel()),
            trigger=IntervalTrigger(minutes=15),
            id="periodic_verse",
            replace_existing=True
        )
        self.scheduler.start()
        logger.info("✅ تم جدولة إرسال الآيات (كل 15 دقيقة)")
    
    def _run_async_job(self, coro):
        """تشغيل مهمة غير متزامنة"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(coro)

# إنشاء نسخة عامة من البوت
bot = QuranBot()

# معالجات الأوامر

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /start"""
    user_id = str(update.effective_user.id)
    
    if user_id not in bot.user_preferences:
        bot.user_preferences[user_id] = {
            "enabled": True,
            "joined_at": datetime.now().isoformat()
        }
        bot.user_preferences[user_id] = bot.user_preferences.get(user_id, {})
        bot.user_preferences[user_id]["enabled"] = True
        bot._save_preferences()
    
    message = """
👋 مرحباً بك في بوت آيات القرآن الكريم!

🕌 هذا البوت ينشر آيات قصيرة من القرآن الكريم في قناة خاصة كل 15 دقيقة.

📚 الأوامر المتاحة:
/verse - احصل على آية عشوائية فوراً
/surah - اختر سورة معينة
/search - ابحث عن آيات
/help - قائمة المساعدة

🙏 بارك الله فيك
"""
    
    await update.message.reply_text(message)
    logger.info(f"✅ مستخدم جديد: {user_id}")

async def get_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /verse - آية عشوائية"""
    verse = bot.quran_api.get_random_verse()
    message = bot.format_verse_message(verse)
    await update.message.reply_text(message, parse_mode="Markdown")
    logger.info(f"✅ تم إرسال آية عشوائية للمستخدم: {update.effective_user.id}")

async def surah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /surah - اختيار سورة"""
    if not context.args:
        await update.message.reply_text(
            "❌ الرجاء تحديد رقم السورة\n"
            "مثال: /surah 1"
        )
        return
    
    try:
        surah_number = int(context.args[0])
        if surah_number < 1 or surah_number > 114:
            await update.message.reply_text("❌ رقم السورة يجب أن يكون بين 1 و 114")
            return
        
        verse = bot.quran_api.get_verse(surah_number, 1)
        message = bot.format_verse_message(verse)
        await update.message.reply_text(message, parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ الرجاء إدخال رقم صحيح")

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /search - البحث عن آيات"""
    if not context.args:
        await update.message.reply_text("❌ الرجاء إدخال كلمة للبحث")
        return
    
    keyword = " ".join(context.args)
    results = bot.quran_api.search_verses(keyword)
    
    if not results:
        await update.message.reply_text(f"❌ لم يتم العثور على نتائج للكلمة: {keyword}")
        return
    
    message = f"🔍 نتائج البحث عن: {keyword}\n\n"
    for i, result in enumerate(results, 1):
        message += f"{i}. {result['surah']} {result['ayah']}\n{result['text']}\n\n"
    
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /help - المساعدة"""
    message = """
📚 قائمة الأوامر:

/start - بدء البوت
/verse - آية عشوائية
/surah <رقم> - آيات من سورة معينة
/search <كلمة> - البحث عن آيات
/help - هذه القائمة

💡 نصائح:
• البوت ينشر آية كل 15 دقيقة في القناة
• يمكنك استخدام الأوامر أعلاه للحصول على آيات فوراً
• تابع القناة للحصول على الآيات الدورية

🙏 بارك الله فيك
"""
    await update.message.reply_text(message)

async def main():
    """الدالة الرئيسية"""
    logger.info("🤖 بدء تشغيل بوت القرآن الكريم (نسخة القناة)...")
    
    # إنشاء التطبيق
    bot.app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إضافة معالجات الأوامر
    bot.app.add_handler(CommandHandler("start", start))
    bot.app.add_handler(CommandHandler("verse", get_verse))
    bot.app.add_handler(CommandHandler("surah", surah_command))
    bot.app.add_handler(CommandHandler("search", search_command))
    bot.app.add_handler(CommandHandler("help", help_command))
    
    # جدولة الإرسال الدوري
    bot.schedule_periodic_verses()
    
    logger.info("✅ البوت جاهز للعمل!")
    logger.info(f"📢 القناة المستهدفة: {bot.channel_id}")
    
    # بدء البوت
    await bot.app.initialize()
    await bot.app.start()
    await bot.app.updater.start_polling()
    
    # الاستمرار في التشغيل
    await bot.app.updater.idle()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")
