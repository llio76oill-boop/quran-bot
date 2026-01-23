# دليل التثبيت والنشر الشامل

## المحتويات
1. [المتطلبات الأساسية](#المتطلبات-الأساسية)
2. [التثبيت المحلي](#التثبيت-المحلي)
3. [الإعدادات الأمنية](#الإعدادات-الأمنية)
4. [النشر على الخادم](#النشر-على-الخادم)
5. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## المتطلبات الأساسية

### على جهازك الشخصي أو الخادم:
- **نظام التشغيل**: Linux/Mac/Windows (مع WSL)
- **Python**: الإصدار 3.10 أو أحدث
- **pip**: مدير الحزم (يأتي مع Python)
- **git**: لاستنساخ المشروع (اختياري)
- **حساب تلغرام**: للحصول على توكن البوت

### الأدوات الاختيارية للإنتاج:
- **Docker**: لتشغيل البوت في حاوية معزولة
- **systemd**: لتشغيل البوت كخدمة نظام
- **nginx**: كخادم وكيل (إذا كنت تستخدم webhooks)

---

## التثبيت المحلي

### الخطوة 1: استنساخ المشروع

```bash
# باستخدام git
git clone https://github.com/your-username/quran-telegram-bot.git
cd quran-telegram-bot

# أو بدون git
mkdir quran-telegram-bot
cd quran-telegram-bot
# ثم انسخ جميع الملفات يدويًا
```

### الخطوة 2: إنشاء بيئة افتراضية

```bash
# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية
# على Linux/Mac:
source venv/bin/activate

# على Windows:
venv\Scripts\activate
```

### الخطوة 3: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### الخطوة 4: إعداد متغيرات البيئة

```bash
# انسخ ملف المثال
cp .env.example .env

# عدّل الملف بمحرر نصي (nano, vim, VSCode, إلخ)
nano .env
```

**ملف `.env` يجب أن يحتوي على:**

```env
# توكن البوت (الحصول عليه من @BotFather)
TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE

# معرف القناة (اختياري - للإرسال إلى قناة)
# الصيغة: @channel_name أو -100123456789
CHANNEL_ID=

# معرف المستخدم الإداري (اختياري)
ADMIN_ID=

# مستوى السجلات
LOG_LEVEL=INFO
```

### الخطوة 5: تشغيل البوت

```bash
python3 quran_bot.py
```

يجب أن ترى رسالة تشير إلى بدء تشغيل البوت:
```
2026-01-13 16:15:00 - quran_bot - INFO - 🤖 بدء تشغيل بوت القرآن الكريم...
```

---

## الإعدادات الأمنية

### 1. حماية ملف `.env`

```bash
# تأكد من أن ملف .env لا يمكن قراءته من قبل الآخرين
chmod 600 .env

# أضفه إلى .gitignore لمنع رفعه إلى git
echo ".env" >> .gitignore
```

### 2. استخدام متغيرات البيئة في الإنتاج

بدلاً من استخدام ملف `.env`، استخدم متغيرات النظام:

```bash
# على Linux/Mac
export TELEGRAM_TOKEN="your_token_here"
export CHANNEL_ID="your_channel_id"

# ثم شغّل البوت
python3 quran_bot.py
```

### 3. تقييد الوصول إلى البوت

يمكنك إضافة فحص للمستخدمين الموثوقين في `quran_bot.py`:

```python
ALLOWED_USERS = [123456789, 987654321]  # معرفات المستخدمين المسموحين

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("عذراً، أنت غير مصرح باستخدام هذا البوت")
        return
    # ... باقي الكود
```

---

## النشر على الخادم

### الخيار 1: تشغيل مباشر على Linux

#### 1.1 استخدام `screen` أو `tmux`

```bash
# باستخدام screen
screen -S quran-bot
cd /path/to/quran-telegram-bot
source venv/bin/activate
python3 quran_bot.py

# اضغط Ctrl+A ثم D للخروج مع إبقاء الجلسة تعمل

# للعودة إلى الجلسة:
screen -r quran-bot
```

#### 1.2 استخدام `systemd` (الطريقة الموصى بها)

إنشاء ملف خدمة:

```bash
sudo nano /etc/systemd/system/quran-bot.service
```

أضف المحتوى التالي:

```ini
[Unit]
Description=Quran Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/quran_bot
Environment="PATH=/home/ubuntu/quran_bot/venv/bin"
ExecStart=/home/ubuntu/quran_bot/venv/bin/python3 /home/ubuntu/quran_bot/quran_bot.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

تفعيل الخدمة:

```bash
# تحديث systemd
sudo systemctl daemon-reload

# تفعيل الخدمة عند بدء النظام
sudo systemctl enable quran-bot

# بدء الخدمة
sudo systemctl start quran-bot

# التحقق من الحالة
sudo systemctl status quran-bot

# عرض السجلات
sudo journalctl -u quran-bot -f
```

### الخيار 2: استخدام Docker

#### 2.1 إنشاء ملف `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "quran_bot.py"]
```

#### 2.2 بناء وتشغيل الحاوية

```bash
# بناء الصورة
docker build -t quran-bot:latest .

# تشغيل الحاوية
docker run -d \
  --name quran-bot \
  -e TELEGRAM_TOKEN="your_token_here" \
  -e CHANNEL_ID="your_channel_id" \
  -v /path/to/logs:/app/logs \
  quran-bot:latest

# عرض السجلات
docker logs -f quran-bot
```

#### 2.3 استخدام `docker-compose`

إنشاء ملف `docker-compose.yml`:

```yaml
version: '3.8'

services:
  quran-bot:
    build: .
    container_name: quran-bot
    environment:
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
      CHANNEL_ID: ${CHANNEL_ID}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

تشغيل:

```bash
docker-compose up -d
```

---

## استكشاف الأخطاء

### المشكلة: البوت لا يستجيب

**الحل:**
1. تحقق من صحة التوكن في `.env`
2. تأكد من اتصالك بالإنترنت
3. تحقق من السجلات: `tail -f quran_bot.log`

### المشكلة: خطأ في الاتصال بـ API

**الحل:**
1. تحقق من اتصالك بالإنترنت
2. جرب الاتصال يدويًا:
   ```bash
   curl https://api.alquran.cloud/v1/surah
   ```
3. تحقق من حالة الخادم

### المشكلة: الآيات لا تُرسل إلى القناة

**الحل:**
1. تأكد من صحة معرف القناة في `.env`
2. تأكد من أن البوت لديه صلاحيات الإرسال في القناة
3. تحقق من السجلات للأخطاء

### المشكلة: استهلاك ذاكرة عالي

**الحل:**
1. تحقق من عدد المستخدمين النشطين
2. أعد تشغيل البوت بانتظام (مثلاً يوميًا)
3. استخدم `memory_profiler` لتتبع الاستهلاك

---

## الصيانة والمراقبة

### مراقبة الأداء

```bash
# عرض استهلاك الموارد
ps aux | grep quran_bot

# عرض السجلات الأخيرة
tail -100 quran_bot.log

# عد الأخطاء
grep "ERROR" quran_bot.log | wc -l
```

### النسخ الاحتياطي

```bash
# نسخ احتياطية للتفضيلات والسجلات
tar -czf quran_bot_backup_$(date +%Y%m%d).tar.gz \
  user_preferences.json \
  quran_bot.log

# نقل النسخة الاحتياطية
scp quran_bot_backup_*.tar.gz user@backup-server:/backups/
```

---

## الدعم والمساعدة

إذا واجهت مشاكل:

1. تحقق من [README.md](README.md)
2. ابحث عن المشكلة في [Issues](https://github.com/your-username/quran-telegram-bot/issues)
3. افتح `Issue` جديد مع وصف المشكلة والسجلات

---

**تم آخر تحديث**: 13 يناير 2026
