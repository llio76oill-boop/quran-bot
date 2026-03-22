# 🚀 نشر بوت الآيات على Supabase

## معلومات المشروع

- **اسم المشروع:** quran-bot
- **المستودع:** https://github.com/llio76oill-boop/quran-bot
- **التوكن:** `sbp_354b67bc23a84de2170d25a8cfeae2246ca868cd`

## خطوات النشر

### 1️⃣ إنشاء مشروع على Supabase

```bash
# اذهب إلى: https://supabase.com
# اختر: New Project
# اسم المشروع: quran-bot
# كلمة المرور: قوية جداً
```

### 2️⃣ ربط مع GitHub

في لوحة Supabase:
1. اذهب إلى: **Deployments**
2. اختر: **Connect Repository**
3. اختر: **GitHub**
4. اختر المستودع: **quran-bot**
5. اختر الفرع: **main**

### 3️⃣ تعيين متغيرات البيئة

في **Settings → Environment Variables**:

```env
TELEGRAM_TOKEN=8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc
CHANNEL_ID=@aya_Quraan1
PORT=8000
```

### 4️⃣ النشر

1. اضغط: **Deploy**
2. اختر الفرع: **main**
3. انتظر: 5-10 دقائق

## التحقق من الحالة

```bash
# عرض السجلات
supabase functions logs

# التحقق من الحالة
curl https://your-project.supabase.co/functions/v1/health
```

## 🔧 الملفات المطلوبة

- ✅ `bot_final.py` - البوت الرئيسي
- ✅ `requirements.txt` - المكتبات
- ✅ `Procfile` - تكوين النشر
- ✅ `.env` - متغيرات البيئة

## 📊 معلومات النشر

| المعلومة | القيمة |
|---------|--------|
| **Platform** | Supabase |
| **Token** | `sbp_354b67bc23a84de2170d25a8cfeae2246ca868cd` |
| **Telegram Token** | `8246193524:AAHzBKhoOjIcgFv_u1tYzC266yYVQl_gLfc` |
| **Channel** | `@aya_Quraan1` |
| **Interval** | 15 دقيقة |
| **Status** | ✅ جاهز للنشر |

## 🎯 بعد النشر

✅ البوت سيعمل **24/7**  
✅ سيرسل آية كل **15 دقيقة**  
✅ التحديثات التلقائية من GitHub  
✅ مراقبة السجلات من Supabase

---

**تم الإنشاء:** 22 مارس 2026
