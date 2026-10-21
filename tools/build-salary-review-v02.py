#!/usr/bin/env python3
"""Build the narrated review from preserved assets and word alignment, without changing WAV/artwork."""
import json,re,math,wave,difflib,hashlib,argparse
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'videos/001-100k-salary';P='videos/001-100k-salary/';OUT=V/'review-v02'
WAV=V/'audio/Why You Feel Broke on a $100,000 Salary.wav'
parser=argparse.ArgumentParser();parser.add_argument('--force',action='store_true');args=parser.parse_args()
if (OUT/'project.json').exists() and not args.force:raise SystemExit('Review exists. Back up edits first; --force rebuilds derived review files only.')
script=(V/'script.md').read_text();body='\n\n'.join(part.split('\n',1)[1] for part in script.split('## ')[1:])
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('’',"'"))
tokens=list(re.finditer(r'\S+',body));source=[norm(t.group()) for t in tokens]
segments=json.loads((V/'review/alignment.json').read_text());heard=[w for s in segments for w in s['words']];target=[norm(w['word']) for w in heard]
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
def cue(phrase,after=0):
 query=[norm(x) for x in phrase.split()]
 candidates=[i for i in range(len(source)-len(query)+1) if source[i:i+len(query)]==query]
 candidates=[i for i in candidates if times[i]>=after-.0005]
 assert candidates,(phrase,after)
 return round(times[candidates[0]],3)
with wave.open(str(WAV)) as wav:
 total=wav.getnframes()/wav.getframerate();samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)
INK='#27332f';GREEN='#286a52';CORAL='#bd6555';BG='#faf6ec';MINT='#e2ecdd';SAND='#eee7d8'
catalog=json.loads((ROOT/'library/props/catalog.json').read_text())['items']
assets={p['id']:{'src':p['src'],'label':p['name'],**({'crop':p['crop']} if 'crop'in p else {})} for p in catalog}
layout=json.loads((ROOT/'videos/002-monthly-payment-trap/asset-layout.json').read_text())
for sheet in layout['sheets']:
 for item in sheet['items']:assets[item['id']]={'src':'videos/002-monthly-payment-trap/'+item['image'],'label':item['name']}
for f in json.loads((V/'artwork.json').read_text())['frames'][:16]:assets['art-'+f['id']]={'src':P+f['image'],'label':f['title']}
for f in json.loads((OUT/'new-scenes.json').read_text())['scenes']:assets['art-new-'+f['id']]={'src':P+'review-v02/'+f['image'],'label':f['title']}
def A(slug):return slug if slug in assets else 'mpt-'+slug
chapters=['THE SIX-FIGURE PARADOX','WHAT ACTUALLY ARRIVES','THE WAITING LIST','IRREGULAR EXPENSES','LIFESTYLE CREEP','THE COMPARISON','THE PLAN','ROOM TO BREATHE']
shots=[]
def add(section,anchor,title,mode,headline,**kw):shots.append(dict(section=section,anchor=anchor,title=title,mode=mode,headline=headline,start=cue(anchor,shots[-1]['start']+.001 if shots else 0),**kw))
def hero(s,a,t,h,message,pose='alex-present',prop='paycheck',detail=''):add(s,a,t,'hero',h,message=message,pose=A(pose),prop=A(prop),detail=detail)
def art(s,a,t,h,key,detail=''):add(s,a,t,'art',h,art=key if key.startswith('art-') else 'art-'+key,detail=detail)
def card(icon,label,value='',detail='',reveal=None):return dict(icon=A(icon),label=label,value=value,detail=detail,reveal=reveal)
def cards(s,a,t,h,items,note=''):add(s,a,t,'cards',h,items=items,note=note)
def mathshot(s,a,t,h,equation,detail,icon='cash-stack'):add(s,a,t,'math',h,equation=equation,detail=detail,icon=A(icon))

