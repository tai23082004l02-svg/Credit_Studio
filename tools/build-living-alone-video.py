#!/usr/bin/env python3
"""Build the narrated collage review from approved cues, preserved WAV and alignment.
Does not overwrite audio, original artwork, old boards or exported MP4 files.
"""
import json,re,math,wave,difflib,hashlib,argparse
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'videos/004-living-alone';P='videos/004-living-alone/';OUT=V/'review'
WAV=V/'audio/tts_20261022_133142_ba54ee.wav'
parser=argparse.ArgumentParser();parser.add_argument('--force',action='store_true');args=parser.parse_args()
if (OUT/'project.json').exists() and not args.force:raise SystemExit('Review exists. Back up manual edits before using --force for derived JSON/VTT files.')
body=(V/'narration.txt').read_text()
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
def cue(phrase,after=0):
 query=[norm(x) for x in phrase.split()]
 candidates=[i for i in range(len(source)-len(query)+1) if source[i:i+len(query)]==query and times[i]>=after-.001]
 assert candidates,(phrase,after)
 return round(times[candidates[0]],3)
with wave.open(str(WAV)) as wav:
 total=wav.getnframes()/wav.getframerate();sample_rate=wav.getframerate();channels=wav.getnchannels();samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)
BG='#f6f0e5';INK='#292722';RED='#873e3d';SAND='#eee3d4';SAGE='#e8e8da';MUTED='#685747'
EXAMPLE='Illustrative example — not national averages'
chapters=['THE KEYS','ONE FRONT DOOR','WHAT CHANGED','THE SMALLER BILLS','ONE INCOME','WHAT PRIVACY IS WORTH','A PLAN FOR ONE','THE ROOM TO STAY']
layout=json.loads((V/'asset-layout.json').read_text());assets={}
for sheet in layout['sheets']:
 for it in sheet['items']:assets[it['id']]={'src':P+it['image'],'label':it['name']}
for j in layout['jobs']:assets['art-'+j['id']]={'src':P+j['image'],'label':j['title']}
plan=json.loads((V/'edit-plan.json').read_text());shots=[]
for row in plan['shots']:
 s=dict(row);s['start']=cue(s['cue'],shots[-1]['start']+.001 if shots else 0);shots.append(s)
shots[0]['start']=0
assert 0<len(shots)<=100
assert all(a['start']<b['start'] for a,b in zip(shots,shots[1:]))
for i,s in enumerate(shots):s['duration']=round((shots[i+1]['start'] if i+1<len(shots) else total)-s['start'],6)
def text(id,t,x,y,w,size=54,fill=INK,enter=0,effect='none',align='center'):
 return dict(id=id,type='text',text=t,x=x,y=y,w=w,h=math.ceil(size*1.18*(t.count('\n')+1)+8),size=size,fill=fill,align=align,enter=round(enter,4),effect=effect,opacity=1,drift=0)
def rect(id,x,y,w,h,fill=SAND,enter=0):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=0,enter=round(enter,4),effect='none',opacity=1,drift=0)
def pic(id,asset,x,y,w,h,enter=0,effect='fade',drift=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=round(enter,4),effect=effect,opacity=1,drift=drift)
def animate(l,prop,keys,easing='smooth',**kw):
 assert len(keys)<=32
 l['animation']=dict(property=prop,easing=easing,keys=[dict(time=round(t,5),value=round(v,6)) for t,v in keys],**kw);return l
def number(l,keys,easing='smooth',format='currency',prefix='',suffix=''):return animate(l,'number',keys,easing,format=format,prefix=prefix,suffix=suffix)
def at(s,phrase):
 t=cue(phrase,s['start']-.001)-s['start']
 assert -.01<=t<s['duration'],(s['id'],phrase,t,s['duration'])
 return max(0,t)
