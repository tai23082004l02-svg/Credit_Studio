#!/usr/bin/env python3
"""Build one primary scenic Musk review; preserve audio, script and existing builds."""
from pathlib import Path
import json,re,math,wave,hashlib
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];V=ROOT/'videos/006-musk-buy-a-country';OUT=V/'review';REL=V.relative_to(ROOT).as_posix()
if (OUT/'project.json').exists():raise SystemExit('Review exists: preserve edits and use a new version.')
body=(V/'narration.txt').read_text();tokens=list(re.finditer(r'\S+',body));rows=json.loads((V/'production/script-timing.json').read_text());times=[r['start'] for r in rows];assert [m.group() for m in tokens]==[r['word'] for r in rows]
chap=json.loads((V/'production/chapters.json').read_text())['chapters'];total=535.525
BG='#0a1925';WHITE='#f5f0e8';GOLD='#ebc58b';TEAL='#8ed2c5';RED='#d98274';PANEL='#102633'
assets={}
for id in ['lisbon','industry','finance','neighborhood','hospital','infrastructure','civic']:assets[id]={'src':f'{REL}/images/generated/{id}-v01.png','label':'Editorial scenic illustration · '+id}
for id in ['musk-standing','musk-palm','musk-thinking','musk-folder','portugal-mainland']:assets[id]={'src':f'{REL}/images/cutouts/{id}.png','label':id}
shots=[];offset=0
for i,p in enumerate(body.strip().split('\n\n')):
 start=0 if i==0 else times[offset];s={'id':f'musk-{i+1:03d}','paragraph':i,'section':next(c['section'] for c in reversed(chap) if start>=c['start']-.01),'start':start,'text':p,'tokenStart':offset,'tokenEnd':offset+len(p.split())};shots.append(s);offset+=len(p.split())
for i,s in enumerate(shots):s['end']=shots[i+1]['start'] if i+1<len(shots) else total;s['duration']=round(s['end']-s['start'],6)
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower());words=[norm(m.group()) for m in tokens]
def cue(s,phrase):
 q=[norm(x) for x in phrase.split()]
 for k in range(s['tokenStart'],s['tokenEnd']-len(q)+1):
  if words[k:k+len(q)]==q:return max(0,times[k]-s['start'])
 raise ValueError((s['paragraph'],phrase))
