#!/usr/bin/env python3
"""Build the full mortgage review from approved narration and preserved timing.
Never changes WAV, old samples or exports. Refuses to replace an existing review.
"""
import json, re, math, wave, hashlib
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; V=ROOT/'videos/005-mortgage-payment'; OUT=V/'review'
if (OUT/'project.json').exists():raise SystemExit('Review exists. Preserve edits and create a new version before rebuilding.')
rows=json.loads((V/'production/script-timing.json').read_text()); body=(V/'narration.txt').read_text()
tokens=list(re.finditer(r'\S+',body)); norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower()); words=[norm(t.group()) for t in tokens]
assert len(rows)==len(tokens)==1241 and all(norm(r['word'])==w for r,w in zip(rows,words))
times=[r['start'] for r in rows]; total=566.45
chap=json.loads((V/'production/chapters.json').read_text())['chapters']
paras=body.strip().split('\n\n'); shots=[]; offset=0
for i,p in enumerate(paras):
 s=dict(id=f'mortgage-{i+1:03d}',paragraph=i,section=next(c['section'] for c in reversed(chap) if times[offset]>=c['start']-.001),start=0 if not i else times[offset],text=p,tokenStart=offset,tokenEnd=offset+len(p.split()))
 shots.append(s);offset+=len(p.split())
for i,s in enumerate(shots):s['duration']=round((shots[i+1]['start'] if i+1<len(shots) else total)-s['start'],6)
assert len(shots)==88 and all(.5<=s['duration']<=120 for s in shots)
def at(s,phrase):
 q=[norm(w) for w in phrase.split()];ii=next((i for i in range(s['tokenStart'],s['tokenEnd']-len(q)+1) if words[i:i+len(q)]==q),None)
 if ii is None:raise ValueError((s['paragraph'],phrase))
 return max(0,round(times[ii]-s['start'],5))
BG='#f6f0e5';INK='#302e29';RED='#873e3d';SAND='#e9dfce';SAGE='#718372';MUTED='#786b5d';LIGHT='#d6dfcd'
assets={'house':json.loads((V/'samples/project.json').read_text())['assets']['house']}
for name in ['keys','bills','repair','compare']:assets[name]={'src':f'library/props/jamie-mortgage/{name}.png','label':'Jamie — '+name}
def text(id,t,x,y,w,size=48,fill=INK,enter=0,align='left'):
 return dict(id=id,type='text',text=t,x=x,y=y,w=w,h=math.ceil(size*1.18*(t.count('\n')+1)+8),size=size,fill=fill,align=align,enter=round(enter,5),effect='none',opacity=1,drift=0)
def rect(id,x,y,w,h,fill=SAND,enter=0,radius=8):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=radius,enter=round(enter,5),effect='none',opacity=1,drift=0)
def pic(id,asset,x,y,w,h,enter=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=round(enter,5),effect='fade',opacity=1,drift=0)
def anim(l,prop,keys,easing='smooth',**extra):
 l['animation']=dict(property=prop,easing=easing,keys=[dict(time=round(t,5),value=round(v,6)) for t,v in keys],**extra);return l