def footer(out,note):out.append(text('note',note,90,950,1740,24,MUTED))
def base(s):return [text('chapter',f'{s["section"]:02d}  /  {chapters[s["section"]-1]}',80,32,1760,24,MUTED,align='left'),rect('rule',80,76,1760,2,RED),text('headline',s['headline'],90,112,1740,64)]
def prop(s,message='',detail='',note=''):
 out=base(s);out += [pic('prop',s['asset'],140,330,650,560,0,'fade',1),rect('copy-panel',900,330,900,570,SAND)]
 out += [text('message',message or s['headline'],950,440,800,58,RED)]
 if detail:out.append(text('detail',detail,950,700,800,35,MUTED))
 if note:footer(out,note)
 return out
def cards(s,items,note=''):
 out=base(s);n=len(items);gap=38;w=(1740-(n-1)*gap)/n
 for i,it in enumerate(items):
  x=90+i*(w+gap);enter=at(s,it['reveal']) if it.get('reveal') else min(.12*i,max(0,s['duration']-.65))
  out += [rect(f'card-{i}',x,335,w,550,SAND if i%2==0 else SAGE,enter),pic(f'icon-{i}','solo4-'+it['icon'],x+45,365,w-90,230,enter,'fade'),text(f'label-{i}',it['label'],x+22,645,w-44,34 if n<=3 else 29,INK,enter)]
  if it.get('value'):out.append(text(f'value-{i}',it['value'],x+22,750,w-44,45 if n<=3 else 30,RED,enter))
 if note:footer(out,note)
 return out
