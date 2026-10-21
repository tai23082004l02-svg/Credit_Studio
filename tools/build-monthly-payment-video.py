#!/usr/bin/env python3
"""Build the narrated review from preserved assets and word alignment, without changing WAV/artwork."""
import json,re,math,wave,difflib,hashlib,argparse
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'videos/002-monthly-payment-trap';P='videos/002-monthly-payment-trap/';OUT=V/'review'
parser=argparse.ArgumentParser();parser.add_argument('--force',action='store_true');args=parser.parse_args()
if (OUT/'project.json').exists() and not args.force:raise SystemExit('Review exists. Back up edits first; --force rebuilds derived review files only.')
script=(V/'script.md').read_text();body='\n\n'.join(part.split('\n',1)[1] for part in script.split('## ')[1:])
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('’',"'"))
tokens=list(re.finditer(r'\S+',body));source=[norm(t.group()) for t in tokens]
segments=json.loads((OUT/'alignment.json').read_text());heard=[w for s in segments for w in s['words']];target=[norm(w['word']) for w in heard]
mapping={}
for block in difflib.SequenceMatcher(None,source,target,autojunk=False).get_matching_blocks():
 for k in range(block.size):mapping[block.a+k]=heard[block.b+k]
known=sorted(mapping)
def wt(i):
 if i in mapping:return mapping[i]['start']
 lo=max((k for k in known if k<i),default=known[0]);hi=min((k for k in known if k>i),default=known[-1])
 return mapping[lo]['start'] if lo==hi else mapping[lo]['start']+(mapping[hi]['start']-mapping[lo]['start'])*(i-lo)/(hi-lo)
times=[wt(i) for i in range(len(tokens))]
assert all(a<=b for a,b in zip(times,times[1:])),'Non-monotonic word mapping'
def cue(phrase):
 query=[norm(x) for x in phrase.split()]
 candidates=[i for i in range(len(source)-len(query)+1) if source[i:i+len(query)]==query]
 assert len(candidates)==1,(phrase,candidates)
 return round(times[candidates[0]],3)
with wave.open(str(V/'audio/monthly-payment-trap-voiceover.wav')) as wav:
 total=wav.getnframes()/wav.getframerate();samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)
INK='#27332f';GREEN='#286a52';CORAL='#bd6555';BG='#faf6ec';MINT='#e2ecdd';SAND='#eee7d8'
catalog=json.loads((ROOT/'library/props/catalog.json').read_text())['items']
assets={p['id']:{'src':p['src'],'label':p['name'],**({'crop':p['crop']} if 'crop'in p else {})} for p in catalog}
layout=json.loads((V/'asset-layout.json').read_text())
for sheet in layout['sheets']:
 for item in sheet['items']:assets[item['id']]={'src':P+item['image'],'label':item['name']}
for j in layout['jobs']:assets['art-'+j['id']]={'src':P+j['image'],'label':j['title']}
def A(slug):return 'mpt-'+slug
chapters=['THE PAYMENT TRAP','THE EASIER QUESTION','THE CROWDED MONTH','THE TOTAL COST','THE TIMING PROBLEM','WHEN PAYMENTS HELP','THE WHOLE MONTH','ROOM FOR LIFE']
shots=[]
def add(section,anchor,title,mode,headline,**kw):shots.append(dict(section=section,anchor=anchor,title=title,mode=mode,headline=headline,start=cue(anchor),**kw))
def hero(s,a,t,h,message,pose='alex-phone',prop='new-phone',detail=''):add(s,a,t,'hero',h,message=message,pose=A(pose),prop=A(prop),detail=detail)
def art(s,a,t,h,key,detail=''):add(s,a,t,'art',h,art='art-'+key,detail=detail)
def card(icon,label,value='',detail='',reveal=None):return dict(icon=A(icon),label=label,value=value,detail=detail,reveal=reveal)
def cards(s,a,t,h,items,note=''):add(s,a,t,'cards',h,items=items,note=note)
def mathshot(s,a,t,h,equation,detail,icon='cash-stack'):add(s,a,t,'math',h,equation=equation,detail=detail,icon=A(icon))

