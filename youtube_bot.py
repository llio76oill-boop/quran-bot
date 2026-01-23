#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلغرام متقدم لمراقبة البث المباشر من YouTube
وإرسال رابط البث إلى قناة تلغرام مع التحديث التلقائي

YouTube Live Stream Monitor Bot for Telegram
"""

import os
import logging
import asyncio
import requests
import subprocess
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# تحميل متغيرات البيئة
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('youtube_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# الثوابت
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL = os.getenv('TELEGRAM_CHANNEL')
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))
PORT = int(os.getenv('PORT', 8000))

# ============================================================
# Web Server البسيط (لـ Render.com)
# ============================================================

class HealthCheckHandler(BaseHTTPRequestHandler):
    """معالج طلبات صحة البوت"""
    
    def do_GET(self):
        """معالج طلبات GET"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        """تعطيل السجلات الافتراضية"""
        pass

def start_web_server():
    """بدء web server بسيط"""
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
        logger.info(f"✅ بدء Web Server على المنفذ {PORT}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ خطأ في Web Server: {e}")

# ============================================================
# فئة البوت الرئيسية
# ============================================================

class YouTubeLiveStreamBot:
    """بوت مراقبة البث المباشر من YouTube"""
    
    def __init__(self, token: str, channel: str, youtube_url: str):
        self.token = token
        self.channel = channel
        self.youtube_url = youtube_url
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.current_stream_url = None
        self.running = True
        self.last_message_id = None
    
    def get_youtube_stream_url(self) -> Optional[str]:
        """استخراج رابط البث المباشر من YouTube باستخدام yt-dlp"""
        try:
            logger.info(f"🔍 جاري البحث عن رابط البث المباشر...")
            
            # محاولة 1: بدون cookies (للبثات العامة)
            cmd = [
                'yt-dlp',
                '-f', 'best',
                '-g',
                '--no-warnings',
                '--socket-timeout', '10',
                self.youtube_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                urls = result.stdout.strip().split('\n')
                stream_url = urls[0] if urls else None
                
                if stream_url:
                    logger.info(f"✅ تم الحصول على رابط البث المباشر")
                    return stream_url
                else:
                    logger.warning("⚠️ لم يتم الحصول على رابط")
                    return None
            else:
                error_msg = result.stderr.lower()
                
                if 'sign in' in error_msg or 'bot' in error_msg:
                    logger.warning("⚠️ YouTube يطلب تأكيد الهوية")
                else:
                    logger.error(f"❌ خطأ في yt-dlp: {result.stderr[:200]}")
                return None
        
        except subprocess.TimeoutExpired:
            logger.error("❌ انتهت مهلة الانتظار عند البحث عن الرابط")
            return None
        except Exception as e:
            logger.error(f"❌ خطأ في استخراج الرابط: {e}")
            return None
    
    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """إرسال رسالة إلى القناة"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.channel,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    self.last_message_id = result['result']['message_id']
                    logger.info(f"✅ تم إرسال الرسالة برقم {self.last_message_id}")
                    return True
            
            logger.error(f"❌ فشل الإرسال: {response.text}")
            return False
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال الرسالة: {e}")
            return False
    
    def edit_message(self, message_id: int, text: str) -> bool:
        """تعديل رسالة موجودة"""
        try:
            url = f"{self.base_url}/editMessageText"
            payload = {
                "chat_id": self.channel,
                "message_id": message_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ تم تحديث الرسالة برقم {message_id}")
                return True
            
            logger.error(f"❌ فشل التعديل: {response.text}")
            return False
        except Exception as e:
            logger.error(f"❌ خطأ في تعديل الرسالة: {e}")
            return False
    
    def format_stream_message(self, stream_url: str) -> str:
        """تنسيق رسالة البث المباشر"""
        return f"""🔴 **البث المباشر الآن**

**رابط البث:**
`{stream_url}`

**الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⏱️ يتم تحديث الرابط تلقائياً كل دقيقة"""
    
    async def monitor_stream(self):
        """مراقبة البث المباشر والإرسال عند التغيير فقط"""
        logger.info("✅ بدء مراقبة البث المباشر")
        logger.info("📌 سيتم إرسال الرابط فقط عند التغيير (بدون رسائل متكررة)")
        
        retry_count = 0
        max_retries = 3
        
        while self.running:
            try:
                stream_url = self.get_youtube_stream_url()
                
                if stream_url:
                    retry_count = 0
                    
                    if stream_url != self.current_stream_url:
                        self.current_stream_url = stream_url
                        message = self.format_stream_message(stream_url)
                        
                        if self.last_message_id:
                            logger.info(f"📝 تم تحديث الرابط! تعديل الرسالة السابقة...")
                            self.edit_message(self.last_message_id, message)
                        else:
                            logger.info(f"📤 تم اكتشاف بث جديد! إرسال رسالة...")
                            self.send_message(message)
                    else:
                        logger.debug("ℹ️ الرابط لم يتغير - لا توجد رسالة جديدة")
                else:
                    if self.current_stream_url is not None:
                        logger.info("⚠️ انتهى البث المباشر")
                        self.current_stream_url = None
                    else:
                        retry_count += 1
                        if retry_count <= max_retries:
                            logger.debug(f"ℹ️ لا يوجد بث مباشر حالياً (محاولة {retry_count}/{max_retries})")
                
                await asyncio.sleep(CHECK_INTERVAL)
            
            except asyncio.CancelledError:
                logger.info("🛑 تم إيقاف مراقبة البث")
                break
            except Exception as e:
                logger.error(f"❌ خطأ في المراقبة: {e}")
                await asyncio.sleep(CHECK_INTERVAL)
    
    async def run(self):
        """تشغيل البوت"""
        logger.info("=" * 60)
        logger.info("🤖 بدء تشغيل بوت مراقبة البث المباشر من YouTube")
        logger.info("=" * 60)
        logger.info(f"📺 رابط YouTube: {self.youtube_url}")
        logger.info(f"📢 القناة: {self.channel}")
        logger.info(f"⏱️ فترة التحديث: {CHECK_INTERVAL} ثانية")
        logger.info(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        if not self.token or not self.channel or not self.youtube_url:
            logger.error("❌ خطأ: TELEGRAM_TOKEN أو TELEGRAM_CHANNEL أو YOUTUBE_URL غير محدد")
            return
        
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                bot_info = response.json()['result']
                logger.info(f"✅ تم الاتصال بـ Telegram: {bot_info['username']}")
            else:
                logger.error(f"❌ فشل الاتصال بـ Telegram: {response.text}")
                return
        except Exception as e:
            logger.error(f"❌ خطأ في الاتصال بـ Telegram: {e}")
            return
        
        logger.info("✅ تم جدولة مراقبة البث المباشر")
        logger.info("✅ البوت جاهز للعمل!")
        logger.info("=" * 60)
        
        monitor_task = asyncio.create_task(self.monitor_stream())
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("🛑 تم إيقاف البوت بواسطة المستخدم")
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
        finally:
            self.running = False
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
            logger.info("🛑 تم إيقاف البوت")

# ============================================================
# الدالة الرئيسية
# ============================================================

async def main():
    """الدالة الرئيسية"""
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    bot = YouTubeLiveStreamBot(TELEGRAM_TOKEN, TELEGRAM_CHANNEL, YOUTUBE_URL)
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")
    except Exception as e:
        logger.error(f"❌ خطأ حرج: {e}")