def text(id,t,x,y,w,size=48,fill=WHITE,align='left',enter=0):return dict(id=id,type='text',text=t,x=x,y=y,w=w,h=math.ceil(size*1.2*(t.count('\n')+1)+6),size=size,fill=fill,align=align,enter=round(enter,4),effect='fade' if enter else 'none',opacity=1,drift=0)
def rect(id,x,y,w,h,fill=PANEL,opacity=1,enter=0,radius=10):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,opacity=opacity,enter=round(enter,4),effect='none',drift=0,radius=radius)
def pic(id,asset,x,y,w,h,enter=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=round(enter,4),effect='fade' if enter else 'none',opacity=1,drift=0)
def animate(l,prop,keys,easing='smooth',**extra):l['animation']=dict(property=prop,easing=easing,keys=[dict(time=round(t,5),value=round(v,6)) for t,v in keys],**extra);return l
def num(l,keys,easing='smooth',currency=True,suffix='',prefix=''):return animate(l,'number',keys,easing,format='currency' if currency else 'integer',prefix=prefix,suffix=suffix)
def rise(l,value,s,at=0,span=1,suffix='',currency=True):l['enter']=round(at,4);return num(l,[(at,0),(min(s['duration']-.05,at+span),value)],suffix=suffix,currency=currency)
titles=[
'COULD ELON MUSK BUY A COUNTRY?','ONE MAN. ONE COUNTRY.','THE ESTIMATED FORTUNE.','A YEAR OF PORTUGAL’S OUTPUT.','TWO NUMBERS. DIFFERENT MEASURES.','A FORTUNE AT NATIONAL SCALE.','WEALTH TODAY. PRODUCTION OVER A YEAR.','FOLLOW THE MONEY.',
'A COUNTRY AT WORK.','WHAT GDP MEASURES.','WHAT GDP DOES NOT MEASURE.','ASSETS AND ANNUAL INCOME.','SCALE DOES NOT SET A PRICE.','PORTUGAL HAS NO GDP PRICE TAG.',
'THE OTHER SIDE OF THE COMPARISON.','WHERE THE WEALTH SITS.','A HIGHER VALUE IS NOT A CASH DEPOSIT.','A LOWER VALUE IS NOT CASH SPENT.','THE RANKING IS NOT A BANK BALANCE.','OWNERSHIP CAN CREATE OPTIONS.',
'FINANCING SOMETHING ENORMOUS.','SELLING REQUIRES A TRANSACTION.','BORROWING ADDS A LIABILITY.','COLLATERAL CAN LOSE VALUE.','MORE OPTIONS. REAL COSTS.','COMPANY CASH AND PERSONAL CASH.',
'A THOUGHT EXPERIMENT.','THE POPULATION USED IN THIS EXAMPLE.','ONE PAYMENT TO EVERY RESIDENT.','THE COST OF ONE ROUND.','A HOUSEHOLD PAYMENT. A NATIONAL TOTAL.','NOW REPEAT IT EACH YEAR.','FIRST, MAKE THE ASSUMPTIONS EXPLICIT.','EIGHT COMPLETE ROUNDS. PART OF A NINTH.','A MODEL, NOT A FUNDING FORECAST.',
'FROM MONEY TO PROJECTS.','WHAT CAPITAL CAN HELP FINANCE.','BUILDING IS ONLY THE BEGINNING.','KEEP THE SCHOOL AND RAILWAY RUNNING.','DELIVERY TAKES MORE THAN MONEY.','REAL COSTS NEED REAL PROJECT DETAILS.','INITIAL INVESTMENT. ONGOING RESOURCES.',
'BACK TO PORTUGAL.','A COUNTRY IS NOT ONE PACKAGE.','OWNERSHIP RIGHTS HAVE A SCOPE.','SOVEREIGNTY IS NOT A PROPERTY BONUS.','A BOND IS A FINANCIAL CLAIM.','INFLUENCE AND THE RIGHT TO GOVERN.',
'CAN THE COMPARISON ANSWER THE QUESTION?','THE NUMBERS DO NOT ESTABLISH A PURCHASE.','EXTRAORDINARY SCALE. PRACTICAL CONDITIONS.','ASK WHAT THE MONEY CAN DELIVER.','FOLLOW THE PROJECT THROUGH TIME.','UNDERSTAND THE POSSIBILITIES.','WHAT THE NUMBER CAN CHANGE.']
assert len(titles)==len(shots)==55
notes=['Forbes estimate · 01 OCT 2026 · GDP/population: World Bank 2025 · Editorial illustrations']*55
for i in [3,4,6,9,10,11,12,13,48,49]:notes[i]='GDP = annual output, not national wealth, public budget or purchase price · World Bank / IMF'
for i in range(26,35):notes[i]='HYPOTHETICAL EDITORIAL MODEL · Rounded population · Not a Musk proposal or government program'
for i in range(35,42):notes[i]='Conceptual projects, not actual Musk-funded works · No assumed unit cost or guaranteed outcome'
for i in range(42,48):notes[i]='Property / securities ownership does not itself transfer sovereignty · Investor.gov / UN Charter'
notes[16]=notes[17]='Conceptual valuation change only · No sale or distribution assumed · Not a real stock-price series'
notes[32]=notes[33]='ASSUME $936B ALREADY CASH · No taxes, returns, inflation, population change or administration costs'
clips=[]
def basic(s,bg):
 im=Image.open(ROOT/assets[bg]['src']);scale=max(2020/im.width,1140/im.height);w=im.width*scale;h=im.height*scale;x=(1920-w)/2;y=(1080-h)/2
 layers=[animate(pic('scenic-background',bg,x,y,w,h),'x',[(0,x-15),(s['duration'],x+15)]),rect('scenic-shade',0,0,1920,1080,BG,.22,radius=0),rect('title-contrast',0,0,1920,226,BG,.87,radius=0),text('chapter',f'{s["section"]:02} / COULD ELON MUSK BUY A COUNTRY?',90,29,1740,25,TEAL),text('headline',titles[s['paragraph']],90,84,1740,60),rect('source-contrast',0,992,1920,88,BG,.96,radius=0),text('source',notes[s['paragraph']],90,1014,1740,23,WHITE)]
 return layers