# 01 — The hook: visual changes follow the individual spoken examples.
hero(1,'You didn’t buy anything','Cảm giác vẫn mua trong khả năng','IT FELT AFFORDABLE.','SO WHY SO LITTLE LEFT?',prop='empty-wallet',detail='One manageable payment at a time.')
hero(1,'The phone was only','Điện thoại chỉ thêm một chút','JUST A LITTLE MORE EACH MONTH.','THE PHONE',prop='new-phone')
hero(1,'The car payment fit','Khoản trả xe vừa ngân sách','IT FIT THE BUDGET.','THE CAR PAYMENT',prop='compact-car')
cards(1,'And those four easy payments?','Bốn khoản trả nghe rất nhẹ','FOUR EASY PAYMENTS?', [card('parcel','A SMALLER PAYMENT'),card('bank-card','STILL A PURCHASE')])
hero(1,'So why does payday arrive','Câu hỏi về ngày lương','PAYDAY ARRIVES.\nWHAT CAN YOU ACTUALLY USE?','WHERE DID IT GO?',pose='alex-receipt',prop='empty-wallet')
hero(1,'Meet Alex.','Alex nhận lương','MEET ALEX.','PAYCHECK RECEIVED',prop='pay-envelope')
art(1,'Then the automatic payments start.','Các khoản tự động lấy tiền','THEN THE PAYMENTS START.','01a')
cards(1,'Alex hasn’t gone on a shopping spree.','Các quyết định nhỏ cộng dồn','NO SHOPPING SPREE.\nJUST A SERIES OF COMMITMENTS.',[card('new-phone','ONE PAYMENT'),card('compact-car','ANOTHER PAYMENT'),card('parcel','AND ANOTHER')])
hero(1,'And that’s the monthly payment trap.','Bẫy trả tiền hằng tháng','THE MONTHLY PAYMENT TRAP.','YOUR FUTURE INCOME',pose='alex-receipt',prop='padlock')
# 02 — Purchase price, monthly presentation and upgrades.
hero(2,'Alex needs a new phone.','Điện thoại cũ cần thay','A REPLACEMENT MAKES SENSE.','A CRACKED SCREEN.\nA WEAK BATTERY.',prop='old-phone',pose='alex-compare')
art(2,'At checkout, there are two ways','Hai cách nhìn cùng điện thoại','ONE PHONE. TWO PRICE FRAMES.','02a')
mathshot(2,'Nine hundred dollars today.','Giá mua ngay','PAY TODAY.','$900','The full purchase price.','new-phone')
mathshot(2,'Or thirty-seven dollars','Khoản trả mỗi tháng','PAY OVER TWO YEARS.','$37.50 / month','24 monthly payments.','new-phone')
cards(2,'Same price, assuming no interest or fees.','Cùng tổng tiền nếu không lãi phí','SAME PRICE.\nVERY DIFFERENT FEELING.',[card('new-phone','PAY TODAY','$900'),card('new-phone','24 MONTHS','$37.50 / month','$37.50 × 24 = $900')],'Assumes no interest or fees · Hypothetical example')
hero(2,'Nine hundred dollars makes Alex','Cảm giác của con số nhỏ','THE SMALLER NUMBER FEELS EASIER.','THE BUDGET CAN ABSORB IT?',pose='alex-compare',prop='comparison-cards')
cards(2,'Then come the questions.','Những lần nâng cấp','MORE STORAGE?\nA BETTER CAMERA?',[card('new-phone','THE BASE MODEL'),card('new-phone','THE UPGRADE')])
mathshot(2,'When the difference gets divided','Chia nhỏ chi phí nâng cấp','THE UPGRADE STARTS LOOKING SMALL.','EXTRA COST ÷ 24','Still part of the full purchase price.','comparison-cards')
hero(2,'Instead of asking,','Câu hỏi về tổng giá','“HOW MUCH DO I WANT\nTO SPEND ON A PHONE?”','THE FULL PRICE',pose='alex-compare',prop='new-phone')
hero(2,'Alex starts asking,','Câu hỏi chuyển sang hằng tháng','“HOW MUCH MORE\nCAN I HANDLE EACH MONTH?”','THE MONTHLY PAYMENT',pose='alex-phone',prop='calendar')
art(2,'And that second question','Quyết định mua trở nên dễ hơn','AN EXPENSIVE PURCHASE.\nAN EASIER-LOOKING DECISION.','02a')
# 03 — Show each real example at its spoken amount, then the full sum.
art(3,'Now look at the rest','Nhìn toàn bộ tháng','NOW LOOK AT THE WHOLE MONTH.','03a')
mathshot(3,'A car payment:','Khoản trả xe','THE CAR PAYMENT.','$525','Due each month in this example.','compact-car')
mathshot(3,'The phone installment:','Khoản trả điện thoại','THE PHONE INSTALLMENT.','$37.50','Due each month in this example.','new-phone')
mathshot(3,'A furniture payment:','Khoản trả nội thất','THE FURNITURE PAYMENT.','$90','Due each month in this example.','sofa')
mathshot(3,'Several buy-now-pay-later purchases,','Tổng kỳ BNPL đến hạn','BUY NOW. PAY LATER.','$120','Installments due THIS month.','parcel')
mathshot(3,'And forty-five dollars in subscriptions.','Đăng ký dịch vụ','THE SUBSCRIPTIONS.','$45','Recurring services in this example.','streaming')
mathshot(3,'That adds up to','Tổng cam kết trong tháng','TOGETHER, THEY ADD UP.','$817.50','525 + 37.50 + 90 + 120 + 45','receipt')
cards(3,'Before rent.','Chưa tính sinh hoạt thiết yếu','BEFORE THE REST OF LIFE.',[dict(icon='home',label='RENT',value='',detail='',reveal='Before rent.'),dict(icon='groceries',label='GROCERIES',value='',detail='',reveal='Before groceries.'),card('compact-car','UTILITIES, INSURANCE\nAND GAS',reveal='Before utilities,')])
cards(3,'These payments aren’t all the same.','Các nghĩa vụ khác nhau','SAME CASH FLOW.\nDIFFERENT OBLIGATIONS.',[card('streaming','SUBSCRIPTIONS','Often cancelable',reveal='A subscription can often'),card('bank-card','LOAN BALANCES','Still owed',reveal='A loan balance still'),card('receipt','INSTALLMENT PLANS','Check interest',reveal='Some installment plans')])
hero(3,'But every one of them','Tất cả đều chiếm chỗ trong dòng tiền','EVERY PAYMENT NEEDS SPACE.','IN THE SAME CASH FLOW',pose='alex-receipt',prop='pay-envelope')
cards(3,'And they didn’t arrive together.','Các khoản được thêm ở những thời điểm khác','SEPARATE DECISIONS.\nONE SHARED MONTH.',[card('compact-car','THE CAR CAME FIRST',reveal='The car came first.'),card('new-phone','SIX MONTHS LATER',reveal='The phone came six months'),card('sofa','AFTER A MOVE',reveal='The furniture showed up')])
hero(3,'Each decision was made','Chỉ nhìn khoản trả trước mắt','ONE PAYMENT IN FRONT OF YOU.','THE REST IS STILL THERE.',pose='alex-compare',prop='bank-card')
art(3,'Now all those decisions','Các quyết định gặp nhau trên lịch','ALL ON THE SAME CALENDAR.','03a')
# 04 — Exact arithmetic stays editable, and metaphors are separate.
hero(4,'This gets especially important','Nhìn ra ngoài khoản trả tháng','LOOK PAST THE MONTHLY NUMBER.','WHEN BORROWING IS INVOLVED',pose='alex-compare',prop='receipt')
mathshot(4,'Imagine Alex is comparing','Giá mua minh họa','A HYPOTHETICAL PURCHASE.','$1,800','Compare the full financing arrangement.','comparison-cards')
mathshot(4,'One option is seventy-five','Lựa chọn 24 tháng','OPTION ONE.','$75 × 24 = $1,800','24 months · Total payments: $1,800','calendar')
mathshot(4,'Another is sixty dollars','Lựa chọn 36 tháng','OPTION TWO.','$60 × 36 = $2,160','36 months · Total payments: $2,160','calendar')
cards(4,'The second option frees up','Thấp hơn mỗi tháng, cao hơn tổng tiền','A SMALLER PAYMENT.\nA BIGGER TOTAL.',[card('coins','EACH MONTH','$15 LESS',reveal='The second option frees up'),card('calendar','OVERALL','$360 MORE','And another year.',reveal='But Alex pays three hundred')],'Simplified hypothetical financing · Not an actual offer')
cards(4,'These are simplified examples,','Điều khoản thực tế khác nhau','REAL FINANCING DEPENDS ON…',[card('bank-card','THE RATE'),card('receipt','THE FEES'),card('clipboard','THE CONTRACT')],'Examples illustrate the comparison; actual terms vary.')
art(4,'A smaller monthly payment can come','Khoản trả nhỏ có nhiều nguyên nhân','A BETTER DEAL?\nOR A LONGER COMMITMENT?','04a','Calendar paths are visual metaphors, not a scale diagram.')
cards(4,'You need the total cost','Hai con số phải xem cùng nhau','TOTAL COST + PAYOFF DATE.',[card('calendar','24 MONTHS','$75 / month','Total: $1,800'),card('calendar','36 MONTHS','$60 / month','Total: $2,160')],'Hypothetical financing · Read actual rates, fees and terms.')
hero(4,'Otherwise, the easiest number','Một con số không đủ quyết định','ONE NUMBER\nISN’T THE WHOLE DEAL.','COMPARE THE COMMITMENT.',pose='alex-compare',prop='comparison-cards')
# 05 — Cash timing, without fabricated overdraft certainty.
art(5,'Then Alex needs a car repair.','Phát sinh sửa xe','A REPAIR THAT CAN’T WAIT.','05a')
hero(5,'The problem isn’t just the repair itself.','Vấn đề là tháng đã kín lịch','THE MONTH ALREADY\nHAS APPOINTMENTS.','$600 REPAIR',pose='alex-repair',prop='wrench')
cards(5,'The car payment is due Tuesday.','Lịch các khoản đến hạn','THE DUE DATES KEEP COMING.',[card('compact-car','TUESDAY','$525',reveal='The car payment is due Tuesday.'),card('sofa','THURSDAY','$90',reveal='The furniture payment comes out'),card('parcel','NEXT WEEK','MORE DUE',reveal='Two installment purchases')],'Illustrative due dates from Alex’s story')
cards(5,'Alex may earn enough','Có đủ cả tháng nhưng thiếu đúng ngày','THE TOTAL IS ONE QUESTION.\nTHE TIMING IS ANOTHER.',[card('pay-envelope','OVER THE MONTH','ENOUGH?'),card('clock','ON THE RIGHT DAY','AVAILABLE?')])
hero(5,'And automatic payments don’t know','Thanh toán tự động vẫn đến','AUTO PAY\nDOESN’T KNOW ABOUT THE REPAIR.','THE MECHANIC NEEDED PAYING.',pose='alex-repair',prop='calendar')
cards(5,'Depending on the account','Hậu quả có thể có khi hụt tiền','WHAT A SHORTFALL CAN MEAN.',[card('alert-bell','AN OVERDRAFT'),card('receipt','A LATE FEE'),card('bank-card','ANOTHER CARD BILL')],'Depends on the account, agreement and circumstances.')
hero(5,'One unexpected expense can expose','Một lần phát sinh bộc lộ khoảng trống','ONE EXPENSE.\nVERY LITTLE FLEXIBILITY.','HOW MUCH ROOM WAS LEFT?',pose='alex-repair',prop='empty-wallet')
cards(5,'The payments were manageable.','Khoản trả và cả tháng','THE PAYMENTS WERE MANAGEABLE.\nTHE MONTH WASN’T.',[card('bank-card','EACH PAYMENT'),card('calendar','THE WHOLE MONTH')])
# 06 — Balanced treatment of useful financing.
art(6,'Paying over time can be useful.','Trả dần có thể hữu ích','PAYMENTS CAN BE USEFUL.','06a')
hero(6,'A reliable car may be necessary','Xe cần thiết để đi làm','A RELIABLE CAR\nMAY BE NECESSARY FOR WORK.','A PRACTICAL NEED',pose='alex-compare',prop='compact-car')
cards(6,'An interest-free installment plan','Khi kế hoạch không tăng giá mua','PRESERVE CASH.\nCHECK THE TERMS.',[card('savings-jar','CASH AVAILABLE TODAY'),card('refrigerator','THE SAME PURCHASE PRICE')],'Only if there is no added cost and the payments fit.')
hero(6,'The useful question is what','Xem tác động lên tài chính','WHAT DOES THIS ARRANGEMENT\nDO TO YOUR FINANCES?','LOOK AT THE WHOLE DEAL.',pose='alex-plan',prop='clipboard')
hero(6,'Would Alex still choose','Có muốn mua ở giá đầy đủ không','WOULD YOU STILL CHOOSE IT\nAT THE FULL PRICE?','THE FULL PRICE',pose='alex-compare',prop='bank-card')
hero(6,'Does financing add interest','Kiểm tra lãi và phí','DOES FINANCING\nADD INTEREST OR FEES?','THE TOTAL COST',pose='alex-plan',prop='receipt')
hero(6,'Will the payments still fit','Tháng tốn kém hơn có trả được không','WILL IT FIT\nA MORE EXPENSIVE MONTH?','THE LESS-PERFECT MONTH',pose='alex-plan',prop='calendar')
hero(6,'And will there be money left','Còn tiền cho chuyện ngoài kế hoạch không','WILL THERE BE MONEY LEFT\nFOR THE REST OF LIFE?','LEAVE SOME ROOM.',pose='alex-buffer',prop='savings-jar')
hero(6,'Those questions leave room','Ra quyết định với đủ thông tin','PRACTICAL BORROWING.\nA CLEARER DECISION.','MORE THAN A MONTHLY NUMBER',pose='alex-compare',prop='comparison-cards')
# 07 — Actionable inventory and a buffer, no invented loan balances.
art(7,'So Alex tries something different.','Alex lập một danh sách','BEFORE THE NEXT PURCHASE: ONE LIST.','07a')
cards(7,'Every installment.','Liệt kê các nghĩa vụ','PUT EVERY COMMITMENT ON THE LIST.',[card('parcel','INSTALLMENTS',reveal='Every installment.'),card('bank-card','MINIMUM DEBT PAYMENTS',reveal='Every minimum debt payment.'),card('streaming','RECURRING SUBSCRIPTIONS',reveal='Every recurring subscription.')])
cards(7,'Next to each one:','Những cột cần ghi','RECORD THE DETAILS.',[card('coins','AMOUNT'),card('clock','DUE DATE'),card('receipt','REMAINING BALANCE'),card('calendar','PAYOFF DATE')],'Include balances and payoff dates where applicable.')
art(7,'For the first time, Alex','Nhìn được cả tháng','THE WHOLE MONTH.\nIN ONE VIEW.','07a')
cards(7,'Then Alex looks at the next','Nhìn cả những tháng sau','HOW LONG WILL IT LAST?',[card('parcel','A SHORT-TERM PLAN','MAY END SOON'),card('compact-car','A CAR LOAN','MAY LAST YEARS')])
cards(7,'Before adding another payment,','Kiểm tra trước khoản trả mới','BEFORE ADDING A PAYMENT…',[card('bank-card','FULL PURCHASE PRICE'),card('receipt','TOTAL FINANCING COST'),card('savings-jar','ESSENTIALS + SAVINGS')])
hero(7,'There’s also a little room','Chừa chỗ cho tháng không hoàn hảo','LEAVE ROOM\nFOR AN IMPERFECT MONTH.','A LITTLE FLEXIBILITY',pose='alex-buffer',prop='savings-jar')
cards(7,'And when an old payment finally ends,','Dừng trước khi thay khoản trả cũ','A PAYMENT ENDS.\nPAUSE BEFORE REPLACING IT.',[card('receipt','THE OLD PAYMENT'),card('broken-chain','ROOM OPENS UP'),card('savings-jar','KEEP SOME OF IT')])
hero(7,'For a while, that money goes','Chuyển tiền sang quỹ đệm','GIVE THAT MONEY\nTO YOUR CASH BUFFER.','KEEP THE ROOM.',pose='alex-buffer',prop='savings-jar')
cards(7,'The paycheck stays the same.','Thu nhập như cũ, tiền tự do nhiều hơn','SAME PAYCHECK.\nMORE AVAILABLE.',[card('pay-envelope','THE SAME INCOME'),card('cash-tray','MORE FLEXIBILITY')])
# 08 — Close with three distinct questions and an unclipped full character.
hero(8,'There’s a reason monthly payments','Vì sao con số nhỏ nghe dễ chịu','ONE LARGE DECISION.\nA SMALLER-LOOKING COMMITMENT.','THE MONTHLY FRAME',prop='new-phone')
cards(8,'Sometimes that commitment is useful.','Cam kết có ích hoặc kéo dài','SOMETIMES USEFUL.\nSOMETIMES LONG-LASTING.',[card('refrigerator','A USEFUL ARRANGEMENT'),card('calendar','AFTER THE EXCITEMENT')])
hero(8,'Alex doesn’t need to avoid','Không phải từ chối mọi khoản vay','NO NEED TO REJECT\nEVERY EXPENSIVE NECESSITY.','UNDERSTAND THE TRADE.',pose='alex-compare',prop='refrigerator')
art(8,'Alex needs a clear view','Nhìn rõ thu nhập tương lai đã cam kết','HOW MUCH FUTURE INCOME\nIS ALREADY SPOKEN FOR?','03a')
cards(8,'Because getting approved','Được duyệt không nói hết ngân sách','APPROVED?\nHOW WILL IT FIT YOUR LIFE?',[card('bank-card','WHAT A LENDER WILL OFFER'),card('calendar','EVERYTHING ELSE YOU PAY')])
hero(8,'Before the next “only forty-nine','Nhìn những tháng của khoản trả mới','BEFORE “ONLY $49 A MONTH”…','LOOK AT THE MONTHS.',pose='alex-plan',prop='calendar')
mathshot(8,'What will you pay in total?','Câu hỏi về tổng chi phí','WHAT WILL YOU PAY IN TOTAL?','THE FULL COST','Not just the next payment.','cash-stack')
hero(8,'What else will need that money?','Câu hỏi về những nhu cầu khác','WHAT ELSE\nWILL NEED THAT MONEY?','YOUR OTHER PRIORITIES',pose='alex-plan',prop='savings-jar')
hero(8,'And when the payment is finally gone,','Câu hỏi về giá trị đánh đổi','WHEN THE PAYMENT IS GONE,\nWILL THE TRADE FEEL WORTH IT?','THINK BEYOND CHECKOUT.',pose='alex-compare',prop='comparison-cards')
art(8,'The goal is to leave enough','Giữ chỗ cho cuộc sống','LEAVE ROOM\nFOR LIFE BETWEEN PURCHASES.','08a')

