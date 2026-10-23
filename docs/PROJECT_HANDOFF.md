# Bàn giao Credit Studio cho phiên chat tiếp theo


## Video006 — toàn bộ hình và bản dựng theo audio v01 (2026-10-23)

Đã nhận WAV `tts_20261023_125715_dda159.wav`, **535,525 giây /25.705.244 byte**, SHA`c26b2cd58cb7b9f7cd9dce14954c7668eabb699145499bb46125f6c8a93e45c5`; giữ nguyên gốc, gitignore. Tạo MP3 dẫn xuất loudnorm−16,85 LUFS /−1,67dBTP, không cắt/thay tốc độ. Căn ASR1068/1115 từ trực tiếp;149 cue EN mặc định tắt, không coi timing tự động là duyệt thủ công từng từ. Script/narration/data-snapshot vẫn giữ nguyên byte.

**Toàn bộ hình đã hoàn thành:**7 background AI theo bối cảnh,4 cutout Musk (đủ tóc/tay/chân/hồ sơ,40px padding, giữ toàn bộ visible pixels),1 outlinePortugal mainland từ Natural Earth;13 khung PNG trích từ cùng timeline. Nguồn/prompt/hash tại images/image-generation.json, tọa độ cắt tại images/musk-crop-map.json. Không nền trắng/giấy kem xuyên suốt; Times New Roman native. Musk là đối tượng được nói đến, không narrator/quote giả/lip-sync. Hình biên tập không phải bằng chứng về sự kiện/dự án Musk thực hiện.

`finance-006` mới mở **review/project.json, revision musk-scenic-review-v01,55 cảnh /535,525 giây**; gallery trong tabHình ảnh trỏ index.html/visuals.json. Chỉ một timeline JSON chính, không thêm bộ thiết kế JSON trùng; link chỉnh mở đúng clip.14 lớp motion nội dung trong11 clip,55 background pan và timed reveals. **MP4 đang xuất, chưa public; không khai báo review URL trước khi có tệp verified.**

Tổng28 media mới (WAV/MP3/8 source AI/5cutout-map/13preview) đã fullSHA-256 verify qua Actions runs39913454802 và39914179416, tải lại public full hash/Range/CORS; manifest hiện236 entry,208 cũ/sáu pin không đổi. Source/preview mới đều R2 và gitignore, không đưa binary vào main.5 metadata dự án cũ/catalog93 entry không đổi. Không sửa hoặc nhập draft người dùng; muốn tiếp tục từ sửa IndexedDB phải nhận backup.

Kiểm tra:3597 mốc hình, font thực TimesNewRomanPS-BoldMT, biên/occlusion chữ/nhân vật, currency/bar/8round72B đúng; xem55 shot contact sheets, art-gallery26ảnhR2/crop/downloadPNGhash/edit link/currentdraft reload/audio/mobile;19unit tests qua. Còn: kiểm tra MP4 khi render xong, upload/hash-verify, bật reviewURL, kiểm tra website công khai và cập nhật báo cáo. Không cần người dùng duyệt hình để tiếp tục.

## Video006 — đã gửi lời đọc Musk / Portugal v01 (2026-10-23)

Chủ đề người dùng đã chọn thay Credit Score: **Could Elon Musk Buy a Country?**, đối chiếu Musk/Bồ Đào Nha, khả năng và giới hạn của tài sản. Đã chuẩn bị `videos/006-musk-buy-a-country/`: **1115 từ /8 phần**, `narration.txt` sạch cho thu/TTS, `script.md`, `sources.md`, `data-snapshot.json`, storyboard ngắn nội bộ và script-validation.json. Chưa nhận audio, chưa có ảnh/timeline/MP4, chưa đăng ký Studio placeholder; không ghi là thành phẩm hoặc script đã được duyệt riêng.

**Yêu cầu hình mới:** Musk là nhân vật được nói đến, **không phải narrator**; giọng kể ngoài, không cho Musk nói/nhép miệng hoặc gán quote tưởng tượng. Có thể tạo minh họa Musk làm đối tượng trong cảnh. Dùng **bối cảnh theo nội dung, không nền trắng/giấy kem xuyên suốt** (Lisbon, công nghiệp, tài chính, công trường/bệnh viện/bản đồ); chữ/số native Times New Roman dễ đọc. Sau audio tự làm toàn bộ hình/dựng, không xin duyệt hình trung gian.

Mốc số liệu đã kiểm tra2026-10-23: Forbes snapshot2026-10-01 **936B USD estimated net worth**, World Bank Portugal2025 GDP~**346.64B USD**, population**10,804,871**. Không gọi GDP là tổng tài sản/ngân sách/giá mua quốc gia. Ví dụ chọn population làm tròn10.8M×$10k/resident=$108B/round≈12% của936B; hypothetical starting936B đã cash, bỏ taxes/returns/inflation/population/admin →8round đầy đủ, còn72B, không đủround9. Không gán model là kế hoạch thật của Musk/chính phủ hoặc dự báo liquidation. Không đổi mốc/số sau khi đã thu mà không tạo version mới.

Đã kiểm tra8phần/script body khớp narration,1115 từ, TTS không heading/link, các phép tính và liên kết local; không render/browser test cho bước văn bản. Giữ nguyên5 dự án, narration/audio/media/JSON cũ, R2manifest và catalog. Tiếp theo: người dùng tạo/gửi audio từ narration.txt; giữ/hash nguồn, căn cảnh theo giọng thật rồi sản xuất theo workflow đã chốt.

## Chốt quy trình tự sản xuất sau audio — 2026-10-23

Người dùng yêu cầu cập nhật GitHub để áp dụng phương pháp mới: cùng chọn chủ đề, trợ lý tự chuẩn bị/kiểm tra kịch bản và gửi lời đọc tiếng Anh Mỹ; người dùng tạo rồi gửi audio gốc; trợ lý tự lo toàn bộ phong cách, minh họa/đạo cụ, bố cục, chuyển động, dựng, kiểm tra và bàn giao MP4 cùng bản Studio chỉnh được. Không cần dừng xin duyệt storyboard, cảnh mẫu, phong cách hoặc từng hình. Thử cảnh nội bộ là tùy nhu cầu, không còn bắt buộc2–3 mẫu trước khi dựng. Người dùng có thể góp ý khi nhận thành phẩm.

Đã ghi quy trình chính tại [PRODUCTION_WORKFLOW.md](PRODUCTION_WORKFLOW.md), đồng bộ AGENTS.md, README.md và NEXT_CHAT.md. Giữ Times New Roman, nguồn/phép tính, crop an toàn và kiểm tra hình/tiếng; bỏ vòng duyệt trung gian không bỏ QA. Giữ WAV gốc, các JSON/bản xuất/backup, bảo vệ sửa IndexedDB, media archive/R2 và sáu pin cũ; không tự duyệt cuối video đã có hoặc đăng lên YouTube. Ước tính20–35% giảm thời gian thực làm (mốc30%),40–60% nếu gồm chờ duyệt chỉ là ước tính, chưa đo/cam kết. Đây là thay đổi tài liệu, không sửa dự án/media; kiểm tra diff và liên kết, không cần render hay chạy browser test.

## Video 005 — bản duyệt đầy đủ v01 đã triển khai (2026-10-23)

Theo yêu cầu triển khai của người dùng, đã hoàn thành **Your Mortgage Payment Is Only the Beginning**, **88 cảnh /566,45 giây (9:26,45)**. `finance-005` mở `review/project.json`, revision **mortgage-review-v01**; MP4 `exports/full-review-v01.mp4` ở R2. Đây là bản duyệt chờ góp ý, chưa được gọi là bản cuối.

Đồ họa nhiều lớp giấy kem/đỏ trầm/sage, Times New Roman thực, bốn nhóm Jamie và căn nhà từ SVG mẫu. **40 lớp chuyển động nội dung trong19 cảnh**, cùng các thẻ hiện theo lời: bills1517→2017 và allocation2267 (repair savings250 tách riêng), cash75000→4000/downpayment60000 sang equity, 12 lần chuyển250→3000, quỹ500/bill3000/gap2500, principal/interest tháng đầu và lịch amortization nén. Không nhạc hoặc rig khớp. Giữ ví dụ hư cấu, 6,5% nominal fixed /30 năm và các giới hạn trong sources.md; không cộng trùng escrow/repair savings hoặc gọi equity là cash.

**Bảo toàn:** narration1241 từ, WAV gốc SHA9586941c…c619c, samples/project.json86,8 giây và catalog93 mục giữ nguyên byte; bốn dự án cũ và toàn bộ204 mapping/sáu pin cũ không đổi. Năm PNG Jamie mới vẫn ở GitHub; không khôi phục media archive vào Git hoặc viết lại lịch sử. WAV/MP3/full MP4/cover mới ở R2, gitignore. Manifest hiện **208 mục /690,237,588 byte**, trong đó sáu local:true cũ; số198/620MB là đợt archive cũ, không phải tổng mới.

