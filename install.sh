#!/bin/bash

# سكريبت تثبيت بوت القرآن الكريم على خادم Linux
# Installation script for Quran Bot on Linux Server

set -e

echo "================================"
echo "🤖 سكريبت تثبيت بوت القرآن الكريم"
echo "Quran Bot Installation Script"
echo "================================"
echo ""

# التحقق من أن المستخدم هو root
if [[ $EUID -ne 0 ]]; then
   echo "❌ هذا السكريبت يجب أن يعمل بصلاحيات root"
   echo "❌ This script must be run as root"
   exit 1
fi

echo "📦 تحديث النظام..."
apt update
apt upgrade -y

echo "📦 تثبيت Python والمتطلبات..."
apt install -y python3 python3-pip git nano curl

echo "📁 إنشاء مجلد البوت..."
mkdir -p /home/quran_bot
cd /home/quran_bot

echo "📥 تثبيت المكتبات المطلوبة..."
pip3 install python-telegram-bot requests python-dotenv apscheduler

echo "✅ تم التثبيت بنجاح!"
echo ""
echo "================================"
echo "📋 الخطوات التالية:"
echo "================================"
echo ""
echo "1. انسخ ملفات البوت إلى /home/quran_bot:"
echo "   - bot_final.py"
echo "   - requirements.txt"
echo "   - .env"
echo ""
echo "2. تأكد من ملف .env يحتوي على:"
echo "   TELEGRAM_TOKEN=your_token"
echo "   CHANNEL_ID=@your_channel"
echo ""
echo "3. لتثبيت الخدمة (Systemd):"
echo "   sudo cp quran_bot.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable quran_bot"
echo "   sudo systemctl start quran_bot"
echo ""
echo "4. للتحقق من حالة البوت:"
echo "   sudo systemctl status quran_bot"
echo ""
echo "5. لعرض السجلات:"
echo "   sudo journalctl -u quran_bot -f"
echo ""
echo "================================"
echo "✅ تم الانتهاء!"
echo "================================"
