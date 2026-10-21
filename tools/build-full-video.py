#!/usr/bin/env python3
"""Build the complete editable review from checked narration timing and existing art.
Run after review/alignment.json has been prepared. Never modifies source recordings or intro.
"""
import json, re, difflib, math, wave
from array import array
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; V=ROOT/'videos/001-100k-salary'; OUT=V/'review'; P='videos/001-100k-salary/'

def norm(s): return re.sub(r'[^a-z0-9]', '',s.lower().replace('’',"'"))
script=(V/'script.md').read_text(); body='\n'.join(script.split('## ')[1:]); body=re.sub(r'^\d\d — .*$', '',body,flags=re.M)
words=list(re.finditer(r'\S+',body)); source=[norm(m.group()) for m in words]
segments=json.loads((OUT/'alignment.json').read_text()); heard=[w for s in segments for w in s['words']]; target=[norm(w['word']) for w in heard]
mapping={}
for b in difflib.SequenceMatcher(None,source,target,autojunk=False).get_matching_blocks():
 for k in range(b.size):mapping[b.a+k]=heard[b.b+k]['start']
known=sorted(mapping)
def wordtime(i):
 if i in mapping:return mapping[i]
 left=max((k for k in known if k<i),default=known[0]);right=min((k for k in known if k>i),default=known[-1])
 return mapping[left] if left==right else mapping[left]+(mapping[right]-mapping[left])*(i-left)/(right-left)
def cue(phrase):
 at=body.index(phrase);i=next(i for i,m in enumerate(words) if m.start()>=at);return round(wordtime(i),3)
intro=json.loads((V/'intro/project.json').read_text()); assets=intro['assets']
for key,crop in {'home':[10,20,375,310],'groceries':[820,30,315,325],'utilities':[1190,30,335,325],'debt':[20,355,365,315],'dentist':[795,365,315,300],'flight':[1150,380,375,290],'laptop':[15,690,395,310],'streaming':[430,710,340,290],'vacation':[1150,675,380,325]}.items():
 assets[key]={'src':P+'images/sheets/life-props.png','crop':crop,'label':key}
