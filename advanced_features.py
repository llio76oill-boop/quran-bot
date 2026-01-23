#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ميزات متقدمة للبوت
Advanced features for Quran Bot
"""

import logging
from typing import Optional, Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# الأوامر المتقدمة
SURAH_NAMES = {
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
    76: "الإنسان", 77: "المرسلات", 78: "النبأ", 79: "النازعات", 80: "عبس",
    81: "التكوير", 82: "الإنفطار", 83: "المطففين", 84: "الانشقاق", 85: "البروج",
    86: "الطارق", 87: "الأعلى", 88: "الغاشية", 89: "الفجر", 90: "البلد",
    91: "الشمس", 92: "الليل", 93: "الضحى", 94: "الشرح", 95: "التين",
    96: "العلق", 97: "القدر", 98: "البينة", 99: "الزلزلة", 100: "العاديات",
    101: "القارعة", 102: "التكاثر", 103: "العصر", 104: "الهمزة", 105: "الفيل",
    106: "قريش", 107: "الماعون", 108: "الكوثر", 109: "الكافرون", 110: "النصر",
    111: "المسد", 112: "الإخلاص", 113: "الفلق", 114: "الناس"
}


class UserPreferences:
    """إدارة تفضيلات المستخدمين"""
    
    def __init__(self):
        self.preferences = {}
    
    def get_preference(self, user_id: str, key: str, default=None):
        """الحصول على تفضيل معين"""
        if user_id not in self.preferences:
            self.preferences[user_id] = {}
        return self.preferences[user_id].get(key, default)
    
    def set_preference(self, user_id: str, key: str, value):
        """تعيين تفضيل معين"""
        if user_id not in self.preferences:
            self.preferences[user_id] = {}
        self.preferences[user_id][key] = value
    
    def toggle_preference(self, user_id: str, key: str, default=False):
        """تبديل تفضيل معين"""
        current = self.get_preference(user_id, key, default)
        self.set_preference(user_id, key, not current)
        return not current


class AdvancedCommands:
    """الأوامر المتقدمة"""
    
    @staticmethod
    def create_surah_keyboard() -> InlineKeyboardMarkup:
        """إنشاء لوحة مفاتيح لاختيار السور"""
        buttons = []
        
        # تقسيم السور إلى صفوف (3 أزرار في كل صف)
        for i in range(1, 115, 3):
            row = []
            for j in range(3):
                surah_num = i + j
                if surah_num <= 114:
                    surah_name = SURAH_NAMES.get(surah_num, f"السورة {surah_num}")
                    row.append(
                        InlineKeyboardButton(
                            f"{surah_num}. {surah_name[:8]}",
                            callback_data=f"surah_{surah_num}"
                        )
                    )
            buttons.append(row)
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def create_settings_keyboard(user_id: str, prefs: UserPreferences) -> InlineKeyboardMarkup:
        """إنشاء لوحة مفاتيح الإعدادات"""
        notifications_enabled = prefs.get_preference(user_id, 'notifications', True)
        daily_verse_enabled = prefs.get_preference(user_id, 'daily_verse', True)
        
        buttons = [
            [
                InlineKeyboardButton(
                    f"🔔 الإشعارات: {'✅' if notifications_enabled else '❌'}",
                    callback_data="toggle_notifications"
                )
            ],
            [
                InlineKeyboardButton(
                    f"📖 الآيات اليومية: {'✅' if daily_verse_enabled else '❌'}",
                    callback_data="toggle_daily_verse"
                )
            ],
            [
                InlineKeyboardButton("🔙 العودة", callback_data="back_to_menu")
            ]
        ]
        
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def create_main_menu_keyboard() -> InlineKeyboardMarkup:
        """إنشاء لوحة مفاتيح القائمة الرئيسية"""
        buttons = [
            [
                InlineKeyboardButton("📖 آية عشوائية", callback_data="random_verse"),
                InlineKeyboardButton("🔍 بحث", callback_data="search")
            ],
            [
                InlineKeyboardButton("📚 اختر سورة", callback_data="choose_surah"),
                InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")
            ],
            [
                InlineKeyboardButton("ℹ️ معلومات", callback_data="info")
            ]
        ]
        
        return InlineKeyboardMarkup(buttons)


class VerseFavorites:
    """إدارة الآيات المفضلة"""
    
    def __init__(self):
        self.favorites = {}
    
    def add_favorite(self, user_id: str, verse: Dict):
        """إضافة آية إلى المفضلة"""
        if user_id not in self.favorites:
            self.favorites[user_id] = []
        
        # تجنب التكرار
        if verse not in self.favorites[user_id]:
            self.favorites[user_id].append(verse)
            return True
        return False
    
    def remove_favorite(self, user_id: str, verse_ref: str):
        """إزالة آية من المفضلة"""
        if user_id in self.favorites:
            self.favorites[user_id] = [
                v for v in self.favorites[user_id]
                if v.get('full_reference') != verse_ref
            ]
            return True
        return False
    
    def get_favorites(self, user_id: str) -> List[Dict]:
        """الحصول على المفضلة"""
        return self.favorites.get(user_id, [])
    
    def is_favorite(self, user_id: str, verse_ref: str) -> bool:
        """التحقق من كون الآية مفضلة"""
        if user_id not in self.favorites:
            return False
        return any(
            v.get('full_reference') == verse_ref
            for v in self.favorites[user_id]
        )


class ReminderScheduler:
    """جدولة التذكيرات الشخصية"""
    
    def __init__(self):
        self.reminders = {}
    
    def set_reminder(self, user_id: str, time: str, enabled: bool = True):
        """تعيين تذكير شخصي"""
        if user_id not in self.reminders:
            self.reminders[user_id] = []
        
        reminder = {
            'time': time,
            'enabled': enabled
        }
        
        self.reminders[user_id].append(reminder)
        return True
    
    def get_reminders(self, user_id: str) -> List[Dict]:
        """الحصول على التذكيرات"""
        return self.reminders.get(user_id, [])
    
    def remove_reminder(self, user_id: str, time: str):
        """إزالة تذكير"""
        if user_id in self.reminders:
            self.reminders[user_id] = [
                r for r in self.reminders[user_id]
                if r['time'] != time
            ]
            return True
        return False


class StatisticsTracker:
    """تتبع إحصائيات الاستخدام"""
    
    def __init__(self):
        self.stats = {}
    
    def track_verse_view(self, user_id: str):
        """تتبع عرض آية"""
        if user_id not in self.stats:
            self.stats[user_id] = {
                'verses_viewed': 0,
                'searches': 0,
                'surahs_read': 0,
                'favorites_added': 0
            }
        
        self.stats[user_id]['verses_viewed'] += 1
    
    def track_search(self, user_id: str):
        """تتبع البحث"""
        if user_id not in self.stats:
            self.stats[user_id] = {
                'verses_viewed': 0,
                'searches': 0,
                'surahs_read': 0,
                'favorites_added': 0
            }
        
        self.stats[user_id]['searches'] += 1
    
    def get_stats(self, user_id: str) -> Dict:
        """الحصول على الإحصائيات"""
        return self.stats.get(user_id, {
            'verses_viewed': 0,
            'searches': 0,
            'surahs_read': 0,
            'favorites_added': 0
        })
    
    def get_user_stats_message(self, user_id: str) -> str:
        """الحصول على رسالة الإحصائيات"""
        stats = self.get_stats(user_id)
        
        message = f"""
📊 إحصائياتك:

📖 عدد الآيات المشاهدة: {stats['verses_viewed']}
🔍 عدد عمليات البحث: {stats['searches']}
📚 عدد السور المقروءة: {stats['surahs_read']}
❤️ الآيات المفضلة: {stats['favorites_added']}
"""
        return message


# مثال على الاستخدام
if __name__ == "__main__":
    # اختبار الميزات
    prefs = UserPreferences()
    prefs.set_preference("123", "notifications", True)
    print(prefs.get_preference("123", "notifications"))
    
    # اختبار الإحصائيات
    tracker = StatisticsTracker()
    tracker.track_verse_view("123")
    tracker.track_search("123")
    print(tracker.get_user_stats_message("123"))
