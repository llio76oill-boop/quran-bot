# 🚀 دليل النشر السريع على خادم Linux

## ⚡ النشر في 5 دقائق فقط!

### الخطوة 1: الاتصال بالخادم

```bash
# استبدل IP_ADDRESS برقم IP الخادم الخاص بك
ssh root@IP_ADDRESS

# مثال:
ssh root@192.168.1.100
```

### الخطوة 2: تحميل السكريبت

```bash
# تحميل سكريبت التثبيت
curl -O https://your-repo/install.sh
chmod +x install.sh

# أو انسخ الملفات يدوياً
mkdir -p /home/quran_bot
cd /home/quran_bot
```

### الخطوة 3: نسخ ملفات البوت

**من جهازك المحلي:**
```bash
# نسخ الملفات إلى الخادم
scp bot_final.py root@IP_ADDRESS:/home/quran_bot/
scp requirements.txt root@IP_ADDRESS:/home/quran_bot/
scp .env root@IP_ADDRESS:/home/quran_bot/
scp quran_bot.service root@IP_ADDRESS:/tmp/
```

### الخطوة 4: تثبيت المتطلبات

```bash
# على الخادم
cd /home/quran_bot

# تثبيت Python والمكتبات
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

### الخطوة 5: تثبيت الخدمة (Systemd)

```bash
# نسخ ملف الخدمة
sudo cp /tmp/quran_bot.service /etc/systemd/system/

# تحديث الخدمات
sudo systemctl daemon-reload

# تفعيل الخدمة
sudo systemctl enable quran_bot

# بدء الخدمة
sudo systemctl start quran_bot
```

### الخطوة 6: التحقق من الحالة

```bash
# التحقق من أن البوت يعمل
sudo systemctl status quran_bot

# يجب أن ترى:
# ● quran_bot.service - Quran Bot Service
#    Loaded: loaded (/etc/systemd/system/quran_bot.service; enabled; vendor preset: enabled)
#    Active: active (running) since ...
```

### الخطوة 7: عرض السجلات

```bash
# عرض السجلات الحالية
sudo journalctl -u quran_bot -f

# يجب أن ترى:
# ✅ البوت جاهز للعمل!
```

---

## ✅ تم! البوت يعمل الآن 24/7

البوت الآن يعمل على الخادم بشكل دائم ويرسل الآيات كل 15 دقيقة!

---

## 📋 أوامر مفيدة

### إدارة الخدمة

```bash
# عرض حالة البوت
sudo systemctl status quran_bot

# إيقاف البوت
sudo systemctl stop quran_bot

# إعادة تشغيل البوت
sudo systemctl restart quran_bot

# تفعيل البوت عند بدء النظام
sudo systemctl enable quran_bot

# تعطيل البوت عند بدء النظام
sudo systemctl disable quran_bot
```

### عرض السجلات

```bash
# عرض السجلات الحالية
sudo journalctl -u quran_bot -f

# عرض آخر 50 سطر
sudo journalctl -u quran_bot -n 50

# عرض السجلات من تاريخ معين
sudo journalctl -u quran_bot --since "2024-01-13"

# البحث عن أخطاء
sudo journalctl -u quran_bot | grep "❌"
```

### مراقبة الموارد

```bash
# عرض استخدام الموارد
top

# عرض استخدام الذاكرة
free -h

# عرض استخدام القرص
df -h

# عرض العمليات التي تستخدم Python
ps aux | grep python3
```

---

## 🔄 تحديث البوت

### تحديث الملفات

```bash
# إيقاف البوت
sudo systemctl stop quran_bot

# نسخ الملفات الجديدة
scp bot_final.py root@IP_ADDRESS:/home/quran_bot/

# إعادة تشغيل البوت
sudo systemctl start quran_bot
```

### تحديث المكتبات

```bash
# تحديث المكتبات
pip3 install --upgrade python-telegram-bot requests python-dotenv apscheduler

# إعادة تشغيل البوت
sudo systemctl restart quran_bot
```

---

## ⚠️ استكشاف الأخطاء

### المشكلة: البوت لا يعمل

```bash
# التحقق من الحالة
sudo systemctl status quran_bot

# عرض السجلات
sudo journalctl -u quran_bot -f

# إعادة تشغيل البوت
sudo systemctl restart quran_bot
```

### المشكلة: البوت يتوقف بعد فترة

```bash
# التحقق من استخدام الموارد
top

# التحقق من الذاكرة
free -h

# إعادة تشغيل البوت
sudo systemctl restart quran_bot
```

### المشكلة: لا توجد رسائل في السجل

```bash
# التحقق من أن الخدمة تعمل
sudo systemctl status quran_bot

# عرض السجلات
sudo journalctl -u quran_bot -n 100

# التحقق من ملف .env
cat /home/quran_bot/.env
```

---

## 🛡️ الأمان

### تغيير صلاحيات الملفات

```bash
# تعيين صلاحيات آمنة
chmod 600 /home/quran_bot/.env
chmod 755 /home/quran_bot/bot_final.py
```

### النسخ الاحتياطية

```bash
# عمل نسخة احتياطية
tar -czf quran_bot_backup_$(date +%Y%m%d).tar.gz /home/quran_bot

# نسخ احتياطية من السجلات
sudo journalctl -u quran_bot > quran_bot_logs_backup.txt
```

---

## 📊 مراقبة البوت

### استخدام UptimeRobot (مجاني)

1. اذهب إلى: https://uptimerobot.com
2. سجل حساب جديد
3. اضغط: Add Monitor
4. اختر: HTTP(s)
5. أضف رابط الخادم: `http://IP_ADDRESS:8080`
6. سيراقب البوت ويخبرك إذا انقطع

---

## 🎉 تم!

البوت الآن يعمل على الخادم 24/7 ويرسل الآيات تلقائياً!

**استمتع بآيات القرآن الكريم! 🙏**