**R2 đã giải quyết cho video005:** credential chat vẫn401 nhưng Actions hoạt động. WAV/MP3 được full S3 SHA-256 verify ở [run39902713876](https://github.com/tai23082004l02-svg/Credit_Studio/actions/runs/39902713876); MP4/cover ở [run39904339143](https://github.com/tai23082004l02-svg/Credit_Studio/actions/runs/39904339143). Tải lại công khai kiểm tra full SHA-256, Range206/CORS trước khi đăng ký. Chuyển qua Git blob tạm8MiB bằng stage-video-media.py/r2-staged-media.yml, không commit/tree/branch chứa binary; không cần reupload WAV hoặc gửi khóa. Xem docs/R2_SETUP.md. Không tải Actions artifact từ chat do Azure redirect403, không in signed URL/credential.

**IndexedDB:** nâng cấp riêng finance-005 từ mortgage-style-samples-v01→mortgage-review-v01, archive nguyên draft cũ và thay main trong cùng giao dịch. Bản lưu tải JSON được và nằm trong .credit.json. Giữ sửa trên currentreview, revision lạ, ID khôi phục; reload không nhân lịch sử. Bản mới dựng từ repo, chưa ghép sửa riêng trong trình duyệt người dùng. Nếu muốn tiếp tục từ chúng, nhận backup trước.

**Kiểm tra:** 5.713 mốc hình, đầu/tay/chân và vùng chữ/ảnh, font TimesNewRomanPS-BoldMT, phụ đề171 cue EN một dòng (mặc định tắt), tua/phát8 vị trí/mobile. Mốc từ dựa ASR, chưa duyệt thủ công từng từ. MP4 H.264/AAC1920×1080/30fps, **16994 khung /566.466667 giây**, giải mã toàn bộ không lỗi; **-16.85 LUFS /-1.53 dBTP**. Đối chiếu WAV ở10/250/555s: lệch0 mẫu, tương quan ngắn hạn>0,995. Kết quả cụ thể review/validation.json. Đã xem contact sheet88 cảnh và khung MP4 thực; kiểm tra archive/history/backup/reload, project-workspaces, nâng cấp002/004 và19unit tests đều qua. Pages run39904544817 thành công; kiểm tra địa chỉ công khai đã qua cover, MP4 tua/phát, editor88 cảnh/audio/canvas và WAV gốc. Trang chủ, projects.json, manifest và review JSON đều HTTP200/khớp hash bản triển khaif83fd2d. Kết quả ghi trong validation.json.

**Tiếp theo:** người dùng mở Studio hoặc MP4 duyệt v01, góp ý kèm timecode. Sửa nhỏ xem trong Studio/đoạn ngắn; xuất tiếp dùng v02, giữ v01 và mọi nguồn/JSON. Không hỏi duyệt lại phong cách hoặc script. Không tạo bộ16 ảnh/bảng96 giây. Các ghi chú pending/401/ba cảnh mẫu phía dưới là lịch sử trước bản đầy đủ này.


## Video 005 — phong cách đã chốt, có minh họa Jamie (2026-10-23)

Người dùng đã chốt phong cách ba cảnh mẫu: **đồ họa nhiều lớp, giấy kem/đỏ trầm/sage, Times New Roman**. Không hỏi duyệt lại phong cách này trước khi triển khai bản đầy đủ. Căn nhà trong mẫu là SVG do trợ lý vẽ; calculator, chữ và số/bar là lớp native Studio, chưa phải hình AI. Theo trao đổi về hình ảnh, đã bổ sung một sheet AI nền trong suốt gồm bốn nhóm minh họa Jamie: nhận chìa khóa, ngồi xem hóa đơn, kiểm tra máy giặt hỏng, so sánh hai giấy tờ. Đây là minh họa cho các cảnh cần người/đồ vật, chữ và số tiếp tục dựng riêng; không tạo bộ16 frame tĩnh.

Nguồn giữ nguyên ở `videos/005-mortgage-payment/images/sources/jamie-homeowner-v01.png` (**1254×1254 RGBA**, 774856 byte); hash và mô tả prompt ở `images/image-generation.json`. Bốn PNG rời ở `library/props/jamie-mortgage/`, không upscale. Sheet có alpha1–3 speckle mờ trong gutter: xác định hình bằng alpha≥4, giữ thêm8px feather gốc và32px padding trong suốt, kiểm tra toàn bộ pixel nhìn thấy còn đủ; không lẹm đầu/tay/chân, góc bàn hoặc cạnh máy giặt. `images/jamie-crop-map.json` phân biệt cell, sourceArtCrop và sourceCrop. Bản source AI không bị sửa.

Đã chạy `tools/index-props.py`, bổ sung tên/nhóm/tags và bốn ID **jamie5-keys / jamie5-bills / jamie5-repair / jamie5-compare**, nhóm **Nhân vật · Jamie**. Kho hiện **93 mục =75 đạo cụ +14 tư thế Alex +4 nhóm Jamie**; toàn bộ89 entry cũ giữ nguyên. Năm PNG mới tổng1682183 byte ở GitHub trong lúc R2 write từ chat còn401; không đưa media đã archive trở lại Git và không thay manifest/pin cũ. Các hình mới chưa được đưa vào bản review đầy đủ vì chưa tạo full timeline/MP4; samples/project.json đã duyệt giữ nguyên để bảo toàn các bản sửa Studio.

Kiểm tra đã qua: toàn bộ93 mục trong Playwright prop-library; tìm/lọc Jamie/hóa đơn, PNG đúng kích thước, thêm vào đúng cảnh, giữ cảnh khác/audio, reload, mobile và chạy lại indexer giữ ID. Script/narration, WAV gốc, samples/project.json và manifest R2 không đổi. Real R2 public integration cũng qua đủ bốn editor/audio/MP4 và bốn gallery; bốn PNG Jamie mới tải từ origin theo allowlist, các media archive vẫn chỉ dùng R2/sáu pin cũ. Đây là kiểm tra đọc công khai, không xác nhận write/auth401 đã được sửa. Chi tiết tại images/validation.json.

Bước tiếp theo: triển khai bản đầy đủ566,45 giây theo timing/audio đã có, dùng bốn minh họa này và lớp đồ họa native, không dừng xin duyệt phong cách lần nữa. Nếu cần dùng sửa riêng trong Studio, nhận backup trước; không reset draft finance-005. Vẫn cần upload/hash-verify WAV/MP3 qua R2 khi xác thực thực tế hoạt động; không coi các PNG mới hoặc bản mẫu là đã hoàn thành full review.


## Video 005 — đã nhận WAV và có ba cảnh mẫu (2026-10-23)

Kịch bản **Your Mortgage Payment Is Only the Beginning** v01 đã được duyệt; giữ nguyên script/narration 1241 từ. Nhận WAV qua chat: **You find a house you can f.wav**, **27.189.644 byte / 566,45 giây (9:26,45), PCM s16le / 24 kHz / mono**, SHA-256 `9586941c972c26238f808a0c6c3ad0a5416f53f0e2ba07410a45e6c6f27c619c`. Bản local giữ nguyên byte, đường dẫn exact đã gitignore; metadata ở `videos/005-mortgage-payment/audio/source.json`.

**R2 còn vướng:** runtime báo biến ready nhưng authenticated HEAD từ môi trường chat trả **HTTP 401**. Chưa upload/verify WAV hoặc MP3 mới, không thêm mapping chưa tồn tại vào manifest, không kết luận khóa Actions hỏng. Full WAV hiện chỉ có ở bản upload chat và bản local, chưa có bản lưu R2 được xác minh. Không commit WAV 27 MB lên GitHub, không lấy khóa từ lịch sử hoặc yêu cầu gửi khóa vào chat. Tiếp tục upload/hash-verify khi quyền thực tế hoạt động; nếu môi trường mới không còn WAV local, nhận lại đúng file gốc trước khi dựng toàn bộ.

Đã nhận dạng cục bộ bằng faster-whisper base.en int8 CPU: **138 segment**, khớp trực tiếp **1159/1241 token**; phần lớn chênh lệch là số tiền/hyphen, có một từ equity không nhận dạng và principal thành homophone principle. `production/alignment.json` và `production/script-timing.json` có mốc; ASR có sai số, không phải xác nhận thủ công từng từ. Có bản MP3 dẫn xuất loudnorm trong work, nguồn không cắt/đổi tốc độ; nguồn WAV -27,37 LUFS.

Theo quy trình duyệt phong cách trước, đã tạo **3 cảnh mẫu / 86,8 giây** có audio trích thật (không liên tục từ đầu WAV), **16 lớp animation trong 2 cảnh**, Times New Roman: calculator, ngân sách 1517→2267 đồng bộ bar/counter, cash75000→4000 và down payment60000 chuyển sang equity. `samples/project.json` là **một bản dựng chỉnh được**, chứa PNG căn nhà và audio montage dưới dạng data URL; `samples/house.svg` giữ nguồn vector, `samples/excerpts.json` ghi vị trí trong WAV. JSON khoảng 2 MB là bản dựng chỉnh sửa, không phải đưa lại media đã archive. Không tạo bộ16 ảnh, bảng96 giây hoặc thiết kế ảnh trùng nội dung.

Đăng ký **finance-005** trỏ bản mẫu thật; mô tả/trạng thái ghi rõ **chờ duyệt phong cách, chưa phải video đầy đủ**. Chưa khai báo WAV/MP4 public không tồn tại. Bốn dự án cũ, kho89 mục, mọi source/export cũ và R2 manifest giữ nguyên. Chưa có full review/MP4 566,45 giây; chưa chốt thời điểm/cảnh toàn bộ hoặc bổ sung nhạc.

Builder `tools/build-mortgage-samples.cjs` nhận MP3 đã chuẩn hóa, script-timing và thư mục scratch; từ chối ghi đè project đã có. Mẫu cần người dùng duyệt phong cách trước khi tạo thêm tài nguyên/dựng toàn bộ; đây là bước duyệt đã thống nhất, không yêu cầu duyệt lại kịch bản. Khi chuyển finance-005 sang bản đầy đủ, bảo toàn mọi draft người dùng bằng backup/archive, không reset mẫu đã chỉnh.

Kiểm tra: validate engine, 869 mốc hình, font Chrome thực TimesNewRomanPS-BoldMT, phát audio/reload/mobile. Báo cáo `samples/validation.json`; đã xuất và decode MP4 thử cục bộ trong work (không xuất/publish full video). Sau khi sửa bố cục để tiền không che mái nhà, browser được kiểm tra lại. Các bước kiểm tra không truy cập IndexedDB trình duyệt của người dùng.

## Video 005 — kịch bản đã duyệt (lịch sử trước khi nhận audio, 2026-10-23)

Theo yêu cầu đề xuất chủ đề và triển khai, đã chuẩn bị **Your Mortgage Payment Is Only the Beginning** ở `videos/005-mortgage-payment/`: script tiếng Anh Mỹ **1241 từ / 8 phần**, narration.txt thuần lời đọc, sources.md với năm nguồn CFPB/phép tính, storyboard ngắn và README/hướng dẫn audio. Thời lượng dự kiến 8–10 phút tùy giọng; **người dùng đã duyệt kịch bản v01 ngày 2026-10-23**. Nội dung script/narration giữ nguyên 1241 từ; **chưa có audio, hình sản xuất, mẫu đã render, timeline JSON hoặc MP4**. Duyệt kịch bản không đồng nghĩa đã duyệt phong cách hình hoặc bản xuất cuối.

Mạch: loan payment → bills + repair savings → escrow không cộng trùng → tiền còn sau nhận nhà → timing sửa chữa → equity khác cash → kiểm tra ngân sách → kết. Ví dụ hư cấu Jamie: nhà300000, down60000, loan240000, nominal fixed6.5%/30 năm → PI1516.963…≈1517; tax300 + insurance125 + HOA75 → bills2017; repair savings250 → allocation2267 trước utilities. First-month interest1300/principal≈217. Cash75000−60000−9000 closing amounts−2000 moving=4000. Không gọi giả định là giá/báo giá hiện tại; savings không phải đã tiêu, không double-count escrow/repair, down payment không biến thành phí mất đi.

Áp dụng quy trình mới: không làm 16 ảnh trước audio hoặc bảng duyệt hình96 giây; kế hoạch chỉ đề xuất ba cảnh mẫu, chưa tạo. Đề xuất đồ họa nhiều lớp nền kem/đỏ trầm/Times New Roman; phong cách chưa được duyệt. Bước tiếp theo: nhận audio gốc từ narration.txt đã duyệt và dựng theo mốc thật. Trong lúc chờ có thể chuẩn bị 2–3 cảnh mẫu theo storyboard; chưa tạo hoặc render mẫu trong lần ghi nhận duyệt này. Chưa đăng ký mục rỗng finance-005 vào projects.json; bốn dự án cũ, kho89 mục, IndexedDB và R2/manifest không đổi.

Kiểm tra bước tài liệu trước: đối chiếu 8 phần với narration, tính lại khoản vay/ngân sách/cash/quỹ, kiểm tra link nội bộ và phạm vi thay đổi. Lần ghi nhận duyệt chỉ cập nhật trạng thái; kiểm tra lời đọc và narration.txt giữ nguyên. Không chạy render hoặc test trình duyệt vì chưa thay code/media. Giữ mọi bản cũ; nếu cần dùng sửa riêng Studio phải nhận backup trước.


## Quy trình sản xuất đã chốt — 2026-10-23

Áp dụng cho sản xuất mới; không xóa hay thay các tài nguyên và bản dựng cũ.

- Người dùng đã duyệt bỏ bước làm sẵn bộ 16 ảnh hoàn chỉnh trước khi có audio. Trình tự: chốt kịch bản/nguồn/phép tính → nhận giọng đọc; trong lúc chờ có thể lập storyboard ngắn và thử 2–3 cảnh mẫu để duyệt phong cách → chia cảnh theo audio thật → tạo hình và các lớp cần thiết, dựng chuyển động trực tiếp trong Studio → kiểm tra và xuất bản duyệt. Không áp số lượng 16 ảnh cố định. Chỉ tạo minh họa nguyên khung hoặc thiết kế ảnh hoàn chỉnh khi thực sự dùng trong video, thumbnail hay mục đích độc lập; không giảm chất lượng hình hoặc bỏ storyboard nội dung. Giữ nguyên toàn bộ bộ hình/bản dựng cũ.
- Bỏ bước tạo bảng duyệt hình im lặng 96 giây. Dựng sơ bộ theo audio thật trong Studio khi có giọng đọc; storyboard nội dung vẫn dùng để lập kế hoạch.
- Tạo đạo cụ theo nhu cầu cảnh, dùng lại kho chung. Sheet dùng khi cần nhiều đạo cụ đồng bộ, không tạo rồi cắt mọi món không cần thiết. Khi dùng sheet, bố trí ô và khoảng đệm an toàn; kiểm tra từng PNG sau cắt ở kích thước gốc và trong cảnh, giữ đủ góc, cạnh, đầu/tay/chân, không lẹm hình hoặc dính ô bên cạnh. Giữ nguồn và tọa độ cắt.
- Bỏ xuất MP4 đầy đủ sau mỗi chỉnh sửa nhỏ. Duyệt trong Studio hoặc xuất đoạn thay đổi; xuất toàn bộ ở mốc duyệt bản dựng sau kiểm tra.
- Bỏ duy trì nhiều bản thiết kế trùng nội dung. Dùng một bản dựng chính chỉnh được; chỉ tạo thiết kế ảnh riêng khi có mục đích sử dụng độc lập. Quy tắc này không cho phép xóa lịch sử, JSON, bản xuất hay bản sao lưu cũ.
- Không dùng Runway trong quy trình hiện tại; ưu tiên đồ họa động có thể chỉnh trong Credit Studio, đồng bộ lời đọc và số liệu, Times New Roman.


## Điểm bắt đầu cho chat mới — 2026-10-23

Đọc **[NEXT_CHAT.md](NEXT_CHAT.md)** trước để nắm trạng thái hiện tại và các quy tắc bảo toàn. Nội dung bên dưới chứa lịch sử theo từng bước; những câu về thiếu CORS, manifest tắt hoặc Pages 404 không còn là trạng thái mới nhất. Repo hiện Public; người dùng đã bật lại Pages. Kiểm tra trực tiếp: Pages built, main /, trang chủ và manifest HTTP 200, R2 enabled:true. Cây tệp sau dọn khoảng 140,6 MB; 198 media / 620,33 MB chuyển khỏi main, sáu ảnh giữ local; lịch sử Git chưa viết lại. Không có bước CORS/Pages đang chờ.

## Dọn GitHub sang R2 — ĐÃ HOÀN TẤT Ở MAIN (2026-10-23)

Người dùng đã lưu CORS. Xác nhận GET Range 206/CORS đúng cho Pages và localhost. Đã bật manifest; **gỡ 198 file / 620.325.763 byte** khỏi main (180 PNG, 4 WAV, 6 MP3, 8 MP4), không thay byte bản gốc. Đủ **204 media / 629.217.384 byte** được copy và tải lại xác minh SHA-256 ở Actions run `39889738423`. Giữ **6 PNG / 8.891.621 byte** trong repo với entry `local:true` do public R2 timeout; xem storage/README.md. Resolver, plan/sync giữ pin. Không xóa object R2 hoặc viết lại lịch sử Git.

Sau khi media đã rời cây làm việc: real R2 integration qua **4 editor/audio/MP4, 4 gallery, 89 đạo cụ, PNG download/canvas export**, chỉ sáu ảnh pin đọc từ origin Studio. 180 ảnh public được tải kiểm tra hash/CORS, 18 audio/video qua GET Range/CORS; sáu ảnh timeout giữ local. `plan()` giữ nguyên toàn bộ manifest sau khi Git không còn media cũ. Restore mẫu từ R2 đúng SHA-256, xóa bản thử sau kiểm tra. 19 unit tests qua. `vietnamese-captions-editor` qua sau khi source đã rời local: draft đã sửa giữ nguyên, English/Vi canvas thật, reload/backup, mobile, WebM thật có audio, dự án cũ và offline fallback; đủ 155 cue vừa một dòng.

Mã nguồn, mọi JSON dự án/thiết kế, revision, caption và bản sửa IndexedDB giữ nguyên. Các nguồn WAV/PNG/MP4 vẫn truy xuất được bằng manifest/restore-media.py; restore đúng thư mục trước khi chạy builders hoặc test đọc filesystem. `.gitignore` chứa chính xác các đường dẫn đã archive và /work/. Sáu ảnh pin còn được theo dõi, không tự chuyển chúng đi. Cache mới r2-media-v3. Repo main còn khoảng 141 MB tệp; lịch sử Git vẫn lớn, chưa force-push. Sau bước dọn, người dùng đã chuyển repo về Public và bật lại Pages; website đã được kiểm tra HTTP 200. Người dùng vẫn cần duyệt video; đừng nhầm migration với bản render mới.

## Kiểm tra lại R2 — 2026-10-23

**Kết quả Actions:** workflow `Diagnose R2 access`, run `39889380000`, hoàn tất **success**: ListObjectsV2 HTTP 200 và GetObject Range HTTP 206 bằng khóa xác thực. Secrets/config trong Actions dùng được; 401 chỉ tái hiện từ môi trường chat, chưa xác định vì sao hai môi trường khác nhau. Chưa thử quyền ghi/xóa, không thay manifest/CORS/media. Không yêu cầu thay khóa Actions đang hoạt động chỉ vì môi trường chat báo lỗi.

Đọc cấu hình main trực tiếp qua GitHub: manifest vẫn tắt. Kiểm tra công khai đủ 26 object trả HTTP 200, đúng kích thước, ảnh mẫu khớp SHA-256; phản hồi HEAD với Origin Pages chưa có Access-Control-Allow-Origin. API xác thực từ môi trường chat sau cập nhật cấu hình vẫn trả 401; không kết luận khóa GitHub Actions hỏng vì đây là nguồn cấu hình riêng. Kết nối GitHub hiện đọc workflow được nhưng không được liệt kê Actions secrets/variables (403). Thêm workflow chẩn đoán thủ công chỉ đọc, không log bí mật; xem docs/R2_SETUP.md. Chưa bật R2, không thay tài nguyên hoặc bản sửa người dùng.

Cập nhật: 2026-10-23. Đây là ghi chú tiếp nối công việc, không phải bản sao toàn bộ lịch sử chat. Kiểm tra trạng thái Git và các thay đổi mới trước khi thực hiện.

## Phụ đề tiếng Việt — video 004 (2026-10-22)

Theo yêu cầu xem hiểu nội dung, đã thêm lựa chọn **Tiếng Anh / Tiếng Việt** cạnh checkbox **Phụ đề** ở đầu preview Studio. Có **155 cue dịch tiếng Việt**, giữ toàn bộ tiếng Anh, mốc và chữ Times New Roman. Chọn ngôn ngữ tự bật phụ đề; `captionLanguage: en|vi` và `showCaptions` lưu trong project, đi cùng JSON/backup và WebM. Dự án cũ mặc định vẫn tiếng Anh; lựa chọn Việt bị vô hiệu nếu chưa có đủ bản dịch. MP4 v01 không xuất lại, không thêm nhạc hoặc đổi audio.

`review/project.json` chỉ thêm `textVi` vào từng cue. Sidecar `review/captions.vi.json` có revision/ngôn ngữ/cue tiếng Anh và bản dịch; VTT tiếng Việt ở `captions.vi.vtt`. Metadata `captionTranslation` là đường dẫn sidecar, được giữ qua cleanMeta/mergeMeta/backup. `video/captions.js` ghép bổ sung vào draft có sẵn **chỉ khi revision và toàn bộ start/end/text tiếng Anh khớp**; giữ timeline, lớp đã sửa, audio, lựa chọn cũ và bản dịch riêng. Không nâng revision hoặc thay toàn bộ draft. Lỗi mạng/khác mốc vẫn mở được bản đang lưu bằng tiếng Anh. Đổi audio vẫn xóa caption cũ theo hành vi trước. Builder chỉ giữ bản dịch khi mốc và chữ khớp sau khi tái tạo; không chạy lại builder hoặc renderer cho thay đổi phụ đề này.

Engine kiểm tra `textVi` tùy chọn và captionLanguage, renderer dùng cùng lựa chọn cho preview/WebM. Header responsive, Times New Roman. Query hub/editor/store/engine/iframe/CSS là `captions-vi-v1`. Đã qua **19 unit test** engine/motion/WebM/media/caption, và Playwright `vietnamese-captions-editor`: draft đã sửa giữ nguyên khi ghép, English/Vi thay đổi canvas thật, lưu/reload/backup, mobile, xuất WebM thật có audio, dự án cũ và offline. 155 cue tiếng Việt đều vừa một dòng ở font caption thực. Đã xem screenshot; kiểm tra MP4, WAV, MP3 và VTT tiếng Anh không đổi byte; project bỏ textVi thì giống hệt bản trước. Vẫn chờ người dùng duyệt video cuối và góp ý kèm timecode.

## Video 004 — bản duyệt đầy đủ từ audio gửi qua chat (2026-10-22, trạng thái mới nhất)

Người dùng gửi **`tts_20261022_133142_ba54ee.wav`** trực tiếp qua chat vì tệp lớn và tiếp tục yêu cầu dựng. Đã lưu nguyên bản vào `videos/004-living-alone/audio/`: **27.720.044 byte, 577,5 giây, PCM 16-bit / 24 kHz / mono**, SHA-256 **`10a7d8bbb78bcab9411979954c4409e9e8a70344bf527d3316258189c5c5194d`**. Không cần người dùng upload lại. Bản gốc giữ nguyên; `review/voiceover.mp3` là dẫn xuất FFmpeg loudnorm (-16 LUFS / -1,5 dBTP mục tiêu), không cắt lời hoặc đổi tốc độ. Chưa nhạc nền.

Đã dùng kế hoạch 91 cue để dựng **91 cảnh / 9 phút 37,5 giây**, **1920×1080 / 30 fps**. Dự án chỉnh được **`review/project.json`**, revision **`living-alone-review-v01`**; MP4 **`exports/full-review-v01.mp4`**. Đây là bản duyệt chờ người dùng, chưa phải bản cuối. `review/README.md` có timecode; `shot-plan.json`, `motion-plan.json`, `source.json`, `alignment.json`, `captions.vtt` ghi mốc và nguồn. 154 đoạn / 1.261 từ nhận dạng; khớp trực tiếp 1.198/1.278 token narration, token số/dấu có nội suy; vẫn có sai số căn tự động mức từ. 155 cue phụ đề một dòng, mặc định tắt trong MP4, bật được trong Studio.

- Giữ phong cách **photographic collage / giấy kem / đỏ trầm / Times New Roman**, không đưa Alex vẽ tay cũ vào cảnh mới. 23 tài nguyên được dùng; 16 thiết kế, ảnh nguồn, sheet và 16 đạo cụ vẫn giữ nguyên.
- **29 lớp chuyển động nội dung trong 15 cảnh**, cùng các thẻ xuất hiện theo lời: rent/internet chia theo hai người, số và thanh cùng mốc/thang, chênh $630/tháng tăng đúng 12 lần thành $7.560/năm; lịch hai tháng và $3.720 chỉ rent + internet; tỷ lệ hộ, phong bì thu nhập và tiền đặt cọc chuyển động. Các giá trị phần chia sẻ đợi cue tương ứng; tiền đặt cọc không bị tính thành chi phí mất đi.
- Dữ liệu lịch sử có nhãn **BLS +4,3%, 12 tháng kết thúc 12/2024** và **Census 38,5 triệu / 29% hộ, năm 2024**, không biến thành giá thuê hiện tại 2026 hoặc phần trăm dân số. Không tạo đường giá/số dư giả. Số tiền đều có nhãn ví dụ hư cấu và phạm vi.
- Ảnh nhân vật/đạo cụ nằm dưới tiêu đề, không bị panel/chữ che; ảnh fit giữ tỉ lệ, thẻ căn giữa. Minh họa tổng thể vẫn là ảnh phẳng; chưa rig khớp.

`projects.json` giữ ID finance-004, nay mở review/audio/MP4 thật. Quy tắc riêng **living-artwork-board-v01→living-alone-review-v01** archive draft bảng hình cũ nguyên vẹn trước khi thay main. Bản cũ tải JSON được và nằm trong `.credit.json`; current review edit/revision lạ/dự án khôi phục không bị reset. Đổi query hub/editor/store/iframe thành `living-review-v1` để bỏ cache bản bảng hình. **Không ghép các sửa riêng chỉ có trong IndexedDB của người dùng**; cần backup nếu tiếp tục từ chúng.

`tools/build-living-alone-video.py` tạo JSON/VTT/timecode từ narration/alignment/kế hoạch; mặc định chặn ghi đè, chỉ `--force` sau khi sao lưu sửa tay. Không sửa WAV/bộ hình/MP4. Dựng MP4 dùng renderer Studio `tools/render-intro.cjs`; lần xuất sau dùng v02, giữ v01.

Đã qua **21 unit test** engine/financial motion/WebM/media-storage. `living-alone-review`: **5.904 mốc hình** trên 91 cảnh, kiểm tra vùng ảnh/chữ, panel không che ảnh, không va chữ/chữ, một dòng caption. Đã xem toàn bộ contact sheet và nhân vật/khung tiền lớn. `living-alone-upgrade`: archive/backup/history download đúng draft cũ, giữ sửa review/reload, audio seek/playback ở 8 mốc, mobile, Tổng quan và loại trừ revision/dự án không phù hợp. `living-alone-artwork`: 16 thiết kế cũ, 2 sheet, 16 PNG và chữ TimesNewRomanPS-BoldMT vẫn đúng. Kết quả MP4/audio thực tế tại `review/validation.json`.

Đối chiếu **345 tệp cũ giữ nguyên byte**, gồm toàn bộ video 001–003, nguồn WAV mới, mọi ảnh/JSON thiết kế/sheet/PNG rời/bảng hình 96 giây của 004 và catalog 89 mục; metadata ba dự án cũ giữ nguyên. Chỉ tài liệu/kế hoạch và status artwork 004 cập nhật; frames/sheets trong artwork giữ nguyên. R2/CORS/manifest không đổi.

Tiếp theo: người dùng duyệt MP4 và góp ý kèm timecode; nhận `.credit.json`/JSON trước nếu cần ghép sửa riêng trong Studio. Không coi bản duyệt là đã được duyệt cuối; chưa thêm nhạc nền hoặc rig khớp.

MP4 thực đã giải mã toàn bộ không lỗi: **17.325 khung, 577,5 giây, H.264/AAC**, 1920×1080 / 30 fps, **65.516.385 byte**. Âm lượng **−16,68 LUFS**, true peak **−1,47 dBTP**. Đối chiếu tiếng tại giây 10/285/570: độ trễ 0 mẫu ở 16 kHz, tương quan trung vị cửa sổ 50 ms >0,9999. Thanh so sánh trong MP4 dài **660 và 436 pixel**, khớp tỉ lệ 1.860 và 1.230; phần chia sẻ chưa hiện trước cue. Đã xem khung cuối $7.560/12 tháng và $3.720/hai tháng.

`project-workspaces` qua toàn bộ assertions khi chạy riêng bằng bản chẩn đoán sau kiểm tra MP4, gồm xuất WebM im lặng thật; hai lần chạy đồng thời với xử lý media bị quá thời gian chờ download. Không đổi mã sản phẩm để xử lý khác biệt thời gian chạy này.

## Video 004 — yêu cầu dựng, chưa tìm thấy audio trên repo (lịch sử trước khi nhận WAV qua chat)

Người dùng báo đã thêm âm thanh và yêu cầu triển khai. Đã `git pull --ff-only origin main`, đối chiếu GitHub API commit/branch và tìm audio trong repo/workspace: main vẫn ở `c8665c4`, chỉ có nhánh main; `videos/004-living-alone/audio/` chỉ có README, không có WAV/MP3 của 004. Không lấy nhầm WAV của 001–003. Đã hỏi nơi lưu; nếu audio chỉ thêm trong Studio thì cần `.credit.json` chứa tệp hoặc nhận WAV/MP3, nếu upload GitHub chưa commit thì hoàn tất commit vào main.

Đã chuẩn bị `videos/004-living-alone/edit-plan.json`: **91 cue cảnh** theo thứ tự lời thoại, có layout/tài nguyên/ý chuyển động và các phép tính cần giữ. Kiểm tra mọi cue khớp đúng bản narration, số cảnh ≤100. Plan chưa có timing, `sourceAudio: null`, không phải dự án video. Chưa tạo review hoặc MP4, chưa sửa projects.json/quy tắc nâng cấp browser draft. Bảng hình 96 giây và mọi tài nguyên gốc vẫn giữ nguyên.

Tiếp theo: kiểm tra lại main vì người dùng có thể commit audio sau lần kiểm tra; khi nhận đúng audio thì đo thời lượng/hash, đối chiếu lời đọc, căn mốc từ và dùng kế hoạch làm cơ sở dựng. Chỉ bật migration finance-004 khi đã có narrated review thật và kiểm tra archive draft cũ. Không tự tạo giọng thay thế hoặc giả định audio khác đúng video.

## Video 004 — bộ hình Living Alone v01 (lịch sử trước khi nhận audio)

Người dùng đã yêu cầu triển khai hình sau lời thoại. Đã tạo bộ **documentary photographic collage** riêng, ảnh cắt ghép có viền, giấy kem, đỏ trầm; chữ Times New Roman. Dự án **finance-004** đã đăng ký ở trang chủ, gallery `videos/004-living-alone/` có tải PNG, JSON thiết kế, sheet/guide và PNG rời.

- **8 minh họa AI mới** (`images/illustrations/01a.png`…`08a.png`) + **8 bảng thông tin** = **16 thiết kế JSON và PNG 1920×1080**. Hình tạo sinh là minh họa biên tập, không phải ảnh tư liệu thật; nguồn, prompt/ghi chú và hash ở `image-generation.json`.
- **2 sheet nguồn trong suốt**, 2 atlas **4×2 ô**, mỗi ô **512×448**, 2 guide có nhãn và **16 PNG đạo cụ rời**. Đã chỉnh lại sheet vì bản thử có đồ vật sát ranh ô; nguồn sản xuất có lề an toàn. PNG riêng lấy đủ vùng alpha + feather 8px + lề trong suốt 32px; atlas không nâng độ phân giải. `crop-map.json` phân biệt sourceCrop/sourceArtCrop với crop/artBounds ở atlas.
- Thêm **16 mục `solo4-*`** nhóm **Nhà ở · Collage**, giữ nguyên 73 mục cũ. Kho chung hiện **89 mục = 75 đạo cụ + 14 tư thế Alex**. Không đổi Alex vẽ tay của video trước.
- Tiêu đề nằm ngoài vùng minh họa, ảnh fit giữ tỉ lệ; nhân vật ngồi ở 06a đầy đủ tóc/tay/hai chân. Hình và nhãn trong thẻ căn giữa. Bảng 02b có thanh cùng thang 1.860, độ dài đúng tỉ lệ 1.860 và 1.230; giữ mọi số minh họa/nhãn nguồn, năm, mẫu số hộ và giới hạn emergency fund.
- **Chưa có audio, MP4 hoặc timeline đầy đủ.** `storyboard/project.json` chỉ là bảng duyệt hình **16×6=96 giây**, revision `living-artwork-board-v01`, audio rỗng, chưa có chuyển động theo lời kể. Không thêm quy tắc nâng cấp browser draft khi chưa có review thật. Ảnh `a` vẫn là ảnh phẳng từng cảnh; đạo cụ và bảng `b` có lớp riêng, chưa rig khớp hoặc nhạc nền.

`tools/build-living-alone-artwork.cjs` đóng gói nguồn đã tạo và xuất khung qua renderer Studio, mặc định chặn ghi đè; chỉ `--force` sau khi sao lưu sửa tay. Các bản thử AI giữ ở `generated_images`, không dùng làm nguồn cắt sản xuất. Không chạy công cụ đóng gói video cũ lên video mới.

Đã qua **10 unit test** engine/WebM/media-storage; `living-alone-artwork` kiểm tra 16 thiết kế, 2 sheet, 16 PNG, biên nguồn, khoảng đệm trong suốt, ảnh không méo, không chồng chữ/chữ hoặc chữ/ảnh, thẻ căn giữa, số học và nhãn, tải tệp, mở/chỉnh trong Studio, bảng im lặng/ẩn MP4, mobile. Chrome xác nhận **TimesNewRomanPS-BoldMT**. Đã xem toàn bộ 16 khung tổng hợp, khung so sánh và nhân vật lớn, hai guide. `project-workspaces`, `prop-library`, `replace-prop` qua. Test tìm “hoa don” nay có thêm mục solo4-bills; test mobile chờ bố cục ổn định sau đổi viewport, không sửa mã sản phẩm.

Đối chiếu **272 tệp cũ giữ nguyên byte**, gồm toàn bộ video 001–003, WAV, dự án, MP4 và nguồn sheet; 73 mục catalog cũ và metadata ba dự án cũ giữ nguyên. Chỉ catalog thêm mục và README thư viện cập nhật số lượng; các tài liệu gốc khác cập nhật trạng thái. Không đọc/ghi bản sửa riêng trong IndexedDB của người dùng; R2/CORS/manifest giữ nguyên. Báo cáo tại `artwork-validation.json`.

Tiếp theo: người dùng duyệt hình và cung cấp WAV gốc vào `videos/004-living-alone/audio/` (gợi ý `living-alone-voiceover.wav`). Căn dựng đầy đủ theo audio, triển khai chuyển động tiền/lịch/checklist, lưu bảng 96 giây cũ, tạo review/MP4 tên mới. Nếu cần ghép sửa riêng trong Studio, nhận `.credit.json`/JSON trước. Sau đó mới thêm quy tắc finance-004 archive bảng cũ trước khi chuyển review thật.

## Video 004 — lời thoại Living Alone v01 (2026-10-22, trước bước tạo hình)

Người dùng cân nhắc kể chuyện/bí ẩn/lịch sử rồi quyết định **quay lại tài chính**, chốt **Why Living Alone Has Become So Expensive** và yêu cầu chuẩn bị lời thoại. Phong cách mới riêng video 004: **phim tài liệu tài chính thu nhỏ, ảnh cắt ghép có viền, giấy kem, đỏ trầm, Times New Roman**, lời đọc tiếng Anh Mỹ. Không đổi phong cách/tài nguyên ba video trước.

Đã lưu `videos/004-living-alone/script.md`: 8 phần / khoảng **1.279 từ**, 8–10 phút dự kiến; `narration.txt` chỉ chứa lời đọc để TTS; `sources.md` đối chiếu nguồn và số học; README/trang hướng dẫn audio. Đây là bản lời thoại v01 chờ người dùng xem, chưa chốt audio. **Chưa có hình, storyboard, audio, dự án dựng hoặc MP4; chưa thêm mục rỗng trong projects.json.**

Mạch: nhận chìa khóa → chi phí theo hộ → giá tăng/living alone phổ biến → khoản nhỏ và upfront → rủi ro một thu nhập → giá trị riêng tư → kế hoạch cho một người → kết. Alex/hai người bạn là minh họa hư cấu: rent 1.800 vs 2.400/2=1.200; internet 60 vs 60/2=30; rent+internet 1.860 vs 1.230, chênh 630/tháng=7.560/năm; 2×1.860=3.720 chỉ hai nhóm chi, không phải emergency target đầy đủ. Luôn ghi minh họa, không national averages. Dữ liệu lịch sử: Census 2024 38,5 triệu/29% **hộ**, BLS rent CPI +4,3% 12 tháng kết thúc 12/2024; không gọi là bộ số mới nhất/giá thuê hiện tại 2026. CFPB hỗ trợ phần quỹ khẩn cấp, mục tiêu tùy hoàn cảnh. Link trực tiếp tại sources.md.

Đã kiểm tra 8 phần, bản narration khớp nội dung script, phép tính, link tài liệu và diff chỉ tài liệu mới + README/handoff; không cần render hoặc test trình duyệt cho thay đổi tài liệu. Video 001–003, projects.json, thư viện, WAV/MP4 và IndexedDB không bị sửa. Tiếp theo: người dùng xem lời thoại, yêu cầu tạo hình theo phong cách mới rồi cung cấp audio để dựng. Chưa tự tạo ảnh hoặc xuất video trong bước lời thoại.

## Mục tiêu và quyết định đã chốt

- Người dùng giao tiếp bằng tiếng Việt, làm video YouTube tài chính cho khán giả Mỹ; lời đọc bằng tiếng Anh Mỹ.
- Người dùng cung cấp âm thanh (có thể do AI đọc). Trợ lý chuẩn bị lời thoại, hình ảnh, phân cảnh, dựng video và bản duyệt chỉnh được trong Credit Studio; người dùng sửa tiểu tiết trước bản xuất cuối.
- Phong cách đã chọn: nhân vật nét vẽ 2D, biểu đồ và biểu tượng đơn giản. Nhân vật Alex có tóc nâu sẫm, áo kem xắn tay, quần xanh teal; nền kem, nét than, xanh tiền, coral cho chi phí và điểm nhấn vàng.
- **Giữ Times New Roman cho toàn bộ chữ**, bao gồm giao diện, chữ trong hình và phụ đề. Website có font serif dự phòng khi thiết bị thiếu font; bản MP4 hiện có được dựng bằng Times New Roman thực.
- **Bố cục thẻ biểu tượng + nhãn:** người dùng góp ý từ ô “Taxes”: những lần dựng sau cần căn giữa cả biểu tượng và chữ theo chiều ngang trong từng ô, giữ khoảng cách giữa hình/chữ và lề cân đối, đồng đều giữa các ô. Đây là yêu cầu áp dụng cho lần sau; chưa thay bố cục hay xuất lại video hiện tại chỉ từ góp ý này.
- **Không cắt/che nhân vật ngoài ý muốn:** người dùng chỉ lỗi ở cảnh “PLAN AROUND WHAT ARRIVES” (ảnh `02b`): đỉnh đầu/tóc Alex bị vùng nền của tiêu đề che ngang. Các lần dựng sau kiểm tra vùng crop, mép khung và lớp nền/chữ chồng lên hình; giữ đầu, tay, chân đầy đủ khi không chủ đích cắt cận. Xem khung tổng hợp lúc vào cảnh, giữa và cuối cảnh, không chỉ kiểm tra chữ có tràn hay không. Lỗi này đã được ghi nhận, chưa sửa bản dựng/MP4 hiện tại vì người dùng đang góp ý cho lần sau.
- Dùng online, quản lý nhiều dự án qua một địa chỉ: https://tai23082004l02-svg.github.io/Credit_Studio/ . Không yêu cầu người dùng nhớ các URL công cụ riêng.

## Website và lưu dữ liệu

Ứng dụng tĩnh HTML/CSS/JavaScript, không có backend hay tài khoản. GitHub Pages triển khai từ nhánh `main`, thư mục gốc. Push vào `main` kích hoạt triển khai; kiểm tra kết quả GitHub Actions trước khi khẳng định bản sửa đã lên website.

Trang chủ có danh sách dự án và các tab Tổng quan, Dựng video, Hình ảnh, Âm thanh & tài liệu. Có tạo dự án, tìm kiếm, đổi tên, thêm tệp và sao lưu/khôi phục `.credit.json`. `/video/` và `/design/` vẫn mở trực tiếp được nhưng là công cụ bên trong luồng chung.

**Dự án tự tạo, bản sửa và tệp tải lên qua website lưu trong IndexedDB của trình duyệt đó; không tự đồng bộ lên GitHub hoặc thiết bị khác.** Chat mới không truy cập được những bản sửa này chỉ bằng việc đọc repo. Khi cần chúng, người dùng dùng **Sao lưu dự án** rồi cung cấp tệp `.credit.json`. Khôi phục tạo dự án riêng, không ghi đè dự án hiện có. Tài nguyên xuất bản sẵn vẫn được tham chiếu từ website.

`projects.json` đăng ký các dự án xuất bản. Dự án tài chính hiện có ID ổn định `finance-001`. Mỗi dự án mới cần thư mục riêng trong `videos/` và mục đăng ký riêng. Giữ khả năng đọc bản sao lưu, dữ liệu IndexedDB và các khóa localStorage cũ.

## Kho đạo cụ dùng chung

Người dùng làm rõ yêu cầu là **kho đạo cụ**, không phải kho audio/video tổng hợp. R2 đã kết nối và kiểm tra đọc/ghi thành công ngày 2026-10-21; tài nguyên đang xuất bản vẫn ở GitHub, chưa chuyển sang R2. Đã thêm nút **Kho đạo cụ** trong đầu trang Studio, route `?view=props` hoặc `?view=props&project=<id>`. Có 31 mục (27 đạo cụ + 4 tư thế Alex trong nhóm **Nhân vật**: vui mừng, lo lắng, suy nghĩ, giới thiệu), tìm kiếm tiếng Việt có/không dấu hoặc từ khóa tiếng Anh, lọc nhóm, xem trước hình và nhãn căn giữa, tải PNG riêng đúng vùng cắt/độ phân giải gốc, chọn dự án video và cảnh rồi thêm lớp ảnh độc lập vào cảnh đó.

Nhân vật dùng chung đầy đủ đầu/tay/chân từ sprite sheet Alex gốc, giữ nền trong suốt. Tải PNG riêng hoặc thêm vào cảnh như các đạo cụ khác; không tạo thêm nhân vật mới ở đợt bổ sung này. Đã kiểm tra 31 mục hiển thị, lọc 4 nhân vật, tìm nhiều từ như “Alex lo lắng”, tải PNG Alex — Giới thiệu đủ 536×769 px và thêm thành lớp riêng vào đúng cảnh; các kiểm tra kho khác vẫn qua.

Danh mục: `library/props/catalog.json`. Ảnh hiện có được tham chiếu từ các sprite sheet gốc trong `videos/001-100k-salary/`; không nhân bản/di chuyển ảnh đang dùng. Đạo cụ mới tải lên `library/props/` (PNG trong suốt ưu tiên, JPG/WebP cũng hỗ trợ), tên không dấu/không khoảng trắng; người dùng báo sau khi commit để trợ lý chạy `python3 tools/index-props.py`, bổ sung tên/nhóm/tags, kiểm tra rồi push. Upload chưa tự đăng ký vào danh mục. ID/đường dẫn đã dùng phải giữ ổn định; phiên bản mới dùng tên tệp riêng.

`assets/js/prop-library.js` kiểm tra dữ liệu, xem trước, xuất PNG và thêm lớp vào cảnh. Video engine nhận thêm nguồn ảnh `library/props/...`. Không thêm login, API ghi GitHub từ website hoặc đồng bộ dự án online. Bản dựng thêm đạo cụ vẫn lưu riêng trong trình duyệt; backup chứa tham chiếu tài nguyên đã xuất bản. Đọc `library/props/README.md` khi tiếp tục mở rộng kho.

Đã kiểm tra: 8 unit test, `tests/prop-library.cjs`, `tests/project-workspaces.cjs`, `tests/video-editor.cjs` đều qua. Kiểm tra kho bao gồm 27 vùng cắt hiện đúng, tìm không dấu/lọc nhóm, PNG tải đúng kích thước, thêm vào đúng cảnh và mở đúng cảnh đó, reload giữ lớp mới, không đổi cảnh khác/audio, thêm PNG mới từ đường dẫn library/props, từ chối nguồn/vùng cắt lỗi, mobile và công cụ lập danh mục giữ ID khi chạy lại.

### Thay đạo cụ ngay trong trình dựng

Chọn lớp ảnh rồi **Chỉnh phần tử → Thay đạo cụ** để mở hộp chọn ngay trong trình dựng. Có tìm nhiều từ/không dấu, lọc nhóm (gồm Nhân vật), hình và tên căn giữa. Chọn mẫu thay toàn bộ lớp ảnh đó, giữ ID lớp, thứ tự lớp, x/y/w/h, enter/effect/opacity/drift, thời lượng cảnh và audio. Ảnh mới giữ đúng tỉ lệ trong khung cũ, không kéo méo. Ảnh tổng thể chỉ thay được toàn bộ lớp, không tự tách vật thể bên trong.

`replaceProp` trong `assets/js/prop-library.js` tạo tham chiếu tài nguyên riêng cho lớp mới; giữ tài nguyên cũ nếu còn cảnh/lớp khác dùng, thu hồi tham chiếu không dùng để tránh tăng mãi. Trình dựng tải ảnh trước khi thay, dùng lịch sử Hoàn tác/Làm lại và lưu dự án hiện tại; không sửa JSON/MP4 xuất bản gốc. Hủy hoặc lỗi tải danh mục giữ bản đang chỉnh. Phím tắt trình dựng không tác động cảnh khi hộp chọn mở.

Kiểm tra: `tests/replace-prop.cjs` qua — thay nhân vật/đạo cụ, giữ hình học/chuyển động/audio/cảnh khác và tham chiếu dùng chung, undo/redo/reload, hủy/lỗi danh mục, mobile, thay nhiều lần không tăng tài nguyên thừa. 8 unit test engine/WebM cũng qua.

## Video đầu tiên: trạng thái thực tế

Tên: **Why You Feel Broke on a $100,000 Salary**.

Thư mục: `videos/001-100k-salary/`.

- `script.md`: lời thoại tiếng Anh chia 8 phần. Các con số là ví dụ minh họa, không phải kết quả thuế phổ quát.
- `audio/Why You Feel Broke on a $100,000 Salary.wav`: âm thanh gốc do người dùng cung cấp, dài khoảng 486,75 giây (8 phút 6,75 giây), PCM mono 24 kHz. **Bảo toàn tệp gốc.**
- `images/scenes/`: 16 ảnh cảnh PNG; `images/sheets/`: 3 bảng tài nguyên nhân vật/đồ vật có nền trong suốt.
- `projects/`: 16 thiết kế JSON có ảnh nền và lớp chữ/số chỉnh được; `artwork.json` và `storyboard.md` mô tả bộ hình/phân cảnh. Ảnh cảnh là ảnh phẳng, không phải mọi chi tiết đều tách lớp.
- `intro/project.json`: bản dựng mở đầu **40,5 giây**, 1920×1080, 30 fps, 8 cảnh có lớp nhân vật/đồ vật/chữ và chuyển động đơn giản.
- `intro/voiceover.mp3`, `alignment.json`, `captions.vtt`: đoạn âm thanh dẫn xuất, mốc từ tự động và 14 đoạn phụ đề. Xem `intro/README.md` để biết thời điểm cụ thể.
- `exports/intro-v01.mp4`: bản duyệt H.264/AAC 40,5 giây, Times New Roman, chưa thêm nhạc nền.

Bản mở đầu kết thúc sau câu “before you buy a single thing”, trước “Meet Alex.” Người dùng đã đánh giá tốt bản duyệt và yêu cầu đổi font, sau đó gộp công cụ quản lý. **Ngày 2026-10-21 đã dựng tiếp toàn bộ thành bản duyệt đầy đủ; xem cập nhật bên dưới.** Chuyển động hiện là fade/slide/pop/drift của các lớp; chưa có rig khớp nhân vật.

## Cập nhật bản dựng đầy đủ — 2026-10-21

Người dùng đã yêu cầu dựng tiếp. Đã dựng toàn bộ **486,75 giây / 64 cảnh**, nối nguyên 8 cảnh intro với 56 cảnh mới. Bản duyệt chỉnh được: `review/project.json`; nguồn âm thanh MP3 toàn bộ: `review/voiceover.mp3`; mốc nhận dạng: `review/alignment.json`; phụ đề: `review/captions.vtt`. Tất cả nằm trong `videos/001-100k-salary/`. `review/README.md` có bảng timecode từng cảnh. Bản MP4 để duyệt: `exports/full-review-v01.mp4` (1920×1080, 30 fps, Times New Roman, lời đọc gốc, chưa nhạc nền). WAV và bản intro cũ được bảo toàn.

`projects.json` vẫn dùng ID `finance-001`, trỏ bản video và MP4 đầy đủ. Trang chủ/Tổng quan xem MP4 mới, tab Dựng video chỉnh timeline. Đã sửa lỗi người dùng thấy Tổng quan 8 phút nhưng trình dựng chỉ 40,5 giây: ưu tiên bản lưu intro cũ, và thông báo mở bản mới bị ẩn trên mobile.

Trình dựng nay tự chuyển riêng `finance-001` từ revision `intro-v01` sang `full-review-v01`. Trước khi chuyển, lưu nguyên vẹn bản cũ vào document slot `history-<uuid>` trong cùng giao dịch IndexedDB với việc thay main; lỗi giao dịch không được làm mất bản cũ. Mục **Bản lưu trước cập nhật** tải từng JSON cũ, hiển thị cả trên điện thoại; `.credit.json` chứa cả lịch sử. Giữ localStorage gốc. Các bản cùng revision full được giữ nguyên khi reload, không tạo thêm lịch sử hoặc reset sửa đổi. Nếu không tải được bản mới, vẫn mở bản cũ. Dự án khác, bản khôi phục và revision khác không tự chuyển. Module/iframe đã đổi tham số phiên bản để bỏ cache ứng dụng cũ.

Các cảnh mới kết hợp nhân vật/đạo cụ tách lớp, thẻ chữ/số, biểu đồ ngân sách đúng tỉ lệ và ảnh cảnh có sẵn. Một số cảnh dùng ảnh tổng thể, không phải mọi chi tiết của ảnh đều chỉnh riêng được. Mốc từ tự động bằng faster-whisper base.en được ánh xạ lại script để giữ đúng chữ; có sai số ở mức từ. Các nhóm đạo cụ quan trọng xuất hiện theo mốc câu. Phụ đề mặc định tắt trong MP4; bật được trong Studio. Chưa có rig khớp hoặc nhạc nền.

Công cụ tái tạo: `tools/build-full-video.py` đọc script, mốc nhận dạng và tài nguyên, tạo lại JSON/VTT/timecode; không chỉnh WAV hay intro. Không chạy lại nếu có bản sửa tay chưa sao lưu. Dựng MP4 bằng `tools/render-intro.cjs` với đầu vào `review/project.json` và đường dẫn xuất mới.

Bước tiếp theo: người dùng xem **bản duyệt đầy đủ v01**, cung cấp các chi tiết cần sửa (tốt nhất kèm timecode). Nếu đã sửa trong trình duyệt, cần nhận `.credit.json` hoặc JSON video trước khi trợ lý tiếp tục từ các sửa đổi đó. Chưa coi bản duyệt là bản cuối đã được người dùng duyệt.

## Mã nguồn và kiểm tra

- `index.html`, `assets/js/hub.js`, `assets/css/hub.css`: trang quản lý và điều hướng chung.
- `assets/js/workspace-store.js`: IndexedDB, danh mục, sao lưu/khôi phục, chuyển dữ liệu cũ.
- `design/index.html`, `assets/js/app.js`, `assets/js/design-model.js`: trình ảnh và kiểm tra dữ liệu thiết kế.
- `video/editor.js`, `video/engine.js`, `video/webm.js`: trình video, bộ vẽ dùng chung và xuất WebM.
- `tools/build-video-projects.py`, `tools/build-intro-project.py`, `tools/build-full-video.py`: tạo lại thiết kế/bản intro từ cấu hình; đọc hướng dẫn trước khi chạy vì có thể thay JSON hiện có.
- `tools/render-intro.cjs`: dựng MP4 từ JSON bằng bộ vẽ dùng chung, Playwright và FFmpeg; dùng đường dẫn xuất mới để giữ bản cũ.

Đọc README để chạy máy chủ, kiểm tra và dựng MP4. Ứng dụng không cần thư viện production. Bộ kiểm tra trình duyệt/công cụ MP4 cần Playwright, Chromium và FFmpeg. Font cục bộ ở môi trường trước nằm ngoài repo tại `/workspace/shared/credit-studio-fonts`; máy mới cần kiểm tra lại, không giả định tệp đó luôn tồn tại. Không đưa tệp font độc quyền vào website/repo.

Đã kiểm tra ở lần triển khai gộp công cụ: 8 bài unit test cho engine/WebM; bộ Playwright `tests/video-editor.cjs` và `tests/project-workspaces.cjs` (tách dữ liệu dự án, lưu lại, âm thanh, xuất WebM, sao lưu/khôi phục và mobile); MP4 thực bằng FFmpeg/ffprobe. GitHub Pages triển khai thành công cho commit `0f542fa`; tài nguyên online đã đối chiếu qua HTTPS. Đây là kết quả của phiên trước, không thay cho kiểm tra phù hợp với thay đổi mới.

Kiểm tra bản đầy đủ ngày 2026-10-21: 8 unit test và cả hai bộ Playwright đã qua, gồm bảo toàn/sao lưu bản sửa cũ, hủy mở bản mới, xác nhận mở và reload bản đầy đủ. Kiểm tra thực tế toàn bộ bố cục chữ bằng Times New Roman, tua audio ở 8 phần, phát đoạn kết, timeline và mobile đã qua. MP4 đã giải mã toàn bộ bằng FFmpeg không lỗi; âm thanh đối chiếu WAV ở giây 10/200/480 có tương quan >0,9999. MP4 dài 486,766667 giây do làm tròn khung 30 fps; audio/timeline 486,75 giây. Xem `review/validation.json` và `review/source.json`. Trạng thái triển khai cần kiểm tra theo commit mới nhất trên GitHub Actions.

Kiểm tra bản sửa mở video: Playwright tái hiện bản intro đã chỉnh trong localStorage/IndexedDB rồi xác nhận tự mở 64 cảnh; JSON cũ được tải lại nguyên vẹn, backup chứa main mới và lịch sử, sửa bản đầy đủ rồi reload vẫn giữ, lịch sử không nhân đôi. Kiểm tra mở trực tiếp `/video/` chỉ có localStorage, lỗi mạng tải bản mới và thử lại thành công. Không cần dựng lại MP4 vì chỉ sửa cách chọn bản dự án.

## Cách tiếp tục trong chat mới

R2 đã kết nối thành công ngày 2026-10-21. Môi trường hiện có đủ `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`, `R2_BUCKET` dưới dạng biến môi trường trực tiếp (nguồn vault), không phải bí mật proxy. Đã thử S3 SigV4 với region `auto`: ListObjectsV2 HTTP 200 (bucket trống), PUT tệp thử 200, GET 200 và đối chiếu đúng nội dung, DELETE 204 để dọn tệp thử. Không lưu giá trị khóa trong repo/log/chat. Tệp riêng `/workspace/.credit-studio/r2.env` vẫn chỉ là mẫu chưa có khóa; nguồn đang dùng là biến môi trường. Chat mới phải kiểm tra các biến có mặt và thử quyền cần dùng, không giả định thông tin phiên cũ tự được truyền sang môi trường khác.

Đã chép và xác minh 26 tệp (128.215.675 byte) lên R2; các bản gốc GitHub được giữ. Public URL, manifest, công cụ và trạng thái mới nhất nằm trong `docs/R2_SETUP.md`. `storage/manifest.json` hiện **enabled: false** vì chờ người dùng lưu CORS và kiểm tra trình duyệt với R2 thật. Đã chuẩn bị bộ phân giải đường dẫn cho kho đạo cụ, trình dựng, audio, MP4 và thư viện ảnh; JSON dự án giữ đường dẫn cũ. Kiểm tra mô phỏng R2 và unit test đã qua; không nhầm với đã kiểm tra thực tế hoặc đã giảm dung lượng GitHub. Bản sửa vẫn lưu trong trình duyệt.

Chọn/đính kèm repo `tai23082004l02-svg/Credit_Studio`, yêu cầu đọc `AGENTS.md`, tài liệu này và README. Chat mới không tự nhớ lịch sử chat cũ. Nếu chưa có quyền truy cập repo, cần kết nối/chọn repo trước. Nếu công việc phụ thuộc bản sửa chỉ có trên trình duyệt, cung cấp bản sao lưu dự án; chỉ GitHub là chưa đủ.

## R2: token thay thế và bước đang chờ

Người dùng đã thông báo thu hồi token cũ và thay khóa. Đã xác nhận danh tính S3 mới khác danh tính từng lộ trước khi di chuyển. Không dùng lại khóa từ lịch sử Git. Công cụ tự chuẩn hóa token value/token ID theo tài liệu Cloudflare; hai biến khóa hiện tại hoạt động, không yêu cầu nhập lại. Chỉ log tên biến/trạng thái.

Người dùng đang tìm **CORS Policy** trong tab Settings của bucket `credit-studio`, không phải Settings tài khoản. Đã gửi cấu hình cho origin GitHub Pages và `http://127.0.0.1:8002`; chi tiết trong `storage/cors.json`. Quyền token hiện tại không sửa CORS qua API (403), nên thực hiện trên UI; không yêu cầu khóa quản trị. Sau khi người dùng lưu, kiểm tra header, trình duyệt R2 thật rồi mới bật manifest, triển khai và kiểm tra website online.

## Video 002 — Bộ hình Monthly Payment Trap (2026-10-21)

Người dùng đã chấp thuận lời thoại **The Monthly Payment Trap: How “Affordable” Keeps You Broke** và yêu cầu tạo toàn bộ hình, sheet đẹp/dễ cắt và đưa lên GitHub. Đã thêm `videos/002-monthly-payment-trap/`, giữ nguyên lời thoại 8 phần khoảng 1.101 từ trong `script.md`, `storyboard.md`, README và hướng dẫn audio. ID ổn định `finance-002` được đăng ký trong `projects.json`; có thể mở từ trang chủ như dự án 001.

Đã có **16 PNG khung 1920×1080 và 16 JSON thiết kế chỉnh được**: 8 cảnh minh họa mới đúng Alex/bảng màu hiện tại, 8 bố cục thông tin có hình/chữ/số/thẻ riêng. Chữ Times New Roman thực khi xuất PNG. Tiêu đề tách ngoài vùng minh họa (y>=254), không dùng nền tiêu đề phủ lên tóc. Ảnh giữ tỉ lệ, hình và nhãn trong thẻ căn giữa. 8 ảnh minh họa vẫn là ảnh tổng thể, chưa tách mọi nét hoặc gắn khớp. `images/scenes/` có PNG hoàn chỉnh; `images/illustrations/` giữ PNG minh họa nguyên bản.

Có **3 atlas trong suốt theo ô đều**, 3 bản `*-guide.png` có viền ô/nhãn Times New Roman, **6 tư thế Alex + 24 đạo cụ**, 30 PNG riêng thêm đệm trong suốt 32 px mỗi phía; không nâng độ phân giải nội dung. `images/sources/` giữ nguyên 3 sheet tạo sinh. `images/crop-map.json` ghi `[x,y,width,height]` theo pixel, ô trên atlas và vùng cắt ở nguồn. `asset-layout.json` mô tả cấu hình; `tools/build-monthly-payment-artwork.cjs` tái tạo atlas, PNG riêng, khung PNG và JSON từ nguồn bằng browser canvas, có chặn ghi đè trừ khi dùng `--force`. Không chạy đè lên bản sửa chưa sao lưu. Font cục bộ chỉ ở `work/`, không commit font độc quyền.

Đã thêm 30 ID `mpt-*` vào Kho đạo cụ bằng vùng cắt atlas mới, giữ 31 mục cũ nguyên vẹn. Tổng kho **61 mục = 51 đạo cụ + 10 tư thế Alex**. Dự án 001, WAV, MP4 và mã ứng dụng cũ không thay đổi; các bản sửa IndexedDB của người dùng không bị đọc/ghi bởi việc bổ sung tài nguyên xuất bản này. Các test cũ được đổi từ số dự án/nhân vật cố định sang đếm danh mục để phù hợp nhiều dự án và nhân vật.

**Chưa nhận audio cho video 002; chưa có MP4 hoặc bản dựng đã căn lời đọc.** `storyboard/project.json` mở trong trình video chỉ là bảng 16 ảnh tĩnh, mỗi cảnh tạm 6 giây (96 giây để duyệt hình), revision `artwork-board-v01`, audio rỗng. Tuyệt đối không gọi đây là video hoàn chỉnh hoặc dùng 96 giây làm thời lượng thật. Thông báo trạng thái này có ở trang chủ, gallery và README.

Đã kiểm tra: 10 unit test engine/WebM/media-storage; các bộ Playwright `tests/monthly-payment-artwork.cjs`, `tests/prop-library.cjs`, `tests/replace-prop.cjs`, `tests/project-workspaces.cjs`; mở/chỉnh cảnh 002 trong Studio, tải PNG Alex, gallery/mobile, 61 đạo cụ, mọi vùng cắt/padding, tỉ lệ ảnh, phép tính và tách vùng tiêu đề. Đã xem bản tổng hợp 16 khung và sheet Alex có nhãn. Xem `videos/002-monthly-payment-trap/validation.json`. Việc kiểm tra này chỉ áp dụng bộ hình; chưa kiểm tra chuyển động/âm thanh video 002 vì chưa có bản dựng theo audio.

Bước tiếp theo: người dùng xem hình và cung cấp WAV/MP3; căn nhiều shot từ 16 bố cục và sheet, giữ khoảng đệm, kiểm tra tóc/tay/chân ở lúc vào/giữa/ra, chuẩn hóa audio dẫn xuất nếu cần nhưng bảo toàn WAV, xuất MP4 duyệt vào tên mới. Chưa nhạc nền hoặc rig khớp. Nếu người dùng đã sửa trong Studio, nhận `.credit.json`/JSON trước khi tiếp tục từ bản sửa đó. Các lỗi MP4 video 001 đã ghi nhận vẫn chưa được sửa trong đợt này.

Triển khai bộ hình: commit `3f3dbef`, GitHub Pages run `39599766439` hoàn tất thành công; `projects.json`, artwork 002, atlas Alex và PNG ngân sách 03b online trả HTTP 200, SHA-256 khớp tệp đã kiểm tra. Kiểm tra tương thích `tests/r2-browser.cjs` cũng qua với R2 mô phỏng và fallback GitHub cho mục mới; đây không phải kiểm tra CORS R2 thật. Runtime manifest vẫn tắt, không thay trạng thái R2.

## Video 002 — Bản duyệt đầy đủ theo audio (2026-10-21)

Người dùng đã tải WAV lên nhánh main (commit `46834af`) và yêu cầu triển khai edit. Đã nhận `videos/002-monthly-payment-trap/audio/monthly-payment-trap-voiceover.wav`: PCM mono 24 kHz 16-bit, **495,475 giây**; bảo toàn nguyên tệp. Đã căn toàn bộ thành **79 cảnh / 8 phút 15,475 giây**, project `review/project.json`, revision `monthly-payment-review-v01`, MP4 `exports/full-review-v01.mp4`, 1920×1080 30 fps H.264/AAC. Đây là bản duyệt v01, chưa phải bản cuối được người dùng chấp thuận.

`review/voiceover.mp3` là dẫn xuất nâng âm lượng bằng FFmpeg loudnorm, không đổi tốc độ hoặc bỏ nội dung. WAV đo khoảng −27,27 LUFS; MP3 dẫn xuất khoảng −16,73 LUFS, true peak −1,65 dBTP. Âm lượng bản MP4 được đo riêng trong `review/validation.json`. Không có nhạc nền; chuyển động lớp fade/pop và drift nhẹ, chưa rig khớp. Phụ đề 128 đoạn có thể bật trong Studio, MP4 mặc định tắt. Mốc từ faster-whisper base.en khớp trực tiếp 1.031/1.101 token script, các từ số/dấu câu nội suy; vẫn có sai số mức từ. `review/alignment.json`, `captions.vtt`, `shot-plan.json`, `source.json`, README timecode và validation ghi nguồn/thực tế.

Dùng 8 minh họa gốc và PNG riêng cho nhân vật/đạo cụ để giữ nhân vật lớn rõ mà không kéo theo khoảng trống toàn ô atlas. Chữ Times New Roman thật (`TimesNewRomanPS-BoldMT` được Chrome xác nhận), đầu/tay/chân đầy đủ, tiêu đề tách khỏi vùng nhân vật; hình và nhãn trong thẻ căn giữa. Đã kiểm tra 237 khung vào/giữa/ra của 79 cảnh bằng hình học và bộ vẽ, từ chối nền hoặc chữ che ảnh, không tràn khung; xem tổng hợp bố cục và khung nhân vật thực. Phụ đề tối đa một dòng trong bản hiện tại, không che chân nhân vật.

`projects.json` vẫn dùng `finance-002`, nay trỏ review đầy đủ, WAV và MP4. `storyboard/project.json` **vẫn nguyên bảng hình 96 giây cũ**; 16 thiết kế ảnh, atlas, PNG riêng và bản duyệt video 001 được giữ. Không chạy lại công cụ tạo hình để tạo bản video. Công cụ mới `tools/build-monthly-payment-video.py` đọc script/mốc từ/tài nguyên để tạo review; chặn ghi đè trừ `--force`, chỉ dùng sau khi sao lưu sửa tay. Công cụ không sửa WAV hoặc MP4.

Để tránh Tổng quan mở bản đầy đủ nhưng Dựng video còn 96 giây, thêm quy tắc chuyển riêng `finance-002` từ `artwork-board-v01` sang `monthly-payment-review-v01`. `canUpgradePublishedVideo` dùng chung ở hub/editor; gọi lại giao dịch `promotePublishedVideo` để lưu toàn bộ draft cũ vào lịch sử trước khi thay main. Giữ nguyên quy tắc intro→full của `finance-001`. Không tự thay revision lạ, bản khôi phục có ID khác hoặc bản review đang chỉnh. Bản cũ tải JSON được và có trong `.credit.json`; reload bản review giữ sửa đổi, không nhân đôi lịch sử. Đã đổi query phiên bản hub/editor/store/iframe để nhận bản sửa mới.

Đã qua 10 unit test engine/WebM/media-storage; Playwright `monthly-payment-review`, `monthly-payment-upgrade`, `monthly-payment-artwork` và `project-workspaces`. Kiểm tra mới gồm archive bảng hình đã sửa nguyên vẹn, tải lịch sử/backup, giữ sửa review khi reload, tua audio ở 8 vị trí và phát gần cuối, mobile, Tổng quan mở đúng 79 cảnh và loại trừ revision không biết/bản khôi phục. MP4 được giải mã toàn bộ và kiểm tra codec/thời lượng/âm lượng/đối chiếu tiếng đọc; kết quả cụ thể ở `review/validation.json`. Source WAV, toàn bộ thư mục video 001 và kho đạo cụ được đối chiếu không đổi.

Tiếp theo: người dùng duyệt v01 và góp ý kèm timecode. Nếu đã sửa trong Studio, nhận `.credit.json` hoặc JSON video trước khi tiếp tục từ bản sửa đó. Các lần xuất sau dùng tên mới, không ghi đè v01. Lỗi che tóc trong MP4 video 001 vẫn là việc riêng chưa sửa. R2/CORS/manifest không thay đổi trong lần dựng này.

## Video 001 dựng lại — bản duyệt v02 (2026-10-21)

Theo yêu cầu dựng lại video đầu tiên sau video 002, đã xây bản v02 dựa trên **bản đầy đủ v01 trong repo**, không phải các sửa riêng chỉ có trên trình duyệt. Giữ nguyên lời đọc, thời lượng 486,75 giây và WAV gốc; tăng từ 64 lên **88 cảnh**. Chưa phải bản xuất cuối được người dùng duyệt.

- Bản chỉnh được: `videos/001-100k-salary/review-v02/project.json`, revision `salary-review-v02`.
- MP4 mới: `exports/full-review-v02.mp4`, 1920×1080 / 30 fps, có giọng đọc chuẩn hóa, chưa nhạc nền hoặc rig khớp.
- `review-v02/README.md`: timecode 88 cảnh; `source.json`: nguồn WAV/hash/căn từ; `validation.json`: kết quả kiểm tra tệp xuất thực tế. Mốc từ dùng lại alignment v01 đối chiếu script, có sai số căn tự động.
- Bốn PNG minh họa mới ở `review-v02/images/`: dòng tiền có cam kết chờ sẵn, quỹ chi phí trong năm, nguồn tiền sau hình ảnh xã hội, kế hoạch tăng lương. Không suy diễn người đăng ảnh phải dùng nợ; nhãn ghi các khả năng. Không thêm tỉ lệ phân chia tiền chưa có trong lời thoại.
- Bốn thiết kế `projects/v02-*.json` có ảnh và chữ Times New Roman tách riêng, thêm vào Hình ảnh; tổng cộng **20 thiết kế**, giữ nguyên 16 thiết kế gốc và các sheet. Chi tiết bên trong mỗi minh họa mới vẫn là một lớp ảnh.
- Tách vùng tiêu đề khỏi vùng nhân vật, sửa lỗi tiêu đề che tóc ở “PLAN AROUND WHAT ARRIVES” trong **MP4 v02**. MP4 v01 bảo lưu vẫn có lỗi cũ. Kiểm tra trọn đầu/tay/chân, thẻ đạo cụ/nhãn căn giữa, các thanh 4.900 + 600 + 500 đúng tỉ lệ trên 6.000 USD minh họa.
- `review-v02/voiceover.mp3` là dẫn xuất WAV, có chuẩn hóa âm lượng; không thay tốc độ hay nội dung. WAV SHA-256 vẫn `340b5ff951c23c3258244296a3adc1ebf6788d0ffe0e75fdf1fabfa50a5cc5df`.

`projects.json` giữ ID `finance-001`, nay mở v02 ở Tổng quan/Dựng video. Quy tắc nâng cấp cho đúng ID: intro-v01→salary-review-v02 hoặc full-review-v01→salary-review-v02; giao dịch lưu nguyên draft cũ vào **Bản lưu trước cập nhật** trước khi thay main. Bản cũ tải JSON được và nằm trong `.credit.json`. Không tự thay bản v02 đang chỉnh, revision lạ hoặc dự án khôi phục có ID khác. Thay đổi riêng của người dùng trong v01 được giữ trong lịch sử, **chưa ghép vào v02**. Quy tắc video 002 vẫn giữ nguyên.

Công cụ mới `tools/build-salary-review-v02.py` tạo dữ liệu từ script/alignment/tài nguyên; `tools/build-salary-v02-designs.cjs` đóng gói bốn thiết kế bổ sung. Mặc định chặn ghi đè; chỉ dùng `--force` sau khi sao lưu bản chỉnh tay. Xuất MP4 bằng `tools/render-intro.cjs` với tên xuất mới. Không chạy công cụ đóng gói ảnh cũ lên các mục v02.

Đã qua 10 unit test engine/WebM/media-storage; Playwright `salary-review-v02` (264 mốc đầu/giữa/cuối), `salary-review-upgrade` (lịch sử chính xác, tải JSON/backup, reload giữ sửa, tua/phát audio, mobile, Tổng quan và mở trực tiếp intro→v02), `salary-v02-artwork` (20 hình tải đủ, bốn thiết kế mở đúng và chữ căn giữa), `project-workspaces`. Các bộ `monthly-payment-upgrade` và `monthly-payment-artwork` vẫn qua. Chrome xác nhận font thực tế TimesNewRomanPS-BoldMT. Đối chiếu 154 tệp media/dự án/catalog đã có: giữ nguyên byte; 16 mục ảnh cũ, toàn bộ video 002 và metadata video 002 không đổi. Không thay cấu hình R2/CORS.

Tiếp theo: người dùng duyệt MP4 v02, gửi góp ý kèm timecode. Nếu cần tiếp tục từ thay đổi riêng đã chỉnh trong Studio, nhận `.credit.json` hoặc JSON video trước. Giữ nguyên các bản xuất cũ, dùng tên v03 cho lần xuất tiếp theo.

MP4 v02 đã giải mã toàn bộ không lỗi, H.264/AAC, 14.603 khung, 486,766667 giây do làm tròn 30 fps. Âm lượng đo thực tế −16,69 LUFS, true peak −1,56 dBTP. Đối chiếu đoạn tiếng ở giây 10/200/480 với WAV: độ trễ 0 mẫu; trung vị tương quan cửa sổ 50 ms đều >0,9999. Kết quả chi tiết ở `review-v02/validation.json`.

## Video 001 — chuyển động nội dung v03 (2026-10-22)

Theo góp ý video còn giống slide, bổ sung **23 lớp chuyển động trong 11 cảnh** trên bản v02 đã xuất bản: tiền di chuyển qua nhóm thu–chi; số dư/thanh ngân sách cùng giảm qua sáu khoản cố định và quỹ không đều; thanh phân bổ tăng đúng tỉ lệ; lịch nhảy 28→29→30→1 và tháng 1→2. Ngày trên lịch là minh họa. Giữ nguyên 88 cảnh / 486,75 giây, lời đọc, caption và đường dẫn audio v02; không thêm nhạc hoặc rig khớp nhân vật. Không tự coi đây là bản cuối được duyệt.

- Dự án mới `videos/001-100k-salary/review-v03/project.json`, revision `salary-motion-v03`; MP4 mới `exports/full-review-v03.mp4`.
- `review-v03/motion-plan.json`: 11 cảnh/23 lớp; `review-v03/README.md`: mốc và cách chỉnh; `validation.json`: kết quả kiểm tra bản xuất thực tế.
- `tools/build-salary-motion-v03.py` đọc v02 rồi tạo v03, mặc định chặn ghi đè. Không dùng `--force` nếu chưa sao lưu bản chỉnh tay. Audio tiếp tục dùng `review-v02/voiceover.mp3`, không nhân bản hoặc sửa file.
- `video/engine.js`: thuộc tính `animation` tùy chọn gồm property width/x/y/number, keys thời gian–giá trị và nhịp smooth/linear/step. Nội suy trực tiếp từ thời gian, không phụ thuộc lịch sử playback, nên tua ngược và xuất cho cùng kết quả. Số hỗ trợ currency USD/integer và prefix/suffix. Kiểm tra loại lớp, giới hạn số, mốc tăng và số lượng mốc; dự án cũ không có animation giữ nguyên cách vẽ.
- Studio có **Chỉnh phần tử → Chuyển động nội dung** để tạo/tắt/chỉnh mốc, nhịp và định dạng số. Có hoàn tác/làm lại, JSON, tự lưu và xuất WebM. Di chuyển/nhân bản lớp dịch cả đường chuyển động; chỉnh rộng thanh co giãn các mốc theo cùng tỉ lệ. Nhân bản tách bản sao keys, không làm đổi lớp nguồn. Không thêm lịch sử cho thay đổi không làm đổi dữ liệu.
- `projects.json` nay mở v03; intro/v01/v02 đã chỉnh trong trình duyệt được lưu nguyên vẹn vào lịch sử bằng giao dịch cũ trước khi chuyển main. Bản v03 đang chỉnh, revision lạ và dự án khôi phục không bị tự thay. V03 dựa trên repo, chưa ghép các sửa riêng trong IndexedDB; muốn tiếp tục từ chúng cần `.credit.json` hoặc JSON.

Kiểm tra: 15 unit test engine/motion/WebM/media; Playwright `salary-motion-review` lấy 4.991 mẫu trên timeline, xác nhận vùng nhân vật, chữ và caption; `video-motion-editor` kiểm tra controls, từ chối mốc sai, hoàn tác/làm lại, sửa/nhân bản đường chuyển động, JSON/reload, mobile và xuất WebM thực có audio, vùng thanh khác nhau giữa hai thời điểm; `salary-motion-upgrade` giữ v02 đã chỉnh nguyên vẹn trong lịch sử/backup và giữ sửa v03; `project-workspaces`, `replace-prop`, `monthly-payment-upgrade`. Chrome tiếp tục xác nhận font thực TimesNewRomanPS-BoldMT. Đối chiếu 175 tệp đã có: WAV, mọi bản dựng/xuất cũ, thiết kế/ảnh và toàn bộ video 002 không đổi byte; metadata video 002, audio, captions và toàn bộ ID/thời lượng clip giữ nguyên. R2/CORS/manifest không thay đổi.

Tiếp theo: duyệt mức độ chuyển động trong v03 và gửi góp ý kèm timecode. Nếu tiếp tục từ các sửa riêng trong Studio, nhận bản sao lưu trước. Lần xuất sau dùng v04, giữ các bản cũ.

MP4 v03 đã giải mã toàn bộ không lỗi: 14.603 khung, 486,766667 giây do làm tròn 30 fps, H.264/AAC. Âm lượng đo thực tế −16,69 LUFS, true peak −1,56 dBTP; đối chiếu tiếng ở giây 10/200/480 có độ trễ 0 mẫu và tương quan ngắn hạn >0,9999. Kiểm tra vùng thanh ngay trong MP4 thấy giảm từ khoảng 1.192 xuống 740 pixel, đúng số dư 3.700/6.000; đã xem khung lịch tháng 2 ngày 1. Có bản xem nhanh **18,36 giây** ở `exports/motion-preview-v03.mp4`, trích ba đoạn từ MP4 đầy đủ.

## Video 003 — bộ hình Car Payment Trap (2026-10-22)

Người dùng đã chọn chủ đề **Your Car Payment Is Keeping You Broke**, nhận lời thoại và yêu cầu tạo hình. Đã lưu lời thoại tiếng Anh từ bản trong chat vào `videos/003-car-payment-trap/script.md` và tạo bộ tài nguyên mới, đăng ký dự án **finance-003** trên trang chủ.

- 8 PNG minh họa mới theo 8 phần lời thoại: đại lý/giá tháng, chi phí sở hữu, kỳ hạn dài, negative equity, cash flow so với resale value, mục tiêu bị chiếm chỗ, so sánh báo giá, lựa chọn xe phù hợp cuộc sống.
- 8 bảng thông tin bổ sung; tổng **16 thiết kế JSON chỉnh được**, 16 PNG xem trước qua cùng renderer Studio. Tiêu đề ngoài vùng minh họa; ảnh giữ tỉ lệ, đầu/tay/chân đầy đủ. Chữ/số Times New Roman tách riêng; hình/nhãn trong thẻ căn giữa.
- 2 sheet nguồn và 2 atlas đóng gói nền trong suốt, có guide ô đều/nhãn tham chiếu. **12 PNG rời mới: 8 đạo cụ ô tô và 4 tư thế Alex**. Cắt theo ô gốc, lấy trọn vùng hình và thêm 32 pixel trong suốt quanh mỗi mục; atlas giữ khoảng đệm ít nhất 40 pixel quanh nét rõ. Không dùng ảnh cảnh phức tạp làm nguồn cắt vật thể.
- `asset-layout.json`: cấu hình; `images/crop-map.json`: sourceCrop/sourceArtCrop theo sheet nguồn, crop/artBounds theo atlas đã đóng gói. Không hoán đổi hệ tọa độ. Các bản nguồn AI giữ nguyên, thông tin/hash tại `image-generation.json`.
- 6 biểu tượng dùng lại từ kho cũ được đóng gói vào `images/reused/`, không đăng ký trùng. Kho chung từ 61 lên **73 mục: 59 đạo cụ và 14 tư thế Alex**, chỉ thêm 12 ID `car3-*`; 61 mục cũ giữ nguyên dữ liệu.
- `tools/build-car-payment-artwork.cjs`: đóng gói/cắt hình/thiết kế và xuất PNG; mặc định chặn ghi đè, chỉ `--force` sau khi sao lưu chỉnh tay. Công cụ không gọi lại AI hoặc sửa bản ghi âm.

**Chưa có WAV/MP3. Chưa căn lời đọc, chưa có MP4 hoàn chỉnh.** `storyboard/project.json` là bảng hình **16 × 6 = 96 giây**, audio rỗng, revision `car-artwork-board-v01`, chỉ để duyệt bố cục. Dự án không khai báo review MP4 hoặc audio chưa tồn tại, nên nút MP4 được ẩn. Các lớp minh họa tổng thể chưa tách tiếp bên trong; PNG rời, thanh và chữ sẽ dùng để dựng chuyển động sau khi nhận audio. Chưa rig khớp hoặc nhạc nền.

Kiểm tra `tests/car-payment-artwork.cjs`: 16 ảnh tải đủ, 2 atlas và 12 PNG rời, bounds vùng cắt, lề trong suốt, hình không kéo méo, tiêu đề không che minh họa, số liệu đúng phép tính và mức làm tròn, tải PNG/JSON, mở cảnh chỉnh được trong Studio, bảng video im lặng/ẩn MP4, mobile và 12 mục mới trong kho chung. Đã xem toàn bộ contact sheet và hai guide; Chrome xác nhận TimesNewRomanPS-BoldMT. Video 001/002, các dự án và bản xuất cũ không thay đổi; metadata hai dự án cũ và 61 mục đạo cụ cũ giữ nguyên.

Số liệu cần giữ: vay $35,000 ở APR 8% / 72 tháng → khoảng $614/tháng, tổng khoảng $44,200 và lãi khoảng $9,200 (fixed rate, không thêm financed fees); 614 + 180 + 160 + 90 = 1,044, một năm 12,528 làm tròn gần 12,500; negative equity 28,000 − 23,000 = 5,000; xe thay 30,000 + nợ cũ 5,000 = 35,000 trước thuế/phí và tùy lender; giảm chi 200/tháng tương đương 2,400/năm. Không cộng depreciation vào toàn bộ payment rồi gọi là cash spending.

Tiếp theo: người dùng làm giọng đọc từ script và tải bản gốc vào `videos/003-car-payment-trap/audio/` (gợi ý `car-payment-trap-voiceover.wav`). Sau khi nhận, căn toàn bộ video và chuyển động theo WAV, tạo review/MP4 tên mới; lưu bảng hình cũ. Nếu đã chỉnh trong Studio, nhận `.credit.json`/JSON trước khi tiếp tục từ sửa riêng đó. Khi có bản narrated review thật, thêm quy tắc nâng cấp riêng finance-003 từ revision bảng hình, dùng giao dịch archive draft cũ trước khi đổi main; chưa thêm quy tắc này lúc chưa có review. R2/CORS/manifest không thay đổi.

Trước khi thu âm video 003, đã sửa một câu chuyển thời gian ở phần 04 từ “A couple of years pass” thành “Some time passes”. Lý do: $28,000 là số dư giả định cho ví dụ negative equity, không phải số dư chính xác sau 24 kỳ của khoản vay $35,000 / APR 8% / 72 tháng ở phần trước. Giữ nguyên các con số và toàn bộ hình; đã thông báo thay đổi cho người dùng.

## Video 003 — bản duyệt đầy đủ theo WAV (2026-10-22)

Đã nhận `audio/tts_20261022_115123_7124d9.wav` từ commit người dùng `b90cae5`: **522,2 giây**, PCM 16-bit / 24 kHz / mono. SHA-256 `e0d47280389d7f6592b3bd6bed5f1b41389b29088da07c14522ac13258888938`. WAV giữ nguyên byte. `review/voiceover.mp3` là dẫn xuất chuẩn hóa âm lượng, không đổi tốc độ hoặc cắt lời; không thêm nhạc nền.

Bản dựng mới **98 cảnh / 8 phút 42,2 giây**, chỉnh được ở `videos/003-car-payment-trap/review/project.json`, revision `car-payment-review-v01`; MP4 `exports/full-review-v01.mp4`. Đây là bản duyệt chờ người dùng, chưa phải bản cuối. `review/README.md` có timecode, `shot-plan.json` có cue và bố cục, `source.json` có nguồn/hash, `alignment.json` có mốc từ. Đối chiếu trực tiếp 1.066/1.155 token của văn bản; các token số và dấu câu có nội suy. Có sai số căn tự động ở mức từ; phụ đề mặc định tắt trong MP4, bật được trong Studio.

- **27 lớp chuyển động nội dung trong 14 cảnh**, cùng các thẻ xuất hiện theo lời đọc: chi phí xe tăng 614→794→954→1.044 USD; thanh/số dùng cùng mốc và cùng thang 1.044 USD minh họa. Tổng chi phí là các đoạn thanh đúng tỉ lệ 614/180/160/90.
- Dư nợ tính bằng công thức khoản vay fixed-rate $35.000 / APR 8% / 72 tháng, lấy 25 mốc cách nhau 3 tháng. Lịch nén có nhãn rõ, counter/thanh cùng nhịp step; không dùng số dư $28.000 của ví dụ trade-in để suy ra đường dư nợ này.
- Phong bì nợ $5.000 đi từ xe cũ sang khoản vay mới; tổng tài trợ tăng $30.000→$35.000, có ghi điều kiện lender và trước tax/fees. Quỹ khoảng thở tăng 12 lần $200 = $2.400/năm.
- Audio thực tế vẫn dùng câu cũ **“A couple of years pass”** ở khoảng 03:18,84, khác script đã sửa trước. Giữ nguyên WAV và lời đọc; header/ghi chú trên hình xác định trade-in là **ví dụ giả định riêng**, không phải số dư chính xác sau hai năm của khoản vay 72 tháng trước đó. Văn bản dùng căn audio ở `review/narration.md`; không đổi lại phần tiếng Anh trong script dự định.
- Times New Roman thực, vùng tiêu đề tách khỏi nhân vật; hình/nhãn căn giữa. Giữ trọn đầu, tay, chân ở các khung chuyển động. Hình minh họa tổng thể vẫn là lớp ảnh; chưa rig khớp nhân vật.

`projects.json` giữ ID finance-003, nay trỏ review/audio/MP4 thật. Quy tắc nâng cấp riêng car-artwork-board-v01→car-payment-review-v01 dùng giao dịch archive draft cũ trước khi thay main. Bảng hình 96 giây đã chỉnh tải JSON được và có trong `.credit.json`; reload giữ sửa review, không nhân đôi lịch sử. Không tự thay revision lạ, bản review đang chỉnh hay dự án khôi phục ID khác. Cập nhật query hub/editor/store/iframe để tránh mở lại bản 96 giây từ cache.

Bản này dựng từ tài nguyên repo, chưa ghép các sửa riêng chỉ có trong IndexedDB. Bảng hình 96 giây, 16 thiết kế/ảnh, sheet/PNG rời và source WAV giữ nguyên. Đối chiếu **254 tệp cũ không đổi byte**, gồm toàn bộ video 001/002, tài nguyên video 003 và kho chung 73 mục; metadata hai dự án cũ cũng không đổi. R2/CORS/manifest giữ nguyên.

Công cụ mới `tools/build-car-payment-video.py` đọc narration/alignment/tài nguyên để tạo review; mặc định chặn ghi đè. Chỉ dùng `--force` sau khi sao lưu sửa tay, không sửa WAV/MP4. Xuất MP4 bằng `tools/render-intro.cjs` với đầu vào review/project.json và tên xuất mới.

Đã qua **20 unit test** engine/financial motion/WebM/media. Playwright `car-payment-review`: **5.363 mốc hình**, kiểm tra biên, hình/chữ và chữ/chữ không chồng nhau, caption một dòng. `car-payment-upgrade`: archive/tải JSON/backup bảng hình đã sửa nguyên vẹn, giữ sửa review khi reload, tua/phát audio, mobile và Tổng quan mở 98 cảnh, loại trừ revision lạ/dự án khôi phục. `car-payment-artwork`: 16 thiết kế, 2 atlas, 12 cutout vẫn dùng được. `project-workspaces` giữ tách dự án/lịch sử/backup/khôi phục. Chrome xác nhận TimesNewRomanPS-BoldMT. Kết quả bản MP4 thực được ghi tại `review/validation.json`.

Tiếp theo: người dùng duyệt MP4 v01 và góp ý kèm timecode. Nếu đã chỉnh riêng trong Studio, nhận `.credit.json`/JSON trước khi tiếp tục từ chúng. Lần xuất sau dùng tên v02, giữ v01 và WAV gốc.

MP4 thực đã giải mã toàn bộ không lỗi: H.264/AAC, 1920×1080 / 30 fps, 15,666 khung, 522.2 giây. Âm lượng đo -16.67 LUFS, true peak -1.45 dBTP. Đối chiếu tiếng ở giây 10/250/515: độ trễ 0 mẫu, tương quan trung vị cửa sổ 50 ms >0,995; chi tiết trong review/validation.json. Kiểm tra ngay trên MP4 thấy thanh bảo hiểm tăng từ 710 lên 912 pixel, khớp mức cuối 794/1.044 × 1.200 pixel; đã xem khung bảng tiết kiệm trong bản xuất.
