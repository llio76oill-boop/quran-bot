# 🚀 دليل شامل: كيفية تشغيل البوت بالطريقة التي تريدها

## 📋 المحتويات
1. [فهم آلية عمل البوت](#فهم-آلية-عمل-البوت)
2. [طرق التشغيل المختلفة](#طرق-التشغيل-المختلفة)
3. [التشغيل على جهازك المحلي](#التشغيل-على-جهازك-المحلي)
4. [التشغيل على خادم دائم](#التشغيل-على-خادم-دائم)
5. [النشر على Render.com](#النشر-على-rendercom)

---

## 🎯 فهم آلية عمل البوت

### ماذا يفعل البوت؟

البوت يقوم بثلاث مهام رئيسية:

```
1️⃣ استقبال الأوامر من المستخدمين
   ↓
   /verse → آية عشوائية فوراً
   /surah 1 → آيات من سورة معينة
   /search كلمة → البحث عن آيات
   /stats → إحصائيات
   /help → قائمة المساعدة

2️⃣ إرسال الآيات دورياً إلى القناة
   ↓
   كل 15 دقيقة → آية عشوائية إلى @aya_Quraan1

3️⃣ الاتصال بـ API القرآن الكريم
   ↓
   https://api.alquran.cloud/v1
```

### البيانات المطلوبة:

```
✅ TELEGRAM_TOKEN = 8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
   (توكن البوت من BotFather)

✅ CHANNEL_ID = @aya_Quraan1
   (معرف القناة التي تنشر عليها الآيات)
```

---

## 🔧 طرق التشغيل المختلفة

### مقارنة الطرق:

| الطريقة | المكان | الاستقرار | التكلفة | الصعوبة |
|--------|--------|----------|--------|--------|
| **جهاز محلي** | حاسوبك | ⭐⭐ | مجاني | سهل |
| **Linux VPS** | خادم | ⭐⭐⭐⭐⭐ | $3-5 | متوسط |
| **Render.com** | سحابة | ⭐⭐⭐⭐⭐ | مجاني | سهل |
| **Docker** | أي مكان | ⭐⭐⭐⭐⭐ | $3-5 | متقدم |

---

## 💻 التشغيل على جهازك المحلي

### الخطوة 1: التحضيرات الأولية

```bash
# 1. تثبيت Python (إذا لم يكن مثبتاً)
# اذهب إلى: https://www.python.org/downloads/

# 2. التحقق من تثبيت Python
python --version
# يجب أن ترى: Python 3.11+

# 3. تثبيت pip (مدير الحزم)
python -m pip --version
```

### الخطوة 2: نسخ ملفات البوت

```bash
# 1. انسخ مجلد البوت إلى جهازك
# من: /home/ubuntu/quran_bot
# إلى: C:\quran_bot (Windows) أو ~/quran_bot (Mac/Linux)

# 2. افتح سطر الأوامر في مجلد البوت
cd quran_bot
```

### الخطوة 3: تثبيت المكتبات

```bash
# تثبيت جميع المكتبات المطلوبة
pip install -r requirements.txt

# أو يدوياً:
pip install python-telegram-bot requests python-dotenv apscheduler
```

### الخطوة 4: إعداد ملف البيئة

```bash
# 1. انسخ ملف .env.example إلى .env
cp .env.example .env

# 2. افتح ملف .env بمحرر نصي
# أضف:
TELEGRAM_TOKEN=8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
CHANNEL_ID=@aya_Quraan1
```

### الخطوة 5: تشغيل البوت

```bash
# شغّل البوت
python3 bot_final.py

# يجب أن ترى:
# ✅ تم تحميل معلومات 114 سورة
# ✅ تم جدولة إرسال الآيات (كل 15 دقيقة)
# ✅ البوت جاهز للعمل!
```

### الخطوة 6: اختبر البوت

```
1. افتح تطبيق تلغرام
2. ابحث عن: @aya_Quraanbot
3. أرسل: /verse
4. يجب أن تتلقى آية فوراً ✅
```

### إيقاف البوت

```bash
# اضغط: Ctrl + C
```

---

## 🖥️ التشغيل على خادم Linux دائم

### الطريقة 1: استخدام nohup (الأسهل)

```bash
# تشغيل البوت في الخلفية
cd /home/quran_bot
nohup python3 bot_final.py > bot_output.log 2>&1 &

# عرض السجلات
tail -f bot_output.log

# إيقاف البوت
pkill -f "python3 bot_final.py"
```

### الطريقة 2: استخدام Systemd (الأفضل)

```bash
# 1. إنشاء ملف الخدمة
sudo nano /etc/systemd/system/quran_bot.service

# 2. أضف المحتوى:
[Unit]
Description=Quran Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/quran_bot
ExecStart=/usr/bin/python3 /home/quran_bot/bot_final.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# 3. احفظ الملف (Ctrl + X ثم Y ثم Enter)

# 4. تفعيل الخدمة
sudo systemctl daemon-reload
sudo systemctl enable quran_bot
sudo systemctl start quran_bot

# 5. التحقق من الحالة
sudo systemctl status quran_bot

# 6. عرض السجلات
sudo journalctl -u quran_bot -f

# 7. إيقاف الخدمة
sudo systemctl stop quran_bot
```

### الطريقة 3: استخدام Docker

```bash
# 1. بناء صورة Docker
docker build -t quran_bot .

# 2. تشغيل الحاوية
docker run -d --name quran_bot quran_bot

# 3. عرض السجلات
docker logs -f quran_bot

# 4. إيقاف الحاوية
docker stop quran_bot
```

---

## ☁️ النشر على Render.com

### الخطوة 1: إعداد GitHub

```
1. اذهب إلى: https://github.com
2. سجل حساب جديد (أو سجل دخول)
3. اضغط: + (أيقونة الإضافة)
4. اختر: New repository
5. أدخل اسم: quran-bot
6. اختر: Public
7. اضغط: Create repository
```

### الخطوة 2: رفع الملفات

```
1. اذهب إلى مستودعك الجديد
2. اضغط: Add file
3. اختر: Upload files
4. اسحب هذه الملفات:
   - bot_final.py
   - requirements.txt
   - Dockerfile
   - .env.example
5. اضغط: Commit changes
```

### الخطوة 3: النشر على Render

```
1. اذهب إلى: https://render.com
2. اضغط: Sign up
3. اختر: Sign up with GitHub
4. اضغط: Dashboard
5. اضغط: New +
6. اختر: Web Service
7. اختر المستودع: quran-bot
8. اضغط: Connect
```

### الخطوة 4: التكوين

**ملء النموذج:**

```
Name: quran-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot_final.py
Plan: Free
```

**إضافة متغيرات البيئة:**

```
TELEGRAM_TOKEN = 8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
CHANNEL_ID = @aya_Quraan1
```

### الخطوة 5: بدء النشر

```
1. اضغط: Create Web Service
2. انتظر النشر (2-3 دقائق)
3. ستظهر رسالة: "Your service is live"
4. ✅ تم! البوت يعمل الآن!
```

---

## 📊 مقارنة سريعة

### للمبتدئين:
**استخدم Render.com**
- سهل جداً
- مجاني
- لا يحتاج معرفة تقنية

### للمتوسطين:
**استخدم Linux VPS + Systemd**
- أرخص على المدى الطويل
- موثوق جداً
- تحكم كامل

### للمتقدمين:
**استخدم Docker + Linux VPS**
- أفضل ممارسات
- سهل التوسع
- احترافي

---

## 🔍 استكشاف الأخطاء

### المشكلة: "ModuleNotFoundError"

**الحل:**
```bash
pip install -r requirements.txt
```

### المشكلة: "TELEGRAM_TOKEN غير محدد"

**الحل:**
```bash
# تأكد من أن ملف .env يحتوي على:
TELEGRAM_TOKEN=your_token_here
CHANNEL_ID=@your_channel
```

### المشكلة: البوت لا يرسل الآيات

**الحل:**
```bash
# 1. تحقق من أن البوت مسؤول في القناة
# 2. تأكد من أن البوت لديه صلاحية "نشر الرسائل"
# 3. عرض السجلات للأخطاء
tail -f bot_output.log
```

### المشكلة: "Unauthorized" أو "Forbidden"

**الحل:**
```
1. افتح القناة @aya_Quraan1
2. اضغط على اسم القناة
3. اختر "إدارة القناة"
4. اختر "المسؤولون"
5. أضف @aya_Quraanbot كمسؤول
6. تأكد من أن لديه صلاحية "نشر الرسائل"
```

---

## 🎯 الخلاصة

### للبدء السريع:
1. ثبت Python
2. ثبت المكتبات: `pip install -r requirements.txt`
3. أعد ملف .env
4. شغّل: `python3 bot_final.py`

### للتشغيل الدائم:
1. استخدم Render.com (الأسهل)
2. أو استخدم Linux VPS + Systemd
3. أو استخدم Docker

### للنشر على الإنترنت:
1. استخدم GitHub
2. ربطه مع Render.com
3. النشر التلقائي عند كل تحديث

---

## 📞 نصائح مهمة

✅ **افعل:**
- احفظ التوكن بأمان
- استخدم متغيرات البيئة
- راقب السجلات
- احفظ نسخ احتياطية

❌ **لا تفعل:**
- لا تضع التوكن في الكود
- لا تشارك التوكن مع أحد
- لا تترك البوت بدون مراقبة

---

**تم آخر تحديث**: 23 يناير 2026

**🚀 ابدأ الآن واستمتع بالبوت!**
