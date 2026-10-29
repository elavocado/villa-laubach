from pathlib import Path
import requests, json, re, hashlib, time
from PIL import Image, ImageDraw

root = Path(__file__).parent
out = root / 'new-photos'
out.mkdir(exist_ok=True)
history = root / 'history'
data = list(json.loads((history/'commons-discovery.json').read_text(encoding='utf-8'))['query']['pages'].values())
for name in ['commons-regional-discovery.json','commons-extra-discovery.json']:
    data += json.loads((history/name).read_text(encoding='utf-8'))
chosen = {
 'File:Laubach (Eifel) 01.jpg':('laubach-st-josef-2020','قرية Laubach: كنيسة St. Josef، وليست الفيلا'),
 'File:Schieferhalden im Kaulenbachtal.jpg':('kaulenbachtal-slate','أكوام الأردواز في Kaulenbachtal'),
 'File:Kaulenbachtal - 2023-02.jpg':('kaulenbachtal-2023','وادي Kaulenbachtal؛ تصوير 2023 بحسب المصدر'),
 'File:Gebäudereste.JPG':('kaulenbachtal-mining-remains','بقايا مبانٍ في منطقة التعدين؛ يُراجع الوصف الأصلي'),
 'File:Maria Martental.jpg':('maria-martental','Maria Martental'),
 'File:Wallfahrtskirche Maria Martental (27770171629).jpg':('maria-martental-church','كنيسة الحج Maria Martental'),
 'File:UlmenerMaarUberblick.JPG':('ulmen-maar-panorama','بحيرة Ulmener Maar'),
 'File:Ulmener Maar 01.jpg':('ulmen-maar','Ulmener Maar'),
 'File:Fritz von Wille 0025.jpg':('historic-ulmen-fritz-von-wille','لوحة تاريخية لقلعة وبحيرة Ulmen؛ ليست صورة المدرسة'),
 'File:Klotten um 1900.jpg':('historic-klotten-circa-1900','Klotten حوالي 1900؛ ليست Laubach'),
 'File:Fachwerk in Monreal.jpg':('monreal-timber-houses','بيوت Monreal التقليدية'),
 'File:Monreal - Idylle an der Elz.jpg':('monreal-elz','Monreal على نهر Elz'),
 'File:BurgCochem1900.jpg':('historic-cochem-photochrom','صورة تاريخية لقلعة Cochem؛ تاريخ المصدر في السجل'),
 'File:Cochem and castle, Moselle, valley of, Germany-LCCN2002713956.jpg':('historic-cochem-and-moselle','Cochem والموزل، صورة تاريخية؛ ليست الفيلا'),
 'File:Panorama Deutsches Eck (10561303714).jpg':('koblenz-deutsches-eck','Deutsches Eck في Koblenz'),
 'File:Geierlay suspension bridge (Unsplash).jpg':('geierlay-bridge','جسر Geierlay في Hunsrück؛ رحلة خارج إيفل'),
 'File:Nürburgring Panorama 2011.jpg':('nuerburgring-panorama-2011','بانوراما Nürburgring من 2011؛ لا تمثل الحالة الحالية بالضرورة'),
}
def plain(s): return re.sub('<[^>]+>', '', s)
manifest=json.loads((out/'licenses-and-sources.json').read_text(encoding='utf-8')) if (out/'licenses-and-sources.json').exists() else []
thumbs={}
response=requests.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','format':'json','titles':'|'.join(chosen),'prop':'imageinfo','iiprop':'url','iiurlwidth':1280},headers={'User-Agent':'VillaLaubachResearch/1.0'},timeout=30)
if response.ok:
    for entry in response.json().get('query',{}).get('pages',{}).values():
        if 'imageinfo' in entry: thumbs[entry['title']]=entry['imageinfo'][0].get('thumburl',entry['imageinfo'][0]['url'])
for item in data:
    if item['title'] not in chosen or any(x['commons_title']==item['title'] for x in manifest): continue
    info=item['imageinfo'][0];meta=info.get('extmetadata',{})
    def value(key): return plain(meta.get(key,{}).get('value',''))
    slug,ar=chosen[item['title']]
    try:
        selected_url=thumbs.get(item['title'],info['url'])
        response=requests.get(selected_url,headers={'User-Agent':'VillaLaubachResearch/1.0'},timeout=45)
        response.raise_for_status()
        file=out/(slug+'.jpg');file.write_bytes(response.content)
        im=Image.open(file);im.verify()
        im=Image.open(file)
        row=dict(file=file.name,commons_title=item['title'],description_ar=ar,source_page=info['descriptionurl'],download_url=info['url'],artist=value('Artist'),credit=value('Credit'),license=value('LicenseShortName'),license_url=value('LicenseUrl'),date=value('DateTimeOriginal'),description=value('ImageDescription'),width=im.width,height=im.height,sha256=hashlib.sha256(response.content).hexdigest(),downloaded='2026-10-29',changes='None; original downloaded. Contact sheet uses resized preview.',publication_status='Candidate under stated file license; retain attribution and review any third-party restrictions.')
        row['download_url']=selected_url
        row['changes']='Wikimedia 1280px preview where available; local file unedited.'
        manifest.append(row)
        print('OK',slug,im.size,flush=True)
    except Exception as exc: print('FAILED',slug,str(exc),flush=True)
    time.sleep(1)
(out/'licenses-and-sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for start in range(0,len(manifest),8):
    batch=manifest[start:start+8];sheet=Image.new('RGB',(1600,340*((len(batch)+3)//4)),'#eee');draw=ImageDraw.Draw(sheet)
    for j,row in enumerate(batch):
        im=Image.open(out/row['file']);im.thumbnail((390,285));x=j%4*400;y=j//4*340;sheet.paste(im,(x,y));draw.text((x+5,y+290),row['file'][:44],fill='black');draw.text((x+5,y+310),row['license'],fill='black')
    sheet.save(out/f'contact-new-{start//8+1}.jpg')
print('TOTAL',len(manifest),flush=True)
