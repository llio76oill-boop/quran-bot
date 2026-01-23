#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبارات الوحدة لبوت القرآن الكريم
Unit tests for the Quran Bot
"""

import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# استيراد المكتبات المطلوبة للاختبار
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# استيراد الوحدات المراد اختبارها
from quran_bot import QuranAPI, QuranBot, start, get_verse, pause_verses, resume_verses, help_command, search_command, surah_command
from advanced_features import AdvancedCommands, UserPreferences, VerseFavorites, StatisticsTracker
from error_handling import RetryStrategy, CircuitBreaker, RateLimiter

class TestQuranAPI(unittest.TestCase):
    """اختبارات فئة QuranAPI"""

    @patch("quran_bot.requests.Session")
    def test_get_random_verse_success(self, mock_session):
        """اختبار الحصول على آية عشوائية بنجاح"""
        # إعداد الاستجابات الوهمية
        mock_surah_list_response = MagicMock()
        mock_surah_list_response.status_code = 200
        mock_surah_list_response.json.return_value = {
            "data": [
                {"number": 1, "numberOfAyahs": 7, "name": "الفاتحة"},
                {"number": 2, "numberOfAyahs": 286, "name": "البقرة"},
            ]
        }

        mock_verse_response = MagicMock()
        mock_verse_response.status_code = 200
        mock_verse_response.json.return_value = {
            "data": {
                "surah": {"name": "الفاتحة", "number": 1},
                "numberInSurah": 1,
                "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            }
        }

        # تم استهلاك الاستجابة الأولى في المُنشئ
        mock_session.return_value.get.side_effect = [
            mock_surah_list_response, 
            mock_verse_response
        ]

        # تشغيل الاختبار
        quran_api = QuranAPI()
        # Manually set surah_info to bypass the constructor call issue in testing
        quran_api.surah_info = mock_surah_list_response.json.return_value['data']
        verse = quran_api.get_random_verse()

        # التأكيدات
        self.assertIsNotNone(verse)
        self.assertEqual(verse["surah"], "الفاتحة")
        self.assertEqual(verse["text"], "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")

    @patch("quran_bot.requests.Session")
    def test_get_verse_failure(self, mock_session):
        """اختبار فشل الحصول على آية"""
        mock_session.return_value.get.return_value.status_code = 500

        quran_api = QuranAPI()
        verse = quran_api.get_verse(1, 1)

        self.assertIsNone(verse)

class TestBotCommands(unittest.TestCase):
    """اختبارات أوامر البوت"""

    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.bot = QuranBot()
        self.update = AsyncMock(spec=Update)
        self.context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
        self.context.bot_data = {"bot": self.bot}
        self.update.effective_user = MagicMock()
        self.update.effective_user.id = 12345
        self.update.message = AsyncMock()

    @patch("quran_bot.QuranBot.format_verse_message", return_value="رسالة الآية")
    def test_get_verse_command(self, mock_format):
        """اختبار أمر /verse"""
        async def run_test():
            with patch.object(self.bot.quran_api, "get_random_verse", return_value={"full_reference": "الفاتحة 1"}):
                await get_verse(self.update, self.context)
                self.update.message.reply_text.assert_called_once_with("رسالة الآية", parse_mode="Markdown")
        
        asyncio.run(run_test())

    def test_start_command(self):
        """اختبار أمر /start"""
        async def run_test():
            await start(self.update, self.context)
            self.update.message.reply_text.assert_called_once()
            self.assertIn(str(self.update.effective_user.id), self.bot.user_preferences)
        
        asyncio.run(run_test())

    def test_pause_resume_commands(self):
        """اختبار أوامر /pause و /resume"""
        async def run_test():
            # Ensure user is in preferences
            self.bot.user_preferences[str(self.update.effective_user.id)] = {"enabled": True}
            
            # اختبار التوقيف
            await pause_verses(self.update, self.context)
            self.update.message.reply_text.assert_called_with("✋ تم توقيف الإرسال مؤقتاً")
            self.assertFalse(self.bot.user_preferences[str(self.update.effective_user.id)]["enabled"])

            # اختبار الاستئناف
            await resume_verses(self.update, self.context)
            self.update.message.reply_text.assert_called_with("▶️ تم استئناف الإرسال")
            self.assertTrue(self.bot.user_preferences[str(self.update.effective_user.id)]["enabled"])

        asyncio.run(run_test())

class TestAdvancedFeatures(unittest.TestCase):
    """اختبارات الميزات المتقدمة"""

    def test_surah_keyboard_creation(self):
        """اختبار إنشاء لوحة مفاتيح السور"""
        keyboard = AdvancedCommands.create_surah_keyboard()
        self.assertIsInstance(keyboard, InlineKeyboardMarkup)
        total_buttons = sum(len(row) for row in keyboard.inline_keyboard)
        self.assertEqual(total_buttons, 114)

    def test_user_preferences(self):
        """اختبار تفضيلات المستخدم"""
        prefs = UserPreferences()
        prefs.set_preference("user1", "notifications", False)
        self.assertFalse(prefs.get_preference("user1", "notifications"))
        prefs.toggle_preference("user1", "notifications")
        self.assertTrue(prefs.get_preference("user1", "notifications"))

class TestErrorHandling(unittest.TestCase):
    """اختبارات معالجة الأخطاء"""

    def test_circuit_breaker(self):
        """اختبار نمط Circuit Breaker"""
        cb = CircuitBreaker(failure_threshold=2, timeout=10)
        self.assertTrue(cb.can_execute())
        cb.record_failure()
        self.assertTrue(cb.can_execute())
        cb.record_failure() # الآن يجب أن يفتح
        self.assertFalse(cb.can_execute())

    def test_rate_limiter(self):
        """اختبار محدد المعدل"""
        limiter = RateLimiter(max_requests=2, time_window=10)
        self.assertTrue(limiter.is_allowed())
        self.assertTrue(limiter.is_allowed())
        self.assertFalse(limiter.is_allowed())

if __name__ == "__main__":
    unittest.main()