# Verify every borrowed legacy prop ID explicitly instead of silently substituting imagery.
ids=set(assets)
for s in shots:
 for item in s.get('items',[]):assert item['icon'] in ids,(item['icon'],sorted(ids))

def text(id,content,x,y,w,size=60,fill=INK,enter=0,effect='fade',align='center'):
 return dict(id=id,type='text',text=content,x=x,y=y,w=w,h=math.ceil(size*1.18*(content.count('\n')+1)+18),size=size,fill=fill,align=align,enter=enter,effect=effect,opacity=1,drift=0)
def image(id,asset,x,y,w,h,enter=0,effect='pop',drift=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=enter,effect=effect,opacity=1,drift=drift)
def box(id,x,y,w,h,fill,enter=0):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=24,enter=enter,effect='fade',opacity=1,drift=0)
def local(phrase,s):return round(max(0,cue(phrase)-s['start']),3)
def layers(s):
 out=[text('chapter',f'{s["section"]:02d}  /  {chapters[s["section"]-1]}',80,35,1760,24,GREEN,effect='none',align='left'),text('headline',s['headline'],85,100,1750,66,effect='none')]
 mode=s['mode']
 if mode=='hero':
  out += [box('panel',700,330,1110,570,MINT),image('alex',s['pose'],100,300,480,650,0,'pop',1),image('prop',s['prop'],1075,350,360,240,.08,'pop'),text('message',s['message'],735,640,1040,56,GREEN,.15)]
  if s.get('detail'):out.append(text('detail',s['detail'],740,805,1030,37,INK,.25))
 elif mode=='art':
  art_height=600 if s['section']==5 and s['anchor'].startswith('Then Alex needs') else 650
  out.append(image('illustration',s['art'],80,285,1760,art_height,.02,'fade',1))
  if s.get('detail'):out.append(text('detail',s['detail'],100,968,1720,28,GREEN,.1))
  if s['section']==5 and s['anchor'].startswith('Then Alex needs'):
   out += [box('repair-price',750,900,420,85,MINT,local('Six hundred dollars.',s)),text('repair-amount','$600',780,913,360,56,CORAL,local('Six hundred dollars.',s))]
 elif mode=='math':
  out += [image('math-icon',s['icon'],785,292,350,225,.02),box('equation-panel',120,565,1680,190,MINT,.04),text('equation',s['equation'],155,605,1610,92,GREEN,.12),text('explanation',s['detail'],140,824,1640,44,INK,.2)]
 elif mode=='cards':
  items=s['items'];n=len(items);gap=36;w=(1740-gap*(n-1))/n
  for i,it in enumerate(items):
   x=90+i*(w+gap);enter=local(it['reveal'],s) if it.get('reveal') else round(.12*i,3)
   # Backgrounds and labels are also delayed: a card never hints at an unspoken number.
   out += [box(f'card-{i}',x,335,w,570,MINT if i%2 else SAND,enter),image(f'icon-{i}',it['icon'],x+40,375,w-80,200,enter+.06),text(f'label-{i}',it['label'],x+20,625,w-40,34 if n>=4 else 39,INK,enter+.08)]
   if it.get('value'):out.append(text(f'value-{i}',it['value'],x+20,748,w-40,44 if n>=3 else 54,GREEN if i==0 else CORAL,enter+.1))
   if it.get('detail'):out.append(text(f'detail-{i}',it['detail'],x+22,842,w-44,30,INK,enter+.14))
  if s.get('note'):out.append(text('note',s['note'],100,968,1720,28,GREEN,.1))
 return out