def number(l,keys,easing='smooth',format='currency',prefix='',suffix=''):return anim(l,'number',keys,easing,format=format,prefix=prefix,suffix=suffix)
def end(s,t,span=.8):return min(s['duration']-.06,t+span)
chapters=['THE NUMBER ON THE SCREEN','THE WHOLE MONTHLY NUMBER','COUNT EACH BILL ONCE','AFTER THE KEYS','WHEN THE BILL ARRIVES','EQUITY AND CASH','TEST AN ORDINARY LIFE','ROOM TO LIVE']
titles=[
 'A PLACE TO CALL YOUR OWN.','ROOM FOR YOUR LIFE.','THEN YOU OPEN THE CALCULATOR.','ABOUT $1,500 A MONTH.','MAYBE THIS IS POSSIBLE.','THE CALCULATOR ANSWERED PART OF IT.','THE PAYMENT ON THE LOAN.','THE LIFE AROUND THE HOUSE.','TWO DIFFERENT NUMBERS.','MEET JAMIE.','A PAYMENT CAN FIT. A BUDGET CAN STRAIN.',
 'START WITH THE PURCHASE.','WHAT IS ACTUALLY BORROWED.','THE ASSUMED LOAN TERMS.','PRINCIPAL + INTEREST.','ADD THE OTHER BILLS.','THE MONTHLY BILLS.','KEEP MONEY FOR REPAIRS.','THE HOUSING ALLOCATION.','THE GAP BEYOND THE LOAN PAYMENT.','SOME IS SPENT. SOME IS SAVED.','REPLACE THE ASSUMPTIONS.',
 'COUNT EACH BILL ONCE.','ALREADY INCLUDED? DO NOT ADD AGAIN.','HOW ESCROW WORKS.','A DIFFERENT ROUTE. THE SAME BILLS.','LOOK INSIDE THE PAYMENT.','SOME COSTS SIT OUTSIDE IT.','FIXED RATE. CHANGING OTHER COSTS.','CHECK YOUR LOAN TYPE.','COMPARE THE SAME CATEGORIES.',
 'NOW LOOK AT THE CASH.','BEFORE THE PURCHASE.','THE DOWN PAYMENT MOVES.','THE OTHER CLOSING AMOUNTS.','AFTER THE CLOSING AMOUNTS.','MOVING AND IMMEDIATE ESSENTIALS.','THE CASH LEFT WITH THE KEYS.','THE DOWN PAYMENT STILL HAS VALUE.','EQUITY IS NOT CASH IN THE BANK.','PAID AHEAD IS NOT PAID TWICE.','CAN YOU HANDLE THE NEXT BILL?','GETTING THE KEYS IS ONE TEST.',
 'MONTH ONE. NOTHING BREAKS.','MONTH TWO. STILL QUIET.','DO I REALLY NEED THIS FUND?','THEN SOMETHING BREAKS.','A HYPOTHETICAL REPAIR.','A YEAR OF MONTHLY TRANSFERS.','BUT THE BILL CAN ARRIVE EARLY.','ONLY TWO TRANSFERS SO FAR.','THE GAP NEEDS ANOTHER SOURCE.','TWO DIFFERENT JOBS.','BUILD OVER TIME. HAVE CASH READY.','THE SAME MONEY. COUNT IT ONCE.',
 'EQUITY CAN LOOK REASSURING.','PRINCIPAL REDUCES THE DEBT.','THE WHOLE PAYMENT IS NOT EQUITY.','THE FIRST MONTH, SPLIT APART.','THE SPLIT CHANGES OVER TIME.','THESE DO NOT REDUCE THE LOAN.','HOME VALUE IS NOT SPENDABLE CASH.','ACCESS CAN HAVE COSTS AND RISKS.','A BILL CAN STILL BE DUE FRIDAY.','TRACK BOTH SIDES.','TWO QUESTIONS ABOUT SECURITY.',
 'BUILD A MONTH AROUND THE HOUSE.','START WITH TAKE-HOME PAY.','INCLUDE THE REST OF YOUR LIFE.','WHAT IS LEFT AFTER THE BILLS?','USE INFORMATION FOR THIS PROPERTY.','READ THE TWO DISCLOSURES.','TRY A TOUGHER MONTH.','WHAT IF ONE THING CHANGES?','TEST SCENARIOS SEPARATELY.','KEEP A WORKABLE RESPONSE.',
 'THE BENEFITS MATTER TOO.','PUT THOSE BENEFITS IN THE DECISION.','LEAVE ROOM FOR THE REST OF LIFE.','DIFFERENT BUYERS. DIFFERENT CHOICES.','NO SINGLE NUMBER FITS EVERYONE.','ASK A BIGGER QUESTION.','WHAT CHOICES DO YOU STILL HAVE?','REPAIR WITHOUT ANOTHER PAYMENT?','CAN YOU KEEP SAVING?','ROOM FOR AN ORDINARY LIFE.','THE CALCULATION STARTS HERE.','THE ROOM YOU HAVE LEFT.'
]
assert len(titles)==88
def base(s,note='FICTIONAL EXAMPLE / Amounts are assumptions, not current quotes or national averages.'):
 return [text('chapter',f'{s["section"]:02d} / {chapters[s["section"]-1]}',90,36,1700,25,MUTED),rect('rule',90,82,1740,2,RED,radius=0),text('headline',titles[s['paragraph']],90,124,1740,64),text('scope',note,90,951,1740,23,MUTED)]
def prop(s,msg,detail='',asset='bills',note=None):
 a=base(s) if note is None else base(s,note);a+=[pic('illustration',asset,105,317,745,582),rect('copy-panel',940,330,880,552),text('message',msg,990,415,780,60,RED,align='center')]
 if detail:a.append(text('detail',detail,990,705,780,32,MUTED,align='center'))
 return a
def cards(s,items,note=None,reveals=None):
 a=base(s) if note is None else base(s,note);n=len(items);w=(1740-32*(n-1))/n
 for i,it in enumerate(items):
  label,value,detail=(*it,'','')[:3];x=90+i*(w+32);t=(reveals or {}).get(i,0)
  a += [rect(f'card-{i}',x,335,w,540,SAND if i%2==0 else LIGHT,t),rect(f'chip-{i}',x+(w-170)/2,385,170,66,RED if i%2==0 else SAGE,t),text(f'chip-label-{i}',str(i+1).zfill(2),x+(w-170)/2,398,170,34,'#ffffff',t,'center'),text(f'label-{i}',label,x+25,505,w-50,38,INK,t,'center')]
  if value:a.append(text(f'value-{i}',value,x+25,650,w-50,68 if len(value)<=10 else 52,RED,t,'center'))
  if detail:a.append(text(f'detail-{i}',detail,x+30,780,w-60,27,MUTED,t,'center'))
 return a
