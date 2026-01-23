# استخدام صورة Python الرسمية
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات البوت
COPY bot_final.py .
COPY .env .

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1

# إنشاء مجلد السجلات
RUN mkdir -p /app/logs

# تشغيل البوت
CMD ["python3", "bot_final.py"]
