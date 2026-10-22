#!/usr/bin/env python3
"""Build the narrated review from preserved assets and word alignment, without changing WAV/artwork."""
import json,re,math,wave,difflib,hashlib,argparse
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
V=ROOT/'videos/003-car-payment-trap';P='videos/003-car-payment-trap/';OUT=V/'review'
parser=argparse.ArgumentParser();parser.add_argument('--force',action='store_true');args=parser.parse_args()
if (OUT/'project.json').exists() and not args.force:raise SystemExit('Review exists. Back up edits first; --force rebuilds derived review files only.')
script=(OUT/'narration.md').read_text();body='\n\n'.join(part.split('\n',1)[1] for part in script.split('## ')[1:])
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
 candidates=[i for i in range(len(source)-len(query)+1) if source[i:i+len(query)]==query]
 candidates=[i for i in candidates if times[i]>=after-.001]
 assert candidates,(phrase,after)
 return round(times[candidates[0]],3)
with wave.open(str(V/'audio/tts_20261022_115123_7124d9.wav')) as wav:
 total=wav.getnframes()/wav.getframerate();samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').astype(float)
INK='#27332f';GREEN='#286a52';CORAL='#bd6555';BG='#faf6ec';MINT='#e2ecdd';SAND='#eee7d8'
catalog=json.loads((ROOT/'library/props/catalog.json').read_text())['items']
assets={p['id']:{'src':p['src'],'label':p['name'],**({'crop':p['crop']} if 'crop'in p else {})} for p in catalog}
oldlayout=json.loads((ROOT/'videos/002-monthly-payment-trap/asset-layout.json').read_text())
for sheet in oldlayout['sheets']:
 for item in sheet['items']:assets[item['id']]={'src':'videos/002-monthly-payment-trap/'+item['image'],'label':item['name']}
layout=json.loads((V/'asset-layout.json').read_text())
for sheet in layout['sheets']:
 for item in sheet['items']:assets[item['id']]={'src':P+item['image'],'label':item['name']}
for j in layout['jobs']:assets['art-'+j['id']]={'src':P+j['image'],'label':j['title']}
def A(slug):return slug
chapters=['THE PAYMENT SCREEN','THE WHOLE COST','THE CALENDAR','THE TRADE-IN GAP','TWO DIFFERENT MEASURES','THE TRADEOFF','BEFORE YOU SHOP','A CAR THAT FITS']
shots=[]
def add(section,anchor,title,mode,headline,**kw):shots.append(dict(section=section,anchor=anchor,title=title,mode=mode,headline=headline,start=cue(anchor,shots[-1]['start']+.01 if shots else 0),**kw))
def hero(s,a,t,h,message,pose='car3-alex-explain-car',prop='car3-red-sedan',detail=''):add(s,a,t,'hero',h,message=message,pose=A(pose),prop=A(prop),detail=detail)
def art(s,a,t,h,key,detail=''):add(s,a,t,'art',h,art='art-'+key,detail=detail)
def card(icon,label,value='',detail='',reveal=None):return dict(icon=A(icon),label=label,value=value,detail=detail,reveal=reveal)
def cards(s,a,t,h,items,note=''):add(s,a,t,'cards',h,items=items,note=note)
def mathshot(s,a,t,h,equation,detail,icon='mpt-cash-stack'):add(s,a,t,'math',h,equation=equation,detail=detail,icon=A(icon))