def big(s,label,value,previous=None,asset='house',maxval=None,when=0,detail=''):
 a=base(s);a += [pic('illustration',asset,100,330,720,550),rect('number-panel',925,330,900,555,SAND),text('amount-label',label,965,365,820,34,INK,align='center')]
 l=text('amount',f'${value:,}',965,465,820,126,RED,when,align='center')
 if previous is not None:number(l,[(when,previous),(end(s,when),value)])
 a.append(l)
 if detail:a.append(text('amount-detail',detail,975,665,800,33,MUTED,when,align='center'))
 if maxval:
  a.append(rect('track',1005,802,740,24,LIGHT));l=rect('meter',1005,802,740*value/maxval,24,RED)
  if previous is not None:anim(l,'width',[(when,740*previous/maxval),(end(s,when),740*value/maxval)])
  a.append(l)
 return a
def calculator(s,amount=None,when=0):
 a=base(s);a += [pic('house', 'house',100,320,760,570),rect('calculator',980,310,730,590,INK,radius=22),rect('screen',1020,350,650,245,BG,radius=12),text('screen-label','PRINCIPAL + INTEREST',1050,380,590,31,MUTED,align='center')]
 if amount:a.append(text('calculator-amount',amount,1040,452,610,100,RED,when,'center'))
 for j in range(6):
  x=1025+j%3*215;y=635+j//3*105;a += [rect(f'button-{j}',x,y,190,80,SAND),text(f'key-{j}',str([7,8,9,4,5,6][j]),x,y+12,190,43,INK,align='center')]
 return a
def budget(s,stage):
 a=base(s);i=s['paragraph'];rowspec=[('LOAN','Principal + interest',1517,RED),('TAX','Property taxes',300,'#b76b5c'),('INS','Homeowners insurance',125,'#c29876'),('HOA','Association fee',75,'#9e8873'),('SAVE','Saved for repairs',250,SAGE)]
 reveals={};initial=1517;target=2017
 if i==15:reveals={1:at(s,'three hundred dollars'),2:at(s,'one hundred twenty-five'),3:at(s,'seventy-five')}
 elif stage>=4:initial=2017
 if i==17:reveals={4:at(s,'two hundred fifty dollars')}
 if i==18:initial=2017;target=2267;reveals={4:at(s,'two thousand two hundred sixty-seven dollars')}
 elif stage==5:initial=target=2267
 keys=[(0,initial)];value=initial;include=4 if stage==4 else stage
 for j,(tag,label,amount,color) in enumerate(rowspec):
  if j>=include and not(i==17 and j==4):continue
  t=reveals.get(j,0);y=315+j*94
  a += [rect(f'chip-{j}',100,y,100,66,color,t,5),text(f'tag-{j}',tag,100,y+17,100,23,'#ffffff',t,'center'),text(f'label-{j}',label,230,y+12,660,39,INK,t),text(f'cost-{j}',f'${amount:,}',910,y+10,240,42,SAGE if j==4 else INK,t,'right')]
  if j==4 and i==17:continue
  before=sum(x[2] for x in rowspec[:j]);bar=rect(f'bar-{j}',100+1700*before/2267,858,1700*amount/2267,46,color,t,0)
  if j in reveals:
   anim(bar,'width',[(t,0),(end(s,t,.65),1700*amount/2267)]);keys += [(t,value),(end(s,t,.65),value+amount)];value+=amount
  a.append(bar)
 label='MONTHLY ALLOCATION' if stage==5 else 'MONTHLY BILLS'
 a += [rect('total-panel',1250,312,570,470,SAND),text('total-label',label,1285,355,500,30,INK,align='center')]
 l=text('total',f'${target:,}',1285,432,500,100,RED,align='center')
 if len(keys)>1:number(l,keys)
 else:l['text']=f'${initial:,}'
 a += [l,text('total-note','BEFORE UTILITIES',1285,580,500,30,MUTED,align='center')]
 if i==17:a.append(text('saved-note','PLUS $250 KEPT\nFOR REPAIRS',1285,665,500,30,SAGE,at(s,'two hundred fifty dollars'),'center'))
 elif stage==5:a.append(text('saved-note','Bills $2,017 + savings $250',1285,665,500,28,MUTED,align='center'))
 a.append(text('assumptions','$240,000 loan · 6.5% fixed interest · 30 years · no financed fees',100,805,1700,24,MUTED))
 return a
