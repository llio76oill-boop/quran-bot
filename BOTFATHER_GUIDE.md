# 📱 دليل مصور: الحصول على توكن البوت من BotFather

## الخطوة 1: فتح تطبيق تلغرام

```
┌─────────────────────────────────┐
│  تطبيق Telegram                │
│                                 │
│  🔍 Search                      │
│  📞 Contacts                    │
│  💬 Messages                    │
│  ⚙️ Settings                    │
└─────────────────────────────────┘
```

---

## الخطوة 2: البحث عن BotFather

```
اضغط على: 🔍 Search

اكتب: @BotFather

ستظهر النتيجة:
┌─────────────────────────────────┐
│ BotFather                       │
│ @BotFather                      │
│ Telegram Bot API                │
│ 9.9M members                    │
└─────────────────────────────────┘
```

---

## الخطوة 3: فتح محادثة مع BotFather

```
اضغط على: BotFather

ستظهر الرسالة:
┌─────────────────────────────────┐
│ BotFather                       │
│ @BotFather                      │
│                                 │
│ I am a bot to create bots.      │
│ If you want to learn how to     │
│ create bots, check out the      │
│ documentation.                  │
│                                 │
│ /newbot - create a new bot      │
│ /mybots - edit your bots        │
│ /mygames - edit your games      │
│ ...                             │
└─────────────────────────────────┘
```

---

## الخطوة 4: إنشاء بوت جديد

```
اكتب في حقل الرسالة: /newbot

اضغط: Send ➤

BotFather يرد:
┌─────────────────────────────────┐
│ Alright! Let's create a new bot.│
│ How are we going to call it?    │
│ Please choose a name for your   │
│ bot.                            │
│                                 │
│ (اكتب اسم البوت)               │
└─────────────────────────────────┘
```

---

## الخطوة 5: اختيار اسم البوت

```
اكتب: Quran Verses Bot

اضغط: Send ➤

BotFather يرد:
┌─────────────────────────────────┐
│ Good. Now let's choose a        │
│ username for your bot.          │
│ It must end in `bot`.           │
│ For example, TetrisBot or       │
│ tetris_bot.                     │
│                                 │
│ (اكتب معرف البوت)              │
└─────────────────────────────────┘
```

---

## الخطوة 6: اختيار معرف البوت

```
اكتب: quran_verses_bot

اضغط: Send ➤

BotFather يرد:
┌─────────────────────────────────┐
│ Done! Congratulations on your   │
│ new bot. You will find it at    │
│ t.me/quran_verses_bot.          │
│                                 │
│ You can now add a description,  │
│ about section and profile       │
│ picture for your bot, see /help │
│ for a list of commands.         │
│                                 │
│ Here's your token:              │
│                                 │
│ 1234567890:ABCDefGHIjklmno...  │
│ PQRstuvWXYZ1234567890          │
│                                 │
│ Use this token to access the    │
│ HTTP API:                       │
│ https://api.telegram.org/bot... │
│                                 │
│ Keep your token secure and      │
│ store it safely!                │
└─────────────────────────────────┘
```

---

## ✅ تم! لديك الآن التوكن

```
التوكن:
1234567890:ABCDefGHIjklmnoPQRstuvWXYZ1234567890

⚠️ احفظ هذا التوكن في مكان آمن!
```

---

## 📋 ملخص الخطوات

| الخطوة | الإجراء | المدخل |
|--------|--------|--------|
| 1 | افتح تلغرام | - |
| 2 | ابحث عن | @BotFather |
| 3 | افتح المحادثة | - |
| 4 | أرسل الأمر | /newbot |
| 5 | اختر اسم البوت | Quran Verses Bot |
| 6 | اختر معرف البوت | quran_verses_bot |
| 7 | احفظ التوكن | ✅ |

---

## 🔐 نصائح الأمان

### ✅ افعل:
- ✅ احفظ التوكن في ملف `.env`
- ✅ أضف `.env` إلى `.gitignore`
- ✅ لا تشارك التوكن مع أحد
- ✅ استخدم متغيرات البيئة في الإنتاج

### ❌ لا تفعل:
- ❌ لا تضع التوكن في الكود مباشرة
- ❌ لا تشارك التوكن في الإنترنت
- ❌ لا تحفظ التوكن في ملفات عادية
- ❌ لا تنسخ التوكن في الرسائل

---

## 🔄 إذا فقدت التوكن

إذا نسيت التوكن أو تسرب:

```
1. افتح تلغرام
2. ابحث عن: @BotFather
3. أرسل: /mybots
4. اختر البوت الخاص بك
5. اختر: API Token
6. اختر: Regenerate token
7. احصل على التوكن الجديد
```

---

## ✨ الآن أنت جاهز!

بعد الحصول على التوكن:

1. انسخ الملف `.env.example` إلى `.env`
2. أضف التوكن في الملف
3. شغّل البوت: `python3 quran_bot.py`
4. اختبر البوت على تلغرام

---

**تم آخر تحديث**: 13 يناير 2026