art=json.loads((V/'artwork.json').read_text())
for f in art['frames']:assets[f['id']]={'src':P+f['image'],'label':f['title']}
GREEN='#276b54';INK='#27332f';CORAL='#b65f49';CREAM='#faf6ec'
def txt(id,t,x,y,w=1080,size=78,fill=INK,enter=0):return dict(id=id,type='text',text=t,x=x,y=y,w=w,h=round(size*1.18*(t.count('\n')+1)+24),size=size,fill=fill,align='left',enter=enter,effect='slide',opacity=1,drift=0)
def img(id,a,x,y,w,h,enter=0,drift=2):return dict(id=id,type='image',asset=a,x=x,y=y,w=w,h=h,enter=enter,effect='pop',opacity=1,drift=drift)
def box(id,x,y,w,h,fill,enter=0):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=24,enter=enter,effect='fade',opacity=1,drift=0)
# Each cue is anchored to the supplied recording through script-to-recognition alignment.
shots=[]
def add(anchor,title,mode,*args):shots.append(dict(anchor=anchor,title=title,mode=mode,args=args,start=cue(anchor)))
add('Meet Alex.','Gặp Alex','hero','MEET ALEX.','$100,000 / YEAR','alex-present','paycheck')
add('Divide that by twelve','Lương trước khấu trừ mỗi tháng','hero','$100,000 ÷ 12','≈ $8,333 / MONTH','alex-think','money')
add("Except that isn't what lands",'Số tiền thực sự vào tài khoản','hero','GROSS PAY ≠\nTAKE-HOME PAY','What actually arrives?','alex-worried','phone')
add('Taxes take a portion.','Các khoản khấu trừ','trio','BEFORE THE PAYCHECK ARRIVES',[('receipt','Taxes'),('shield','Health insurance'),('piggy','Retirement')])
add("For our example, let's say",'Giả định tiền thực nhận','hero','TAKE-HOME PAY','$6,000 / MONTH','alex-present','paycheck')
add("That's an illustration",'Giới hạn ví dụ','trio','AN ILLUSTRATION, NOT EVERY PAYCHECK',[('home','Location'),('shield','Benefits'),('receipt','Tax circumstances')])
add("But here's the important part.",'Hai con số để lập ngân sách','compare','WHAT YOU HEAR','WHAT ARRIVES','$100,000 / YEAR','$6,000 / MONTH','paycheck','phone')
add('And if Alex spends based','Lập ngân sách theo số tiền thực nhận','art','02b','PLAN AROUND\nWHAT ARRIVES.','Illustrative take-home pay: $6,000 / month')
add("Now let's give that six thousand",'Ngân sách tháng','budget',-1)
add('Rent: twenty-three','Tiền thuê nhà','budget',0)
add('Transportation: eight','Chi phí đi lại','budget',1)
add('Groceries and eating','Thực phẩm và ăn ngoài','budget',2)
add('Utilities, internet','Điện nước, internet, điện thoại','budget',3)
add('Student loans or other','Khoản trả nợ','budget',4)
add('Then three hundred','Các chi phí khác','budget',5)
add('Total?','Tổng chi phí cố định','budget',6)
add('Alex has eleven hundred','Số dư sau chi phí cố định','balance',1100,'AFTER RECURRING COSTS','$6,000 − $4,900 = $1,100')
add('But notice what happened.','Lương đã được cam kết','art','03b','MOST OF IT\nIS COMMITTED.','Before the weekend even starts.')
add("The money didn't disappear.",'Danh sách chờ của tiền lương','hero',"IT DIDN’T DISAPPEAR.",'It arrived with a waiting list.','alex-worried','receipt')
add('Then real life walks in.','Những khoản chi trong năm','trio','THEN REAL LIFE WALKS IN.',[('dentist','The dentist'),('flight','A family wedding'),('laptop','A broken laptop')])
add('These expenses feel like surprises','Chi không đều nhưng có thể dự tính','art','04a','NOT EVERY MONTH.\nBUT MOST YEARS.','Irregular does not mean impossible to plan for.')
add('If Alex needs an average','Trừ chi phí không đều','balance',500,'AFTER IRREGULAR COSTS','$1,100 − $600 = $500')
add('Five hundred dollars of breathing','Khoảng thở còn lại','hero','BREATHING ROOM','$500 / MONTH','alex-think','savings')
add("And if those irregular costs aren't",'Chi phí chuyển sang thẻ tín dụng','art','04b','THIS MONTH’S COST.\nNEXT MONTH’S PAYMENT.','When irregular expenses are not planned for.')
add("That's how a decent income",'Cảm giác luôn đi sau','hero','ONE STEP BEHIND.','Even with a decent income.','alex-worried','card')
add("But there's another part",'Mức sống trước khi tăng lương','trio','BEFORE THE RAISES',[('home','A smaller apartment'),('car','An older car'),('food','An occasional treat')])
add('Then the raises started','Những lần nâng cấp','art','05a','A RAISE.\nAN UPGRADE.','Each choice had a reasonable explanation.')
add('The nicer apartment cut','Lý do nghe hợp lý','trio','EACH CHOICE MAKES SENSE',[('home','A shorter commute'),('car','More reliability'),('streaming','Only a few dollars')])
add('None of those decisions','Cam kết đi kèm tăng lương','hero','ANOTHER RAISE.\nANOTHER COMMITMENT.','The pattern is what matters.','alex-think','receipt')
add('More money came in.','Thu nhập và cam kết cùng tăng','art','05b','MORE IN.\nMORE PROMISED AWAY.','Less new breathing room than expected.')
add('This is lifestyle creep.','Lifestyle creep','hero','LIFESTYLE CREEP','Yesterday’s luxuries. Today’s normal.','alex-present','money')
add('And once a higher standard','Lùi một bước để có tự do','compare','THE UPGRADE','THE TRADE-OFF','More monthly payments','Less flexibility','receipt','savings')
add('Then Alex opens social media.','Bảng tin mạng xã hội','art','06a','THE HIGHLIGHT REEL','A house. Italy. A boat.')
add('Nobody is posting their','Những gì bảng tin không cho thấy','compare','WHAT YOU SEE','WHAT YOU DON’T','The purchase','The payments','vacation','card')
add("And a photo doesn't tell",'Nguồn tiền sau một tấm ảnh','trio','A PHOTO DOESN’T SHOW THE FUNDING',[('savings','Savings or debt?'),('gift','Family help?'),('money','A larger income?')])
add('But your brain fills','So sánh với phần mình không biết','hero','YOUR BRAIN\nFILLS THE BLANKS.','Their spending becomes your benchmark.','alex-think','phone')
add('Now your paycheck has','Hai cuộc sống','art','06b','ONE PAYCHECK.\nTWO LIVES.','The life you live. The life you feel you should live.')
add("That's an expensive comparison.",'Cái giá của sự so sánh','hero','AN EXPENSIVE\nCOMPARISON.','Choose your own starting point.','alex-worried','wallet')
add('So how does Alex get','Bắt đầu kế hoạch','hero','MAKE SOME\nBREATHING ROOM.','Start with what actually arrives.','alex-present','paycheck')
add('Build the plan around','Lập kế hoạch theo thực nhận','compare','THE JOB OFFER','YOUR MONTHLY PLAN','$100,000 / YEAR','$6,000 TAKE-HOME','paycheck','phone')
add('Then look at the biggest','Ba khoản lớn cần xem lại','trio','START WITH THE BIGGEST COMMITMENTS',[('home','Housing'),('car','Transportation'),('debt','Debt payments')])
add('Canceling a subscription','Tìm đúng nguồn gây áp lực','compare','SMALL SAVINGS','BIG PRESSURE','A cheaper subscription','An expensive car payment','streaming','car')
add('Some changes take time.','Thay đổi cần thời gian','hero','CHANGE TAKES TIME.','A lease. A repayment plan. One step at a time.','alex-think','calendar')
add('Next, stop calling predictable','Lập quỹ cho chi phí dự tính','trio','SET SOMETHING ASIDE EACH PAYDAY',[('wrench','Car repairs'),('receipt','Annual bills'),('gift','Holiday spending')])
add('When the bill arrives','Tiền đã được giao việc','hero','THE BILL ARRIVES.\nTHE MONEY IS READY.','Give predictable expenses a place in the plan.','alex-present','savings')
add('And when your income rises','Lên kế hoạch cho lần tăng lương','hero','PLAN THE RAISE\nBEFORE YOU SPEND IT.','Decide before it becomes routine.','alex-think','money')
add('Some can improve your life','Chia tăng lương cho hiện tại và tương lai','trio','GIVE THE INCREASE A JOB',[('food','Life today'),('savings','Savings & goals'),('debt','Less debt')])
add("The point isn't to reject",'Không để nâng cấp ăn hết tăng lương','art','07b','ENJOY THE UPGRADE.\nKEEP SOME FREEDOM.','Do not commit the entire raise.')
add('Of course, not every tight','Áp lực thật sự của chi phí thiết yếu','art','08a','NOT EVERY TIGHT BUDGET\nIS A LIFESTYLE PROBLEM.','Childcare. Medical needs. Family. Location.')
add("Sometimes the biggest issue",'Chi phí thiết yếu có thể rất cao','hero','ESSENTIAL COSTS\nCAN BE HIGH.','Start with your actual circumstances.','alex-think','shield')
add('But whatever the cause','Điểm bắt đầu chung','hero','WHERE IS THE MONEY\nALREADY COMMITTED?','Find the commitments first.','alex-present','receipt')
add('Because a higher salary','Thu nhập và kế hoạch','compare','A HIGHER SALARY','A WORKABLE PLAN','More options','Intentional choices','money','calendar')
add('For Alex, financial progress','Những bước tiến nhỏ','trio','PROGRESS CAN LOOK LIKE THIS',[('paid','One less payment'),('home','A smaller fixed cost'),('savings','A cash buffer')])
add('Not something impressive','Khoảng thở không cần phô trương','art','08b','ROOM TO BREATHE.','Enough space to stop feeling trapped.')
add('And that raises a better','Câu hỏi cuối','hero','A BETTER QUESTION…','More than “Do I make good money?”','alex-think','savings')
add('How much of the money','Kết video','ending','IS YOUR MONEY BUILDING\nTHE LIFE YOU ACTUALLY WANT?')