def cash(s,amount,previous=None,equity=60000,moving=False,detail=''):
 a=base(s);i=s['paragraph'];a += [rect('cash-panel',100,315,750,565,SAND),text('cash-label','CASH AVAILABLE',135,350,680,32,INK,align='center')]
 l=text('cash',f'${amount:,}',135,445,680,110,RED,at(s,'seventy-five thousand dollars') if i==32 else 0,align='center');t=0
 if previous is not None:
  phrase={32:'seventy-five thousand dollars',33:'sixty thousand',35:'six thousand dollars',37:'four thousand dollars'}.get(i);t=at(s,phrase) if phrase else 0;number(l,[(t,previous),(end(s,t,.9),amount)])
 a += [l,text('cash-detail',detail,150,675,650,33,MUTED,align='center'),text('equity-label','DOWN PAYMENT → EQUITY',1040,330,780,33,INK,align='center'),pic('house','house',1125,485,610,405)]
 l=text('equity',f'${equity:,}',1100,395,660,66,SAGE,align='center')
 if i==33:number(l,[(t,0),(end(s,t,.9),60000)])
 a += [l,text('equity-note','Value in the home ≠ cash in the bank',1020,907,800,28,MUTED,align='center')]
 if moving:
  for k in range(1):
   x=875+k*10;y=605-k*10;to=1010+k*10
   a += [anim(rect(f'note-{k}',x,y,110,55,SAGE,t),'x',[(t,x),(end(s,t,.9),to)]),anim(rect(f'note-inner-{k}',x+6,y+6,98,43,LIGHT,t),'x',[(t,x+6),(end(s,t,.9),to+6)]),anim(text(f'note-symbol-{k}','$',x+10,y+10,90,27,SAGE,t,'center'),'x',[(t,x+10),(end(s,t,.9),to+10)])]
 return a
def flow(s):
 a=cards(s,[('YOUR PAYMENT','',''),('ESCROW','',''),('TAX + INSURANCE','','')]);D=s['duration'];t=end(s,.25,max(.4,D-1))
 for k in range(1):
  a.append(anim(rect(f'flow-note-{k}',535+k*12,700,95,50,SAGE,.25),'x',[(.25,535+k*12),(t,1470+k*12)]))
  a.append(anim(text(f'flow-symbol-{k}','$',545+k*12,708,75,27,'#ffffff',.25,'center'),'x',[(.25,545+k*12),(t,1480+k*12)]))
 return a
def calendar(s,month):
 a=prop(s,f'MONTH {month}','','house');a += [rect('calendar',1100,590,555,240,BG),rect('calendar-head',1100,590,555,52,RED),text('month-label','ILLUSTRATIVE MONTH',1120,605,515,24,'#ffffff',align='center'),text('month-number',str(month),1120,665,515,104,INK,align='center'),text('quiet-month','No repair bill has arrived yet.',990,838,780,27,MUTED,align='center')];return a
