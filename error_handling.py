#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالجة الأخطاء والاستقرار
Error handling and stability management
"""

import logging
import time
import requests
from typing import Optional, Callable, Any
from functools import wraps
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class RetryStrategy:
    """استراتيجية إعادة المحاولة"""
    
    @staticmethod
    def create_session_with_retries(
        retries: int = 3,
        backoff_factor: float = 0.5,
        status_forcelist: tuple = (500, 502, 503, 504)
    ) -> requests.Session:
        """إنشاء جلسة مع استراتيجية إعادة محاولة"""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session


def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    """ديكوريتور لإعادة محاولة الدالة عند حدوث استثناء"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # exponential backoff
                        logger.warning(
                            f"محاولة {attempt + 1}/{max_retries} فشلت: {e}. "
                            f"إعادة المحاولة بعد {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"فشلت جميع المحاولات ({max_retries}): {e}")
            
            raise last_exception
        
        return wrapper
    return decorator


class ConnectionPool:
    """تجميع الاتصالات للحفاظ على الاستقرار"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.active_connections = 0
        self.failed_attempts = {}
    
    def acquire(self) -> bool:
        """الحصول على اتصال"""
        if self.active_connections < self.max_connections:
            self.active_connections += 1
            return True
        return False
    
    def release(self):
        """تحرير اتصال"""
        if self.active_connections > 0:
            self.active_connections -= 1
    
    def record_failure(self, endpoint: str):
        """تسجيل فشل الاتصال"""
        if endpoint not in self.failed_attempts:
            self.failed_attempts[endpoint] = 0
        self.failed_attempts[endpoint] += 1
    
    def reset_failure(self, endpoint: str):
        """إعادة تعيين عداد الفشل"""
        if endpoint in self.failed_attempts:
            self.failed_attempts[endpoint] = 0
    
    def get_failure_count(self, endpoint: str) -> int:
        """الحصول على عدد محاولات الفشل"""
        return self.failed_attempts.get(endpoint, 0)


class CircuitBreaker:
    """نمط Circuit Breaker لمنع الفشل المتكرر"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False
    
    def record_success(self):
        """تسجيل نجاح"""
        self.failure_count = 0
        self.is_open = False
    
    def record_failure(self):
        """تسجيل فشل"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.is_open = True
            logger.warning(
                f"Circuit breaker مفتوح بعد {self.failure_count} فشل"
            )
    
    def can_execute(self) -> bool:
        """التحقق من إمكانية التنفيذ"""
        if not self.is_open:
            return True
        
        # محاولة إغلاق الدائرة بعد انقضاء المهلة الزمنية
        if time.time() - self.last_failure_time >= self.timeout:
            logger.info("محاولة إغلاق Circuit breaker...")
            self.is_open = False
            self.failure_count = 0
            return True
        
        return False


class RateLimiter:
    """تحديد معدل الطلبات"""
    
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def is_allowed(self) -> bool:
        """التحقق من السماح بالطلب"""
        current_time = time.time()
        
        # إزالة الطلبات القديمة
        self.requests = [
            req_time for req_time in self.requests
            if current_time - req_time < self.time_window
        ]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        
        return False
    
    def get_wait_time(self) -> float:
        """الحصول على وقت الانتظار المتبقي"""
        if not self.requests:
            return 0
        
        oldest_request = self.requests[0]
        current_time = time.time()
        wait_time = self.time_window - (current_time - oldest_request)
        
        return max(0, wait_time)


class HealthCheck:
    """فحص صحة النظام"""
    
    def __init__(self):
        self.last_check_time = None
        self.is_healthy = True
        self.error_count = 0
        self.error_threshold = 10
    
    def check_api_health(self, api_url: str, timeout: int = 5) -> bool:
        """فحص صحة API"""
        try:
            response = requests.get(api_url, timeout=timeout)
            if response.status_code == 200:
                self.is_healthy = True
                self.error_count = 0
                logger.info(f"✅ API صحي: {api_url}")
                return True
            else:
                self.error_count += 1
                logger.warning(f"⚠️ API غير صحي: {response.status_code}")
                return False
        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ خطأ في فحص API: {e}")
            
            if self.error_count >= self.error_threshold:
                self.is_healthy = False
                logger.critical(f"🔴 النظام غير صحي بعد {self.error_count} أخطاء")
            
            return False
    
    def get_health_status(self) -> dict:
        """الحصول على حالة الصحة"""
        return {
            'is_healthy': self.is_healthy,
            'error_count': self.error_count,
            'last_check_time': self.last_check_time
        }


class LogRotation:
    """إدارة تدوير السجلات"""
    
    @staticmethod
    def setup_rotating_logger(
        log_file: str,
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5
    ) -> logging.Logger:
        """إعداد logger مع تدوير السجلات"""
        from logging.handlers import RotatingFileHandler
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        return logger


# مثال على الاستخدام
if __name__ == "__main__":
    # اختبار Circuit Breaker
    cb = CircuitBreaker(failure_threshold=3)
    
    for i in range(5):
        if cb.can_execute():
            print(f"محاولة {i + 1}: يمكن التنفيذ")
            cb.record_failure()
        else:
            print(f"محاولة {i + 1}: الدائرة مفتوحة")
    
    # اختبار Rate Limiter
    limiter = RateLimiter(max_requests=3, time_window=10)
    
    for i in range(5):
        if limiter.is_allowed():
            print(f"طلب {i + 1}: مسموح")
        else:
            print(f"طلب {i + 1}: تم تجاوز الحد")
