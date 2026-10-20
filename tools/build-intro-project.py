#!/usr/bin/env python3
"""Build the layered intro project from bundled art. Does not modify images or source audio."""
import json, math, wave
from array import array
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VIDEO=ROOT/'videos/001-100k-salary'
PREFIX='videos/001-100k-salary/'
assets={}
for i,pose in enumerate(['celebrate','worried','think','present']):
    assets['alex-'+pose]={'src':PREFIX+'images/sheets/alex-poses.png','crop':[i*511.5,0,511.5,769],'label':'Alex — '+pose}
for key,index,label in [('paycheck',0,'Phong bì lương'),('money',1,'Tiền mặt'),('coins',2,'Tiền xu'),('wallet',3,'Ví tiền'),('receipt',4,'Hóa đơn'),('shield',5,'Bảo hiểm'),('piggy',6,'Hũ tiết kiệm'),('card',7,'Thẻ tín dụng'),('calendar',8,'Lịch ngày lương'),('savings',9,'Quỹ dự phòng'),('paid',10,'Đã thanh toán'),('arrow',11,'Mũi tên')]:
    assets[key]={'src':PREFIX+'images/sheets/finance-props.png','crop':[(index%4)*362,(index//4)*362,362,362],'label':label}
for key,index,label in [('car',1,'Xe'),('food',2,'Thực phẩm'),('phone',3,'Điện thoại và điện'),('gift',5,'Quà'),('wrench',10,'Sửa chữa')]:
    assets[key]={'src':PREFIX+'images/sheets/life-props.png','crop':[(index%4)*384,(index//4)*1024/3,384,1024/3],'label':label}

def image(name,asset,x,y,w,h,enter=0,effect='slide',drift=0):
    return dict(id=name,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=enter,effect=effect,opacity=1,drift=drift)
def text(name,content,x,y,w,size=78,fill='#27332f',enter=0,effect='fade',align='left'):
    return dict(id=name,type='text',text=content,x=x,y=y,w=w,h=round(size*1.18*(content.count('\n')+1)+20),size=size,fill=fill,align=align,enter=enter,effect=effect,opacity=1,drift=0)
def rect(name,x,y,w,h,fill,enter=0):
    return dict(id=name,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=24,enter=enter,effect='fade',opacity=1,drift=0)
def scene(id,title,seconds,layers):
    return dict(id=id,title=title,duration=seconds,background='#faf6ec',fade=.14,layers=layers)
# Explicit source rectangles exclude neighboring sprites; original PNGs remain unchanged.
for key,crop in {
 'alex-celebrate':[15,0,525,769], 'alex-worried':[530,0,511.5,769],
 'alex-think':[1015,0,496,769], 'alex-present':[1510,0,536,769],
 'paycheck':[24,30,360,340], 'money':[400,70,340,300],
 'coins':[745,45,350,320], 'wallet':[1110,70,320,300],
 'receipt':[25,370,355,335], 'shield':[400,370,310,325],
 'piggy':[730,380,365,320], 'card':[1110,400,325,300],
 'calendar':[20,720,370,325], 'savings':[400,690,315,355],
 'paid':[740,700,355,340], 'arrow':[1105,690,325,345],
 'car':[395,100,420,240], 'food':[820,30,315,325],
 'phone':[1190,30,335,325], 'gift':[430,350,320,320], 'wrench':[800,685,310,310],
}.items():assets[key]['crop']=crop
assets['phone']={'src':PREFIX+'intro/props.png','crop':[80,20,520,690],'label':'Điện thoại — tài khoản ngân hàng'}
assets['food']={'src':PREFIX+'intro/props.png','crop':[660,45,770,650],'label':'Đồ ăn mang về'}
assets['tire']={'src':PREFIX+'intro/props.png','crop':[1510,90,610,570],'label':'Lốp xe xẹp'}
clips=[
 scene('01-success','Công việc và lần tăng lương',4.25,[
  image('alex','alex-celebrate',90,205,500,752,0,'fade',3),
  text('hook','YOU FINALLY\nDID IT.',745,205,1060,112,enter=.05,effect='slide'),
  image('offer','paycheck',760,565,310,310,1.65,'pop'),
  text('job','THE JOB.',1120,590,600,60,enter=1.78),
  text('raise','THE RAISE.',1120,705,600,60,fill='#276b54',enter=3.02),
 ]),
 scene('02-salary','Lương sáu con số',5.15,[
  image('alex','alex-present',90,230,515,774,0,'slide',3),
  text('label','SIX FIGURES.',740,145,1000,71,enter=.12),
  rect('salary-card',700,300,1090,370,'#e2ecda',.35),
  text('salary','$100,000',755,330,1000,165,fill='#276b54',enter=2.6,effect='pop'),
  text('year','A YEAR',765,550,900,62,enter=3.55),
  image('coins','coins',1350,710,330,260,.8,'pop',4),
 ]),
 scene('03-relief','Tiền sẽ hết căng thẳng?',4.25,[
  image('alex','alex-present',95,235,510,767,0,'slide',2),
  text('promise','MONEY STRESS?',745,225,1080,94,enter=.1),
  text('gone','FINALLY OVER.',745,390,1080,99,fill='#276b54',enter=1.2,effect='slide'),
  image('piggy','piggy',825,630,290,290,.7,'pop',3),
  image('paid','paid',1260,630,290,290,1.6,'pop',2),
 ]),
 scene('04-bank-account','Kiểm tra tài khoản trước khi ăn',4.8,[
  image('alex','alex-worried',65,255,510,767,0,'fade',2),
  text('bank','CHECKING YOUR\nBANK ACCOUNT…',685,155,1120,94,enter=.1,effect='slide'),
  image('phone','phone',770,485,280,380,.7,'pop'),
  image('food','food',1230,510,430,360,2.9,'slide'),
  text('takeout','BEFORE TAKEOUT.',685,905,1120,59,fill='#b65f49',enter=3.6),
 ]),
 scene('05-tires','Một bộ lốp xe và phép tính trong đầu',5.4,[
  image('alex','alex-think',65,245,510,767,0,'fade',3),
  text('tires','NEW TIRES?',730,155,1100,100,fill='#b65f49',enter=.2,effect='pop'),
  image('car','car',690,480,400,270,.25,'slide'),
  image('tire','tire',1210,405,420,450,.9,'pop'),
  text('math','MENTAL GYMNASTICS.',710,910,1100,58,enter=2.4,effect='slide'),
 ]),
 scene('06-payday','Chờ ngày lương giải cứu',4.45,[
  image('alex','alex-worried',80,245,505,759,0,'slide',3),
  text('payday','PAYDAY.',740,155,1060,120,fill='#b65f49',enter=.15,effect='pop'),
  image('calendar','calendar',780,385,460,460,.4,'slide',2),
  image('paycheck','paycheck',1400,480,320,320,1.7,'pop'),
  text('rescue','A RESCUE MISSION.',740,910,1100,64,enter=2.55),
 ]),
 scene('07-question','Sáu con số mà vẫn thiếu tiền?',6.55,[
  image('alex','alex-think',75,245,510,767,0,'fade',3),
  text('question','SO, WHAT\nHAPPENED?',725,145,1070,109,enter=.2,effect='slide'),
  image('wallet','wallet',760,585,330,330,1.25,'pop'),
  text('contrast','SIX FIGURES.\nSTILL BROKE?',1180,615,650,68,fill='#b65f49',enter=2.2),
 ]),
 scene('08-follow-money','Đi theo dòng tiền',5.65,[
  image('alex','alex-present',65,245,510,767,0,'slide',3),
  text('follow','LET’S FOLLOW\nTHE MONEY.',715,155,1110,107,fill='#276b54',enter=.2,effect='slide'),
  image('paycheck','paycheck',700,575,300,300,.2,'pop'),
  image('arrow','arrow',1080,620,220,220,1.4,'fade'),
  image('receipt','receipt',1400,565,300,300,2.3,'pop'),
  text('before','BEFORE YOU BUY A SINGLE THING.',715,935,1110,42,enter=2.7),
 ]),
]
clips[0]['fade']=0
clips[0]['layers'][0]['effect']='none'
clips[0]['layers'][1]['effect']='none'
clips[0]['layers'][1]['enter']=0
assert math.isclose(sum(c['duration'] for c in clips),40.5)
captions=[
 (0,1.6,'You finally did it.'),(1.78,2.75,'You got the job.'),(3.02,4.1,'You got the raise.'),
 (4.46,6.55,'Your salary now has six figures.'),(6.92,9.2,'One hundred thousand dollars a year.'),
 (9.56,13.55,"That sounds like the moment money is supposed to stop being stressful."),
 (13.96,18.35,"But somehow, you’re still checking your bank account before ordering takeout."),
 (18.68,23.55,"Your car needs new tires, and suddenly you’re doing mental gymnastics."),
 (24.1,24.85,'And payday?'),(25.14,28.05,'Payday still feels like a rescue mission.'),
 (28.5,30.1,'So what happened?'),(30.52,34.7,'How can someone make a hundred thousand dollars a year and still feel broke?'),
 (35.18,36.65,"Let’s follow the money."),(37.08,40.25,'Because the answer starts before you buy a single thing.'),
]
# Read amplitudes without changing the original user WAV.
with wave.open(str(next((VIDEO/'audio').glob('*.wav'))),'rb') as wav:
    assert wav.getsampwidth()==2 and wav.getnchannels()==1
    rate=wav.getframerate();samples=array('h',wav.readframes(round(40.5*rate)))
    peaks=[];block=max(1,len(samples)//400)
    for i in range(400):
        chunk=samples[i*block:(i+1)*block]
        peaks.append(round(min(1,math.sqrt(sum(v*v for v in chunk)/max(1,len(chunk)))/7000),3))
project=dict(kind='credit-studio-video',version=1,revision='intro-v01',name='Video 001 — Bản duyệt mở đầu 40,5 giây',width=1920,height=1080,fps=30,audio=dict(src=PREFIX+'intro/voiceover.mp3',offset=0,volume=1),assets=assets,clips=clips,captions=[dict(start=s,end=e,text=t) for s,e,t in captions],showCaptions=False,waveform=peaks,waveformDuration=40.5)
(VIDEO/'intro/project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')

def timestamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for s,e,t in captions:vtt += [f'{timestamp(s)} --> {timestamp(e)}',t,'']
(VIDEO/'intro/captions.vtt').write_text('\n'.join(vtt),encoding='utf-8')
print('Built 8 layered shots, 40.5 seconds, 14 subtitle cues and waveform.')