# Narrative cuts keyed to the actual narration, not fixed slideshow timing.
art(1,'The salesperson asks','Câu hỏi ở đại lý','THE PAYMENT FITS.\nDOES THE CAR?','01a')
hero(1,'What monthly payment','Câu hỏi về khoản trả tháng','“WHAT PAYMENT\nARE YOU COMFORTABLE WITH?”','THE MONTHLY NUMBER',pose='car3-alex-keys',prop='car3-car-keys')
hero(1,'You give them a number','Đưa ra con số tháng','YOU GIVE THEM A NUMBER.','THE TERMS CAN MOVE.',pose='car3-alex-compare-offers',prop='car3-offer-sheet')
hero(1,'Good news.','Đề nghị được duyệt','GOOD NEWS.\nTHEY MADE IT WORK.','DOES THE WHOLE COST FIT?',prop='car3-loan-folder')
art(1,'You drive home','Nhận chiếc xe mới','A NICER CAR.\nA PAYMENT THAT FITS.','01a')
cards(1,'At least,','Vài tháng sau khoản trả vẫn được','THE PAYMENT IS MANAGEABLE.',[card('car3-red-sedan','THE CAR PAYMENT'),card('mpt-savings-jar','THE REST OF THE BUDGET')])
hero(1,'But saving money','Tiết kiệm không theo kịp','BUT SAVING MONEY ISN’T.','VERY LITTLE ROOM LEFT.',pose='car3-alex-phone-quote',prop='mpt-empty-wallet')
cards(1,'The emergency fund','Quỹ dự phòng thẻ tín dụng chi bất ngờ','THE OTHER PRESSURES.',[card('mpt-savings-jar','EMERGENCY FUND',detail='Barely moving',reveal='The emergency fund'),card('mpt-bank-card','CREDIT CARD',detail='Balance hanging around',reveal='The credit card balance'),card('mpt-wrench','UNEXPECTED COSTS',detail='What can wait?',reveal='And every unexpected')])
art(1,'The car didn’t suddenly','Những phần chưa thấy trên màn hình','THE COSTS\nWEREN’T ALL ON THE SCREEN.','02a')
add(1,'Let’s follow the money.','Bắt đầu theo dòng tiền','flow','LET’S FOLLOW THE MONEY.')
hero(2,'Meet Alex.','Gặp Alex','MEET ALEX.','A MONTHLY TRANSPORTATION BUDGET',pose='car3-alex-keys',prop='car3-red-sedan')
cards(2,'Alex brings home','Thu nhập và số tiền vay','THE STARTING NUMBERS.',[card('mpt-pay-envelope','TAKE-HOME PAY','$6,000 / month'),card('car3-loan-folder','AMOUNT FINANCED','$35,000')],note='Illustrative example · Income and vehicle financing are separate figures.')
add(2,'At eight percent','Lãi suất kỳ hạn và khoản trả','loan-offer','THE LOAN PAYMENT.')
cards(2,'That’s a simplified','Giả định khoản vay minh họa','A SIMPLIFIED EXAMPLE.',[card('car3-loan-folder','FIXED RATE','8% APR'),card('mpt-calendar','LOAN LENGTH','72 months'),card('car3-offer-sheet','EXTRA FINANCED FEES','Not included')],note='Real rates, fees and qualification vary.')
hero(2,'Six hundred and fourteen dollars doesn’t','Khoản trả có vẻ làm được','NOT SMALL.\nBUT IT SOUNDS POSSIBLE.','ABOUT $614 / MONTH',prop='car3-red-sedan')
art(2,'Then the other costs arrive.','Những chi phí khác đến','THE PAYMENT\nIS ONLY THE START.','02a')
add(2,'In Alex’s example, insurance','Thêm bảo hiểm','cost-meter','INSURANCE JOINS THE PAYMENT.',before=614,after=794,cost='INSURANCE: $180 / MONTH',prop='car3-auto-insurance')
add(2,'Gas adds','Thêm nhiên liệu','cost-meter','GAS JOINS THE BUDGET.',before=794,after=954,cost='GAS: $160 / MONTH',prop='car3-fuel-pump')
add(2,'And Alex sets aside','Thêm bảo dưỡng đăng ký','cost-meter','PLAN FOR UPKEEP, TOO.',before=954,after=1044,cost='MAINTENANCE + REPAIRS + REGISTRATION: $90',prop='mpt-wrench')
hero(2,'Those are illustrative','Ví dụ không phải mức trung bình','ILLUSTRATIVE AMOUNTS.','YOUR COSTS CAN BE DIFFERENT.',prop='car3-offer-sheet')
add(2,'Now the car needs','Tổng chi phí mỗi tháng','cost-total','ABOUT $1,044 / MONTH.')
mathshot(2,'Roughly twelve thousand','Chi phí theo năm','ROUGHLY $12,500 / YEAR.','$1,044 × 12 = $12,528','Rounded to about $12,500 in the narration.','car3-red-sedan')
cards(2,'And that doesn’t include','Chưa bao gồm đỗ xe và phí đường','PLUS PARKING OR TOLLS.',[card('car3-red-sedan','PARKING'),card('car3-offer-sheet','TOLLS')])
cards(2,'Alex bought the car','Hai con số khác nhau','ONE PURCHASE.\nTWO DIFFERENT COMMITMENTS.',[card('car3-red-sedan','PAYMENT IN MIND','About $600'),card('car3-auto-insurance','TRANSPORTATION BUDGET','About $1,000')],note='Actual illustrative total above: about $1,044 per month.')
hero(2,'Those are two different decisions.','Khoản trả khác toàn bộ quyết định','TWO DIFFERENT DECISIONS.','LOOK BEYOND THE PAYMENT.',prop='mpt-comparison-cards')
hero(3,'So why does','Vì sao hỏi khoản tháng đầu tiên','WHY START\nWITH THE MONTHLY PAYMENT?','IT IS AN EASIER NUMBER.',prop='car3-offer-sheet')
hero(3,'Because the payment can change','Khoản tháng đổi giá xe không đổi','THE PAYMENT CAN CHANGE.','THE CAR MAY NOT GET CHEAPER.',prop='car3-red-sedan')
art(3,'One way is','Kéo dài thời hạn vay','SMALLER PAYMENTS.\nMORE MONTHS.','03a')
cards(3,'For the same amount','Giữ số tiền vay và lãi suất','SAME AMOUNT. SAME RATE.',[card('mpt-calendar','LONGER TERM','Lower monthly bill'),card('car3-loan-folder','MORE TIME','Interest lasts longer')],note='For otherwise comparable fixed-rate financing.')
add(3,'But interest keeps','Lãi tích lũy theo thời gian','interest','INTEREST HAS MORE TIME.')
mathshot(3,'In Alex’s example, seventy-two','Bảy mươi hai khoản trả','72 PAYMENTS.\nABOUT $44,200 REPAID.','≈ $614 × 72 ≈ $44,200','Rounded display · Fixed-rate example · No extra financed fees.','car3-loan-folder')
cards(3,'That’s about nine thousand','Tiền gốc và tiền lãi','PRINCIPAL + INTEREST.',[card('car3-loan-folder','ORIGINAL PRINCIPAL','$35,000'),card('mpt-cash-stack','TOTAL INTEREST','About $9,200')],note='Totals use the unrounded monthly loan calculation, then round for display.')
hero(3,'The payment made','Cảm giác mua được','THE PURCHASE FELT REACHABLE.','THE CALENDAR TELLS MORE.',prop='car3-car-keys')
add(3,'The calendar helped hide','Lịch dư nợ qua kỳ hạn','amortization','72 MONTHS OF COMMITMENT.')
cards(3,'A different job.','Những thay đổi trong sáu năm','LIFE CAN CHANGE.',[card('mpt-pay-envelope','A DIFFERENT JOB',reveal='A different job.'),card('home','A MOVE',reveal='A move.'),card('gift','A NEW BABY',reveal='A new baby.'),card('car3-offer-sheet','A RENT INCREASE',reveal='A rent increase.')])
add(3,'The payment stays','Khoản trả vẫn trên lịch','calendar','THE PAYMENT STAYS ON THE CALENDAR.')
cards(3,'And depending on','Sửa xe khi vẫn trả nợ','REPAIRS MAY ARRIVE\nBEFORE THE LOAN ENDS.',[card('car3-loan-folder','LOAN PAYMENT'),card('mpt-wrench','REPAIR COSTS')])
art(4,'A couple of years pass.','Chuyển sang ví dụ đổi xe riêng','A SEPARATE\nTRADE-IN EXAMPLE.','04a',detail='The following trade-in figures are hypothetical, not year-two balances for the earlier loan.')
hero(4,'Alex starts looking','Xem chiếc xe khác','LOOKING AT ANOTHER CAR.','ANOTHER FINANCING DECISION',prop='car3-teal-sedan')
cards(4,'Maybe the family','Lý do đổi xe','THE REASONS CAN MAKE SENSE.',[card('home','MORE SPACE',reveal='Maybe the family'),card('mpt-wrench','RELIABILITY',reveal='Maybe the current'),card('car3-teal-sedan','A NEWER LOOK',reveal='Maybe the newer')])
hero(4,'But there’s a problem.','Vấn đề trước khi đổi xe','BUT THERE’S A PROBLEM.','WHAT IS STILL OWED?',pose='car3-alex-phone-quote',prop='car3-loan-folder')
add(4,'Suppose Alex still owes','Số dư vay giả định','trade-owed','STILL OWED: $28,000.')
add(4,'The trade-in offer','Giá thu đổi xe','trade-offer','TRADE-IN OFFER: $23,000.')
add(4,'That leaves a','Khoản thiếu năm nghìn','equity-gap','A $5,000 GAP.')
cards(4,'This is negative equity:','Định nghĩa âm vốn chủ sở hữu','NEGATIVE EQUITY.',[card('car3-loan-folder','OWED','$28,000'),card('car3-red-sedan','VEHICLE VALUE','$23,000'),card('car3-trade-in-envelope','GAP','$5,000')],note='Separate illustrative trade-in scenario, not a balance derived from the earlier loan.')
add(4,'Trading in the car','Khoản nợ không biến mất','debt-transfer','THE GAP DOESN’T DISAPPEAR.')
hero(4,'Alex needs to cover','Phải xử lý khoản thiếu','THE GAP NEEDS TO BE COVERED.','IT DOESN’T VANISH AT TRADE-IN.',prop='car3-trade-in-envelope')
cards(4,'If a lender allows','Điều kiện cộng nợ vào vay mới','IF THE LENDER ALLOWS IT…',[card('car3-teal-sedan','REPLACEMENT','$30,000',reveal='A thirty-thousand-dollar replacement'),card('car3-trade-in-envelope','OLD DEBT GAP','$5,000'),card('car3-loan-folder','NEW FINANCING','$35,000',reveal='Can become thirty-five thousand')],note='Before taxes and fees · Approval is not guaranteed.')
add(4,'Five thousand dollars of','Nợ cũ trong khoản vay mới','rolled-debt','NEW CAR.\nOLD DEBT COMES ALONG.')
hero(4,'A longer term might','Kỳ hạn lại làm khoản trả dễ chịu','A COMFORTABLE PAYMENT?','CHECK THE WHOLE ARRANGEMENT.',prop='mpt-calendar')
add(4,'But now the next car','Xe mới mang hóa đơn cũ','debt-transfer','PART OF THE PREVIOUS CAR’S BILL.')
art(4,'Repeat that cycle,','Vòng chuyển nợ sang xe tiếp theo','THE CAR CHANGES.\nTHE DEBT FINDS A NEW HOME.','04a',detail='Separate hypothetical trade-in example · Financing depends on the lender.')
hero(5,'There’s another number','Một thước đo nữa','ANOTHER NUMBER:\nDEPRECIATION.','THE CAR’S CHANGING VALUE',prop='car3-red-sedan')
art(5,'As a car loses','Giá trị thị trường giảm','VALUE CAN BE HARDER\nTO RECOVER WHEN YOU SELL.','05a')
cards(5,'That matters when','Khi giá trị bán lại quan trọng','TRADE. MOVE. EXIT THE LOAN.',[card('car3-red-sedan','TRADE IN'),card('home','MOVE'),card('car3-loan-folder','GET OUT OF THE LOAN')])
cards(5,'But don’t simply add','Không cộng hai thước đo sai cách','DON’T DOUBLE-COUNT.',[card('mpt-cash-stack','MONTHLY CASH FLOW','Money leaving'),card('car3-teal-sedan','DEPRECIATION','Loss of value')],note='Do not add depreciation to the entire payment and call it monthly cash spending.')
hero(5,'Part of the payment','Một phần khoản trả giảm nợ','PART OF THE PAYMENT\nREDUCES THE DEBT.','PRINCIPAL REPAYMENT',prop='car3-loan-folder')
hero(5,'Depreciation describes','Khấu hao là mất giá xe','DEPRECIATION\nDESCRIBES LOST VALUE.','A DIFFERENT MEASURE',prop='car3-red-sedan')
art(5,'They measure different things.','Hai thước đo khác nhau','CASH FLOW\nAND CAR VALUE.','05a')
cards(5,'For a monthly budget,','Ngân sách tháng theo tiền rời tài khoản','TRACK THE CASH LEAVING.',[card('car3-loan-folder','LOAN PAYMENT'),card('car3-fuel-pump','OPERATING COSTS')])
cards(5,'For the bigger purchase','Xem toàn bộ quyết định mua','THE BIGGER PURCHASE DECISION.',[card('car3-loan-folder','INTEREST'),card('mpt-wrench','OWNERSHIP COSTS'),card('car3-teal-sedan','VALUE WHEN SOLD')])
hero(5,'The uncomfortable part','Xe cũ đi nợ vẫn chưa xong','GETTING OLDER.\nSTILL FINANCIALLY UNFINISHED.','CHECK THE WHOLE COMMITMENT.',prop='car3-red-sedan')
hero(6,'Back in Alex’s budget,','Quay lại ngân sách tháng','ABOUT $1,000 EVERY MONTH.','TRANSPORTATION HAS A JOB.',prop='car3-red-sedan',detail='Illustrative all-in amount above: about $1,044.')
art(6,'That money supports','Xe giúp công việc và đời sống','TRANSPORTATION\nDOES SOMETHING USEFUL.','08a')
hero(6,'But the same dollars','Một đồng tiền không thể làm mọi việc','THE SAME DOLLARS\nCAN’T DO EVERY JOB.','WHAT ELSE NEEDS THAT MONEY?',prop='mpt-savings-jar')
cards(6,'Build an emergency fund','Những mục tiêu không dùng cùng một đô la','THE SAME DOLLARS\nCAN’T DO EVERY JOB.',[card('mpt-savings-jar','EMERGENCY FUND',reveal='Build an emergency fund'),card('mpt-bank-card','CREDIT CARD DEBT',reveal='Pay down a credit card'),card('home','A FUTURE MOVE',reveal='Or cover a future move')])
art(6,'That’s the tradeoff.','Đánh đổi giữa các nhu cầu','WHAT DOES THE CAR\nPUSH ASIDE?','06a')
hero(6,'And small changes','Thay đổi nhỏ vẫn có ý nghĩa','SMALL CHANGES\nCAN STILL MATTER.','LOOK FOR SOME ROOM.',prop='mpt-savings-jar')
add(6,'If Alex could safely','Hai trăm mỗi tháng thành hai nghìn bốn trăm','savings-year','$200 LESS PER MONTH.\n$2,400 MORE ROOM PER YEAR.')
hero(6,'It wouldn’t instantly','Không hứa giải quyết mọi vấn đề','NOT AN INSTANT FIX.','A LITTLE MORE FLEXIBILITY.',prop='mpt-savings-jar')
cards(6,'It could make the next repair','Sửa xe không nhất thiết thêm nợ thẻ','THE NEXT REPAIR\nDOESN’T HAVE TO START A CYCLE.',[card('mpt-wrench','REPAIR COST'),card('mpt-savings-jar','A CASH BUFFER'),card('mpt-bank-card','LESS NEW DEBT')])
hero(6,'The goal isn’t','Không cần chi phí bằng không','THE GOAL ISN’T\nZERO TRANSPORTATION COST.','SAFE. RELIABLE. WORKABLE.',prop='car3-red-sedan')
art(6,'It’s to leave enough','Giữ khoảng trống cho đời sống','LEAVE ROOM\nFOR THE REST OF YOUR LIFE.','08a')
hero(7,'Before shopping','Tự đặt ngân sách trước khi mua','BUILD YOUR NUMBER\nBEFORE SHOPPING.','THE WHOLE TRANSPORTATION COST',pose='car3-alex-compare-offers',prop='car3-offer-sheet')
cards(7,'Include the payment,','Tính đủ các nhóm chi phí','PAYMENT + OWNERSHIP COSTS.',[card('car3-red-sedan','PAYMENT'),card('car3-auto-insurance','INSURANCE'),card('car3-fuel-pump','FUEL'),card('mpt-wrench','UPKEEP + FEES')],note='Include registration and regular parking or tolls, too.')
hero(7,'Get an insurance quote','Báo giá bảo hiểm cho đúng chiếc xe','QUOTE THE ACTUAL VEHICLE.','CHECK INSURANCE BEFORE YOU BUY.',pose='car3-alex-phone-quote',prop='car3-auto-insurance')
hero(7,'Then look at','Tiền còn sau các hóa đơn thiết yếu','WHAT REMAINS\nAFTER ESSENTIAL BILLS?','START WITH YOUR OWN BUDGET.',prop='mpt-pay-envelope')
cards(7,'How much can you spend','Vẫn tiến bộ với tiết kiệm và nợ','KEEP MAKING PROGRESS.',[card('mpt-savings-jar','SAVINGS'),card('mpt-bank-card','DEBT PAYDOWN')])
art(7,'Set that limit','Đặt giới hạn trước khi thay điều khoản','COMPARE THE WHOLE DEAL.','07a')
hero(7,'When comparing offers,','Đặt các điều khoản cạnh nhau','COMPARE OFFERS\nSIDE BY SIDE.','THE WHOLE DEAL',pose='car3-alex-compare-offers',prop='mpt-comparison-cards')
cards(7,'The out-the-door price.','Năm yếu tố so sánh cạnh nhau','PUT THESE SIDE BY SIDE.',[card('car3-offer-sheet','OUT-THE-DOOR\nPRICE',reveal='The out-the-door price.'),card('car3-loan-folder','AMOUNT\nFINANCED',reveal='The amount financed.'),card('car3-offer-sheet','APR',reveal='The annual percentage rate.'),card('mpt-calendar','LOAN\nLENGTH',reveal='The loan length.'),card('mpt-cash-stack','TOTAL OF\nPAYMENTS',reveal='And the total of payments.')])
cards(7,'Check whether optional','Kiểm tra sản phẩm tùy chọn và phí','CHECK WHAT WAS ADDED.',[card('car3-offer-sheet','OPTIONAL PRODUCTS'),card('car3-loan-folder','FINANCED FEES')])
cards(7,'If there’s a trade-in,','Tách giá xe khỏi số tiền còn nợ','TRADE-IN VALUE\nAND LOAN BALANCE.',[card('car3-red-sedan','WHAT IT IS WORTH'),card('car3-loan-folder','WHAT YOU STILL OWE')])
hero(7,'A monthly payment is useful','Khoản trả hữu ích nhưng chưa đủ','A USEFUL NUMBER.\nAN INCOMPLETE PICTURE.','JUDGE THE WHOLE DEAL.',prop='mpt-comparison-cards')
hero(8,'If you already own','Đã có xe thì bắt đầu từ dữ kiện','ALREADY OWN THE CAR?','START WITH THE FACTS.',pose='car3-alex-phone-quote',prop='car3-loan-folder')
cards(8,'Find your payoff amount','Bắt đầu với thông tin khoản vay hiện tại','START WITH THE FACTS.',[card('car3-loan-folder','PAYOFF\nAMOUNT',reveal='Find your payoff amount'),card('car3-offer-sheet','INTEREST\nRATE',reveal='Interest rate, remaining'),card('mpt-calendar','REMAINING\nTERM',reveal='Remaining term,'),card('car3-red-sedan','VEHICLE\nVALUE',reveal='And a realistic estimate')])
hero(8,'Refinancing may help','Tái cấp vốn khi có lợi','REFINANCING MAY HELP.','IF THE WHOLE DEAL IMPROVES.',pose='car3-alex-phone-quote',prop='car3-loan-folder')
cards(8,'Compare fees,','So sánh phí ngày kết thúc tổng còn lại','COMPARE THE REMAINING COST.',[card('car3-offer-sheet','FEES'),card('mpt-calendar','NEW PAYOFF DATE'),card('mpt-cash-stack','TOTAL REMAINING COST')])
art(8,'A lower payment created','Khoản thấp nhờ kéo dài có thể đắt hơn','A LOWER PAYMENT\nCAN STILL COST MORE OVERALL.','03a')
hero(8,'Selling or downsizing','Bán hoặc giảm quy mô xe','SELLING OR DOWNSIZING\nMAY HELP.','COMPARE THE FULL CHANGE.',prop='car3-teal-sedan')
cards(8,'But include any negative','Tính đủ chi phí khi đổi lựa chọn','COUNT THE COSTS OF CHANGING.',[card('car3-trade-in-envelope','NEGATIVE EQUITY'),card('car3-red-sedan','REPLACEMENT\nTRANSPORTATION'),card('car3-offer-sheet','TRANSACTION COSTS')])
hero(8,'Sometimes keeping','Giữ xe đáng tin và trả xong nợ','KEEP A RELIABLE CAR.\nFINISH THE LOAN.','SOMETIMES THAT IS THE BETTER MOVE.',pose='car3-alex-keys',prop='car3-red-sedan')
hero(8,'And if you’re struggling','Liên hệ bên cho vay sớm','STRUGGLING TO MAKE PAYMENTS?','CONTACT THE LENDER EARLY.',pose='car3-alex-phone-quote',prop='phone',detail='Ask what options are available before falling behind.')
hero(8,'You don’t need a decision','Quyết định vừa ngân sách thay vì phô trương','A DECISION\nYOUR BUDGET CAN LIVE WITH.','NOT JUST AN IMPRESSIVE DRIVEWAY.',prop='car3-red-sedan')
art(8,'A good car should','Chiếc xe phục vụ đời sống','A CAR THAT FITS\nTHE REST OF YOUR LIFE.','08a')
art(8,'Its financing should','Khoản vay chừa chỗ cho mục tiêu','LEAVE ROOM\nFOR WHERE LIFE GOES NEXT.','06a')
hero(8,'Before the next purchase,','Câu hỏi trước khi mua tiếp','MORE THAN\n“CAN I MAKE THIS PAYMENT?”','WHAT ELSE DOES YOUR LIFE NEED?',prop='car3-offer-sheet')
art(8,'After paying for this car,','Câu hỏi kết về phần đời còn lại','AFTER THE CAR,\nCAN YOU AFFORD YOUR LIFE?','08a')

