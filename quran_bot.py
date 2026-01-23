#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلغرام لإرسال آيات قصيرة من القرآن الكريم
Quran Telegram Bot - Sends random Quranic verses every 15 minutes
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
CHANNEL_ID = os.getenv('CHANNEL_ID')
QURAN_API_URL = "https://api.alquran.cloud/v1"
QURAN_EDITION = "ar.alafasy"  # النسخة العربية
QURAN_EDITION_TRANSLATION = "ar.asad"  # الترجمة

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
                logger.info(f"تم تحميل معلومات {len(self.surah_info)} سورة")
        except Exception as e:
            logger.error(f"خطأ في تحميل معلومات السور: {e}")
    
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
            logger.error(f"خطأ في الحصول على آية عشوائية: {e}")
            return None
    
    def get_verse(self, surah: int, ayah: int, edition: str = None) -> Optional[Dict]:
        """الحصول على آية محددة"""
        try:
            if edition is None:
                edition = self.edition
            
            url = f"{self.base_url}/ayah/{surah}:{ayah}/{edition}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                return {
                    'surah': data.get('surah', {}).get('name', 'السورة'),
                    'surah_number': data.get('surah', {}).get('number', surah),
                    'ayah_number': data.get('numberInSurah', ayah),
                    'text': data.get('text', ''),
                    'edition': edition,
                    'full_reference': f"{data.get('surah', {}).get('name', 'السورة')} {data.get('numberInSurah', ayah)}"
                }
        except Exception as e:
            logger.error(f"خطأ في جلب الآية {surah}:{ayah}: {e}")
        
        return None
    
    def get_surah_verses(self, surah: int) -> Optional[List[Dict]]:
        """الحصول على جميع آيات سورة محددة"""
        try:
            url = f"{self.base_url}/surah/{surah}/{self.edition}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                ayahs = data.get('ayahs', [])
                
                verses = []
                for ayah in ayahs:
                    verses.append({
                        'surah': data.get('name', 'السورة'),
                        'surah_number': surah,
                        'ayah_number': ayah.get('numberInSurah', 0),
                        'text': ayah.get('text', ''),
                        'full_reference': f"{data.get('name', 'السورة')} {ayah.get('numberInSurah', 0)}"
                    })
                
                return verses
        except Exception as e:
            logger.error(f"خطأ في جلب آيات السورة {surah}: {e}")
        
        return None
    
    def search_verses(self, query: str) -> Optional[List[Dict]]:
        """البحث عن آيات تحتوي على كلمة معينة"""
        try:
            url = f"{self.base_url}/search/{query}/{self.edition}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                results = response.json().get('data', {}).get('matches', [])
                
                verses = []
                for result in results[:10]:  # تحديد النتائج إلى 10
                    verses.append({
                        'surah': result.get('surah', {}).get('name', 'السورة'),
                        'surah_number': result.get('surah', {}).get('number', 0),
                        'ayah_number': result.get('numberInSurah', 0),
                        'text': result.get('text', ''),
                        'full_reference': f"{result.get('surah', {}).get('name', 'السورة')} {result.get('numberInSurah', 0)}"
                    })
                
                return verses
        except Exception as e:
            logger.error(f"خطأ في البحث عن '{query}': {e}")
        
        return None