# 01 — Keep the hook, replace sparse/repeated layouts with short visual beats.
hero(1,'You finally did it.','Công việc và bước tiến mới','YOU FINALLY DID IT.','A NEW CHAPTER',pose='alex-celebrate',prop='paycheck')
cards(1,'You got the job.','Công việc, tăng lương, sáu con số','THE JOB. THE RAISE. SIX FIGURES.',[card('paycheck','THE JOB'),card('money','THE RAISE'),card('coins','SIX FIGURES')])
mathshot(1,'One hundred thousand dollars a year.','Lương năm sáu con số','A SIX-FIGURE SALARY.','$100,000 / year','Before deductions.','paycheck')
hero(1,'That sounds like the moment','Kỳ vọng hết áp lực tiền','MONEY STRESS.\nFINALLY OVER?','THAT WAS THE EXPECTATION.',pose='alex-present',prop='savings')
hero(1,'But somehow,','Kiểm tra tài khoản trước khi đặt đồ ăn','CHECKING YOUR ACCOUNT\nBEFORE ORDERING TAKEOUT.','STILL DOING THE MATH.',pose='alex-worried',prop='phone')
cards(1,'Your car needs new tires,','Một bộ lốp khiến phải tính toán','NEW TIRES.\nNEW MENTAL GYMNASTICS.',[card('car','THE CAR'),card('tire','ANOTHER EXPENSE')])
hero(1,'And payday?','Chờ ngày lương giải cứu','PAYDAY.\nSTILL A RESCUE MISSION.','WAITING FOR THE NEXT DEPOSIT',pose='alex-worried',prop='calendar')
cards(1,'So what happened?','Thu nhập tốt nhưng vẫn thiếu tiền','SIX FIGURES.\nSTILL FEELING BROKE?',[card('paycheck','A GOOD SALARY'),card('wallet','VERY LITTLE ROOM')])
art(1,"Let's follow the money.",'Theo dòng tiền từ đầu','LET’S FOLLOW THE MONEY.','new-cashflow')
# 02 — Gross vs net, deductions without fabricated tax rates.
hero(2,'Meet Alex.','Gặp Alex','MEET ALEX.','$100,000 / YEAR',pose='alex-present',prop='paycheck')
mathshot(2,'Divide that by twelve,','Đổi lương năm sang tháng','DIVIDE BY TWELVE.','≈ $8,333 / month','Gross pay in this example.','money')
hero(2,'Sounds pretty comfortable.','Nghe có vẻ thoải mái','SOUNDS COMFORTABLE.','ON PAPER.',pose='alex-think',prop='money')
cards(2,"Except that isn't what lands",'Lương trên giấy khác tiền vào tài khoản','GROSS PAY ≠ TAKE-HOME PAY.',[card('paycheck','ON PAPER','$100,000 / year'),card('phone','IN THE BANK','WHAT ARRIVES?')])
cards(2,'Taxes take a portion.','Các khoản khấu trừ','BEFORE THE PAYCHECK ARRIVES.',[card('receipt','TAXES',reveal='Taxes take a portion.'),card('shield','HEALTH INSURANCE',reveal='Health insurance takes another.'),card('piggy','RETIREMENT',reveal='Retirement contributions may')],'Actual deductions vary; no universal tax rate is assumed.')
mathshot(2,"For our example, let's say",'Tiền thực nhận minh họa','IN OUR EXAMPLE.','$6,000 / month','After deductions · An illustration, not every paycheck.','paycheck')
hero(2,"That's an illustration,",'Giới hạn ví dụ thực nhận','AN ILLUSTRATION.\nNOT EVERY PAYCHECK.','YOUR ACTUAL PAY CAN DIFFER.',pose='alex-think',prop='paycheck')
cards(2,'The actual amount depends','Các yếu tố thay đổi thực nhận','YOUR PAYCHECK CAN BE DIFFERENT.',[card('home','LOCATION'),card('shield','BENEFITS'),card('receipt','TAX CIRCUMSTANCES')])
hero(2,'Alex hears','Con số Alex nghe','WHAT ALEX HEARS.','$100,000 / YEAR',pose='alex-think',prop='paycheck')
hero(2,"Alex's checking account sees",'Con số tài khoản nhận','WHAT THE ACCOUNT SEES.','$6,000 / MONTH',pose='alex-plan',prop='phone')
cards(2,'Those are two very different','Hai điểm xuất phát ngân sách','TWO VERY DIFFERENT STARTING POINTS.',[card('paycheck','GROSS SALARY','$100,000 / year'),card('phone','TAKE-HOME PAY','$6,000 / month')],'Take-home pay is hypothetical for this story.')
art(2,'And if Alex spends based','Sửa cảnh tiêu đề từng che tóc','PLAN AROUND\nWHAT ARRIVES.','02b')
# 03 — Big readable amounts first, then an orderly centered summary and exact bar.
art(3,"Now let's give that six thousand",'Dòng tiền bắt đầu có nơi đến','GIVE THE PAYCHECK\nSOMEWHERE TO GO.','new-cashflow')
mathshot(3,'Rent: twenty-three hundred dollars.','Tiền thuê nhà','RENT.','$2,300','An apartment in a fairly expensive area.','home')
mathshot(3,'Transportation: eight hundred','Chi phí đi lại tổng hợp','TRANSPORTATION.','$850','More than the car payment alone.','car')
cards(3,"That's the car payment,",'Bốn phần của chi phí xe','THE COST OF GETTING AROUND.',[card('receipt','CAR PAYMENT'),card('shield','INSURANCE'),card('car','GAS'),card('wrench','MAINTENANCE')])
mathshot(3,'Groceries and eating out:','Thực phẩm và ăn ngoài','GROCERIES + EATING OUT.','$650','Illustrative monthly expense.','groceries')
mathshot(3,'Utilities, internet, and phone:','Điện nước internet điện thoại','UTILITIES. INTERNET. PHONE.','$400','Illustrative monthly expense.','utilities')
mathshot(3,'Student loans or other debt payments:','Khoản trả nợ','DEBT PAYMENTS.','$400','Student loans or other debt payments.','debt')
mathshot(3,'Then three hundred dollars','Các chi phí khác','OTHER MONTHLY COSTS.','$300','Subscriptions, clothes and gifts.','gift')
add(3,'Total?','Tổng hợp sáu khoản cố định','budget','THE MONTHLY COMMITMENTS.')
add(3,'Alex has eleven hundred dollars left.','Số dư sau chi cố định','balance','AFTER RECURRING COSTS.',amount=1100)
hero(3,"Now, eleven hundred dollars isn't nothing.",'Vẫn còn chỗ trong ngân sách','THERE IS STILL ROOM.','$1,100 LEFT',pose='alex-buffer',prop='savings-jar')
art(3,'But notice what happened.','Lương đã có cam kết trước cuối tuần','MOST OF IT\nWAS ALREADY COMMITTED.','03b')
art(3,"The money didn't disappear.",'Tiền đến cùng danh sách chờ','IT DIDN’T DISAPPEAR.\nIT ARRIVED WITH A WAITING LIST.','new-cashflow')
# 04 — Annual costs get their own visual, then a clear 6000/4900/600/500 recap.
cards(4,'Then real life walks in.','Những khoản trong năm','THEN REAL LIFE WALKS IN.',[card('dentist','THE DENTIST',reveal='A trip to the dentist.'),card('flight','A FAMILY WEDDING',reveal='A flight to a family wedding.'),card('laptop','A BROKEN LAPTOP',reveal='A laptop that decides')])
art(4,'These expenses feel like surprises','Chi phí không đến hằng tháng','NOT EVERY MONTH.\nBUT NOT IMPOSSIBLE TO PLAN FOR.','04a')
art(4,'But some version of them','Lập quỹ cho các khoản trong năm','SOME VERSION\nHAPPENS MOST YEARS.','new-annual-funds')
mathshot(4,'If Alex needs an average','Trừ dự trù chi phí không đều','SET ASIDE $600 A MONTH.','$1,100 − $600 = $500','An average allowance for irregular expenses.','calendar')
add(4,'Five hundred dollars of breathing room.','Tổng hợp dòng tiền còn lại','balance','FIVE HUNDRED DOLLARS\nOF BREATHING ROOM.',amount=500)
hero(4,'Enough to make progress, yes.','Vẫn có thể tiến bộ','ENOUGH TO MAKE PROGRESS.','SOME BREATHING ROOM.',pose='alex-buffer',prop='savings-jar')
cards(4,'But a lot less than Alex imagined','Kỳ vọng và khoảng trống thực tế','LESS THAN THE OFFER MADE IT FEEL.',[card('paycheck','ANNUAL GROSS SALARY','$100,000'),card('savings-jar','MONTHLY ROOM LEFT','$500')],'Different measures: annual gross salary vs monthly budget remainder.')
art(4,"And if those irregular costs aren't",'Chi phí chuyển sang thẻ','THIS MONTH’S EXPENSE.\nNEXT MONTH’S PAYMENT.','04b')
cards(4,'Next month, the budget gets','Khoản trả cho chuyện đã qua','A NEW BILL.\nFOR SOMETHING THAT ALREADY HAPPENED.',[card('receipt','THE PAST PURCHASE'),card('bank-card','THE NEW PAYMENT')])
hero(4,"That's how a decent income",'Cảm giác luôn đi sau','A DECENT INCOME.\nALWAYS ONE STEP BEHIND?','THE COMMITMENTS ADD UP.',pose='alex-worried',prop='card')
# 05 — Distinguish deliberate improvements from automatic new commitments.
hero(5,"But there's another part",'Nhìn lại trước khi tăng lương','BEFORE THE RAISES.','A DIFFERENT BASELINE',pose='alex-think',prop='calendar')
cards(5,'The apartment was smaller.','Mức sống trước kia','A SMALLER SET OF COMMITMENTS.',[card('home','A SMALLER APARTMENT',reveal='The apartment was smaller.'),card('car','AN OLDER CAR',reveal='The car was older.'),card('food','AN OCCASIONAL TREAT',reveal='Dinner delivery was')])
art(5,'Then the raises started coming.','Các lần nâng cấp','A RAISE.\nAN UPGRADE.','05a')
hero(5,'And every upgrade had','Lý do nâng cấp nghe hợp lý','EACH UPGRADE\nHAD A REASON.','THE CHOICES MADE SENSE.',pose='alex-think',prop='comparison-cards')
cards(5,'The nicer apartment cut','Những lý do cho từng lựa chọn','SHORTER COMMUTE.\nMORE RELIABILITY. A FEW DOLLARS.',[card('home','A SHORTER COMMUTE',reveal='The nicer apartment cut'),card('car','MORE RELIABILITY',reveal='The newer car felt'),card('streaming','A FEW DOLLARS EACH',reveal='The extra subscriptions were')])
hero(5,'None of those decisions','Không quy mọi nâng cấp là sai','NOT NECESSARILY\nA MISTAKE.','LOOK AT THE PATTERN.',pose='alex-think',prop='shield')
art(5,'The problem was that every raise','Mỗi lần tăng lương thêm cam kết','ANOTHER RAISE.\nANOTHER COMMITMENT.','05b')
cards(5,'More money came in.','Thu nhập và tiền hứa trả cùng tăng','MORE IN.\nMORE PROMISED AWAY.',[card('money','MONEY COMING IN'),card('receipt','MONEY ALREADY PROMISED')])
hero(5,'This is lifestyle creep.','Mức sống tăng dần','LIFESTYLE CREEP.','YESTERDAY’S LUXURIES.\nTODAY’S NORMAL.',pose='alex-present',prop='money')
cards(5,'It rarely feels like','Không phải một lần mua sắm lớn','LESS LIKE A SHOPPING SPREE.\nMORE LIKE A NEW ROUTINE.',[card('parcel','ONE BIG PURCHASE?'),card('calendar','A HIGHER BASELINE')])
hero(5,'It feels like slowly turning','Thói quen chi tiêu thay đổi dần','YESTERDAY’S LUXURIES.\nTODAY’S NORMAL EXPENSES.','THE BASELINE MOVES.',pose='alex-think',prop='calendar')
hero(5,'And once a higher standard','Lùi một bước có thể thêm tự do','STEPPING BACK\nCAN CREATE MORE FREEDOM.','LESS COMMITTED. MORE FLEXIBLE.',pose='alex-think',prop='savings-jar')
# 06 — A new funding-context illustration avoids treating every social post as debt.
art(6,'Then Alex opens social media.','Bảng tin mạng xã hội','THE HIGHLIGHT REEL.','06a')
cards(6,'Someone just bought a house.','Ba hình ảnh dễ đem so sánh','A HOUSE. ITALY. A BOAT.',[card('home','A HOUSE',reveal='Someone just bought a house.'),card('flight','ITALY',reveal='Someone else is in Italy.'),card('vacation','A BOAT',reveal='A person Alex barely remembers')])
cards(6,'Nobody is posting their','Những gì không có trên bảng tin','WHAT YOU DON’T SEE.',[card('shield','THE INSURANCE DEDUCTIBLE',reveal='Nobody is posting their'),card('card','THE CREDIT CARD INTEREST',reveal='Nobody is making a highlight reel')])
art(6,"And a photo doesn't tell",'Nguồn tiền mà bức ảnh không cho biết','A PHOTO DOESN’T\nSHOW THE FUNDING.','new-social-context','Savings, debt, family help or a larger income: possibilities, not assumptions.')
hero(6,'But your brain fills','Não tự điền phần còn thiếu','YOUR BRAIN\nFILLS IN THE BLANKS.','EVERYONE ELSE LOOKS COMFORTABLE.',pose='alex-think',prop='phone')
hero(6,'So you start treating their spending','Lấy chi tiêu người khác làm chuẩn','THEIR SPENDING\nBECOMES YOUR BENCHMARK.','CAN YOUR PAYCHECK SUPPORT IT?',pose='alex-phone',prop='bank-card')
art(6,'Now your paycheck has','Một lương gánh hai cuộc sống','ONE PAYCHECK.\nTWO LIVES.','06b')
cards(6,'The life you actually live.','Cuộc sống thật và cuộc sống mong đợi','THE LIFE YOU LIVE.\nTHE LIFE YOU FEEL YOU SHOULD LIVE.',[card('home','YOUR ACTUAL LIFE',reveal='The life you actually live.'),card('vacation','THE EXPECTED LIFE',reveal='And the life you feel')])
hero(6,"That's an expensive comparison.",'Cái giá của sự so sánh','AN EXPENSIVE COMPARISON.','START WITH YOUR OWN NUMBERS.',pose='alex-think',prop='wallet')
# 07 — Break the action plan into manageable, specific visual steps.
hero(7,'So how does Alex get','Bắt đầu tìm khoảng thở','START WITH\nWHAT ACTUALLY ARRIVES.','TAKE-HOME PAY',pose='alex-plan',prop='pay-envelope')
cards(7,'Build the plan around','Lập ngân sách trên thực nhận','THE JOB OFFER\nISN’T THE MONTHLY PLAN.',[card('paycheck','GROSS SALARY','$100,000 / year'),card('phone','TAKE-HOME PAY','$6,000 / month')],'Take-home figure is illustrative for this story.')
cards(7,'Then look at the biggest','Ba cam kết lớn nên xem lại','START WITH THE BIGGEST COMMITMENTS.',[card('home','HOUSING',reveal='Housing.'),card('car','TRANSPORTATION',reveal='Transportation.'),card('debt','DEBT PAYMENTS',reveal='Debt payments.')])
cards(7,'Canceling a subscription can help.','Nhỏ và lớn trong ngân sách','SMALL SAVINGS CAN HELP.\nFIND THE BIG PRESSURE.',[card('streaming','A CHEAPER SUBSCRIPTION'),card('car','AN EXPENSIVE CAR PAYMENT')])
hero(7,'But if the real pressure','Chọn đúng nguồn gây áp lực','FIX THE SOURCE\nOF THE PRESSURE.','THE BIG RECURRING COST',pose='alex-plan',prop='car')
cards(7,'Some changes take time.','Thay đổi cần thời gian','SOME CHANGES TAKE TIME.',[card('calendar','A LEASE MAY NEED TO END'),card('debt','A DEBT NEEDS A PLAN')])
hero(7,"You don't have to fix everything",'Không cần sửa hết trong một ngày','NOT EVERYTHING\nHAS TO CHANGE TODAY.','ONE STEP AT A TIME.',pose='alex-plan',prop='clipboard')
art(7,'Next, stop calling predictable','Lập quỹ cho khoản có thể dự tính','PREDICTABLE COSTS\nDESERVE A PLAN.','new-annual-funds')
cards(7,'Car repairs, annual bills,','Ba nhóm quỹ dự tính','SET SOMETHING ASIDE EACH PAYDAY.',[card('wrench','CAR REPAIRS',reveal='Car repairs,'),card('receipt','ANNUAL BILLS',reveal='annual bills,'),card('gift','HOLIDAY SPENDING',reveal='and holiday spending')])
hero(7,'When the bill arrives,','Tiền được giao việc trước khi hóa đơn đến','THE BILL ARRIVES.\nTHE MONEY HAS A JOB.','READY FOR A PREDICTABLE COST.',pose='alex-buffer',prop='savings-jar')
art(7,'And when your income rises,','Chia tăng lương có kế hoạch','PLAN THE RAISE\nBEFORE IT BECOMES ROUTINE.','new-raise-plan')
cards(7,'Some can improve your life today.','Hiện tại tiết kiệm và trả nợ','GIVE THE INCREASE A JOB.',[card('food','LIFE TODAY',reveal='Some can improve your life'),card('savings-jar','SAVINGS + GOALS',reveal='Some can build savings,'),card('debt','LESS DEBT',reveal='reduce debt,')],'No fixed allocation or guaranteed result is assumed.')
hero(7,"The point isn't to reject every upgrade.",'Không cần từ chối mọi nâng cấp','ENJOY AN UPGRADE.\nKEEP SOME FREEDOM.','DON’T COMMIT THE ENTIRE RAISE.',pose='alex-buffer',prop='cash-tray')
# 08 — Essential-cost context, visible progress and a clear final question.
hero(8,'Of course, not every tight budget','Không phải mọi khó khăn đều do mức sống','NOT EVERY TIGHT BUDGET\nIS A LIFESTYLE PROBLEM.','START WITH THE REAL CIRCUMSTANCES.',pose='alex-think',prop='shield')
art(8,'Childcare, medical needs,','Áp lực thật từ chi phí thiết yếu','CHILDCARE. MEDICAL NEEDS.\nFAMILY. LOCATION.','08a')
hero(8,"Sometimes the biggest issue isn't",'Chi phí thiết yếu có thể thực sự cao','ESSENTIAL COSTS\nCAN BE GENUINELY HIGH.','THIS ISN’T ALWAYS CARELESS SPENDING.',pose='alex-think',prop='home')
art(8,'But whatever the cause,','Tìm tiền đã được cam kết ở đâu','WHERE IS THE MONEY\nALREADY COMMITTED?','new-cashflow')
cards(8,'Because a higher salary','Thu nhập cho lựa chọn nhưng cần kế hoạch','MORE OPTIONS.\nSTILL NEEDS A PLAN.',[card('money','A HIGHER SALARY'),card('clipboard','A WORKABLE PLAN')])
cards(8,'For Alex, financial progress','Những tiến bộ có thể bắt đầu nhỏ','PROGRESS CAN START WITH…',[card('paid','ONE LESS PAYMENT',reveal='one less payment,'),card('home','A SMALLER FIXED COST',reveal='a smaller fixed expense,'),card('savings-jar','A CASH BUFFER',reveal='or a cash buffer')])
art(8,'Not something impressive enough','Khoảng thở không cần phô trương','NOT SOMETHING\nYOU NEED TO POST.','08b')
hero(8,'Just enough space to stop feeling trapped.','Bớt cảm giác bị mắc kẹt','ENOUGH SPACE\nTO STOP FEELING TRAPPED.','ROOM TO BREATHE.',pose='alex-buffer',prop='savings-jar')
hero(8,'And that raises a better question','Câu hỏi tốt hơn về tiền','MORE THAN\n“DO I MAKE GOOD MONEY?”','WHAT IS YOUR MONEY HELPING YOU BUILD?',pose='alex-think',prop='savings-jar')
art(8,'How much of the money I make','Câu hỏi kết về cuộc sống muốn xây','IS YOUR MONEY BUILDING\nTHE LIFE YOU ACTUALLY WANT?','08b')