L=[]
def panel(x=820,y=300,w=1000,h=620):L.append(rect('information-panel',x,y,w,h,PANEL,.94))
def person(asset='musk-standing',x=190,y=286,w=470,h=670):L.append(pic('subject',asset,x,y,w,h))
def map_pic(x=1180,y=290,w=500,h=650):L.append(pic('map-outline','portugal-mainland',x,y,w,h))
def hero(head,detail='',subject=None,map=False):
 if subject:person(subject)
 elif map:map_pic(x=165,y=300,w=430,h=630)
 x=790 if subject or map else 280;w=1030 if subject or map else 1360;panel(x=x,y=334,w=w,h=500)
 L.append(text('statement',head,x+50,388,w-100,67,GOLD,'center'))
 if detail:L.append(text('detail',detail,x+60,660,w-120,32,WHITE,'center'))
def cards(items,s,phrases=None,y=390,h=390):
 gap=32;x=100;w=(1720-gap*(len(items)-1))/len(items)
 for j,(label,value,detail) in enumerate(items):
  xx=x+j*(w+gap);at=cue(s,phrases[j]) if phrases else min(j*.35,max(0,s['duration']-.8))
  L.append(rect(f'card-{j}',xx,y,w,h,PANEL,.94,at));L.append(text(f'label-{j}',label,xx+24,y+35,w-48,27 if len(items)>3 else 30,TEAL,'center',at));L.append(text(f'value-{j}',value,xx+25,y+min(140,h*.36),w-50,min(58,int((w-64)/max(1,len(value))/.75)),GOLD,'center',at))
  if detail:L.append(text(f'detail-{j}',detail,xx+24,y+h-85,w-48,27,WHITE,'center',at))
def flow(s,items,phrases=None):
 cards(items,s,phrases,y=355,h=470)
 if len(items)==3:
  at=.6;span=min(s['duration']-.3,5);note=rect('moving-claim',210,862,105,48,TEAL);animate(note,'x',[(at,210),(max(at+.1,span),1605)]);L.extend([note,text('moving-label','TRANSACTION / CLAIM',100,925,1720,24,TEAL,'center')])
