from pathlib import Path
from PIL import Image
import json, html, csv

root=Path(__file__).parent
folder=root/'new-photos'
manifest=json.loads((folder/'licenses-and-sources.json').read_text(encoding='utf-8'))
for row in manifest:
    if row['file']=='maria-martental-church.jpg':
        row['description_ar']='مشهد ميلاد داخل كنيسة Maria Martental؛ صورة موسمية وليست منظرًا عامًا للكنيسة'
    if row['file']=='historic-cochem-and-moselle.jpg':
        row['description_ar']='Cochem والموزل تاريخيًا؛ تكوين قريب جدًا من النسخة التاريخية الأخرى، لا صورتان لزاويتين مختلفتين'
(folder/'licenses-and-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
e=lambda v:html.escape(str(v),quote=True)
credits=['# Image credits / Bildnachweise','Downloaded 29 October 2026. Licences reproduced from individual Commons file metadata. No blanket licence applies to this collection. The original local house images are not covered by these licences.','']
cards=[]
for row in manifest:
    historical=row['file'].startswith('historic-')
    size=Image.open(folder/row['file']).size
    assert size==(row['width'],row['height'])
    credit=f"{row['commons_title']} — {row['artist']} — {row['license']}"
    credits.extend([f"## {row['file']}",credit,f"Source: {row['source_page']}",f"Licence: {row['license_url'] or 'See source page public-domain statement'}",f"Date in metadata: {row['date']}",f"Credit/source supplied by file: {row['credit']}",f"Changes: {row['changes']}",f"Dimensions: {row['width']} × {row['height']}",''])
    licence=f'<a href="{e(row["license_url"])}">{e(row["license"])}</a>' if row['license_url'] else e(row['license'])
    cards.append(f'''<article class="photo {'old' if historical else ''}">
<a href="new-photos/{e(row['file'])}"><img loading="lazy" src="new-photos/{e(row['file'])}" alt="{e(row['description_ar'])}"></a>
<div class="details"><span class="tag">{'أرشيف المنطقة' if historical else 'صورة إضافية للمنطقة'}</span><h3>{e(row['description_ar'])}</h3><p class="latin">{e(row['artist'])} · {licence}</p><p class="latin">{row['width']} × {row['height']} · <a href="{e(row['source_page'])}">Source & full licence</a></p></div></article>''')
(folder/'CREDITS.md').write_text('\n\n'.join(credits),encoding='utf-8')
with (folder/'photo-manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(manifest[0]));writer.writeheader();writer.writerows(manifest)
page='''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Villa Laubach — القصة والمنطقة والصور</title>
<style>
:root{--green:#173b31;--paper:#f6f1e7;--ink:#23372f;--gold:#bc8a4f}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.85 Tahoma,Arial,sans-serif}a{color:inherit;text-underline-offset:4px}header{background:var(--green);color:#fff;padding:30px 6vw}header b{font:24px Georgia;letter-spacing:2px}header span{float:left;font-size:13px;opacity:.7}.intro{display:grid;grid-template-columns:1fr 1fr;min-height:550px}.intro img{width:100%;height:100%;max-height:650px;object-fit:cover}.intro div{padding:70px 6vw}h1{font-size:clamp(30px,3.5vw,52px);line-height:1.5;margin:20px 0}h2{font-size:30px}.eyebrow{color:var(--gold);font-size:14px;font-weight:bold}.wrap{max-width:1400px;padding:40px 5vw;margin:auto}.timeline{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;border-top:1px solid #c9c5b9;padding-top:25px}.timeline strong{display:block;font:34px Georgia;color:var(--green)}.note{background:#e7e8de;padding:24px;border-right:4px solid var(--gold)}.themes{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.theme{background:white;padding:25px}.theme b{display:block;color:var(--green);font-size:22px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}.photo{background:white;overflow:hidden}.photo img{width:100%;height:270px;object-fit:contain;background:#e5e2da;display:block}.details{padding:22px}.details h3{font-size:18px;line-height:1.7}.latin{direction:ltr;text-align:left;font:13px/1.6 Arial;overflow-wrap:anywhere}.tag{font-size:12px;color:#765831}.old{border-top:4px solid var(--gold)}.links{display:flex;gap:14px;flex-wrap:wrap}.links a{padding:9px 15px;background:var(--green);color:white;text-decoration:none;font-size:14px}footer{padding:40px 5vw;background:var(--green);color:white;font-size:14px}@media(max-width:850px){.intro{grid-template-columns:1fr}.intro div{padding:35px 6vw}.intro img{max-height:400px}.grid,.themes{grid-template-columns:1fr 1fr}.timeline{grid-template-columns:1fr 1fr}}@media(max-width:550px){.grid,.themes{grid-template-columns:1fr}header span{float:none;display:block}}
</style>
<header><b dir="ltr">VILLA LAUBACH</b><span>بحث تحريري وبصري · 29 أكتوبر 2026 · ليس الموقع النهائي</span></header>
<section class="intro"><div><span class="eyebrow">بيت له تاريخ · ومنطقة تستحق الرحلة</span><h1>الحكاية تبدأ من مدرسة قديمة… وتكمل بين إيفل والموْزل.</h1><p>سجل التراث الرسمي يؤرخ الجزء الأقدم من المدرسة في نفس عنوان الفيلا إلى 1842، وجزءًا آخر إلى نحو 1900. دي نقطة البداية الأقوى لهوية المكان.</p><p><b>الاتجاه المعتمد:</b> موقع ألماني وإنجليزي بلا أسعار معلنة؛ صور حقيقية، قصة موثقة، ورحلات تحفّز الاستفسار.</p></div><img src="source-material/original-photos/469790413.jpg" alt="واجهة الفيلا والتراس في إحدى صور المجموعة الأصلية"></section>
<main class="wrap"><p class="note"><b>إضافة البحث الأعمق:</b> نص Airbnb يذكر وحدة الضيوف وloft منفصلًا للمضيف داخل المبنى؛ نراجع استخدام الخارج ولا نعد بانفراد كامل بالمبنى. ملخص الحقائق النهائي ومصادر الصور الأرشيفية الجديدة في الرابط التالي.</p><h2>خط زمني قابل للاستخدام</h2><div class="timeline"><div><strong>1455</strong>أول ذكر موثق للقرية بحسب مصدرها الرسمي</div><div><strong>1842</strong>الجزء الأقدم من المدرسة بحسب GDKE</div><div><strong>~1900</strong>الجزء الآخر من المبنى</div><div><strong>اليوم</strong>بيت عطلات وبداية لاكتشاف المنطقة</div></div>
<p class="note">1842 أدق من سنة 1850 في وصف المضيف. صورة تاريخية مؤكدة للواجهة نفسها لم تظهر في البحث المفتوح. صور المدرسة الأخرى التي تحمل اسم Laubach استُبعدت عند اختلاف الموقع.</p>
<div class="links"><a href="deep-search-final/FINAL-RESEARCH-AR.md">الخلاصة النهائية الأحدث</a><a href="deep-search-final/IMAGE-SELECTION.md">اختيار الصور للموقع</a><a href="research-round-3/FINDINGS-AR.md">إضافات الجولة الثالثة</a><a href="research-round-3/ARCHIVE-REQUEST-DRAFTS-DE.md">مسودات طلب الأرشيف</a><a href="history/HISTORY-AND-STORY-AR.md">التاريخ والمصادر</a><a href="DESTINATIONS-AR.md">دليل الرحلات</a><a href="website-story-DE-EN-v2.md">مقدمة الموقع DE / EN</a><a href="new-photos/CREDITS.md">نسب الصور والتراخيص</a><a href="history/GDKE-Laubach-page.png">صفحة السجل الرسمي</a></div>
<h2>ثلاثة أبواب للرحلة</h2><div class="themes"><div class="theme"><b>قريب من روح المكان</b>Kaulenbachtal، تراث الأردواز، Digi-Pfad، Maria Martental وطبيعة القرية.</div><div class="theme"><b>إيفل والموْزل</b>Ulmen، Cochem، Monreal، البحيرات والقلاع. كل صورة تحمل اسم وجهتها الحقيقي.</div><div class="theme"><b>اهتمامات متنوعة</b>Nürburgring للهواة، Klotti للعائلات، وKoblenz وGeierlay لرحلات أوسع.</div></div>
<h2>الصور الإضافية التي جُمعت</h2><p>COUNT صورة محفوظة، تشمل صورًا تاريخية للمنطقة. ليست كلها حديثة التصوير، وليست صورًا جديدة لداخل الفيلا. تم فحص المجموعة بصريًا وحفظ مصدر ورخصة كل ملف. النسخ الإضافية معظمها 1280 بكسل للبحث والمعاينة؛ المصدر يتيح مراجعة الأصل.</p><section class="grid">CARDS</section>
<h2>خيط أرشيفي أقرب للقرية</h2><p>في Der Bergmann رقم 35، صفحة 12، صورة قطار الإنشاءات الأول في Laubach سنة 1894 وخريطة المحطة. وفي العدد 39، صفحة 22، مقال عن سجلات مدرسة Laubach مع صورة فصل غير محددة المكان. تُحفظ كمرجع لا كصور مرخصة للنشر.</p><div class="links"><a href="history/bergmann35-page-12.png">معاينة صفحة القطار والخريطة</a><a href="history/bergmann39-page-22.png">معاينة المقال المدرسي</a></div>
<p class="note">في التشغيل الفعلي: لا نَعِد بأن كل مسار متاح؛ صفحة Wilde Endert الحالية تذكر أضرار جسر قرب الشلال. نربط الزائر دائمًا بمعلومات المشغل الحالية.</p></main><footer>ملف إعداد للموقع. الصور الأصلية للفيلا لها حقوق مستقلة. الصور الإضافية تخضع لرخصة كل ملف؛ يلزم إظهار الاعتمادات والإشارة إلى التعديلات حسب شروطه.</footer></html>'''
page=page.replace('COUNT',str(len(manifest))).replace('CARDS',''.join(cards))
(root/'research-board.html').write_text(page,encoding='utf-8')
print('Gallery built:',len(manifest),'verified image files')
