# قرارداد اولیه REST API

این سند قرارداد سطح بالا است و پیش از پیاده‌سازی باید با OpenAPI نهایی شود.

## Endpointهای عمومی

### جست‌وجوی آگهی‌ها

`GET /api/v1/jobs`

پارامترهای پیشنهادی:

- `q`: جست‌وجوی متنی
- `location`
- `workplace_type`
- `employment_type`
- `seniority`
- `skills`
- `source`
- `salary_min`
- `salary_max`
- `published_after`
- `published_before`
- `page`
- `page_size`
- `sort`

پاسخ باید شامل نتایج، تعداد کل یا metadata مناسب pagination و اطلاعات query اعمال‌شده باشد.

### جزئیات آگهی

`GET /api/v1/jobs/{job_id}`

باید مدل نرمال‌شده، زمان آخرین مشاهده و لینک منبع اصلی را برگرداند.

### منابع

`GET /api/v1/sources`

در نسخه عمومی فقط اطلاعات غیرحساس و قابل نمایش منابع برگردد.

## Endpointهای مدیریتی

- `GET /api/v1/admin/sources`
- `POST /api/v1/admin/sources/{source_id}/runs`
- `GET /api/v1/admin/collection-runs`
- `GET /api/v1/admin/collection-runs/{run_id}`
- `POST /api/v1/admin/jobs/{job_id}/reprocess`

تمام endpointهای مدیریتی نیازمند احراز هویت، authorization و audit log هستند.

## اصول API

- نسخه‌بندی از مسیر `/api/v1` آغاز شود.
- خطاها قالب استاندارد و قابل‌مصرف برای frontend داشته باشند.
- مقدار `page_size` محدود شود.
- rate limiting برای endpointهای عمومی فعال باشد.
- فیلدهای داخلی مانند payload خام در API عمومی قرار نگیرند.
- تاریخ‌ها با ISO 8601 و timezone مشخص برگردند.
- تغییرات ناسازگار با نسخه قبلی با نسخه جدید API انجام شوند.

## وضعیت‌های HTTP

- `200`: درخواست موفق
- `201`: ایجاد موفق عملیات مدیریتی
- `400`: پارامتر نامعتبر
- `401`: احراز هویت لازم است
- `403`: دسترسی کافی نیست
- `404`: رکورد پیدا نشد
- `429`: عبور از rate limit
- `500`: خطای غیرمنتظره سرور
- `503`: سرویس وابسته موقتاً در دسترس نیست