for i,s in enumerate(shots):
 bg='lisbon' if i<14 or i>=48 else 'industry' if i<20 else 'finance' if i<26 else 'neighborhood' if i<35 else 'hospital' if i<38 else 'infrastructure' if i<42 else 'civic'
 L=basic(s,bg)
 if i in [0,1]:
  person('musk-standing',x=180,y=287,w=490,h=680);map_pic(x=1270,y=300,w=430,h=610);L.extend([rect('hook-panel',730,405,440,260,PANEL,.95),text('hook','MUSK\n& PORTUGAL',750,450,400,60,GOLD,'center'),text('map-label','MAINLAND OUTLINE',1180,925,620,23,WHITE,'center')])
 elif i==2:
  person('musk-folder');panel();L.extend([text('amount-label','ESTIMATED NET WORTH',880,360,880,36,TEAL,'center'),rise(text('wealth','$936 B',880,447,880,120,GOLD,'center'),936,s,cue(s,'nine hundred'),1.2,' B'),text('date','FORBES · 01 OCT 2026',880,665,880,34,WHITE,'center'),text('not-cash','Ownership value, not available cash',880,770,880,31,WHITE,'center')])
 elif i==3:
  map_pic(x=170,y=300,w=470,h=630);panel();at=cue(s,'three hundred');L.extend([text('amount-label','ANNUAL GDP · 2025',880,360,880,36,TEAL,'center'),text('gdp','$346.6 B',880,468,880,116,GOLD,'center',at),text('definition','Goods and services produced in one year',875,690,890,34,WHITE,'center'),text('date','WORLD BANK · CURRENT US DOLLARS',880,797,880,29,TEAL,'center')])
 elif i==4:
  panel(x=230,y=300,w=1460,h=630);L.extend([text('stock-label','MUSK / NET WORTH · 01 OCT 2026',300,337,1300,29,WHITE),text('stock-value','$936 B',300,382,1300,60,GOLD),rect('stock-bar',300,469,1300,32,GOLD),text('flow-label','PORTUGAL / ANNUAL GDP · 2025',300,540,1300,29,WHITE),text('flow-value','$346.6 B',300,585,1300,60,TEAL),rect('flow-bar',300,672,1300*346.6/936,32,TEAL),text('ratio','2.7× numerical scale · different measures',300,770,1300,48,GOLD,'center',cue(s,'two point seven'))])
 elif i==5:hero('A FORTUNE\nAT NATIONAL SCALE.','A scale comparison does not establish purchasing power.','musk-thinking')
 elif i==6:cards([('NET WORTH','AT ONE DATE','Estimated assets minus liabilities'),('GDP','OVER A YEAR','Value of production')],s)
 elif i==7:hero('FOLLOW\nTHE MONEY.','From the headline to actual financing.','musk-palm')
 elif i==8:cards([('RESTAURANT','DINNER','Final goods and services'),('SOFTWARE','PROJECT','Economic activity'),('FACTORY','GOODS','Production'),('PUBLIC SERVICES','SERVICES','Work across the economy')],s,['restaurant','software business','factory','Teachers'],y=650,h=285)
 elif i==9:
  panel(x=190,y=320,w=1540,h=590);L.extend([text('definition','FINAL GOODS + SERVICES',250,370,1420,60,GOLD,'center'),text('period','PRODUCED DURING A PERIOD',250,470,1420,40,WHITE,'center')]);start=.6;span=max(.3,s['duration']-1.0)
  for j in range(12):L.extend([rect(f'month-{j}',250+j*118,610,103,100,TEAL,.8,start+j/12*span),text(f'month-label-{j}',str(j+1),250+j*118,635,103,33,BG,'center',start+j/12*span)])
  L.append(text('year-label','ONE YEAR OF OUTPUT',250,775,1420,40,TEAL,'center'))
 elif i==10:cards([('GDP ≠','BANK BALANCE','Not money sitting in an account'),('GDP ≠','PUBLIC BUDGET','Not government spending'),('GDP ≠','PURCHASE PRICE','Not the price of national assets')],s,['bank balance',"government's",'combined sale'])
 elif i==11:cards([('INVESTMENTS','ASSET VALUE','A stock of wealth'),('ANNUAL SALARY','YEARLY INCOME','A flow over time')],s)
 elif i==12:hero('THE SAME DISTINCTION.\nA LARGER SCALE.','Wealth, income and output measure different things.',map=True)
 elif i==13:hero('SCALE.\nNO PRICE TAG.','GDP does not value every asset in Portugal.',map=True)
 elif i==14:hero('LOOK INSIDE\nTHE FORTUNE.','Ownership, valuation and cash are different.','musk-thinking')
 elif i==15:
  person('musk-folder');panel();L.extend([text('formula','ASSETS − LIABILITIES',870,375,900,52,GOLD,'center'),text('formula-result','= NET WORTH',870,480,900,63,TEAL,'center'),text('company-label','OWNERSHIP INTERESTS',870,635,900,29,WHITE,'center'),text('companies','SpaceX · Tesla',870,718,900,62,GOLD,'center',cue(s,'SpaceX'))])
 elif i in [16,17]:
  panel(x=180,y=310,w=1560,h=610);L.extend([text('valuation-label','OWNERSHIP VALUATION',240,365,1370,35,WHITE),text('direction','CAN RISE' if i==16 else 'CAN FALL',240,435,1370,62,GOLD),rect('valuation-track',240,550,1400,42,'#294958'),animate(rect('valuation-bar',240,550,400 if i==16 else 1200,42,TEAL),'width',[(.4,400 if i==16 else 1200),(max(.8,s['duration']-.4),1200 if i==16 else 400)]),text('cash-label','CASH RECEIVED' if i==16 else 'CASH SPENT',240,665,1000,37,WHITE),text('cash-zero','$0',1280,650,350,70,TEAL,'right'),text('scenario','Price change alone; no sale or distribution in this illustration',240,812,1400,28,WHITE,'center')])
 elif i==18:hero('ESTIMATED WEALTH\nIS NOT A CASH BALANCE.','A ranking does not show money ready to transfer.','musk-standing')
 elif i==19:flow(s,[('OWNERSHIP','REAL VALUE','An economic asset'),('FINANCING','OPTIONS','Sale or eligible borrowing'),('TRANSACTION','CONDITIONS','Constraints and consequences')])
 elif i==20:hero('FINANCE\nSOMETHING ENORMOUS.','First: how would the cash become available?','musk-palm')
 elif i==21:flow(s,[('SELL ASSETS','FIND BUYERS','A transaction is required'),('SALE PRICE','CAN CHANGE','Large positions and market impact'),('PROCEEDS','CONDITIONAL','Taxes and restrictions may apply')],['selling assets','buyers','taxes'])
 elif i==22:flow(s,[('ELIGIBLE HOLDINGS','COLLATERAL','Only if lenders agree'),('BORROWING','CASH LOAN','Ownership may be retained'),('OBLIGATION','DEBT + INTEREST','Collateral requirements remain')])
 elif i==23:
  panel(x=230,y=330,w=1460,h=570);L.extend([text('collateral-label','COLLATERAL VALUE',290,390,1340,44,GOLD,'center'),rect('collateral-track',300,500,1320,42,'#294958'),animate(rect('collateral-bar',300,500,1200,42,TEAL),'width',[(0,1200),(s['duration']*.6,600)]),text('requirement','MORE SECURITY / REPAYMENT',290,650,1340,54,WHITE,'center',cue(s,'lender'))])
 elif i==24:hero('MORE OPTIONS.\nREAL COSTS.','Financing access does not remove the obligations.','musk-thinking')
 elif i==25:cards([('COMPANY','COMPANY CASH','Corporate funds'),('SHAREHOLDER','PERSONAL CASH','Separate from company accounts')],s)
 elif i==26:hero('A THOUGHT\nEXPERIMENT.','An editorial example, not an actual program.')
 elif i==27:
  map_pic(x=170,y=310,w=450,h=610);panel();L.extend([text('population-label','PORTUGAL · 2025 POPULATION',870,370,900,32,TEAL,'center'),text('population','≈10.8 MILLION',870,465,900,87,GOLD,'center',cue(s,'ten point eight')),text('population-note','Rounded for the arithmetic example',870,680,900,34,WHITE,'center'),text('source-population','World Bank · exact estimate 10,804,871',870,780,900,28,TEAL,'center')])
 elif i==28:
  panel(x=350,y=330,w=1220,h=570);L.extend([text('payment-label','EACH RESIDENT · INCLUDING CHILDREN',410,380,1100,36,TEAL,'center'),rise(text('payment','$10,000',410,484,1100,120,GOLD,'center'),10000,s,cue(s,'ten thousand'),.9),text('frequency','ONE PAYMENT',410,735,1100,40,WHITE,'center')])
 elif i==29:
  panel(x=230,y=300,w=1460,h=630);at=cue(s,'one hundred');L.extend([text('model-equation','10.8M RESIDENTS × $10,000',290,345,1340,47,TEAL,'center'),rise(text('round-cost','$108 B',290,440,1340,112,GOLD,'center'),108,s,at,1.0,' B'),text('share-label','SHARE OF THE $936B ESTIMATE',290,635,1340,29,WHITE,'center'),rect('share-track',300,700,1320,36,'#294958'),animate(rect('share-bar',300,700,1,36,TEAL,1,at),'width',[(at,0),(min(s['duration']-.1,at+1),1320*108/936)]),text('share','≈12%',290,785,1340,65,TEAL,'center',cue(s,'roughly twelve'))])
 elif i==30:cards([('HOUSEHOLD','$10,000 ONCE','Hypothetical per resident'),('NATIONAL TOTAL','≈$108 B','Rounded population')],s,y=620,h=320)
 elif i==31:hero('REPEAT THE PAYMENT\nEVERY YEAR.','A new scenario with the same starting amount.')
 elif i==32:
  panel(x=160,y=300,w=1600,h=645);L.extend([text('assume-cash','ASSUME $936B IS ALREADY CASH',210,342,1500,55,GOLD,'center'),text('exclude-label','FOR THIS MODEL ONLY, IGNORE:',210,455,1500,34,TEAL,'center')])
  excluded=[('TAXES','taxes'),('RETURNS','investment returns'),('INFLATION','inflation'),('POPULATION CHANGE','population changes'),('ADMINISTRATION','administration costs')]
  for j,(label,phrase) in enumerate(excluded):
   at=cue(s,phrase);xx=230+(j%3)*490;yy=555+(j//3)*150;L.extend([rect(f'excluded-card-{j}',xx,yy,455,112,'#294958',.97,at),text(f'excluded-{j}',label,xx+20,yy+34,415,29,WHITE,'center',at)])
 elif i==33:
  panel(x=170,y=285,w=1580,h=670);t8=cue(s,'eight complete');begin=.4;finish=max(begin+.7,t8+.6);keys=[(0,936)]+[(begin+(j/8)*(finish-begin),936-108*j) for j in range(1,9)];years=[(t,(936-v)/108) for t,v in keys]
  L.extend([num(text('cash','$936 B',230,335,1460,100,GOLD,'center'),keys,'step',suffix=' B'),num(text('rounds','0 FULL ROUNDS',230,475,1460,44,TEAL,'center'),years,'step',False,' FULL ROUNDS'),rect('cash-track',270,580,1380,42,'#294958'),animate(rect('cash-bar',270,580,1380,42,TEAL),'width',[(t,v/936*1380) for t,v in keys],'step'),text('annual-cost','$108B PER ANNUAL ROUND',230,670,1460,35,WHITE,'center'),text('ninth-round','ROUND 9: $72B AVAILABLE / $108B NEEDED',230,790,1460,43,GOLD,'center',cue(s,'ninth'))])
 elif i==34:hero('THE MODEL SHOWS\nA RECURRING COMMITMENT.','It does not forecast Musk’s liquidation proceeds.')
 elif i==35:hero('FROM CAPITAL\nTO PROJECTS.','Initial funding connects to real-world delivery.')
 elif i==36:cards([('CAPITAL','BUILDINGS','A project needs funding'),('CAPITAL','EQUIPMENT','Resources must be available'),('CAPITAL','RESEARCH','Work takes people and time'),('CAPITAL','INFRASTRUCTURE','Conditions differ by project')],s,['buildings','equipment','research','infrastructure'],y=650,h=285)
 elif i==37:cards([('INITIAL FUNDING','BUILD','Construction and equipment'),('AFTER OPENING','OPERATE','Staff · medicine · utilities · upkeep')],s,['construction','opening'],y=620,h=320)
 elif i==38:cards([('SCHOOL','TEACHERS','Beyond the classrooms'),('RAILWAY','OPERATIONS','Beyond the tracks')],s,['teachers','operations'],y=650,h=285)
 elif i==39:cards([('DELIVERY','PEOPLE','Skills and labor'),('DELIVERY','MATERIALS','Physical resources'),('DELIVERY','APPROVALS','Conditions to meet'),('DELIVERY','TIME','Work to complete')],s,['people','materials','approvals','time'],y=650,h=285)
 elif i==40:hero('NO FICTIONAL UNIT COST\nBECOMES A REAL QUOTE.','Project, place and standard determine actual costs.')
 elif i==41:cards([('INITIAL','INVESTMENT','What makes the project possible'),('AFTERWARD','RESOURCES','What keeps it working')],s,y=620,h=320)
 elif i==42:hero('RETURN\nTO PORTUGAL.','A country is more than one transaction.',map=True)
 elif i==43:cards([('PRIVATE','PROPERTY','Different owners'),('PUBLIC','ASSETS','Different institutions'),('PEOPLE','RIGHTS','Their own decisions')],s,['private property','public assets','people'])
 elif i==44:cards([('BUSINESS / LAND','OWNERSHIP RIGHTS','Rights connected to that asset'),('GOVERNMENT','PUBLIC AUTHORITY','Not transferred by buying property')],s)
 elif i==45:hero('SOVEREIGNTY.','No automatic transfer with a property transaction.',map=True)
 elif i==46:flow(s,[('INVESTOR','LENDS MONEY','Buys a government bond'),('BOND','FINANCIAL CLAIM','Under its contractual terms'),('COUNTRY','SOVEREIGNTY','Not acquired with the bond')])
 elif i==47:cards([('WEALTH','INFLUENCE','Can be economically significant'),('GOVERNING','AUTHORITY','No automatic right to govern')],s)
 elif i==48:hero('CAN GDP SET\nA COUNTRY’S PRICE?','Estimated net worth versus annual production.','musk-thinking')
 elif i==49:hero('THAT CONCLUSION\nDOES NOT FOLLOW.','The comparison does not establish a purchase.',map=True)
 elif i==50:hero('EXTRAORDINARY SCALE.\nPRACTICAL CONDITIONS.','Liquidity · financing · choices','musk-folder')
 elif i==51:hero('WHAT CAN\nTHE MONEY DELIVER?','Follow it beyond the headline.')
 elif i==52:cards([('AVAILABILITY','CASH','What could be raised?'),('DELIVERY','PROJECT','What could it deliver?'),('OPERATIONS','PEOPLE','Who would operate it?'),('LONG TERM','10 YEARS','What keeps it working?')],s,['made available','investment deliver','operate it','ten years'],y=550,h=380)
 elif i==53:hero('UNDERSTAND\nTHE POSSIBILITIES.','And the resources needed to make them real.','musk-palm')
 elif i==54:hero('FOLLOW THE MONEY.','What it changes. How long it lasts. Where its power ends.','musk-standing')
 clips.append(dict(id=s['id'],title=f'{s["section"]:02} · {titles[i]}'[:100],duration=s['duration'],background=BG,fade=0,layers=L));s['title']=titles[i];s['background']=bg
# Clean English cues follow the unchanged source text.
caps=[];group=[]
def flush():
 if not group:return
 a,b=group[0],group[-1];start=times[a];stop=min(total,times[b+1]-.01 if b+1<len(times) else total,max(start+.2,times[b]+.45))
 if stop>start:caps.append(dict(start=round(start,3),end=round(stop,3),text=' '.join(tokens[k].group() for k in group)))
 group.clear()
for k,w in enumerate(tokens):
 if group and len(' '.join([*(tokens[j].group() for j in group),w.group()]))>72:flush()
 group.append(k)
 if len(group)>=9 or len(group)>=3 and re.search(r'[.!?]$',w.group()):flush()
flush()
source=V/'audio/tts_20261023_125715_dda159.wav';assert hashlib.sha256(source.read_bytes()).hexdigest()=='c26b2cd58cb7b9f7cd9dce14954c7668eabb699145499bb46125f6c8a93e45c5'
with wave.open(str(source)) as f:pcm=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)
peaks=[round(min(1,float(np.sqrt(np.mean(c*c)))/7000),3) for c in np.array_split(pcm,1400)]
project=dict(kind='credit-studio-video',version=1,revision='musk-scenic-review-v01',name='Musk & Portugal — Bản dựng bối cảnh v01',width=1920,height=1080,fps=30,audio=dict(src=f'{REL}/review/voiceover.mp3',offset=0,volume=1),assets=assets,clips=clips,captions=caps,showCaptions=False,captionLanguage='en',waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n');(OUT/'shot-plan.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2)+'\n')
motion=[{'clipId':c['id'],'layers':[l['id'] for l in c['layers'] if 'animation' in l]} for c in clips];(OUT/'motion-plan.json').write_text(json.dumps(motion,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt.extend([f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],''])
(OUT/'captions.vtt').write_text('\n'.join(vtt));info=json.loads((V/'audio/source.json').read_text());info.update(reviewRevision=project['revision'],alignment='faster-whisper base.en int8 + sequence alignment; automatic timing has uncertainty',wordMatches=1068,scriptWords=1115,sourceSpeedChanged=False,sourceContentChanged=False,music=False);(OUT/'source.json').write_text(json.dumps(info,indent=2)+'\n')
readme=['# Musk & Portugal — Bản dựng bối cảnh v01','','55 cảnh /535,525 giây /1920×1080 /30fps. Bản dựng từ script đã gửi và audio người dùng; chưa phải bản cuối được duyệt.','', 'Bảy scenic background AI và bốn tư thế Musk là minh họa biên tập, không phải ảnh tư liệu/sự kiện thật. Musk chỉ là đối tượng được nói đến. Chữ/số/đồ thị native Times New Roman; nền scenic có crop cover có chủ ý, không bóp méo; cutout nhân vật giữ đủ silhouette. Không nhạc hoặc lip-sync/rig nhân vật.','', 'Tài sản ròng là snapshot2026-10-01, GDP/population2025; GDP khác wealth/budget/price. Model936B giả định đã cash và không tax/returns/inflation/population/admin, không phải dự báo.','', 'Một JSON chính; preview trong thư viện lấy từ timeline này, không nhân bản thành bộ thiết kế JSON. Bản sửa IndexedDB riêng cần backup khi bàn giao. Audio gốc và source image/crop map được giữ; không ghi đè bản xuất.','', '| Bắt đầu | Kết thúc | Cảnh |','| --- | --- | --- |']
readme.extend(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["title"]} |' for s in shots);(OUT/'README.md').write_text('\n'.join(readme)+'\n')
print(json.dumps({'clips':len(clips),'duration':sum(c['duration'] for c in clips),'assets':len(assets),'captions':len(caps),'animatedLayers':sum('animation' in l for c in clips for l in c['layers'])}))