def layers(s,i):
 mode=s['mode'];a=s['args'];base=[]
 section=next((n for n,(lo,hi) in enumerate([(40.5,cue("Now let's give")),(cue("Now let's give"),cue('Then real life')),(cue('Then real life'),cue("But there's another")),(cue("But there's another"),cue('Then Alex opens')),(cue('Then Alex opens'),cue('So how does')),(cue('So how does'),cue('Of course,')),(cue('Of course,'),999)],2) if lo<=s['start']<hi),2)
 labels={2:'THE PAYCHECK',3:'THE WAITING LIST',4:'IRREGULAR EXPENSES',5:'LIFESTYLE CREEP',6:'THE COMPARISON',7:'THE PLAN',8:'BREATHING ROOM'}
 base.append(txt('chapter',f'{section:02d}  /  {labels[section]}',90,45,1740,25,GREEN))
 if mode=='hero':
  title,sub,pose,prop=a
  base += [img('alex',pose,75,245,480,720,0,3),txt('headline',title,650,180,1180,92),box('card',625,485,1190,220,'#e2ecda',.18),txt('message',sub,675,530,1080,57,GREEN,.25),img('prop',prop,1110,755,330,230,.5)]
 elif mode=='trio':
  title,items=a;base += [txt('headline',title,100,155,1720,72)]
  for j,(prop,label) in enumerate(items):
   x=110+j*585;base += [box('tile'+str(j),x,355,535,570,'#eee8d8',j*.45),img('prop'+str(j),prop,x+80,400,370,300,j*.45+.15),txt('label'+str(j),label,x+35,760,465,44,INK,j*.45+.3)]
 elif mode=='compare':
  left,right,lv,rv,lp,rp=a
  for j,(label,value,prop) in enumerate([(left,lv,lp),(right,rv,rp)]):
   x=110+j*890;base += [box('panel'+str(j),x,200,810,730,'#eee8d8' if j==0 else '#e2ecda',j*.3),txt('label'+str(j),label,x+40,245,730,48),img('prop'+str(j),prop,x+230,370,350,300,j*.3+.2),txt('value'+str(j),value,x+45,745,720,58,GREEN if j else CORAL,j*.3+.35)]
 elif mode=='art':
  frame,title,sub=a
  if frame=='05b':
   base=[img('illustration',frame,0,0,1920,1080,0,1),box('paper',1135,190,745,740,CREAM),txt('headline',title,1190,270,645,68,GREEN,.15),txt('message',sub,1190,650,630,39,INK,.5)]
  else:
   base=[img('illustration',frame,0,70,1920,1000,0,1),box('paper',0,0,1920,310,CREAM),txt('headline',title,90,55,1740,64,GREEN,.1),txt('message',sub,95,225,1730,34,INK,.4)]
 elif mode=='budget':
  upto=a[0];base += [txt('headline','WHERE $6,000 GOES',100,125,1720,76),txt('note','Illustrative monthly budget',105,230,1600,34,GREEN)]
  rows=[('home','Rent',2300),('car','Transportation',850),('groceries','Food',650),('utilities','Utilities / internet / phone',400),('debt','Debt payments',400),('gift','Other',300)]
  for j,(prop,label,value) in enumerate(rows):
   x=100+(j%3)*585;y=330+(j//3)*290;active=j<=upto
   base += [box('tile'+str(j),x,y,545,255,'#e2ecda' if active else '#eee8d8'),img('icon'+str(j),prop,x+15,y+25,150,150),txt('category'+str(j),label,x+180,y+35,340,30),txt('amount'+str(j),f'${value:,}' if active else '—',x+180,y+105,340,61,GREEN if active else '#8b8c80',.2 if j==upto else 0)]
  total=sum(r[2] for r in rows[:max(0,upto+1)]);base += [txt('running',f'COMMITTED: ${total:,}     |     LEFT: ${6000-total:,}',110,950,1700,45,GREEN,.4)]
 elif mode=='balance':
  amount,label,equation=a;base += [txt('headline',label,100,140,1720,69),txt('equation',equation,110,270,1700,100,GREEN,.15),box('track',110,520,1700,115,'#e5dfd0'),box('committed',110,520,1700*(6000-amount)/6000,115,'#d48a73',.3),box('available',110+1700*(6000-amount)/6000,520,1700*amount/6000,115,'#719e7c',.5),txt('legend','Committed / planned costs',110,680,1100,44,CORAL),txt('left',f'${amount:,} LEFT',1250,680,560,60,GREEN,.5),img('alex','alex-think',500,760,220,250),img('jar','savings',1000,760,250,250)]
 elif mode=='ending':
  base=[img('illustration','08b',0,100,1920,980,0,1),box('paper',0,0,1920,355,CREAM),txt('question',a[0],110,75,1700,76,GREEN)]
 return base
reveals={
 'Các khoản khấu trừ':['Taxes take a portion.','Health insurance takes another.','Retirement contributions may'],
 'Những khoản chi trong năm':['A trip to the dentist.','A flight to a family wedding.','A laptop that decides'],
 'Mức sống trước khi tăng lương':['The apartment was smaller.','The car was older.','Dinner delivery was'],
 'Lý do nghe hợp lý':['The nicer apartment cut','The newer car felt','The extra subscriptions were'],
 'Ba khoản lớn cần xem lại':['Housing.','Transportation.','Debt payments.'],
 'Những bước tiến nhỏ':['one less payment,','a smaller fixed expense,','or a cash buffer'],
 'Chia tăng lương cho hiện tại và tương lai':['Some can improve your life','Some can build savings,','reduce debt,'],
 'Lập quỹ cho chi phí dự tính':['Car repairs,','annual bills,','and holiday spending'],
}
clips=intro['clips'].copy()
with wave.open(str(next((V/'audio').glob('*.wav')))) as wav:
 total=wav.getnframes()/wav.getframerate();samples=array('h',wav.readframes(wav.getnframes()))
for i,s in enumerate(shots):
 end=shots[i+1]['start'] if i+1<len(shots) else total
 start=40.5 if i==0 else s['start'];dur=round(end-start,6)
 assert dur>=.5,(s,dur)
 items=layers(s,i)
 if s['title'] in reveals:
  for j,phrase in enumerate(reveals[s['title']]):
   for item in items:
    if item['id'] in (f'tile{j}',f'prop{j}',f'label{j}'):
     item['enter']=round(max(0,cue(phrase)-start),3)
 clips.append(dict(id=f'full-{i+9:02d}',title=s['title'],duration=dur,background=CREAM,fade=.12 if i+1<len(shots) else 0,layers=items))
block=math.ceil(len(samples)/1200);peaks=[]
for i in range(1200):
 chunk=samples[i*block:(i+1)*block];peaks.append(round(min(1,math.sqrt(sum(v*v for v in chunk)/max(1,len(chunk)))/7000),3))
# Captions retain script spelling, with boundaries mapped to recognition word timestamps.
captions=[]
for sentence in re.finditer(r'[^.!?]+[.!?]+(?:[”\"])?',body):
 content=sentence.group().strip()
 if not content:continue
 ids=[i for i,m in enumerate(words) if m.start()>=sentence.start() and m.start()<sentence.end()]
 if not ids:continue
 start=wordtime(ids[0]);last=ids[-1];end=wordtime(last)+.3
 if last+1<len(words):end=min(end,wordtime(last+1)-.04)
 if end<=start:end=start+.5
 captions.append(dict(start=round(start,3),end=round(min(total,end),3),text=content))
# Preserve the manually checked intro captions.
captions=intro['captions']+[c for c in captions if c['start']>=40.5]
project={**intro,'revision':'full-review-v01','name':'Video 001 — Bản duyệt đầy đủ 8 phút 06 giây','assets':assets,'clips':clips,'audio':{'src':P+'review/voiceover.mp3','offset':0,'volume':1},'captions':captions,'waveform':peaks,'waveformDuration':total}
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in captions:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
lines=['# Bản duyệt đầy đủ v01','',f'Thời lượng {total:.3f} giây; {len(clips)} cảnh; {len(captions)} đoạn phụ đề. Giữ nguyên 8 cảnh mở đầu.','', '| Bắt đầu | Kết thúc | Cảnh |','|---|---|---|']
t=0
for c in clips:lines.append(f'| {stamp(t)} | {stamp(t+c["duration"])} | {c["title"]} |');t+=c['duration']
lines += ['','Audio MP3 dẫn xuất từ WAV gốc, không cắt bỏ nội dung. Mốc từ nhận dạng tự động bằng faster-whisper base.en, đối chiếu với script; có sai số ở mức từ. Phụ đề có thể bật/tắt trong Studio. Không có nhạc nền. Chuyển động lớp 2D, chưa có rig khớp nhân vật.','', 'Biểu đồ ngân sách thể hiện đúng tỉ lệ $6,000: chi cố định $4,900, còn $1,100; dự trù không đều $600, còn $500. Các khoản khấu trừ không được gán tỉ lệ thuế giả định.','', 'Chạy lại: `python3 tools/build-full-video.py`. Lệnh thay bản JSON/VTT dẫn xuất trong review, không thay intro hay WAV gốc.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
print(f'Built {len(clips)} scenes, {t:.3f}s, {len(captions)} captions; script matched {len(mapping)}/{len(words)} words.')