def item(icon,label,value='',reveal=None):return dict(icon=icon,label=label,value=value,reveal=reveal)
def layers(s):
 mode=s['layout'];D=s['duration'];end=max(.2,D-.2);quick=min(1.2,end)
 if mode=='illustration':
  out=base(s);out.append(pic('illustration',s['asset'],90,285,1740,650,0,'fade',1.5));return out
 if mode=='prop':
  messages={
   'house-keys':('YOUR OWN SPACE.','Some costs can be shared; privacy is a personal choice.'),
   'apartment':('THE HOUSEHOLD COST.','The listing is only part of the commitment.'),
   'bills':('THE WHOLE BILL.','One income has to carry the commitments.'),
   'router':('ONE CONNECTION.','The plan does not automatically cost half.'),
   'pay-envelope':('ONE HOUSEHOLD INCOME.','No automatic second paycheck.'),
   'fridge':('STILL RUNNING.','Some costs keep going regardless of household size.'),
   'armchair':('A WHOLE PIECE OF FURNITURE.','One person still needs a place to sit.'),
   'groceries':('BUY WHAT YOU WILL USE.','Portions, storage and waste all matter.'),
   'reserve-jar':('PROTECT SOME BREATHING ROOM.','A buffer depends on your own obligations.'),
   'calculator':('COMPARE THE BIG COMMITMENTS.','Include the costs of changing your plan.'),
   'support-phone':('HAVE SOMEONE TO CALL.','Independence can include a support network.'),
   'notebook':('MAKE AN HONEST PLAN.','Leave room for life beyond the rent.')}
  key=s['asset'].removeprefix('solo4-');msg,detail=messages.get(key,('LOOK AT THE WHOLE PICTURE.',''))
  return prop(s,msg,detail)
 if mode=='example-intro':return prop(s,'ILLUSTRATIVE AMOUNTS.','Alex and the two friends are fictional. Local prices vary.',EXAMPLE)
 if mode=='scope-note':
  if s['section']==2:return prop(s,'RENT + INTERNET ONLY.','Utilities and other living costs are not included.',EXAMPLE)
  if s['section']==3:return prop(s,'A NATIONAL PRICE CHANGE.','Not the price of your next apartment. City and lease differences matter.','BLS · Rent of primary residence CPI · 12 months ending Dec. 2024')
  return prop(s,'YOUR OWN NUMBERS MAY DIFFER.','Compare the tradeoff using your own budget.',EXAMPLE)
 if mode=='bill-reveal':
  if s['cue'].startswith('Then'):
   return cards(s,[item('apartment','RENT',reveal='Rent.'),item('bills','ELECTRICITY',reveal='Electricity.'),item('router','INTERNET',reveal='Internet.'),item('groceries','GROCERIES',reveal='Groceries.')])
  return cards(s,[item('house-keys','ONE PERSON'),item('bills','FULL BILLS')],'Some costs change with usage; others barely move.')
 if mode=='two-factors':return cards(s,[item('bills','HIGHER PRICES'),item('house-keys','NOBODY TO SPLIT WITH')],'Two pressures on a one-person household, not a numerical allocation.')
 if mode in ['rent-solo','rent-shared','internet-split','rent-compare','monthly-total']:
  out=base(s);amounts={'rent-solo':(1800,None),'rent-shared':(2400,1200),'rent-compare':(1800,1200),'internet-split':(60,30),'monthly-total':(1860,1230)}
  left,right=amounts[mode]
  if mode=='monthly-total' and s['section']==5:right=None
  labels=('LIVING ALONE','SHARE PER PERSON')
  if mode=='rent-shared':labels=('TWO-BEDROOM TOTAL','EACH OF TWO FRIENDS')
  for j,(val,label) in enumerate(zip((left,right),labels)):
   if val is None:continue
   x=100+j*920;enter=0
   if j==1 and s['section']==2:
    if mode=='rent-shared':enter=at(s,'Split equally,')
    elif mode=='internet-split':enter=at(s,'Each friend pays thirty.')
    elif mode=='monthly-total':enter=at(s,'Each friend pays twelve hundred and thirty.')
   stop=min(end,enter+quick)
   out += [rect(f'cost-card-{j}',x,330,800,555,SAND if j==0 else SAGE,enter),pic(f'cost-icon-{j}','solo4-'+('apartment' if mode.startswith('rent') else 'router'),x+280,355,240,180,enter,'fade'),text(f'cost-label-{j}',label,x+35,575,730,34,enter=enter),number(text(f'cost-value-{j}',f'${val:,}',x+35,650,730,90,RED,enter),[(enter,0),(stop,val)]),rect(f'cost-track-{j}',x+70,815,660,16,SAGE,enter)]
   maxval=max(left,right or 0);out.append(animate(rect(f'cost-meter-{j}',x+70,815,660*val/maxval,16,RED,enter),'width',[(enter,0),(stop,660*val/maxval)]))
   if mode=='monthly-total' and s['section']==2:out.append(text(f'sum-{j}','$1,800 + $60' if j==0 else '$1,200 + $30',x+35,770,730,28,MUTED,enter))
  if right is None:out += [pic('solo-key','solo4-house-keys',1100,360,620,350),text('solo-explanation','ONE PERSON PAYS THE FULL RENT.' if mode=='rent-solo' else 'RENT + INTERNET ONLY.',1040,760,760,38,RED)]
  if mode=='rent-shared':footer(out,EXAMPLE+' · $2,400 ÷ 2 = $1,200 each')
  elif mode=='internet-split':footer(out,EXAMPLE+' · $60 per apartment; $30 each when split by two')
  elif mode=='monthly-total':footer(out,EXAMPLE+' · Rent + internet only; total per person')
  else:footer(out,EXAMPLE+' · Monthly rent only')
  return out
 if mode=='monthly-gap':
  out=base(s);out += [pic('gap-prop',s['asset'],170,350,570,480),text('gap-label','RENT + INTERNET DIFFERENCE',850,340,940,36),number(text('monthly-gap','$630',850,445,940,140,RED),[(0,0),(quick,630)]),text('gap-detail','PER MONTH',850,645,940,46),text('gap-equation','$1,860 − $1,230 = $630',850,775,940,42,MUTED)]
  footer(out,EXAMPLE+' · Compare your own living arrangements');return out
 if mode=='annual-gap':
  out=base(s);out.append(text('annual-equation','$630 PER MONTH × 12 MONTHS',130,320,1660,48))
  span=min(end,max(.2,D-1.4));keys=[(0,0)]+[(span*i/12,630*i) for i in range(1,13)]
  out.append(number(text('annual-gap','$7,560',130,430,1660,145,RED),keys,easing='step'))
  for i in range(12):
   x=160+i*134;reveal=span*(i+1)/12;out += [rect(f'month-{i+1}',x,680,112,110,SAND,reveal),text(f'month-label-{i+1}',str(i+1),x,708,112,36,RED,reveal)]
  out.append(text('annual-label','PER YEAR · RENT + INTERNET GAP',130,840,1660,40));footer(out,EXAMPLE+' · Compressed 12-month illustration');return out
 if mode=='sharing-flow':
  out=cards(s,[item('apartment','ONE HOUSEHOLD COST'),item('house-keys','TWO PEOPLE CAN SHARE')],'Some costs do not double with a second person; not every bill divides equally.')
  # A separate bill strip moves above the cards; no cutouts overlap the labels.
  out.append(animate(pic('moving-bill','solo4-bills',230,280,100,48,0,'none'),'x',[(0,230),(end,1570)]));return out
 if mode=='rent-stat':
  out=base(s);out += [pic('rent-building','solo4-apartment',150,330,560,560),text('rent-stat','+4.3%',820,365,1000,150,RED),text('rent-stat-label','RENT OF PRIMARY RESIDENCE CPI',820,595,1000,36),text('rent-stat-period','12 months ending December 2024',820,710,1000,38)]
  footer(out,'Source: U.S. Bureau of Labor Statistics · Historical national index change, not a rent quote');return out
 if mode=='price-concept':return cards(s,[item('bills','SLOWER PRICE GROWTH','Prices still rise'),item('calculator','LOWER PRICES','A different claim')],'Conceptual comparison only · No invented inflation curve or price series')
 if mode=='household-stat':
  out=base(s);out += [text('household-count','38.5 MILLION',120,330,1680,110,RED),text('household-label','ONE-PERSON HOUSEHOLDS · 2024',120,495,1680,44),number(text('household-share','29%',120,625,1680,105,RED),[(0,0),(min(end,at(s,'roughly twenty-nine')),29)],format='integer',suffix='%'),text('household-denominator','OF U.S. HOUSEHOLDS — NOT PEOPLE',120,785,1680,39)]
  footer(out,'Source: U.S. Census Bureau · 2024 families and living arrangements');return out
 if mode=='denominator':return prop(s,'HOUSEHOLDS. NOT PEOPLE.','29% refers to U.S. households in 2024.','Source: U.S. Census Bureau · 2024')
 if mode=='variable-costs':return cards(s,[item('groceries','FOOD','One person uses less'),item('bills','UTILITIES','Usage can be lower')],'Some costs shrink; the exact amounts depend on the home and usage.')
 if mode=='food-tradeoff':return cards(s,[item('groceries','PRICE PER SERVING','Only if you eat it'),item('fridge','STORAGE + PORTIONS','Avoid unused food')],'Compare the cost of what you actually use, not only the package price.')
 if mode=='move-in-reveal':return cards(s,[item('moving-box','MOVING + FURNITURE'),item('deposit','DEPOSITS + SETUP')],'Upfront cash is a separate list; refundable deposits are not automatically money lost.')
 if mode=='cost-categories':return cards(s,[item('bills','MONTHLY','Recurring bills'),item('moving-box','UPFRONT','One-time purchases')],'Do not count one-time setup as a repeating monthly bill.')
 if mode=='deposit':
  out=base(s);out += [rect('deposit-panel',105,325,1710,570,SAND),animate(pic('deposit-envelope','solo4-deposit',180,360,480,420,0,'none'),'x',[(0,180),(end,530)]),text('deposit-message','CASH TIED UP',1100,425,660,64,RED),text('deposit-detail','A refundable deposit can still limit the cash available now.',1100,650,660,35)]
  footer(out,'Refundable does not mean immediately available · Not automatically a permanent expense');return out
 if mode=='income-risk':
  out=cards(s,[item('pay-envelope','ONE PAYCHECK'),item('bills','THE FULL HOUSEHOLD BILL')],'A loss of income does not automatically reduce the rent or utility commitments.')
  out.append(animate(pic('income-envelope','solo4-pay-envelope',200,285,130,45,0,'none'),'x',[(0,200),(end,1550)]));return out
 if mode=='two-income-note':return cards(s,[item('pay-envelope','POSSIBLE SECOND INCOME'),item('bills','SHARED RISKS REMAIN')],'Not guaranteed protection: two earners can both lose work, and two people have more expenses.')
 if mode=='two-months':
  out=base(s);out += [text('two-month-equation','2 MONTHS × $1,860',140,310,1640,56),number(text('two-month-total','$3,720',140,420,1640,140,RED),[(0,0),(end*.45,1860),(end*.85,3720)],easing='step')]
  for i in range(2):
   x=490+i*540;t=end*(.45 if i==0 else .85);out += [pic(f'calendar-{i+1}','solo4-calendar',x,650,400,190,t,'none'),text(f'month-number-{i+1}',f'MONTH {i+1}',x,865,400,32,RED,t)]
  footer(out,EXAMPLE+' · Rent + internet only; not a complete emergency-fund target');return out
 if mode=='excluded-costs':return cards(s,[item('groceries','FOOD'),item('bills','UTILITIES'),item('house-keys','TRANSPORT'),item('reserve-jar','HEALTHCARE')],'The $3,720 example above excludes these and other obligations; it is not a full fund target.')
 if mode=='privacy-reveal':return cards(s,[item('armchair','REST',reveal='sleeping properly'),item('house-keys','SAFETY',reveal='Recovering from a difficult relationship.'),item('notebook','QUIET',reveal='Having a quiet place to work.')],'Privacy and safety have value; no universal dollar value is assigned.')
 if mode=='privacy-tradeoff':return cards(s,[item('armchair','WHAT YOU GET'),item('calculator','WHAT YOU GIVE UP')],'Estimate your own difference and decide whether the tradeoff fits your life.')
 if mode=='budget-reveal':return cards(s,[item('apartment','RENT + FEES'),item('bills','UTILITIES + INTERNET'),item('notebook','INSURANCE'),item('house-keys','TRANSPORTATION')],'Include all recurring costs tied to the location before signing a lease.')
 if mode=='transport-note':return prop(s,'A LOWER RENT CAN COST MORE OVERALL.','Include transportation, safety and commute before comparing homes.')
 if mode=='essentials':return cards(s,[item('apartment','ESSENTIAL BILLS'),item('groceries','NECESSARY SPENDING'),item('notebook','OTHER OBLIGATIONS')],'Bare-bones monthly budget: what still needs paying if income stops.')
 if mode=='buffer':return prop(s,'START WITH YOUR OWN ESSENTIALS.','Even a small reserve can help. Building it takes time.','CFPB emergency-fund guidance · The right amount depends on your situation.')
 if mode=='housing-options':return cards(s,[item('apartment','SMALLER HOME'),item('house-keys','OTHER NEIGHBORHOOD'),item('router','LOWER-COST PLAN')],'Compare safety, commute, availability and moving costs; savings are not guaranteed.')
 if mode=='closing-plan':return cards(s,[item('bills','RECURRING BILLS'),item('moving-box','MOVE-IN COSTS'),item('reserve-jar','A BUFFER')],'The home stays quiet; the plan includes the months that do not go smoothly.')
 raise ValueError('Unknown layout: '+mode)