class QuranBot:
    """فئة البوت الرئيسية"""
    
    def __init__(self):
        self.quran_api = QuranAPI()
        self.scheduler = BackgroundScheduler()
        self.user_preferences = {}  # تخزين تفضيلات المستخدمين
        self.load_preferences()
    
    def load_preferences(self):
        """تحميل تفضيلات المستخدمين من ملف"""
        try:
            if os.path.exists('user_preferences.json'):
                with open('user_preferences.json', 'r', encoding='utf-8') as f:
                    self.user_preferences = json.load(f)
                logger.info(f"تم تحميل تفضيلات {len(self.user_preferences)} مستخدم")
        except Exception as e:
            logger.error(f"خطأ في تحميل التفضيلات: {e}")
    
    def save_preferences(self):
        """حفظ تفضيلات المستخدمين"""
        try:
            with open('user_preferences.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطأ في حفظ التفضيلات: {e}")
    
    def format_verse_message(self, verse: Dict) -> str:
        """تنسيق رسالة الآية"""
        if not verse:
            return "عذراً، حدث خطأ في جلب الآية"
        
        message = f"""
📖 *{verse['full_reference']}*

{verse['text']}

⏰ الوقت: {datetime.now().strftime('%H:%M:%S')}
"""
        return message
    
    async def send_daily_verse(self, context: ContextTypes.DEFAULT_TYPE):
        """إرسال آية يومية إلى القناة"""
        try:
            verse = self.quran_api.get_random_verse()
            if verse:
                message = self.format_verse_message(verse)
                
                if CHANNEL_ID:
                    await context.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=message,
                        parse_mode='Markdown'
                    )
                    logger.info(f"تم إرسال الآية: {verse['full_reference']}")
                else:
                    logger.warning("لم يتم تحديد معرف القناة (CHANNEL_ID)")
        except Exception as e:
            logger.error(f"خطأ في إرسال الآية: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start"""
    user_id = str(update.effective_user.id)
    
    # تسجيل المستخدم
    if user_id not in context.bot_data.get('bot', {}).user_preferences:
        context.bot_data.get('bot', {}).user_preferences[user_id] = {
            'enabled': True,
            'joined_at': datetime.now().isoformat()
        }
        context.bot_data.get('bot', {}).save_preferences()
    
    welcome_message = """
👋 مرحباً بك في بوت آيات القرآن الكريم!

سيتم إرسال آية قصيرة من القرآن الكريم كل 15 دقيقة.

الأوامر المتاحة:
/start - عرض هذه الرسالة
/verse - احصل على آية عشوائية فوراً
/surah - اختر سورة معينة
/search - ابحث عن آيات
/pause - توقف الإرسال مؤقتاً
/resume - استئناف الإرسال
/help - عرض المساعدة
"""
    
    await update.message.reply_text(welcome_message)
    logger.info(f"مستخدم جديد: {user_id}")


async def get_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /verse - إرسال آية عشوائية فوراً"""
    try:
        bot = context.bot_data.get('bot')
        verse = bot.quran_api.get_random_verse()
        message = bot.format_verse_message(verse)
        
        await update.message.reply_text(message, parse_mode='Markdown')
        logger.info(f"تم إرسال آية عشوائية للمستخدم: {update.effective_user.id}")
    except Exception as e:
        logger.error(f"خطأ في أمر /verse: {e}")
        await update.message.reply_text("عذراً، حدث خطأ في جلب الآية")


async def pause_verses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /pause - توقف الإرسال مؤقتاً"""
    user_id = str(update.effective_user.id)
    bot = context.bot_data.get('bot')
    
    if user_id in bot.user_preferences:
        bot.user_preferences[user_id]['enabled'] = False
        bot.save_preferences()
        await update.message.reply_text("✋ تم توقيف الإرسال مؤقتاً")
        logger.info(f"توقيف الإرسال للمستخدم: {user_id}")
    else:
        await update.message.reply_text("أنت لم تكن مشتركاً في الخدمة")


async def resume_verses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /resume - استئناف الإرسال"""
    user_id = str(update.effective_user.id)
    bot = context.bot_data.get('bot')
    
    if user_id not in bot.user_preferences:
        bot.user_preferences[user_id] = {
            'enabled': True,
            'joined_at': datetime.now().isoformat()
        }
    else:
        bot.user_preferences[user_id]['enabled'] = True
    
    bot.save_preferences()
    await update.message.reply_text("▶️ تم استئناف الإرسال")
    logger.info(f"استئناف الإرسال للمستخدم: {user_id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /help"""
    help_text = """
📚 دليل الاستخدام:

*الأوامر الأساسية:*
/verse - احصل على آية عشوائية الآن
/surah - اختر سورة معينة لعرض آياتها
/search - ابحث عن آيات تحتوي على كلمة معينة

*التحكم في الإرسال:*
/pause - توقف الإرسال الدوري مؤقتاً
/resume - استئناف الإرسال الدوري

*معلومات:*
/help - عرض هذه الرسالة
/start - عرض رسالة الترحيب

ℹ️ يتم إرسال آية عشوائية كل 15 دقيقة تلقائياً
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /search"""
    if not context.args:
        await update.message.reply_text("الرجاء إدخال كلمة للبحث\nمثال: /search الرحمن")
        return
    
    try:
        query = ' '.join(context.args)
        bot = context.bot_data.get('bot')
        verses = bot.quran_api.search_verses(query)
        
        if verses:
            response = f"🔍 نتائج البحث عن '{query}':\n\n"
            for i, verse in enumerate(verses[:5], 1):
                response += f"{i}. {verse['full_reference']}\n{verse['text'][:100]}...\n\n"
            
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"لم يتم العثور على نتائج للبحث عن '{query}'")
    except Exception as e:
        logger.error(f"خطأ في أمر /search: {e}")
        await update.message.reply_text("عذراً، حدث خطأ في البحث")


async def surah_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /surah"""
    if not context.args:
        await update.message.reply_text(
            "الرجاء إدخال رقم السورة (من 1 إلى 114)\nمثال: /surah 1"
        )
        return
    
    try:
        surah_number = int(context.args[0])
        if not (1 <= surah_number <= 114):
            await update.message.reply_text("رقم السورة يجب أن يكون بين 1 و 114")
            return
        
        bot = context.bot_data.get('bot')
        verses = bot.quran_api.get_surah_verses(surah_number)
        
        if verses:
            response = f"📖 سورة {verses[0]['surah']}\n\n"
            for verse in verses[:3]:  # عرض أول 3 آيات فقط
                response += f"{verse['ayah_number']}. {verse['text']}\n\n"
            
            response += f"... (إجمالي {len(verses)} آية)"
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text("عذراً، حدث خطأ في جلب السورة")
    except ValueError:
        await update.message.reply_text("الرجاء إدخال رقم صحيح")
    except Exception as e:
        logger.error(f"خطأ في أمر /surah: {e}")
        await update.message.reply_text("عذراً، حدث خطأ")


def main():
    """الدالة الرئيسية"""
    if not TELEGRAM_TOKEN:
        logger.error("لم يتم تحديد TELEGRAM_TOKEN")
        return
    
    # إنشاء التطبيق
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إنشاء كائن البوت
    bot = QuranBot()
    app.bot_data['bot'] = bot
    
    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verse", get_verse))
    app.add_handler(CommandHandler("pause", pause_verses))
    app.add_handler(CommandHandler("resume", resume_verses))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("surah", surah_command))
    
    # إعداد جدولة الإرسال الدوري
    job_queue = app.job_queue
    
    # إرسال آية كل 15 دقيقة
    job_queue.run_repeating(
        bot.send_daily_verse,
        interval=900,  # 15 دقيقة
        first=10  # ابدأ بعد 10 ثوانٍ
    )
    
    logger.info("🤖 بدء تشغيل بوت القرآن الكريم...")
    logger.info(f"معرف القناة: {CHANNEL_ID}")
    
    # بدء البوت
    app.run_polling()


if __name__ == '__main__':
    main()