def text(id,content,x,y,w,size=60,fill=INK,enter=0,effect='fade',align='center'):
 return dict(id=id,type='text',text=content,x=x,y=y,w=w,h=math.ceil(size*1.18*(content.count('\n')+1)+18),size=size,fill=fill,align=align,enter=enter,effect=effect,opacity=1,drift=0)
def image(id,asset,x,y,w,h,enter=0,effect='pop',drift=0):return dict(id=id,type='image',asset=asset,x=x,y=y,w=w,h=h,enter=enter,effect=effect,opacity=1,drift=drift)
def box(id,x,y,w,h,fill,enter=0):return dict(id=id,type='rect',x=x,y=y,w=w,h=h,fill=fill,radius=24,enter=enter,effect='fade',opacity=1,drift=0)
def local(phrase,s):return round(max(0,cue(phrase,s['start']-.001)-s['start']),3)
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
 elif mode=='cards':
  items=s['items'];n=len(items);gap=36;w=(1740-gap*(n-1))/n
  for i,it in enumerate(items):
   x=90+i*(w+gap);enter=local(it['reveal'],s) if it.get('reveal') else round(.12*i,3)
   # Backgrounds and labels are also delayed: a card never hints at an unspoken number.
   out += [box(f'card-{i}',x,335,w,570,MINT if i%2 else SAND,enter),image(f'icon-{i}',it['icon'],x+40,375,w-80,200,enter+.06),text(f'label-{i}',it['label'],x+20,625,w-40,28 if n>=5 else 33 if n==4 else 39,INK,enter+.08)]
   if it.get('value'):out.append(text(f'value-{i}',it['value'],x+20,748,w-40,44 if n>=3 else 54,GREEN if i==0 else CORAL,enter+.1))
   if it.get('detail'):out.append(text(f'detail-{i}',it['detail'],x+22,842,w-44,30,INK,enter+.14))
  if s.get('note'):out.append(text('note',s['note'],100,968,1720,28,GREEN,.1))
 return out