def annual(s):
 a=base(s);t=at(s,'three thousand dollars');span=max(.3,end(s,t));keys=[(0,0)]+[(span*k/12,250*k) for k in range(1,13)]
 a += [text('formula','$250 EACH MONTH × 12 TRANSFERS',100,300,1720,43,INK,align='center'),number(text('reserve','$0',100,385,1720,122,SAGE,align='center'),keys,'step')]
 for k in range(12):
  x=150+(k%6)*270;y=565+(k//6)*140;reveal=span*(k+1)/12
  a += [rect(f'month-{k}',x,y,235,115,LIGHT,reveal),text(f'month-label-{k}',f'MONTH {k+1}',x+10,y+35,215,29,INK,reveal,'center')]
 a.append(text('compressed','Compressed 12-transfer illustration · before withdrawals or interest',110,880,1700,25,MUTED,align='center'));return a
def split(s,over_time=False):
 a=base(s);D=s['duration'];payment=240000*(.065/12)/(1-(1+.065/12)**-360);rate=.065/12
 if over_time:
  months=[1,60,120,180,240,300,360];samples=[]
  for m in months:
   balance=240000*(1+rate)**(m-1)-payment*((1+rate)**(m-1)-1)/rate;interest=round(balance*rate);samples.append((m,interest,1517-interest))
  ts=[.12+(D-.3)*k/(len(samples)-1) for k in range(len(samples))]
  a.append(number(text('month','MONTH 1',100,305,1700,60,RED,align='center'),list(zip(ts,months)),'step','integer','MONTH ',''))
  ik=list(zip(ts,[x[1] for x in samples]));pk=list(zip(ts,[x[2] for x in samples]))
 else:
  ti=at(s,'thirteen hundred dollars');tp=at(s,'two hundred seventeen dollars');ik=[(ti,0),(end(s,ti),1300)];pk=[(tp,0),(end(s,tp),217)]
  a.append(text('month','FIRST MONTH / $1,517 LOAN PAYMENT',100,305,1700,46,RED,align='center'))
 for j,(label,keys,color) in enumerate([('INTEREST',ik,RED),('PRINCIPAL',pk,SAGE)]):
  y=450+j*195;start=keys[0][0]
  a += [text(f'part-label-{j}',label,110,y,390,38,INK),number(text(f'part-value-{j}','$0',1440,y-8,350,66,color,start,'right'),keys,'step' if over_time else 'smooth'),rect(f'track-{j}',110,y+90,1680,25,SAND)]
  a.append(anim(rect(f'part-bar-{j}',110,y+90,1,25,color,start),'width',[(t,v/1517*1680) for t,v in keys],'step' if over_time else 'smooth'))
 a.append(text('split-note','Rounded figures · $240,000 loan · 6.5% fixed interest · 30 years',100,870,1700,25,MUTED,align='center'))
 if over_time:a.append(text('term-note','Compressed loan term · no extra payments · no home-price forecast',100,910,1700,24,MUTED,align='center'))
 return a
def grid(s):
 a=base(s);entries=[('HOUSING BILLS','housing bills'),('REPAIR SAVINGS','repair allowance'),('UTILITIES','utilities'),('FOOD','food'),('TRANSPORT','transportation'),('DEBT PAYMENTS','debt payments'),('OTHER EXPENSES','other expenses')]
 for k,(label,phrase) in enumerate(entries):
  t=at(s,phrase);x=100+(k%4)*445;y=340+(k//4)*265
  a += [rect(f'category-{k}',x,y,405,225,SAND if k!=1 else LIGHT,t),text(f'category-label-{k}',label,x+20,y+73,365,35,INK,t,'center')]
 return a
def documents(s):
 a=base(s)
 for k,(label,phrase) in enumerate([('LOAN ESTIMATE','The Loan Estimate'),('CLOSING DISCLOSURE','The Closing Disclosure')]):
  x=190+k*850;t=at(s,phrase);a += [rect(f'paper-{k}',x,310,670,565,'#fffcf5',t),text(f'paper-label-{k}',label,x+35,350,600,34,RED,t,'center')]
  for z,field in enumerate(['Loan terms','Escrow / other costs','Cash needed to close']):
   a += [text(f'field-{k}-{z}',field,x+55,470+105*z,560,31,INK,t),rect(f'line-{k}-{z}',x+55,530+105*z,560,2,SAND,t,0)]
 a.append(text('concept','Conceptual layouts · check your actual disclosures and resolve differences',110,903,1700,25,MUTED,align='center'));return a
def build(s):
 i=s['paragraph']
 if i in [0,1]:return prop(s,'A PLACE TO\nCALL YOUR OWN.','Space, control, and a home you can picture.', 'house' if i==0 else 'keys')
 if i in [2,3,4,6,86]:return calculator(s,None if i==2 else ('≈ $1,500' if i in [3,4] else '$1,517'))
 if i in [5,7,8,10]:return prop(s,*{5:('ONE PAYMENT.\nPART OF THE PICTURE.','The loan calculation covers one part of ownership.'),7:('THE LIFE AROUND\nTHE HOUSE.','Bills, upkeep and the cash you keep available.'),8:('LOAN PAYMENT\n≠ FULL BUDGET','Compare the same categories.'),10:('A PAYMENT CAN FIT.\nA BUDGET CAN STRAIN.','Leave room for expenses beyond the loan.')}[i],asset='compare' if i in [5,8] else 'bills')
 if i==9:return prop(s,'MEET JAMIE.','A fictional buyer. All amounts are illustrative.','keys')
 if i==11:
  a=cards(s,[('HOME PRICE','$300,000','Fictional purchase'),('DOWN PAYMENT','$60,000','20% in this example')],reveals={0:at(s,'three-hundred-thousand-dollar'),1:at(s,'sixty thousand dollars')})
  for j,(phrase,val) in enumerate([('three-hundred-thousand-dollar',300000),('sixty thousand dollars',60000)]):
   t=at(s,phrase);number(next(l for l in a if l['id']==f'value-{j}'),[(t,0),(end(s,t),val)])
  return a
 if i==12:return big(s,'MORTGAGE PRINCIPAL',240000,0,when=at(s,'two-hundred-forty-thousand-dollar'),asset='house',detail='$300,000 price − $60,000 down')
 if i==13:return cards(s,[('STANDARD FIXED LOAN','30 YEARS','360 monthly payments'),('ASSUMED INTEREST','6.5%','Nominal interest, not APR'),('FINANCED FEES','$0','None added to this example')],reveals={0:at(s,'thirty-year'),1:at(s,'six-point-five-percent'),2:at(s,'no fees')})
 if i==14:return big(s,'PRINCIPAL + INTEREST',1517,0,when=at(s,'fifteen hundred seventeen dollars'),maxval=2267,detail='$240,000 · 6.5% fixed interest · 30 years')
 if i in [15,16,17,18]:return budget(s,5 if i==18 else 4)
 if i==19:return cards(s,[('LOAN PAYMENT','$1,517','Principal + interest'),('HOUSING ALLOCATION','$2,267','Bills + repair savings'),('DIFFERENCE','+$750','Before utilities')],reveals={2:at(s,'seven hundred fifty dollars')})
 if i==20:return cards(s,[('MONEY PAID OUT','$2,017','Monthly bills'),('MONEY YOU KEEP','$250','Repair savings')],reveals={1:at(s,'The repair money')})
 if i==21:return prop(s,'YOUR PROPERTY.\nYOUR NUMBERS.','Replace every assumption with local information.','compare')
 if i in [22,23,25,26,30]:return prop(s,*{22:('LOOK INSIDE\nTHE PAYMENT.','Make sure you know what is included.'),23:('ALREADY INCLUDED?\nCOUNT IT ONCE.','Do not add tax or insurance a second time.'),25:('A DIFFERENT ROUTE.\nTHE SAME BILLS.','Escrow does not make taxes or insurance disappear.'),26:('PRINCIPAL + INTEREST\nOR TOTAL PAYMENT?','Those labels can describe different bundles.'),30:('COMPARE LIKE\nWITH LIKE.','A smaller number can include fewer bills.')}[i],asset='compare' if i in [22,26,30] else 'bills')
 if i==24:return flow(s)
 if i==27:return cards(s,[('ASSOCIATION FEE','SEPARATE','May be paid outside the loan payment'),('MAINTENANCE','BUDGET FOR IT','Usually needs its own allowance')],reveals={1:at(s,'Maintenance')})
 if i==28:return cards(s,[('SCHEDULED P&I','FIXED','Typical standard fixed-rate loan'),('TAX + INSURANCE','CAN CHANGE','Total collection can change too')],reveals={1:at(s,'Property taxes')})
 if i==29:return cards(s,[('JAMIE’S EXAMPLE','20% DOWN','Conventional loan assumption'),('MORTGAGE INSURANCE','$0 HERE','Other loans can differ')])
 if i==31:return prop(s,'CASH IN\nTHE BANK.','The purchase changes what remains available.','bills')
 if i==32:return cash(s,75000,0,equity=0,detail='Starting savings in this fictional example')
 if i==33:return cash(s,15000,75000,moving=True,detail='$60,000 moves into the home')
 if i==34:
  a=cards(s,[('OTHER CLOSING AMOUNTS','$9,000','Assumed total, not a universal fee'),('WHAT IS INSIDE','FEES + PREPAIDS','Also initial escrow funding')],reveals={0:at(s,'nine thousand dollars'),1:at(s,'including the fees')});t=at(s,'nine thousand dollars');number(next(l for l in a if l['id']=='value-0'),[(t,0),(end(s,t),9000)]);return a
 if i==35:return cash(s,6000,15000,detail='No credits or earlier deposits in this example')
 if i==36:return big(s,'MOVING + ESSENTIALS',2000,0,when=at(s,'two thousand'),asset='keys',detail='A separate assumed outlay')
 if i==37:return cash(s,4000,6000,detail='After down payment, closing amounts and moving')
 if i==38:return cash(s,4000,equity=60000,detail='The down payment has value in the home')
 if i in [39,40,41,42]:return prop(s,*{39:('EQUITY IS NOT\nCASH IN THE BANK.','It is not immediately available for the next bill.'),40:('PAID AHEAD.\nNOT PAID TWICE.','Prepaid tax or insurance is not another copy of the bill.'),41:('WHAT HAPPENS\nWHEN A BILL ARRIVES?','Can the remaining cash handle it?'),42:('GETTING THE KEYS\nIS ONE TEST.','Having breathing room afterward is another.')}[i],asset='compare' if i==39 else 'bills')
 if i in [43,44]:return calendar(s,i-42)
 if i==45:return prop(s,'DO I REALLY\nNEED THIS FUND?','A quiet month can hide a future bill.','bills')
 if i==46:return prop(s,'THEN SOMETHING\nBREAKS.','The repair has a deadline of its own.','repair')
 if i==47:return big(s,'HYPOTHETICAL REPAIR BILL',3000,0,when=at(s,'three-thousand-dollar repair'),asset='repair',detail='An illustrative amount, not a job quote')
 if i==48:return annual(s)
 if i==49:return prop(s,'MONTH TWO.\nTHE BILL ARRIVES.','An early bill does not wait for a year of saving.','repair')
 if i==50:return big(s,'TWO MONTHLY TRANSFERS',500,0,when=at(s,'five hundred dollars'),asset='bills',maxval=3000,detail='2 × $250 = $500 accumulated')
 if i==51:
  a=cards(s,[('REPAIR BILL','$3,000','Hypothetical'),('ACCUMULATED','$500','Two transfers'),('GAP','$2,500','Needs another available source')]);stop=end(s,0);number(next(l for l in a if l['id']=='value-2'),[(0,0),(stop,2500)]);a += [rect('gap-track',1317,750,468,12,LIGHT),anim(rect('gap-bar',1317,750,390,12,RED),'width',[(0,0),(stop,390)])];return a
 if i in [52,53]:return cards(s,[('MONTHLY ALLOWANCE','OVER TIME','Build the reserve'),('STARTING CUSHION','READY EARLY','Helps with bad timing')])
 if i==54:
  a=flow(s)
  labels=[l for l in a if l['id'].startswith('label-')]
  for l,t in zip(labels,['SET ASIDE','REPAIR FUND','PAY REPAIR']):l['text']=t
  return a
 if i in [55,56,57]:return prop(s,*{55:('THE VALUE\nIN YOUR HOME.','Equity matters, but it answers a different question.'),56:('PRINCIPAL PAID\nREDUCES THE DEBT.','Home value can also change.'),57:('THE ENTIRE PAYMENT\nIS NOT EQUITY.','Interest does not reduce the loan balance.')}[i],asset='house')
 if i in [58,59]:return split(s,i==59)
 if i==60:return cards(s,[('PROPERTY TAX','$300','Does not reduce principal'),('INSURANCE','$125','Does not reduce principal'),('HOA','$75','Does not reduce principal')])
 if i==61:return cards(s,[('ESTIMATED HOME VALUE','NOT CASH','Price changes do not fund checking'),('AVAILABLE CASH','SPENDABLE','A separate number')])
 if i==62:return prop(s,'ACCESS CAN HAVE\nCOSTS AND RISKS.','Selling or another loan may be needed. Price gains are not guaranteed.','compare')
 if i==63:return prop(s,'THE BILL IS\nDUE FRIDAY.','Balance-sheet progress may not solve a cash deadline.','bills')
 if i in [64,65]:return cards(s,[('EQUITY','WHAT YOU OWN','Wealth in the home'),('CASH','WHAT YOU CAN PAY','Available money')])
 if i==66:return prop(s,'BUILD A MONTH\nAROUND THE HOUSE.','Start with the complete housing allocation.','bills')
 if i==67:return prop(s,'TAKE-HOME PAY.','Use the money that actually reaches your account.','bills')
 if i==68:return grid(s)
 if i==69:return cards(s,[('SAVING','WHAT REMAINS?','Keep other goals visible'),('EMERGENCIES','WHAT REMAINS?','Your own circumstances matter'),('LIFE','WHAT REMAINS?','Leave room beyond housing')])
 if i==70:return prop(s,'CHECK THIS\nPROPERTY.','Insurance quotes · local taxes · association documents · inspection','compare')
 if i==71:return documents(s)
 if i==72:return prop(s,'TRY A LESS\nCOMFORTABLE MONTH.','See what would change the plan.','compare')
 if i==73:return cards(s,[('INSURANCE','RISES','Test the effect'),('REPAIR','ARRIVES EARLY','Test the timing'),('INCOME','FALLS','Test the response')],note='Illustrative scenarios, not a forecast or a dollar estimate.',reveals={1:at(s,'What if a repair'),2:at(s,'What if income')})
 if i==74:return cards(s,[('ONE CHANGE','TEST IT','You do not need every bad event at once'),('ANOTHER CHANGE','TEST IT','Look for a workable response')],note='Scenario planning · no universal affordability threshold.')
 if i==75:return prop(s,'KEEP A\nWORKABLE RESPONSE.','Know which changes would leave you without one.','compare')
 if i==76:return cards(s,[('STABILITY','',''),('CONTROL','',''),('A PLACE TO STAY','','')],note='The nonfinancial benefits of a home belong in the decision too.')
 if i in [77,78]:return prop(s,*{77:('THE BENEFITS\nCOUNT TOO.','A home is more than a calculator result.'),78:('ROOM FOR THE\nREST OF YOUR LIFE.','Benefits are easier to enjoy with breathing room.')}[i],asset='keys',note='Personal priorities differ; no universal dollar value is assigned.')
 if i==79:return cards(s,[('SMALLER PROPERTY','','One possible choice'),('MORE TIME TO SAVE','','Another possible choice'),('COMFORTABLE FIT','','Different circumstances')],note='Different buyers, different choices; no option fits everyone.')
 if i==80:return prop(s,'YOUR HOME.\nYOUR CIRCUMSTANCES.','No single down payment or repair allowance fits every buyer.','compare')
 if i==81:
  a=base(s,'Consider the full budget and the cash that remains.');a += [text('closing-question','WHAT DOES THE HOME\nLEAVE YOU?',140,380,1640,108,RED,align='center')];return a
 if i==82:return cards(s,[('AFTER THE BILLS','','What remains?'),('AFTER UPKEEP SAVINGS','','What remains?'),('AFTER THE PURCHASE','','What choices remain?')])
 if i in [83,84,85]:return prop(s,*{83:('REPAIR WITHOUT\nANOTHER PAYMENT?','The cash cushion and repair savings have a job.'),84:('CAN YOU\nKEEP SAVING?','Keep goals beyond the house in view.'),85:('ROOM FOR AN\nORDINARY LIFE.','Every expense need not feel like a setback.')}[i],asset='repair' if i==83 else 'keys',note='Choose using your own income, obligations and priorities.')
 if i==87:return prop(s,'THE ROOM\nYOU HAVE LEFT.','That is what tells you whether the home fits.','keys',note='Your Mortgage Payment Is Only the Beginning')
 raise ValueError(i)
clips=[]
for s in shots:
 layers=build(s)
 assert all(l['enter']<s['duration'] for l in layers),(s['paragraph'],s['duration'])
 clips.append(dict(id=s['id'],title=f'{s["section"]:02d} · {titles[s["paragraph"]]}',duration=s['duration'],background=BG,fade=0 if not clips else .04,layers=layers))
caps=[];group=[]
def flush():
 if not group:return
 first,last=group[0],group[-1];start=times[first];stop=min(total,times[last+1]-.015 if last+1<len(times) else total,max(start+.2,times[last]+.4))
 if stop>start:caps.append(dict(start=round(start,3),end=round(stop,3),text=' '.join(tokens[k].group() for k in group)))
 group.clear()
for k,t in enumerate(tokens):
 if group and len(' '.join([*(tokens[j].group() for j in group),t.group()]))>72:flush()
 group.append(k)
 if len(group)>=9 or (len(group)>=3 and re.search(r'[.!?]$',t.group())):flush()
flush()
source=V/'audio/You find a house you can f.wav'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='9586941c972c26238f808a0c6c3ad0a5416f53f0e2ba07410a45e6c6f27c619c'
with wave.open(str(source)) as f:samples=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)
peaks=[round(min(1,float(np.sqrt(np.mean(c*c)))/7000),3) for c in np.array_split(samples,1400)]
project=dict(kind='credit-studio-video',version=1,revision='mortgage-review-v01',name='Mortgage Payment — Bản duyệt đầy đủ v01',width=1920,height=1080,fps=30,audio=dict(src='videos/005-mortgage-payment/review/voiceover.mp3',offset=0,volume=1),assets=assets,clips=clips,captions=caps,captionLanguage='en',showCaptions=False,waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
for s in shots:s['title']=titles[s['paragraph']];s['end']=round(s['start']+s['duration'],6)
(OUT/'shot-plan.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2)+'\n')
motion=[{'clipId':c['id'],'start':s['start'],'layers':[l['id'] for l in c['layers'] if 'animation'in l]} for c,s in zip(clips,shots) if any('animation'in l for l in c['layers'])]
(OUT/'motion-plan.json').write_text(json.dumps(motion,indent=2)+'\n')
info=json.loads((V/'audio/source.json').read_text());info.update(reviewRevision=project['revision'],sourceSpeedChanged=False,narrationUnchanged=True,buildFrom='Approved repository script, sample visual style and Jamie illustrations; browser-only edits are not included',music=False)
(OUT/'source.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
readme=['# Mortgage Payment — Bản duyệt đầy đủ v01','',f'**88 cảnh /566,45 giây /1920×1080 /30 fps**, chờ người dùng duyệt, chưa phải bản cuối.','',f'{sum(len(m["layers"]) for m in motion)} lớp chuyển động nội dung trong {len(motion)} cảnh; các thẻ hiện theo lời. Times New Roman, bốn nhóm Jamie và hình nhà SVG. Không thêm nhạc hoặc rig khớp.','', 'Audio gốc, script, sample JSON và các bản sửa IndexedDB được bảo toàn. Bản đầy đủ dựng từ repo; không ghép các sửa riêng chưa bàn giao.','', '| Bắt đầu | Kết thúc | Cảnh |','| --- | --- | --- |']
for s in shots:readme.append(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["title"]} |')
readme += ['','Timing từ ASR và ánh xạ kịch bản; số/hyphen có nội suy. Phụ đề tiếng Anh mặc định tắt, bật được trong Studio. Giữ nguyên nguồn WAV, không đổi tốc độ.','', 'Builder từ chối ghi đè review đã có. Khi sửa, dùng JSON/bản sao lưu của người dùng nếu cần; xuất phiên bản mới và giữ v01.']
(OUT/'README.md').write_text('\n'.join(readme)+'\n')
print(json.dumps({'clips':len(clips),'duration':sum(c['duration'] for c in clips),'captions':len(caps),'animatedLayers':sum(len(m['layers']) for m in motion),'animatedClips':len(motion)}))