assert 0<len(shots)<=100
shots[0]['start']=0
assert all(a['start']<b['start'] for a,b in zip(shots,shots[1:])),[(s['title'],s['start']) for s in shots]
clips=[]
for i,s in enumerate(shots):
 end=shots[i+1]['start'] if i+1<len(shots) else total;length=round(end-s['start'],6)
 assert .5<=length<=120,(s['title'],length)
 ll=layers(s)
 for l in ll:
  assert l['enter']<length-.05,(s['title'],l['id'],l['enter'],length)
 clips.append(dict(id=f'mpt-review-{i+1:03d}',title=s['title'],duration=length,background=BG,fade=.08 if i else 0,layers=ll))

# Captions use approved spelling and recognition timing; do not invent missing voice content.
caps=[];group=[]
def flush():
 if not group:return
 first,last=group[0],group[-1];start=times[first];wordend=mapping[last]['end'] if last in mapping else times[last]+.25
 end=min(total,max(start+.18,wordend+.22),times[last+1]-.025 if last+1<len(tokens) else total)
 if end>start:caps.append(dict(start=round(start,3),end=round(end,3),text=' '.join(tokens[j].group() for j in group)))
 group.clear()
for i,t in enumerate(tokens):
 group.append(i)
 if len(group)>=14 or (len(group)>=3 and re.search(r'[.!?][”\"]?$',t.group())):flush()