# Deterministic content animation: sample time, never accumulate frame state.
def animate(l,prop,keys,easing='smooth',**kw):
 l['animation']=dict(property=prop,easing=easing,keys=[dict(time=round(t,5),value=round(v,6)) for t,v in keys],**kw);return l
def number(l,keys,easing='smooth',format='currency',prefix='',suffix=''):return animate(l,'number',keys,easing,format=format,prefix=prefix,suffix=suffix)
def rect(id,x,y,w,h,fill=GREEN):
 l=box(id,x,y,w,h,fill);l.update(effect='none',radius=0);return l
def pic(id,asset,x,y,w,h):return image(id,asset,x,y,w,h,0,'none')
def label(id,t,x,y,w,size=44,fill=INK):return text(id,t,x,y,w,size,fill,effect='none')
def content_layers(s):
 mode=s['mode'];D=s['duration'];end=max(.5,D-.3)
 if mode not in ['flow','loan-offer','cost-meter','cost-total','interest','amortization','calendar','trade-owed','trade-offer','equity-gap','debt-transfer','rolled-debt','savings-year']:return layers(s)
 out=[label('chapter',f'{s["section"]:02d}  /  {chapters[s["section"]-1]}',80,35,1760,24,GREEN),label('headline',s['headline'],85,100,1750,66)]
 out[0]['align']='left'
 if mode=='loan-offer':
  clone={**s,'mode':'cards','items':[card('car3-loan-folder','ANNUAL RATE','8% APR'),card('mpt-calendar','LOAN LENGTH','72 months',reveal='Over seventy-two months'),card('car3-red-sedan','MONTHLY PAYMENT','≈ $614',reveal='The payment is about')],'note':'$35,000 financed · Simplified fixed-rate example · No additional financed fees.'};out=layers(clone)
  for l in out:
   if l['id']=='value-2':number(l,[(l['enter'],0),(min(D-.2,l['enter']+1.1),614)],prefix='≈ ')
 elif mode=='flow':
  out += [pic('alex','car3-alex-explain-car',80,325,360,610),rect('flow-path',555,400,1160,6,SAND)]
  for j,(icon,title) in enumerate([('mpt-pay-envelope','WHAT ARRIVES'),('car3-red-sedan','WHAT THE CAR TAKES'),('mpt-savings-jar','WHAT IS LEFT')]):
   x=510+j*435;out += [rect(f'flow-card-{j}',x,530,400,345,MINT),pic(f'flow-icon-{j}',icon,x+95,560,210,170),label(f'flow-label-{j}',title,x+12,780,376,29)]
  for j in range(2):
   x=570+j*130;out.append(animate(pic(f'moving-money-{j}','mpt-cash-stack',x,345,100,90),'x',[(0,x),(end,1550+j*130)]))
 elif mode=='cost-meter':
  before,after=s['before'],s['after'];keys=[(.1,before),(min(end,2.5),after)]
  out += [pic('alex','car3-alex-phone-quote',100,320,420,620),label('running-label','RUNNING MONTHLY CAR COST',600,315,1200,34),number(label('cost-value',f'${after:,}',600,390,1200,104,GREEN),keys),rect('cost-track',600,550,1200,78,SAND),animate(rect('cost-meter',600,550,1200*after/1044,78),'width',[(t,v/1044*1200) for t,v in keys]),rect('addition-panel',600,690,1200,220,MINT),pic('addition-icon',s['prop'],625,710,210,170),label('addition',s['cost'],890,745,870,34,CORAL),label('note','Illustrative monthly amounts · Meter scale: the $1,044 example total.',100,968,1720,28,GREEN)]
 elif mode=='cost-total':
  out.append(number(label('total-value','$1,044',100,330,1720,110,GREEN),[(0,0),(min(end,1.4),1044)]));x=110
  for j,(cost,title,color) in enumerate([(614,'PAYMENT',GREEN),(180,'INSURANCE','#668879'),(160,'GAS','#c3973e'),(90,'UPKEEP + FEES',CORAL)]):
   width=1700*cost/1044;out.append(animate(rect(f'cost-segment-{j}',x,540,width,90,color),'width',[(.12+j*.2,0),(min(end,1.5+j*.2),width)]));out += [label(f'cost-label-{j}',title,100+j*430,720,430,31),label(f'cost-amount-{j}',f'${cost}',100+j*430,800,430,58,GREEN)];x+=width
  out.append(label('note','Illustrative monthly costs · Parking and tolls not included.',100,968,1720,28,GREEN))
 elif mode=='interest':
  rate=.08/12;pmt=35000*rate/(1-(1+rate)**-72);paid=pmt*72;interest=paid-35000
  out += [pic('loan','car3-loan-folder',250,320,350,220),pic('cash','mpt-cash-stack',1320,320,350,220),label('principal-label','ORIGINAL PRINCIPAL',100,600,800,38),label('principal-value','$35,000',100,680,800,82,GREEN),label('total-label','PAID OVER THE FULL TERM',1020,600,800,38),number(label('total-value','≈ $44,184',1020,680,800,82,CORAL),[(0,35000),(end,paid)],prefix='≈ '),label('note','Simplified $35,000 / 8% APR / 72-month loan · Rounded to about $44,200 in narration.',100,968,1720,27,GREEN)]
 elif mode=='amortization':
  rate=.08/12;pmt=35000*rate/(1-(1+rate)**-72);keys=[];monthkeys=[]
  for month in range(0,73,3):
   t=.12+(end-.12)*month/72;balance=max(0,35000*(1+rate)**month-pmt*((1+rate)**month-1)/rate);keys.append((t,balance));monthkeys.append((t,month))
  out += [pic('alex','car3-alex-compare-offers',100,320,420,620),number(label('month','MONTH 72 / 72',600,305,1200,38,GREEN),monthkeys,easing='step',format='integer',prefix='MONTH ',suffix=' / 72'),label('balance-label','LOAN BALANCE',600,385,1200,34),number(label('balance-value','$0',600,445,1200,96,GREEN),keys,easing='step'),rect('balance-track',600,610,1200,78,SAND),animate(rect('balance-meter',600,610,1200,78),'width',[(t,v/35000*1200) for t,v in keys],easing='step'),label('terms','Fixed rate: 8% APR · Monthly payment ≈ $614',600,760,1200,40),label('note','Compressed illustrative timeline · Exact loan formula at 3-month snapshots · No extra fees.',100,968,1720,27,GREEN)]
 elif mode=='calendar':
  months=[1,12,24,36,48,60,72];keys=[(.1+(end-.1)*j/(len(months)-1),v) for j,v in enumerate(months)]
  out += [rect('calendar-paper',130,330,720,575,MINT),rect('calendar-top',130,330,720,110,GREEN),label('calendar-label','MONTH',160,358,660,46,'#ffffff'),number(label('month','72',160,510,660,160),keys,easing='step',format='integer'),label('term-note','OF A 72-MONTH TERM',160,818,660,29,GREEN),pic('car','car3-red-sedan',1075,365,600,300),label('payment','≈ $614 / MONTH',960,760,840,58,GREEN),label('note','Compressed timeline for the earlier fixed-rate loan example.',100,968,1720,28,GREEN)]
 elif mode=='trade-owed':
  out += [pic('loan','car3-loan-folder',785,305,350,230),label('owed-value','$28,000',100,625,1720,112,GREEN),label('note','Separate hypothetical trade-in example, not a year-two balance for the earlier loan.',100,968,1720,27,GREEN)]
 elif mode in ['trade-offer','equity-gap']:
  clone={**s,'mode':'cards','items':[card('car3-loan-folder','STILL OWED','$28,000'),card('car3-red-sedan','TRADE-IN OFFER','$23,000')]+([card('car3-trade-in-envelope','GAP','$5,000')] if mode=='equity-gap' else []),'note':'Separate hypothetical trade-in scenario · The old loan is not assumed to be paid off.'};out=layers(clone)
  if mode=='equity-gap':
   for l in out:
    if l['id']=='value-2':number(l,[(.2,0),(min(end,1.8),5000)])
 elif mode=='debt-transfer':
  out += [rect('transfer-line',470,445,1000,6,SAND),pic('old-car','car3-red-sedan',130,650,620,230),pic('new-car','car3-teal-sedan',1170,650,620,230),label('old-label','OLD CAR',130,900,620,38),label('new-label','NEXT PURCHASE',1170,900,620,38)]
  out += [animate(pic('old-debt','car3-trade-in-envelope',500,350,200,160),'x',[(.1,500),(end,1110)]),animate(label('gap-label','$5,000 GAP',500,535,250,36,CORAL),'x',[(.1,500),(end,1110)])]
  out.append(label('note','A hypothetical unpaid gap still needs to be covered · New financing depends on approval.',100,1000,1720,25,GREEN))
 elif mode=='rolled-debt':
  keys=[(.12,30000),(min(end,3.1),35000)]
  out += [pic('alex','car3-alex-compare-offers',100,320,420,620),label('equation','$30,000 + $5,000',600,340,1200,72),number(label('new-total','$35,000',600,465,1200,104,CORAL),keys),label('total-note','NEW AMOUNT FINANCED',600,605,1200,34),rect('debt-path',760,805,850,6,SAND),animate(pic('gap-envelope','car3-trade-in-envelope',700,710,190,160),'x',[(.1,700),(min(end,3.1),1240)]),pic('new-loan','car3-loan-folder',1510,710,220,170),label('note','Separate hypothetical example · Before taxes and fees · If the lender permits the rollover.',100,968,1720,27,GREEN)]
 elif mode=='savings-year':
  begin=.3;finish=max(begin+.1,D-.65);keys=[(0,0)]
  out += [pic('alex','car3-alex-explain-car',100,320,420,620),label('monthly','$200 LESS EACH MONTH',600,300,1200,46,GREEN)]
  for j in range(12):
   t=begin+(finish-begin)*(j+1)/12;keys.append((t,200*(j+1)));col=j%4;row=j//4;x=635+col*295;y=520+row*130
   bg=rect(f'month-cell-{j}',x,y,265,110,MINT);bg.update(enter=t,effect='fade');month=label(f'month-label-{j}',f'MONTH {j+1}',x+10,y+12,245,22);month.update(enter=t);value=label(f'month-amount-{j}','$200',x+10,y+51,245,32,GREEN);value.update(enter=t);out += [bg,month,value]
  out.append(number(label('annual-room','$2,400',600,390,1200,92,GREEN),keys,easing='step'))
  out.append(label('note','Illustrative reduction · Keep transportation safe and reliable · $200 × 12 = $2,400.',100,968,1720,27,GREEN))
 return out

