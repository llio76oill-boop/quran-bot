# 🚀 دليل البدء السريع - تشغيل البوت في 5 دقائق

## ⚠️ الخطوة الأولى والأهم: الحصول على توكن البوت

هذه هي الخطوة الأساسية التي يجب أن تفعلها أولاً!

---

## 📱 الخطوة 1: إنشاء بوت جديد على تلغرام

### 1.1 افتح تطبيق تلغرام

```
تطبيق Telegram
    ↓
ابحث عن: @BotFather
    ↓
اضغط: Start
```

### 1.2 أرسل الأمر `/newbot`

```
أنت:
/newbot

BotFather:
Alright! Let's create a new bot. How are we going to call it?
Please choose a name for your bot.
```

### 1.3 اختر اسم البوت

```
أنت:
Quran Verses Bot

BotFather:
Good. Now let's choose a username for your bot. 
It must end in `bot`. For example, TetrisBot or tetris_bot.
```

### 1.4 اختر معرف البوت (يجب أن ينتهي بـ bot)

```
أنت:
quran_verses_bot

BotFather:
Done! Congratulations on your new bot. 
You will find it at t.me/quran_verses_bot. 
You can now add a description, about section and profile picture for your bot, 
see /help for a list of commands.

Here's your token:
1234567890:ABCDefGHIjklmnoPQRstuvWXYZ1234567890

Use this token to access the HTTP API:
https://api.telegram.org/bot1234567890:ABCDefGHIjklmnoPQRstuvWXYZ1234567890/getMe

Keep your token secure and store it safely!
```

### ✅ تم! لديك الآن التوكن

**التوكن هو:**
```
1234567890:ABCDefGHIjklmnoPQRstuvWXYZ1234567890
```

⚠️ **احفظ هذا التوكن في مكان آمن - لا تشاركه مع أحد!**

---

## 💻 الخطوة 2: إعداد البوت على جهازك

### 2.1 انسخ ملف متغيرات البيئة

```bash
cd /home/ubuntu/quran_bot
cp .env.example .env
```

### 2.2 افتح ملف `.env` بمحرر نصي

```bash
nano .env
```

### 2.3 أضف التوكن الذي حصلت عليه

**الملف قبل التعديل:**
```env
TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE
CHANNEL_ID=
```

**الملف بعد التعديل:**
```env
TELEGRAM_TOKEN=1234567890:ABCDefGHIjklmnoPQRstuvWXYZ1234567890
CHANNEL_ID=
```

### 2.4 احفظ الملف

```
اضغط: Ctrl + X
اضغط: Y (لتأكيد الحفظ)
اضغط: Enter
```

---

## 📦 الخطوة 3: تثبيت المكتبات المطلوبة

```bash
cd /home/ubuntu/quran_bot
pip install -r requirements.txt
```

**ستظهر رسائل مثل:**
```
Collecting python-telegram-bot==21.1
  Downloading python_telegram_bot-21.1-py3-none-any.whl (1.5 MB)
Installing collected packages: ...
Successfully installed ...
```

---

## ▶️ الخطوة 4: تشغيل البوت

```bash
python3 quran_bot.py
```

**إذا نجح التشغيل، ستظهر رسائل مثل:**
```
2026-01-13 16:15:00,123 - quran_bot - INFO - 🤖 بدء تشغيل بوت القرآن الكريم...
2026-01-13 16:15:00,456 - quran_bot - INFO - تم تحميل معلومات 114 سورة
2026-01-13 16:15:00,789 - quran_bot - INFO - تم تحميل تفضيلات 0 مستخدم
2026-01-13 16:15:01,012 - quran_bot - INFO - ✅ البوت جاهز للعمل!
```

---

## 🧪 الخطوة 5: اختبار البوت

### 5.1 افتح تطبيق تلغرام

### 5.2 ابحث عن البوت الذي أنشأته

```
ابحث عن: @quran_verses_bot
(أو اسم البوت الذي اخترته)
```

### 5.3 اضغط على البوت وأرسل الأوامر التالية

```
أرسل: /start

البوت يرد:
👋 مرحباً بك في بوت آيات القرآن الكريم!
سأرسل لك آية قصيرة كل 15 دقيقة...
```

### 5.4 جرب أوامر أخرى

```
أرسل: /verse

البوت يرد:
📖 الفاتحة - الآية 1
بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
```

```
أرسل: /help

البوت يرد:
📚 قائمة الأوامر المتاحة:
/start - بدء البوت
/verse - آية عشوائية
/surah 1 - آيات من سورة معينة
/search كلمة - البحث عن آيات
/pause - إيقاف الإرسال
/resume - استئناف الإرسال
/help - هذه القائمة
```

---

## ✅ تم! البوت يعمل بنجاح

**الآن البوت:**
- ✅ يستقبل الأوامر منك
- ✅ يرسل آيات عشوائية كل 15 دقيقة
- ✅ يرد على جميع الأسئلة

---

## 🛑 إيقاف البوت

إذا أردت إيقاف البوت:

```bash
اضغط: Ctrl + C
```

**ستظهر رسالة:**
```
^C
2026-01-13 16:20:00,000 - quran_bot - INFO - 🛑 تم إيقاف البوت
```

---

## 🔄 إعادة تشغيل البوت

```bash
python3 quran_bot.py
```

---

## ⚠️ حل المشاكل الشائعة

### المشكلة 1: "ModuleNotFoundError: No module named 'telegram'"

**الحل:**
```bash
pip install -r requirements.txt
```

---

### المشكلة 2: "KeyError: 'TELEGRAM_TOKEN'"

**الحل:**
- تأكد من أن ملف `.env` موجود
- تأكد من أنك أضفت التوكن بشكل صحيح
- أعد تشغيل البوت

---

### المشكلة 3: البوت لا يرد على الأوامر

**الحل:**
1. تأكد من أن البوت يعمل (يجب أن تظهر رسائل في الطرفية)
2. تأكد من التوكن صحيح
3. جرب أمر `/start` مرة أخرى

---

### المشكلة 4: "Connection refused" أو خطأ في الاتصال

**الحل:**
- تأكد من اتصالك بالإنترنت
- جرب إعادة تشغيل البوت

---

## 📊 مثال على جلسة عمل كاملة

```bash
# 1. انتقل إلى مجلد المشروع
cd /home/ubuntu/quran_bot

# 2. تأكد من وجود ملف .env
ls -la .env

# 3. شغّل البوت
python3 quran_bot.py

# الآن البوت يعمل! 🎉
# افتح تلغرام وجرب الأوامر

# لإيقاف البوت: Ctrl + C
```

---

## 🎯 الخطوات التالية

بعد تشغيل البوت بنجاح:

1. **اختبر جميع الأوامر** - تأكد من أن كل شيء يعمل
2. **اقرأ التوثيق** - اطلع على README.md و HOW_IT_WORKS.md
3. **شغّل البوت 24/7** - اتبع INSTALLATION_GUIDE.md

---

## 📞 تحتاج إلى مساعدة؟

إذا واجهت مشكلة:

1. اقرأ قسم "حل المشاكل الشائعة" أعلاه
2. اطلع على INSTALLATION_GUIDE.md
3. تحقق من السجلات في quran_bot.log

---

**تم آخر تحديث**: 13 يناير 2026

**🎉 مبروك! أنت الآن جاهز لتشغيل بوت القرآن الكريم!**
