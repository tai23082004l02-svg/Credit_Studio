#!/usr/bin/env python3
"""Add editable deterministic financial motion to preserved salary review v02."""
import json,argparse
from pathlib import Path
root=Path(__file__).resolve().parents[1];folder=root/'videos/001-100k-salary';out=folder/'review-v03'
parser=argparse.ArgumentParser();parser.add_argument('--force',action='store_true');args=parser.parse_args()
if (out/'project.json').exists() and not args.force:raise SystemExit('Back up edits before using --force.')
p=json.loads((folder/'review-v02/project.json').read_text());p['revision']='salary-motion-v03';p['name']='Why You Feel Broke — Bản duyệt chuyển động v03'
BG='#faf6ec';GREEN='#286a52';INK='#27332f';RED='#bd6555';SAND='#eee7d8'
def base(id,type,x,y,w,h,**kw):return dict(id=id,type=type,x=x,y=y,w=w,h=h,enter=0,effect='none',opacity=1,drift=0,**kw)
def txt(id,s,x,y,w,size=44,fill=INK):return base(id,'text',x,y,w,size*1.3,text=s,size=size,fill=fill,align='center')
def rect(id,x,y,w,h,fill=GREEN):return base(id,'rect',x,y,w,h,fill=fill,radius=0)
def img(id,asset,x,y,w,h):return base(id,'image',x,y,w,h,asset=asset)
def motion(l,prop,keys,**kw):l['animation']=dict(property=prop,easing='smooth',keys=[dict(time=t,value=v) for t,v in keys],**kw);return l
def counter(l,keys,format='currency',prefix='',suffix=''):return motion(l,'number',keys,format=format,prefix=prefix,suffix=suffix)
def headers(c):return [l for l in c['layers'] if l['id'] in ['chapter','headline']]
changed=[]
# A consistent account meter across the six cost shots; exact balances, no fabricated data.
for index,start,end,label in [(22,6000,3700,'RENT: $2,300'),(23,3700,2850,'TRANSPORTATION: $850'),(25,2850,2200,'FOOD: $650'),(26,2200,1800,'UTILITIES + INTERNET + PHONE: $400'),(27,1800,1400,'DEBT PAYMENTS: $400'),(28,1400,1100,'OTHER COSTS: $300')]:
 c=p['clips'][index];finish=min(2.25,c['duration']-.4);keys=[(.15,start),(finish,end)];bar=rect('remaining-meter',600,550,1200*end/6000,78);motion(bar,'width',[(t,v/6000*1200) for t,v in keys]);value=counter(txt('remaining-value',f'${end:,}',600,370,1200,108,GREEN),keys)
 c['layers']=headers(c)+[img('alex','alex-think',100,325,420,600),txt('remaining-label','MONTHLY PAY LEFT',600,300,1200,34),value,rect('meter-track',600,550,1200,78,SAND),bar,rect('cost-panel',600,690,1200,165,'#e2ecdd'),txt('cost-label',label,625,740,1150,42,RED),txt('note','Illustrative monthly budget · Running balance after each commitment.',100,968,1720,28,GREEN)];changed.append(index)
# Animate the irregular-expense subtraction in time with its spoken conclusion.
c=p['clips'][37];keys=[(0,1100),(5.6,1100),(8.3,500)];bar=motion(rect('remaining-meter',600,550,100,78),'width',[(t,v/6000*1200) for t,v in keys]);c['layers']=headers(c)+[img('alex','alex-think',100,325,420,600),txt('remaining-label','ROOM AFTER AN IRREGULAR-EXPENSE PLAN',580,300,1240,32),counter(txt('remaining-value','$500',600,370,1200,108,GREEN),keys),rect('meter-track',600,550,1200,78,SAND),bar,txt('cost-label','$1,100 − $600 = $500',600,735,1200,64,RED),txt('note','Illustrative monthly average · The meter uses the same $6,000 scale.',100,968,1720,28,GREEN)];changed.append(37)
# Follow actual moving money between separated account/cost/reserve destinations.
c=p['clips'][8];layers=headers(c)+[img('alex','alex-present',80,320,360,610),rect('flow-line',570,400,1110,6,SAND)]
for j,(label,asset) in enumerate([('TAKE-HOME PAY','money'),('COMMITMENTS','receipt'),('ROOM TO BREATHE','mpt-savings-jar')]):
 if asset not in p['assets']:asset='money'
 x=510+j*435;layers += [rect('flow-card-'+str(j),x,525,400,350,'#e2ecdd'),img('flow-icon-'+str(j),asset,x+90,555,220,170),txt('flow-label-'+str(j),label,x+10,775,380,30)]
for j in range(2):
 a=img('moving-money-'+str(j),'money',570,350,100,90);motion(a,'x',[(0,570+j*130),(c['duration']-.45,1550+j*130)]);layers.append(a)
c['layers']=layers+[txt('note','Follow what arrives, what is committed and what remains.',100,968,1720,28,GREEN)];changed.append(8)
# Date rollover makes the next-month obligation visible. Dates are illustrative, never advice.
c=p['clips'][42];D=c['duration'];daykeys=[(0,28),(.8,28),(1.3,29),(2.1,29),(2.6,30),(3.4,30),(3.9,1),(D,1)];monthkeys=[(0,1),(3.4,1),(3.9,2),(D,2)]
c['layers']=headers(c)+[rect('calendar-paper',140,330,700,575,'#e2ecdd'),rect('calendar-top',140,330,700,110,GREEN),counter(txt('calendar-month','MONTH 2',170,355,640,46,'#ffffff'),monthkeys,format='integer',prefix='MONTH '),counter(txt('calendar-day','1',170,500,640,170),daykeys,format='integer'),txt('calendar-label','ILLUSTRATIVE DATES',170,815,640,28,GREEN),img('bill','receipt',1150,350,350,350),txt('bill-label','NEXT MONTH.\nSAME PURCHASE.',970,750,820,52,RED)];changed.append(42)
# Final composition fills to its exact 4900 / 600 / 500 proportions.
for i in [30,38]:
 c=p['clips'][i]
 for j,l in enumerate([l for l in c['layers'] if l['id'].startswith('bar-') and l['type']=='rect']):motion(l,'width',[(.1+j*.4,0),(min(c['duration']-.4,1.4+j*.4),l['w'])])
 changed.append(i)
for l in p['clips'][42]['layers']:
 if l.get('animation',{}).get('property')=='number':l['animation']['easing']='step'
# Keep only assets actually referenced, including the new presentational character/props.
used={l['asset'] for c in p['clips'] for l in c['layers'] if l['type']=='image'};p['assets']={k:v for k,v in p['assets'].items() if k in used}
out.mkdir(exist_ok=True);(out/'project.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
report=dict(basedOn='review-v02/project.json',revision=p['revision'],durationSeconds=sum(c['duration'] for c in p['clips']),clips=len(p['clips']),changedClips=[dict(index=i+1,title=p['clips'][i]['title']) for i in sorted(changed)],animatedLayers=sum('animation'in l for c in p['clips'] for l in c['layers']),audioUnchanged=p['audio'],notes=['Same narration, timing and assets as v02','No music or character joint rigs','Calendar dates are illustrative; day rollover uses numeric keyframes','Previous reviews and exports are preserved'])
(out/'motion-plan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['clips','durationSeconds','animatedLayers']},indent=2))