assert 0<len(shots)<=100
shots[0]['start']=0
assert all(a['start']<b['start'] for a,b in zip(shots,shots[1:])),[(s['title'],s['start']) for s in shots]
clips=[]
for i,s in enumerate(shots):
 end=shots[i+1]['start'] if i+1<len(shots) else total;length=round(end-s['start'],6)
 assert .5<=length<=120,(s['title'],length)
 s['duration']=length
 ll=content_layers(s)
 for l in ll:
  assert l['enter']<length-.05,(s['title'],l['id'],l['enter'],length)
 clips.append(dict(id=f'car-review-{i+1:03d}',title=s['title'],duration=length,background=BG,fade=.08 if i else 0,layers=ll))

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
project=dict(kind='credit-studio-video',version=1,revision='car-payment-review-v01',name='Car Payment Trap — Bản duyệt đầy đủ v01',width=1920,height=1080,fps=30,audio=dict(src=P+'review/voiceover.mp3',offset=0,volume=1),assets={k:v for k,v in assets.items() if k in used},clips=clips,captions=caps,showCaptions=False,waveform=peaks,waveformDuration=total)
OUT.mkdir(exist_ok=True);(OUT/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
vtt=['WEBVTT','']
for c in caps:vtt += [f'{stamp(c["start"])} --> {stamp(c["end"])}',c['text'],'']
(OUT/'captions.vtt').write_text('\n'.join(vtt))
shotdata=[dict(**s,end=round(s['start']+clips[i]['duration'],6),clipId=clips[i]['id']) for i,s in enumerate(shots)]
(OUT/'shot-plan.json').write_text(json.dumps(shotdata,ensure_ascii=False,indent=2)+'\n')
lines=['# Video 003 — Bản duyệt đầy đủ v01','',f'**{total:.3f} giây · {len(clips)} cảnh · 1920×1080 · 30 fps.** Căn theo WAV gốc; không phải bảng hình 96 giây.','', 'Dự án chỉnh được: `project.json`. Audio dẫn xuất chuẩn hóa: `voiceover.mp3`. WAV và bảng hình/thiết kế cũ được giữ nguyên. MP4: `../exports/full-review-v01.mp4`.','', '| Bắt đầu | Kết thúc | Cảnh |','|---|---|---|']
for s in shotdata:lines.append(f'| {stamp(s["start"])} | {stamp(s["end"])} | {s["title"]} |')
lines += ['','Chữ Times New Roman; tiêu đề tách khỏi nhân vật, hình/nhãn căn giữa. Chuyển động nội dung: thanh chi phí, số dư vay, lịch và dòng tiền; chưa rig khớp. Chưa có nhạc nền. Phụ đề mặc định tắt, bật được trong Studio.','',f'Nhận dạng mốc từ bằng faster-whisper base.en; đối chiếu script, khớp trực tiếp {len(mapping)}/{len(tokens)} token. Các token số và dấu câu có nội suy theo từ lân cận; vẫn có sai số mức từ. Không cắt bỏ hoặc đổi tốc độ giọng đọc.','', 'Tạo lại: `python3 tools/build-car-payment-video.py --force` chỉ sau khi sao lưu bản sửa tay; không ghi đè WAV/MP4. Dựng MP4 theo README gốc với đầu vào `review/project.json` và tên xuất mới.']
lines += ['', '27 lớp chuyển động nội dung trong 14 cảnh: thanh chi phí, dư nợ vay, lịch, chuyển nợ và tiết kiệm 12 tháng.', '', 'Audio giữ câu chuyển thời gian cũ A couple of years pass; trade-in là ví dụ giả định riêng, không phải số dư hai năm của khoản vay trước. Xem narration.md. WAV và bảng hình 96 giây giữ nguyên; bản duyệt chờ người dùng xem.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
sourceinfo={'source':P+'audio/tts_20261022_115123_7124d9.wav','sha256':hashlib.sha256((V/'audio/tts_20261022_115123_7124d9.wav').read_bytes()).hexdigest(),'duration':total,'sampleRate':24000,'channels':1,'alignmentModel':'faster-whisper base.en int8 CPU','matchedScriptTokens':len(mapping),'scriptTokens':len(tokens),'normalization':'Derived MP3 only: FFmpeg loudnorm, target -16 LUFS, true peak -1.5 dBTP; original WAV unchanged.','music':False,'sourceSpeedChanged':False,'narrationText':'review/narration.md','tradeInExample':'Separate hypothetical example; audio uses earlier time transition; WAV preserved.'}
(OUT/'source.json').write_text(json.dumps(sourceinfo,indent=2)+'\n')
print(f'Built {len(clips)} clips, {total:.3f}s, {len(caps)} captions; matched {len(mapping)}/{len(tokens)} source tokens. Assets: {len(project["assets"])}')
print('Longest:',[(s['title'],round(s['end']-s['start'],2)) for s in sorted(shotdata,key=lambda x:x['end']-x['start'],reverse=True)[:6]])
