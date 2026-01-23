# 🚀 دليل شامل: نشر البوت على خادم دائم (24/7)

## 📋 المحتويات
1. [نظرة عامة على الخيارات](#نظرة-عامة-على-الخيارات)
2. [الطريقة 1: خادم Linux (VPS)](#الطريقة-1-خادم-linux-vps)
3. [الطريقة 2: خدمات استضافة مجانية](#الطريقة-2-خدمات-استضافة-مجانية)
4. [الطريقة 3: Docker](#الطريقة-3-docker)
5. [المراقبة والصيانة](#المراقبة-والصيانة)

---

## 🎯 نظرة عامة على الخيارات

### مقارنة الطرق المختلفة:

| الطريقة | التكلفة | الصعوبة | الاستقرار | الأداء |
|--------|--------|--------|----------|--------|
| **Linux VPS** | 3-5 دولار/شهر | متوسط | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **خدمات مجانية** | مجاني | سهل | ⭐⭐⭐ | ⭐⭐⭐ |
| **Docker** | 3-5 دولار/شهر | متقدم | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Heroku** | مجاني/مدفوع | سهل | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🖥️ الطريقة 1: خادم Linux (VPS)

### الخطوة 1: اختر مزود الخدمة

**خيارات موصى بها:**
- **DigitalOcean** - $4/شهر (موصى به جداً)
- **Linode** - $5/شهر
- **Vultr** - $2.5/شهر
- **AWS** - مجاني للسنة الأولى
- **Google Cloud** - مجاني للسنة الأولى

### الخطوة 2: إنشاء خادم جديد

**مواصفات موصى بها:**
- **نظام التشغيل**: Ubuntu 22.04 LTS
- **الذاكرة**: 512 MB (كافية)
- **المعالج**: 1 vCPU (كافي)
- **التخزين**: 10 GB (كافي)

### الخطوة 3: الاتصال بالخادم

```bash
# استخدم SSH للاتصال
ssh root@YOUR_SERVER_IP

# مثال:
ssh root@192.168.1.100
```

### الخطوة 4: تثبيت البرامج المطلوبة

```bash
# تحديث النظام
sudo apt update
sudo apt upgrade -y

# تثبيت Python
sudo apt install -y python3 python3-pip

# تثبيت Git (اختياري)
sudo apt install -y git

# تثبيت Nano (محرر نصي)
sudo apt install -y nano
```

### الخطوة 5: نسخ ملفات البوت

#### الطريقة أ: استخدام Git (إذا كان لديك مستودع)

```bash
# استنساخ المستودع
git clone https://github.com/your-username/quran-bot.git
cd quran-bot
```

#### الطريقة ب: نسخ يدوي

```bash
# إنشاء مجلد للبوت
mkdir -p /home/quran_bot
cd /home/quran_bot

# انسخ ملفات البوت من جهازك المحلي
# استخدم SCP أو FTP أو انسخ يدوياً
```

### الخطوة 6: تثبيت المتطلبات

```bash
cd /home/quran_bot

# تثبيت المكتبات
pip3 install -r requirements.txt

# أو بشكل مباشر:
pip3 install python-telegram-bot requests python-dotenv apscheduler
```

### الخطوة 7: إعداد ملف البيئة

```bash
# إنشاء ملف .env
nano .env

# أضف:
TELEGRAM_TOKEN=8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
CHANNEL_ID=@aya_Quraan1
```

### الخطوة 8: اختبر البوت

```bash
# شغّل البوت للاختبار
python3 bot_final.py

# يجب أن ترى:
# ✅ البوت جاهز للعمل!
```

### الخطوة 9: تشغيل البوت في الخلفية

#### الطريقة أ: استخدام Screen (الأسهل)

```bash
# تثبيت Screen
sudo apt install -y screen

# إنشاء جلسة جديدة
screen -S quran_bot

# شغّل البوت
python3 bot_final.py

# اضغط: Ctrl + A ثم D (للخروج دون إيقاف البوت)
```

**للعودة إلى البوت:**
```bash
screen -r quran_bot
```

**لعرض جميع الجلسات:**
```bash
screen -ls
```

#### الطريقة ب: استخدام Systemd (الأفضل)

```bash
# إنشاء ملف خدمة
sudo nano /etc/systemd/system/quran_bot.service
```

**أضف المحتوى التالي:**
```ini
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
```

**احفظ الملف:**
```
Ctrl + X
Y
Enter
```

**تفعيل الخدمة:**
```bash
# تحديث الخدمات
sudo systemctl daemon-reload

# تفعيل الخدمة
sudo systemctl enable quran_bot

# بدء الخدمة
sudo systemctl start quran_bot

# التحقق من الحالة
sudo systemctl status quran_bot
```

**أوامر مفيدة:**
```bash
# إيقاف البوت
sudo systemctl stop quran_bot

# إعادة تشغيل البوت
sudo systemctl restart quran_bot

# عرض السجلات
sudo journalctl -u quran_bot -f

# عرض آخر 50 سطر
sudo journalctl -u quran_bot -n 50
```

---

## 🆓 الطريقة 2: خدمات استضافة مجانية

### خيار 1: Replit

**المميزات:**
- ✅ مجاني تماماً
- ✅ سهل جداً
- ✅ لا يحتاج خادم

**الخطوات:**

1. **اذهب إلى**: https://replit.com
2. **سجل حساب جديد**
3. **اضغط**: Create
4. **اختر**: Python
5. **انسخ الملفات**:
   - `bot_final.py`
   - `requirements.txt`
   - `.env`

6. **شغّل البوت**:
   ```bash
   python3 bot_final.py
   ```

7. **للعمل 24/7**: استخدم خدمة UptimeRobot المجانية

### خيار 2: PythonAnywhere

**المميزات:**
- ✅ مجاني
- ✅ سهل
- ✅ دعم جيد

**الخطوات:**

1. **اذهب إلى**: https://www.pythonanywhere.com
2. **سجل حساب جديد**
3. **اضغط**: Upload a file
4. **انسخ ملفات البوت**
5. **فتح Bash Console**
6. **ثبت المتطلبات**:
   ```bash
   pip3 install -r requirements.txt
   ```

7. **شغّل البوت**:
   ```bash
   python3 bot_final.py
   ```

### خيار 3: Heroku (مدفوع الآن)

**ملاحظة**: Heroku توقفت عن تقديم خدمات مجانية

---

## 🐳 الطريقة 3: Docker

### الخطوة 1: تثبيت Docker

```bash
# على Ubuntu/Debian
sudo apt install -y docker.io

# على CentOS/RHEL
sudo yum install -y docker

# بدء خدمة Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### الخطوة 2: إنشاء Dockerfile

```bash
nano Dockerfile
```

**أضف المحتوى:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# نسخ الملفات
COPY requirements.txt .
COPY bot_final.py .
COPY .env .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل البوت
CMD ["python3", "bot_final.py"]
```

### الخطوة 3: بناء صورة Docker

```bash
# بناء الصورة
docker build -t quran_bot:latest .

# التحقق من الصورة
docker images
```

### الخطوة 4: تشغيل الحاوية

```bash
# تشغيل الحاوية
docker run -d --name quran_bot quran_bot:latest

# التحقق من الحاوية
docker ps

# عرض السجلات
docker logs quran_bot

# متابعة السجلات
docker logs -f quran_bot
```

### الخطوة 5: إدارة الحاوية

```bash
# إيقاف الحاوية
docker stop quran_bot

# إعادة تشغيل الحاوية
docker restart quran_bot

# حذف الحاوية
docker rm quran_bot

# حذف الصورة
docker rmi quran_bot:latest
```

### استخدام Docker Compose (اختياري)

```bash
nano docker-compose.yml
```

**أضف:**
```yaml
version: '3'
services:
  quran_bot:
    build: .
    container_name: quran_bot
    restart: always
    environment:
      TELEGRAM_TOKEN: 8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
      CHANNEL_ID: @aya_Quraan1
```

**التشغيل:**
```bash
docker-compose up -d
```

---

## 📊 المراقبة والصيانة

### 1. مراقبة البوت

#### استخدام UptimeRobot (مجاني)

```
1. اذهب إلى: https://uptimerobot.com
2. سجل حساب جديد
3. اضغط: Add Monitor
4. اختر: HTTP(s)
5. أضف رابط الخادم
6. سيراقب البوت ويخبرك إذا انقطع
```

#### مراقبة يدوية

```bash
# التحقق من حالة الخدمة
sudo systemctl status quran_bot

# عرض استخدام الموارد
top

# عرض استخدام الذاكرة
free -h

# عرض استخدام القرص
df -h
```

### 2. النسخ الاحتياطية

```bash
# نسخ احتياطية من ملفات البوت
tar -czf quran_bot_backup.tar.gz /home/quran_bot

# نسخ احتياطية من السجلات
cp quran_bot.log quran_bot_backup.log
```

### 3. التحديثات

```bash
# تحديث المكتبات
pip3 install --upgrade python-telegram-bot

# تحديث النظام
sudo apt update && sudo apt upgrade -y

# إعادة تشغيل البوت
sudo systemctl restart quran_bot
```

### 4. استكشاف الأخطاء

```bash
# عرض السجلات
tail -f quran_bot.log

# البحث عن أخطاء
grep "❌" quran_bot.log

# عرض آخر 100 سطر
tail -100 quran_bot.log

# عرض السجلات من تاريخ معين
journalctl -u quran_bot --since "2024-01-13"
```

---

## 📈 أفضل الممارسات

### ✅ افعل:
- ✅ استخدم Systemd للتشغيل الدائم
- ✅ راقب استخدام الموارد
- ✅ احفظ نسخ احتياطية منتظمة
- ✅ حدّث المكتبات بانتظام
- ✅ استخدم متغيرات البيئة للأمان

### ❌ لا تفعل:
- ❌ لا تشارك التوكن
- ❌ لا تضع التوكن في الكود مباشرة
- ❌ لا تترك البوت بدون مراقبة
- ❌ لا تستخدم جذر (root) إلا عند الضرورة

---

## 🎯 الخيار الموصى به

**للمبتدئين**: استخدم **Replit** أو **PythonAnywhere**
- سهل جداً
- لا يحتاج معرفة تقنية
- مجاني

**للمتقدمين**: استخدم **Linux VPS + Systemd**
- أكثر استقراراً
- تحكم كامل
- أرخص على المدى الطويل

**للمحترفين**: استخدم **Docker + Linux VPS**
- أفضل ممارسات
- سهل النشر
- قابل للتوسع

---

## 📞 نصائح مهمة

### للحفاظ على البوت يعمل 24/7:

1. **استخدم Systemd** - يعيد تشغيل البوت تلقائياً عند الانقطاع
2. **راقب الموارد** - تأكد من أن الخادم لديه موارد كافية
3. **حدّث البرامج** - احفظ البرامج محدثة
4. **احفظ نسخ احتياطية** - احفظ ملفاتك بانتظام
5. **استخدم UptimeRobot** - ليخبرك إذا انقطع البوت

---

**تم آخر تحديث**: 13 يناير 2026

**🎉 الآن أنت جاهز لنشر البوت على خادم دائم!**