# Verify every borrowed legacy prop ID explicitly instead of silently substituting imagery.
ids=set(assets)
for s in shots:
 for item in s.get('items',[]):assert item['icon'] in ids,(item['icon'],sorted(ids))

def text(id,content,x,y,w,size=60,fill=INK,enter=0,effect='fade',align='center'):
 return dict(id=id,type='text',text=content,x=x,y=y,w=w,h=math.ceil(size*1.18*(content.count('\n')+1)+18),size=size,fill=fill,align=align,enter=enter,effect=effect,opacity=1,drift=0)
def image(id,asset,x,y,w,h,enter=0,effect='pop',drift=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=enter,effect=effect,opacity=1,drift=drift)
def box(id,x,y,w,h,fill,enter=0):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=24,enter=enter,effect='fade',opacity=1,drift=0)
def local(phrase,s):return round(max(0,cue(phrase,s['start'])-s['start']),3)
def layers(s):
 out=[text('chapter',f'{s["section"]:02d}  /  {chapters[s["section"]-1]}',80,35,1760,24,GREEN,effect='none',align='left'),text('headline',s['headline'],85,100,1750,66,effect='none')]
 mode=s['mode']
 if mode=='hero':
  out += [box('panel',700,330,1110,570,MINT),image('alex',s['pose'],100,300,480,650,0,'pop',1),image('prop',s['prop'],1075,350,360,240,.08,'pop'),text('message',s['message'],735,640,1040,56,GREEN,.15)]
  if s.get('detail'):out.append(text('detail',s['detail'],740,805,1030,37,INK,.25))
 elif mode=='art':
  out.append(image('illustration',s['art'],80,285,1760,650,.02,'fade',1))
  if s.get('detail'):out.append(text('detail',s['detail'],100,968,1720,28,GREEN,.1))
 elif mode=='math':
  out += [image('math-icon',s['icon'],785,292,350,225,.02),box('equation-panel',120,565,1680,190,MINT,.04),text('equation',s['equation'],155,605,1610,92,GREEN,.12),text('explanation',s['detail'],140,824,1640,44,INK,.2)]
 elif mode=='budget':
  items=[('home','Rent',2300),('car','Transportation',850),('groceries','Food',650),('utilities','Utilities / internet / phone',400),('debt','Debt payments',400),('gift','Other',300)]
  for i,(asset,label,value) in enumerate(items):
   x=90+(i%3)*590;y=320+(i//3)*290
   out += [box(f'budget-{i}',x,y,550,265,MINT if i%2 else SAND),image(f'budget-icon-{i}',asset,x+185,y+20,180,105,.02,'fade'),text(f'budget-label-{i}',label,x+20,y+142,510,30),text(f'budget-amount-{i}',f'${value:,}',x+20,y+190,510,52,GREEN)]
  out.append(text('budget-total','TOTAL COMMITTED: $4,900',100,935,1720,44,CORAL))
 elif mode=='balance':
  available=s['amount'];parts=[(4900,CORAL)]+([(600,'#c3973e'),(500,GREEN)] if available==500 else [(1100,GREEN)])
  equation='$1,100 − $600 = $500' if available==500 else '$6,000 − $4,900 = $1,100'
  out.append(text('balance-equation',equation,100,340,1720,92,GREEN,.08))
  x=100
  for i,(amount,color) in enumerate(parts):
   part=box(f'bar-{i}',x,550,1720*amount/6000,100,color,.12+i*.08);part['radius']=0;out.append(part);x+=1720*amount/6000
  labels=[('RECURRING COSTS','$4,900'),('IRREGULAR PLAN','$600'),('ROOM LEFT','$500')] if available==500 else [('RECURRING COSTS','$4,900'),('ROOM LEFT','$1,100')]
  w=1720/len(labels)
  for i,(label,value) in enumerate(labels):out += [text(f'bar-label-{i}',label,100+i*w,720,w,38),text(f'bar-value-{i}',value,100+i*w,800,w,64,GREEN if i==len(labels)-1 else CORAL)]
  out.append(text('budget-note','Illustrative monthly budget · Bar segments follow the $6,000 total.',100,968,1720,28,GREEN))
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
 clips.append(dict(id=f'salary-v02-{i+1:03d}',title=s['title'],duration=length,background=BG,fade=.08 if i else 0,layers=ll))

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
project=dict(kind='credit-studio-video',version=1,revision='salary-review-v02',name='Why You Feel Broke — Bản duyệt đầy đủ v02',width=1920,height=1080,fps=30,audio=dict(src=P+'review-v02/voiceover.mp3',offset=0,volume=1),assets={k:v for k,v in assets.items() if k in used},clips=clips,captions=caps,showCaptions=False,waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
shotdata=[dict(**s,end=round(s['start']+clips[i]['duration'],6),clipId=clips[i]['id']) for i,s in enumerate(shots)]
(OUT/'shot-plan.json').write_text(json.dumps(shotdata,ensure_ascii=False,indent=2)+'\n')
lines=['# Video 001 — Bản duyệt cải thiện v02','',f'**{total:.3f} giây · {len(clips)} cảnh · 1920×1080 · 30 fps.** Căn theo WAV gốc; giữ nguyên lời đọc và thời lượng v01.','', 'Dự án chỉnh được: `project.json`. Audio dẫn xuất chuẩn hóa: `voiceover.mp3`. WAV, intro và review/MP4 v01 được giữ nguyên. MP4 mới: `../exports/full-review-v02.mp4`.','', '| Bắt đầu | Kết thúc | Cảnh |','|---|---|---|']
for s in shotdata:lines.append(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["title"]} |')
lines += ['','Chữ Times New Roman; tiêu đề tách khỏi nhân vật, hình/nhãn căn giữa. Hiệu ứng lớp fade/pop và drift nhẹ, chưa rig khớp. Chưa có nhạc nền. Phụ đề mặc định tắt, bật được trong Studio.','',f'Nhận dạng mốc từ bằng faster-whisper base.en; đối chiếu script, khớp trực tiếp {len(mapping)}/{len(tokens)} token. Các token số và dấu câu có nội suy theo từ lân cận; vẫn có sai số mức từ. Không cắt bỏ hoặc đổi tốc độ giọng đọc.','', 'Tạo lại: `python3 tools/build-salary-review-v02.py --force` chỉ sau khi sao lưu bản sửa tay; không ghi đè WAV/MP4. Dựng MP4 theo README gốc với đầu vào `review-v02/project.json` và tên xuất mới.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
sourceinfo={'source':P+'audio/Why You Feel Broke on a $100,000 Salary.wav','sha256':hashlib.sha256(WAV.read_bytes()).hexdigest(),'duration':total,'sampleRate':24000,'channels':1,'alignmentModel':'faster-whisper base.en int8 CPU','matchedScriptTokens':len(mapping),'scriptTokens':len(tokens),'normalization':'Derived MP3 only: FFmpeg loudnorm, target -16 LUFS, true peak -1.5 dBTP; original WAV unchanged.','music':False,'sourceSpeedChanged':False,'alignmentSource':P+'review/alignment.json','preservedReviewV01':P+'review/project.json','preservedMP4V01':P+'exports/full-review-v01.mp4','newIllustrations':4}
(OUT/'source.json').write_text(json.dumps(sourceinfo,indent=2)+'\n')
print(f'Built {len(clips)} clips, {total:.3f}s, {len(caps)} captions; matched {len(mapping)}/{len(tokens)} source tokens. Assets: {len(project["assets"])}')
print('Longest:',[(s['title'],round(s['end']-s['start'],2)) for s in sorted(shotdata,key=lambda x:x['end']-x['start'],reverse=True)[:6]])