clips=[]
for s in shots:
 assert .45<=s['duration']<=120,(s['id'],s['duration'])
 ll=layers(s)
 for l in ll:assert l['enter']<s['duration'],(s['id'],l['id'],l['enter'],s['duration'])
 clips.append(dict(id=s['id'],title=f'{s["section"]:02} · {s["headline"].replace(chr(10)," ")}',duration=s['duration'],background=BG,fade=.06 if clips else 0,layers=ll))
# Original spelling with recognition timing; numerical tokens can be interpolated.
caps=[];group=[]
def flush():
 if not group:return
 first,last=group[0],group[-1];start=times[first];wordend=mapping[last]['end'] if last in mapping else times[last]+.25
 end=min(total,max(start+.18,wordend+.18),times[last+1]-.025 if last+1<len(tokens) else total)
 if end>start:caps.append(dict(start=round(start,3),end=round(end,3),text=' '.join(tokens[j].group() for j in group)))
 group.clear()
for i,t in enumerate(tokens):
 group.append(i)
 if len(group)>=12 or (len(group)>=3 and re.search(r'[.!?][”\"]?$',t.group())):flush()
flush()
peaks=[round(min(1,float(np.sqrt(np.mean(c*c)))/7000),3) for c in np.array_split(samples,1400)]
used={l['asset'] for c in clips for l in c['layers'] if l['type']=='image'}
project=dict(kind='credit-studio-video',version=1,revision='living-alone-review-v01',name='Living Alone — Bản duyệt đầy đủ v01',width=1920,height=1080,fps=30,audio=dict(src=P+'review/voiceover.mp3',offset=0,volume=1),assets={k:v for k,v in assets.items() if k in used},clips=clips,captions=caps,showCaptions=False,waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
shotdata=[dict(**s,end=round(s['start']+s['duration'],6)) for s in shots];(OUT/'shot-plan.json').write_text(json.dumps(shotdata,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
motion=[dict(clipId=c['id'],layout=s['layout'],start=s['start'],layers=[l['id'] for l in c['layers'] if l.get('animation')]) for c,s in zip(clips,shots) if any(l.get('animation') for l in c['layers'])]
(OUT/'motion-plan.json').write_text(json.dumps(motion,indent=2)+'\n')
sourceinfo=dict(receivedVia='User-provided chat attachment',sourceBytes=WAV.stat().st_size,source=P+'audio/'+WAV.name,sha256=hashlib.sha256(WAV.read_bytes()).hexdigest(),duration=total,sampleRate=sample_rate,channels=channels,alignmentModel='faster-whisper base.en int8 CPU',matchedScriptTokens=len(mapping),scriptTokens=len(tokens),normalization='Derived MP3: two-pass FFmpeg loudnorm, target -16 LUFS / -1.5 dBTP; original WAV unchanged.',music=False,sourceSpeedChanged=False,narrationText='../narration.txt',captions='Default off; original spelling with automatic word timing, including interpolated numeric tokens.')
(OUT/'source.json').write_text(json.dumps(sourceinfo,indent=2)+'\n')
lines=['# Video 004 — Bản duyệt đầy đủ v01','',f'**{total:.3f} giây · {len(clips)} cảnh · 1920×1080 / 30 fps.** Chờ người dùng duyệt, chưa phải bản cuối.','', 'Dự án chỉnh được: `project.json`; MP4: `../exports/full-review-v01.mp4`; audio dẫn xuất: `voiceover.mp3`. WAV gốc và bảng duyệt hình 96 giây giữ nguyên.','',f'{sum(len(m["layers"]) for m in motion)} lớp chuyển động nội dung trong {len(motion)} cảnh, cùng thẻ hiện theo lời kể. Times New Roman; collage ảnh và đạo cụ. Chưa nhạc nền hoặc rig khớp.','', '| Bắt đầu | Kết thúc | Cảnh |','|---|---|---|']
for s in shotdata:lines.append(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["headline"].replace(chr(10)," ")} |')
lines += ['','Mốc từ tự động base.en; có nội suy token số và sai số mức từ. Phụ đề mặc định tắt trong MP4, bật được trong Studio. Không cắt lời hoặc đổi tốc độ audio.','',f'Khớp trực tiếp {len(mapping)}/{len(tokens)} token narration. Kết quả kiểm tra hình/audio/tệp xuất ở `validation.json`.','', 'Tiếp theo: người dùng duyệt và gửi góp ý kèm timecode; nếu đã chỉnh riêng trong Studio, nhận `.credit.json`/JSON trước. Xuất lần sau dùng v02, giữ v01.','', 'Tạo lại: `python3 tools/build-living-alone-video.py` mặc định chặn ghi đè. Chỉ `--force` sau khi sao lưu sửa tay. Công cụ không sửa WAV, bộ hình hoặc MP4.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
print(f'Built {len(clips)} clips, {total:.3f}s, {len(caps)} captions, {len(used)} assets; matched {len(mapping)}/{len(tokens)} tokens; {sum(len(m["layers"]) for m in motion)} animated layers in {len(motion)} clips.')
print('Longest shots:',[(s['id'],s['duration'],s['layout']) for s in sorted(shots,key=lambda s:s['duration'],reverse=True)[:6]])
