# معماری سیستم

## تصمیم اصلی

نسخه اول با معماری **Modular Monolith** ساخته می‌شود. مرزهای ماژول‌ها از ابتدا مشخص هستند تا در صورت رشد بار یا تیم، جداسازی سرویس‌ها امکان‌پذیر باشد.

## اجزای اصلی

- **API**: ارائه endpointهای عمومی و مدیریتی
- **Collectors**: اتصال به منابع مختلف و دریافت داده خام
- **Ingestion**: مدیریت batch، اجرای مجدد و ثبت وضعیت
- **Normalization**: تبدیل داده منبع به schema مشترک
- **Deduplication**: تشخیص آگهی تکراری و ادغام نسخه‌ها
- **Jobs**: اجرای پردازش‌های پس‌زمینه و زمان‌بندی
- **Search**: query، فیلتر، sorting و indexing
- **Admin**: کنترل منابع و مشاهده عملیات
- **Observability**: logging، metrics، health و error tracking

## جریان داده

```text
Scheduler
  -> Queue
  -> Collector
  -> Raw Job Record
  -> Validation
  -> Normalization
  -> Deduplication
  -> Database
  -> Search Index
  -> REST API
  -> Web Dashboard
```

## مرزهای مهم

### Collector

Collector فقط مسئول ارتباط با منبع، pagination، rate limit و تبدیل پاسخ منبع به یک رکورد خام است. Collector نباید منطق جست‌وجو یا مدل نمایش frontend را بشناسد.

### Domain

مدل نهایی آگهی، وضعیت lifecycle، تشخیص منقضی شدن و قوانین duplicate در domain نگهداری می‌شوند، نه داخل collector اختصاصی.

### API

API باید از serviceهای دامنه استفاده کند و مستقیماً منطق collector یا queryهای پراکنده در endpointها قرار ندهد.

## انتخاب ذخیره‌سازی

- PostgreSQL برای داده اصلی، روابط، وضعیت پردازش و جست‌وجوی اولیه
- Redis برای queue، cache و rate limiting
- OpenSearch فقط زمانی اضافه شود که PostgreSQL از نظر relevance یا حجم جست‌وجو کافی نباشد

## قابلیت اطمینان

- هر batch شناسه یکتا دارد.
- پردازش‌ها باید idempotent باشند.
- خطای هر منبع به‌صورت جداگانه ثبت می‌شود.
- داده خام قبل از نرمال‌سازی نگهداری می‌شود.
- عملیات طولانی در worker انجام می‌شوند.