flush()
peaks=[]
for chunk in np.array_split(samples,1400):peaks.append(round(min(1,float(np.sqrt(np.mean(chunk*chunk)))/7000),3))
used={l['asset'] for c in clips for l in c['layers'] if l['type']=='image'}
project=dict(kind='credit-studio-video',version=1,revision='monthly-payment-review-v01',name='Monthly Payment Trap — Bản duyệt đầy đủ v01',width=1920,height=1080,fps=30,audio=dict(src=P+'review/voiceover.mp3',offset=0,volume=1),assets={k:v for k,v in assets.items() if k in used},clips=clips,captions=caps,showCaptions=False,waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
shotdata=[dict(**s,end=round(s['start']+clips[i]['duration'],6),clipId=clips[i]['id']) for i,s in enumerate(shots)]
(OUT/'shot-plan.json').write_text(json.dumps(shotdata,ensure_ascii=False,indent=2)+'\n')
lines=['# Video 002 — Bản duyệt đầy đủ v01','',f'**{total:.3f} giây · {len(clips)} cảnh · 1920×1080 · 30 fps.** Căn theo WAV gốc; không phải bảng hình 96 giây.','', 'Dự án chỉnh được: `project.json`. Audio dẫn xuất chuẩn hóa: `voiceover.mp3`. WAV và bảng hình/thiết kế cũ được giữ nguyên. MP4: `../exports/full-review-v01.mp4`.','', '| Bắt đầu | Kết thúc | Cảnh |','|---|---|---|']
for s in shotdata:lines.append(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["title"]} |')
lines += ['','Chữ Times New Roman; tiêu đề tách khỏi nhân vật, hình/nhãn căn giữa. Hiệu ứng lớp fade/pop và drift nhẹ, chưa rig khớp. Chưa có nhạc nền. Phụ đề mặc định tắt, bật được trong Studio.','',f'Nhận dạng mốc từ bằng faster-whisper base.en; đối chiếu script, khớp trực tiếp {len(mapping)}/{len(tokens)} token. Các token số và dấu câu có nội suy theo từ lân cận; vẫn có sai số mức từ. Không cắt bỏ hoặc đổi tốc độ giọng đọc.','', 'Tạo lại: `python3 tools/build-monthly-payment-video.py --force` chỉ sau khi sao lưu bản sửa tay; không ghi đè WAV/MP4. Dựng MP4 theo README gốc với đầu vào `review/project.json` và tên xuất mới.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
sourceinfo={'source':P+'audio/monthly-payment-trap-voiceover.wav','sha256':hashlib.sha256((V/'audio/monthly-payment-trap-voiceover.wav').read_bytes()).hexdigest(),'duration':total,'sampleRate':24000,'channels':1,'alignmentModel':'faster-whisper base.en int8 CPU','matchedScriptTokens':len(mapping),'scriptTokens':len(tokens),'normalization':'Derived MP3 only: FFmpeg loudnorm, target -16 LUFS, true peak -1.5 dBTP; original WAV unchanged.','music':False,'sourceSpeedChanged':False}
(OUT/'source.json').write_text(json.dumps(sourceinfo,indent=2)+'\n')
print(f'Built {len(clips)} clips, {total:.3f}s, {len(caps)} captions; matched {len(mapping)}/{len(tokens)} source tokens. Assets: {len(project["assets"])}')
print('Longest:',[(s['title'],round(s['end']-s['start'],2)) for s in sorted(shotdata,key=lambda x:x['end']-x['start'],reverse=True)[:6]])
