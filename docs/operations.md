# عملیات و production readiness

## محیط‌ها

- `development`: توسعه محلی و داده آزمایشی
- `staging`: شبیه‌سازی production با منابع کنترل‌شده
- `production`: داده واقعی و دسترسی محدود

تنظیمات و secretها باید بر اساس محیط جدا باشند و در repository قرار نگیرند.

## Logging

لاگ‌ها باید ساختاریافته باشند و حداقل شامل این موارد شوند:

- timestamp به UTC
- level
- service یا module
- request id یا run id
- source id در پردازش جمع‌آوری
- مدت اجرا
- پیام خطا و نوع exception

payload کامل منبع، credential و اطلاعات حساس کاربر نباید در لاگ ثبت شود.

## Metrics و alertها

Metrics پیشنهادی:

- تعداد اجرای موفق و ناموفق هر منبع
- مدت هر collection run
- تعداد آگهی دریافت‌شده و معتبر
- نرخ duplicate
- اندازه صف worker
- latency و error rate API
- latency جست‌وجو
- تعداد آگهی‌های بدون به‌روزرسانی

Alertهای مهم:

- شکست چند اجرای متوالی یک منبع
- افزایش ناگهانی خطای normalization
- توقف worker یا رشد صف
- پر شدن فضای database
- افزایش خطای API

## Backup و بازیابی

- backup زمان‌بندی‌شده PostgreSQL
- نگهداری چند نسخه در بازه مشخص
- تست دوره‌ای restore
- تعریف هدف RPO و RTO پیش از production
- در نظر گرفتن سیاست retention برای raw data

## امنیت

- secret manager برای credentialها
- TLS برای ارتباطات بیرونی
- احراز هویت قوی پنل مدیریت
- حداقل سطح دسترسی برای database و worker
- validation ورودی‌ها
- sanitization محتوای نمایش‌داده‌شده
- dependency scanning و به‌روزرسانی امنیتی

## استقرار

Pipeline استقرار باید شامل این مراحل باشد:

1. lint و type check
2. unit و integration test
3. build artifact یا image
4. migration کنترل‌شده
5. deploy به staging
6. smoke test
7. deploy به production
8. بررسی metrics و امکان rollback
