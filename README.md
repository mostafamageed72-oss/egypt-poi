# مصدر الرادارات والمطبات الليلي (اختياري – مجاني)

1. على GitHub اعمل مستودع **عام (Public)** جديد، مثلًا `egypt-poi`.
2. ارفع محتويات المجلد ده (`build_poi.py` ومجلد `.github`) للمستودع.
3. من تبويب **Actions** شغّل `Egypt POI extract` مرة بإيدك (Run workflow). بعدها بيشتغل لوحده كل يوم 01:30 UTC.
   - مفيش أي مفاتيح أو أسرار مطلوبة (بيستخدم صلاحية GitHub الافتراضية).
4. في Cloudflare → الـWorker → Settings → Variables أضف متغير **عادي** (مش سر):
   `POI_EXTRACT_URL` = `https://raw.githubusercontent.com/<اسمك>/egypt-poi/main/data`
5. تأكد من `/poi/status` إن `extract_source` = مفعّل.

لو الملف وقف يتحدّث أكتر من 3 أيام الوركر بيرجع تلقائيًا لـ Overpass.
البيانات من OpenStreetMap (رخصة ODbL) عبر Geofabrik.
