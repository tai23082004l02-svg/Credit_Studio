# Bàn giao nhanh Credit Studio

## Video 007 — ảnh nguyên cảnh, chỉ bàn giao bản dựng chỉnh được (2026-10-23)

Theo mẫu `1023.mp4` và trao đổi hiện tại, người dùng chọn cách làm **mỗi cảnh một ảnh minh họa hoàn chỉnh** gồm nhân vật/bối cảnh/đạo cụ, thay ảnh theo ý lời đọc và pan nhẹ. Không tách tay/chân/đồ vật hoặc tiếp tục bố cục thẻ thông tin cũ. Chữ/số quan trọng để riêng trong Studio, Times New Roman. Tạo số cảnh theo audio, không áp bộ16ảnh. Quyết định này thay hướng hình ảnh mặc định trước đó, giữ mọi bản cũ.

Video mới **Your Raise Disappeared Before Payday**, `finance-007`, thư mục `videos/007-raise-disappeared/`: **12 cảnh /55,475 giây**, revision `raise-whole-scene-v01`, `review/project.json`. Nhận WAV `tts_20261023_141853_9b1922.wav`, **2.662.844 byte**, 24kHz mono, SHA256 `df8191cc53dd711304beafb890f76bde0543085a792597daa69bc8d51c4e7bd9`, giữ nguyên nguồn. MP3 dẫn xuất loudnorm; không đổi tốc độ. **Người dùng chỉ yêu cầu bản dựng chỉnh được, không cần MP4; không tạo MP4 hoặc thêm review MP4 vào registry.**

12ảnh nguyên cảnh được tạo từ ba sheet AI với cùng nhân vật áo xanh; giữ nguồn và tọa độ crop toàn cảnh, không phải bộ phận nhân vật. Cận cảnh/cắt người có chủ ý trong nguồn được giữ; Studio fit toàn bộ ảnh và pan trong canvas, không crop thêm. Header native Times New Roman;17cue EN tùy chọn mặc định tắt. Tình huống giả định: tăng thực nhận300/tháng; phone30 +gym50 +delivery100 =180, phần còn120 cho các khoản còn lại, không gán chi phí từng món chưa nêu.

17media mới được upload và full S3 hash/Range/CORS verify ở Actions run39917767103, sau đó chat kiểm tra public full SHA256/Range/CORS trước khi append manifest. Không thay mapping cũ/sáu pin, không commit binary archive hoặc sửa dự án khác. Bản backup tự chứa ảnh/MP3/WAV gốc được kiểm tra khôi phục thành ID riêng; bản sửa browser vẫn ở IndexedDB. Xem review/validation.json và media-validation.json để biết kiểm tra thực tế. Không coi video là đã được duyệt cuối.


Cập nhật **2026-10-23**, múi giờ Asia/Saigon. Đây là trạng thái hiện tại; ghi chú lịch sử trong PROJECT_HANDOFF.md có thể mô tả các bước chưa hoàn thành ở thời điểm cũ.


## Video006 — hình và MP4 v01 hoàn chỉnh (2026-10-23)

Đã hoàn thành yêu cầu làm toàn bộ hình theo audio và bản duyệt đầy đủ **55 cảnh /535,525 giây**, revision **musk-scenic-review-v01**, IDfinance-006.7 scenic backgrounds AI,4 Musk cutouts,1 native outlinePortugal mainland,13 khung PNG từ cùng timeline; không thêm thiết kế JSON trùng. Musk chỉ là đối tượng được nói đến, giọng kể ngoài; cảnh theo nội dung, không nền trắng/giấy kem xuyên suốt, Times New Roman native.14 lớp motion nội dung trong11 clip,55 background pans và timed reveals, không nhạc/lip-sync.

MP4 mới `exports/full-review-v01.mp4`: H.264/AAC1920×1080/30fps, **16066 khung /535.533333 giây**, full decode qua; **-16.86LUFS /-1.67dBTP**, tiếng ở10/250/528s lệch0 mẫu và tương quan50ms>0,995 với WAV gốc. Gallery online đã qua26ảnhR2, tảiPNGhash, mở đúngclip, giữ sửa/reload/backup và mobile. MP4 trên R2 đã qua browser tua/phát bảy mốc, editor/audio/canvas và WAV gốc; sáu dự án/five galleries qua regression. Đã sửa cache CORS khi mở gallery sau cover trang chủ, tảiPNG và backup vẫn qua. Kiểm tra lại website sau deploy; kết quả tại review/validation.json và images/validation.json.

Media mới full SHA-256 authenticated và public/Range/CORS verified qua Actions runs39913454802 (nguồn/audio/cutout),39914179416 (13preview) và39915797680 (MP4). Manifest hiện **237 entry**; toàn bộ208 mapping/sáu pin trước episode không đổi. Không commit binary mới, không đưa archive trở lại main hoặc viết lại lịch sử. WAV gốc SHA`c26b2cd58cb7b9f7cd9dce14954c7668eabb699145499bb46125f6c8a93e45c5`, script/narration/data-snapshot1115 từ,5 dự án cũ/catalog93 giữ nguyên.

Giữ nguyên mốc936B snapshot2026-10-01/GDP2025~346.64B/population2025; GDP không phải wealth/budget/country price. Model108B/round là giả định biên tập all-cash/no-tax/no-return…,8round đủ và72B còn lại, không gán cho chương trình thật của Musk/chính phủ. ASR1068/1115 direct token matches,149cue EN defaultoff, timing không phải duyệt thủ công từng từ.

User có thể xem hình/Studio/MP4 và góp ý nếu muốn; không cần duyệt hình trung gian. Muốn tiếp tục từ sửa IndexedDB phải nhận backup; dùng version mới cho lần xuất tiếp, giữ v01. Các ghi chú “MP4 đang xuất” bên dưới là bước ảnh trước khi hoàn tất bản này.

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

## Quy trình mới — trợ lý tự xử lý toàn bộ phần hình và dựng (2026-10-23)

Người dùng đã chốt áp dụng [PRODUCTION_WORKFLOW.md](PRODUCTION_WORKFLOW.md): cùng chọn chủ đề; trợ lý kiểm tra và gửi kịch bản/lời đọc tiếng Anh Mỹ để người dùng tạo audio; nhận audio gốc rồi tự chọn phong cách, làm hình/đạo cụ, bố cục, chuyển động, dựng, kiểm tra và bàn giao MP4 cùng bản chỉnh được trên Studio. **Không dừng chờ duyệt storyboard, phong cách, 2–3 cảnh mẫu hoặc từng hình.** Storyboard/thử cảnh chỉ dùng nội bộ khi hữu ích; không bắt buộc tạo mẫu. Thành phẩm vẫn có thể nhận góp ý sau.

Quyết định này thay vòng duyệt hình trung gian của quy trình cũ bên dưới; giữ Times New Roman, kiểm tra chất lượng/số liệu/crop/audio, WAV gốc, JSON, bản xuất, IndexedDB/backup và R2. Không tự coi các video cũ là đã được duyệt cuối, không tự đăng lên YouTube. Ước tính giảm20–35% thời gian sản xuất (tham khảo30%), hoặc40–60% tổng thời gian gồm chờ duyệt; chưa có số đo thực tế/cam kết. Lần cập nhật này chỉ đổi tài liệu/quy trình, không sửa video hoặc dữ liệu dự án.

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

Đăng ký **finance-005** trỏ bản mẫu thật; mô tả/trạng thái ghi rõ **phong cách đã duyệt, chưa phải video đầy đủ**. Chưa khai báo WAV/MP4 public không tồn tại. Bốn dự án cũ, kho89 mục, mọi source/export cũ và R2 manifest giữ nguyên. Chưa có full review/MP4 566,45 giây; chưa chốt thời điểm/cảnh toàn bộ hoặc bổ sung nhạc.

Builder `tools/build-mortgage-samples.cjs` nhận MP3 đã chuẩn hóa, script-timing và thư mục scratch; từ chối ghi đè project đã có. Người dùng đã duyệt phong cách; có thể tạo thêm tài nguyên/dựng toàn bộ mà không hỏi duyệt lại phong cách hoặc kịch bản. Khi chuyển finance-005 sang bản đầy đủ, bảo toàn mọi draft người dùng bằng backup/archive, không reset mẫu đã chỉnh.

Kiểm tra: validate engine, 869 mốc hình, font Chrome thực TimesNewRomanPS-BoldMT, phát audio/reload/mobile. Báo cáo `samples/validation.json`; đã xuất và decode MP4 thử cục bộ trong work (không xuất/publish full video). Sau khi sửa bố cục để tiền không che mái nhà, browser được kiểm tra lại. Các bước kiểm tra không truy cập IndexedDB trình duyệt của người dùng.


## Quy trình sản xuất đã chốt — 2026-10-23

Áp dụng cho sản xuất mới; không xóa hay thay các tài nguyên và bản dựng cũ.

- Người dùng đã duyệt bỏ bước làm sẵn bộ 16 ảnh hoàn chỉnh trước khi có audio. Trình tự: chốt kịch bản/nguồn/phép tính → nhận giọng đọc; trong lúc chờ có thể lập storyboard ngắn và thử 2–3 cảnh mẫu để duyệt phong cách → chia cảnh theo audio thật → tạo hình và các lớp cần thiết, dựng chuyển động trực tiếp trong Studio → kiểm tra và xuất bản duyệt. Không áp số lượng 16 ảnh cố định. Chỉ tạo minh họa nguyên khung hoặc thiết kế ảnh hoàn chỉnh khi thực sự dùng trong video, thumbnail hay mục đích độc lập; không giảm chất lượng hình hoặc bỏ storyboard nội dung. Giữ nguyên toàn bộ bộ hình/bản dựng cũ.
- Bỏ bước tạo bảng duyệt hình im lặng 96 giây. Dựng sơ bộ theo audio thật trong Studio khi có giọng đọc; storyboard nội dung vẫn dùng để lập kế hoạch.
- Tạo đạo cụ theo nhu cầu cảnh, dùng lại kho chung. Sheet dùng khi cần nhiều đạo cụ đồng bộ, không tạo rồi cắt mọi món không cần thiết. Khi dùng sheet, bố trí ô và khoảng đệm an toàn; kiểm tra từng PNG sau cắt ở kích thước gốc và trong cảnh, giữ đủ góc, cạnh, đầu/tay/chân, không lẹm hình hoặc dính ô bên cạnh. Giữ nguồn và tọa độ cắt.
- Bỏ xuất MP4 đầy đủ sau mỗi chỉnh sửa nhỏ. Duyệt trong Studio hoặc xuất đoạn thay đổi; xuất toàn bộ ở mốc duyệt bản dựng sau kiểm tra.
- Bỏ duy trì nhiều bản thiết kế trùng nội dung. Dùng một bản dựng chính chỉnh được; chỉ tạo thiết kế ảnh riêng khi có mục đích sử dụng độc lập. Quy tắc này không cho phép xóa lịch sử, JSON, bản xuất hay bản sao lưu cũ.
- Không dùng Runway trong quy trình hiện tại; ưu tiên đồ họa động có thể chỉnh trong Credit Studio, đồng bộ lời đọc và số liệu, Times New Roman.


## Repo và website

- Repo: `tai23082004l02-svg/Credit_Studio`, nhánh `main`, hiện **Public**.
- Website: https://tai23082004l02-svg.github.io/Credit_Studio/
- Người dùng đã bật lại Pages sau lần đổi Private → Public. Đã kiểm tra API Pages `built`, nguồn `main /`; trang chủ và manifest online trả **HTTP 200**, manifest **enabled:true**. Không tiếp tục báo website 404 theo ghi chú cũ.
- Không đổi visibility, hosting hoặc viết lại lịch sử Git nếu không có yêu cầu mới.

## Mục tiêu và phối hợp

- Làm video YouTube tài chính bằng tiếng Anh cho khán giả Mỹ; trao đổi với người dùng bằng **tiếng Việt**.
- Người dùng chuẩn bị giọng đọc; trợ lý chuẩn bị hình, storyboard, chuyển động, dựng và xuất bản duyệt.
- Đưa bản dựng chỉnh được vào Studio để người dùng sửa trước khi chốt. Trang chủ quản lý nhiều dự án; không xây trang riêng rời luồng Studio.
- **Times New Roman** xuyên suốt. Căn giữa hình/nhãn thẻ đạo cụ, giữ khoảng đệm cân đối. Kiểm tra đầu/tay/chân không bị cắt hoặc chữ/nền che.
- Tăng chuyển động có ý nghĩa: thanh tiền, số tiền, lịch và trạng thái phải đồng bộ; không chỉ fade/slide ảnh.

## Bốn video đang có

| ID / thư mục dưới videos/ | Dự án đầy đủ hiện tại | Thời lượng / số cảnh | Phong cách |
| --- | --- | --- | --- |
| finance-001 / 001-100k-salary | review-v03/project.json; salary-motion-v03 | 486,75 giây / 88 | Nhân vật Alex, nét vẽ 2D |
| finance-002 / 002-monthly-payment-trap | review/project.json; monthly-payment-review-v01 | 495,475 giây / 79 | Nét vẽ 2D |
| finance-003 / 003-car-payment-trap | review/project.json; car-payment-review-v01 | 522,2 giây / 98 | Nét vẽ 2D |
| finance-004 / 004-living-alone | review/project.json; living-alone-review-v01 | 577,5 giây / 91 | Ảnh cắt ghép tài liệu, giấy kem, đỏ trầm |

Tên video 004: **Why Living Alone Has Become So Expensive**. Hiện là dự án mới nhất, có 29 lớp chuyển động nội dung trong 15 cảnh; giữ 16 thiết kế, hai atlas và 16 đạo cụ collage. Không ép phong cách Alex cũ vào dự án này. Cả các bản duyệt chưa được xác nhận là bản xuất cuối; chưa thêm nhạc nền hoặc rig chuyển động khớp.

Video 001: intro 40,5 giây là bản thử cũ, không phải bản đầy đủ. Lỗi nền tiêu đề che tóc ở “PLAN AROUND WHAT ARRIVES” còn trong MP4 v01 được bảo tồn, đã sửa từ review v02. Giữ review v01/v02/v03 và các bản xuất cũ. Video 002–004 giữ các bảng hình 96 giây trước khi có audio ở storyboard/project.json; không mở nhầm chúng làm bản dựng mới nhất.

Kho chung: **93 mục = 75 đạo cụ + 14 tư thế Alex + 4 nhóm Jamie**. Có thay đạo cụ trong trình dựng, giữ vị trí, khung kích thước, thời gian và hiệu ứng; timeline, audio, undo/redo, xuất WebM.

## Phụ đề tiếng Việt

- Video 004 có **155 cue tiếng Anh và bản dịch Việt**; chọn Tiếng Việt cạnh checkbox Phụ đề trong trình dựng. Ngôn ngữ được lưu, dùng cho preview và WebM.
- Giữ nguyên lời tiếng Anh và thời gian. textVi là trường bổ sung, captionLanguage là en/vi; dự án cũ mặc định tiếng Anh.
- captions.vi.json chỉ ghép vào draft khi revision và toàn bộ start/end/text tiếng Anh khớp; giữ sửa riêng, bản dịch riêng và timeline. Không thay cả dự án bằng bản repo.
- MP4 gốc chưa render lại để đốt phụ đề Việt. Các video khác chưa được dịch đầy đủ.

## R2 và dung lượng sau dọn

- Bucket `credit-studio`; cấu hình nguồn: **storage/manifest.json**. Giữ đường dẫn logic trong JSON; mediaURL chọn R2 hoặc ảnh local được giữ.
- Đủ **204 file / 629.217.384 byte** đã chép, tải lại và đối chiếu SHA-256 trên R2. Chứng cứ: Actions run **39889738423**; chi tiết storage/migration-report.json.
- Đã gỡ khỏi main **198 file / 620.325.763 byte**: 180 PNG, 4 WAV, 6 MP3, 8 MP4. Tất cả bản gốc và bản xuất vẫn ở R2.
- Giữ **6 PNG / 8.891.621 byte** trên GitHub, entry **local:true**, vì public GET R2 timeout dù bản S3 đúng hash. Danh sách ở storage/README.md; không tự xóa hoặc bỏ pin. plan/sync phải giữ pin và các entry đã archive.
- Cây tệp sau dọn khoảng **140,6 MB**, trước dọn 760,88 MB. **Lịch sử Git vẫn chứa media cũ**, nên dung lượng toàn bộ repo và clone không giảm tương ứng. Chưa force-push/viết lại lịch sử. Hai repo khác chưa được dọn.
- CORS đã được người dùng lưu thủ công; GET/HEAD và Range cho origin Pages, localhost:8000, 127.0.0.1:8000/8002. Không yêu cầu quyền quản trị bucket chỉ để upload file.
- R2 đang phục vụ file công khai; đọc bằng URL không cần khóa. Quản lý file cần xác thực.

## Khóa API và quyền truy cập

- Không đặt khóa trong repo, HTML/JS, JSON dự án, log hoặc chat. Repo và website đang công khai. GitHub Secrets và biến bí mật môi trường cloud là hai nguồn cấu hình riêng.
- Actions dùng R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL, R2_BUCKET. Workflow r2-diagnostic.yml kiểm tra chỉ đọc; r2-sync.yml copy không ghi đè sai hash và tải lại xác minh toàn bộ.
- Actions đã xác thực đọc được R2 và đã upload thành công. Môi trường chat từng trả 401 dù Actions hoạt động; chat mới phải kiểm tra lại quyền thực tế, không vội kết luận khóa Actions hỏng.
- Quyền liệt kê Actions Secrets/Variables và sửa Pages bằng kết nối trợ lý từng bị 403. Không hiển thị giá trị khóa, không yêu cầu gửi khóa vào chat. Token cũ từng lộ trong Git được người dùng báo đã thu hồi; không khôi phục hoặc dùng khóa trong lịch sử.

## Tiếp tục chỉnh và dựng

1. Đọc AGENTS.md, README.md, tài liệu này; xem PROJECT_HANDOFF.md và docs/R2_SETUP.md khi cần chi tiết. Kiểm tra trạng thái main hiện tại trước khi sửa.
2. Trước khi sửa video cụ thể, đọc README/script/storyboard/review notes của video đó. Không tự chọn chủ đề hoặc đổi nội dung khi chưa có yêu cầu.
3. **Bản sửa của người dùng nằm trong IndexedDB**, không tự lên GitHub hoặc R2. Nếu cần tiếp tục từ sửa riêng, nhận **Sao lưu dự án .credit.json** hoặc JSON trước. Không reset draft bằng bản repo, không đổi revision chỉ để cập nhật tài nguyên.
4. WAV/PNG/MP3/MP4 được archive không còn sẵn trong clone. Trước khi chạy builder hoặc test cần filesystem: `python3 tools/restore-media.py videos/004-living-alone/` (đổi thư mục theo video); dùng `--all` khi thật sự cần tất cả. Restore kiểm tra SHA-256, từ chối ghi đè nội dung khác, các đường dẫn cũ được gitignore.
5. Không commit lại media đã archive hoặc /work/. Khi có tài nguyên mới, copy/verify R2 và cập nhật manifest trước khi bỏ bản Git. Giữ các JSON chỉnh sửa, nguồn, lời thoại và báo cáo kiểm tra.
6. Nhận góp ý kèm timecode, chỉnh bản đầy đủ; kiểm tra bố cục, nhân vật, audio, phép tính và cue. Xuất tên phiên bản mới, không ghi đè bản cũ. Cập nhật bàn giao sau thay đổi đáng kể.

## Kiểm tra đã qua và việc còn chờ

Sau khi gỡ file local đã qua: **19 unit tests** engine/motion/WebM/media/caption; real R2 integration cho 4 editor/audio/MP4, 4 gallery, 89 đạo cụ, PNG download/canvas export; chỉ sáu ảnh pin được tải từ origin Studio. Vietnamese-caption editor qua: giữ draft đã sửa, EN/VI, reload/backup, mobile, WebM thật có audio, legacy/offline. Restore mẫu đúng hash, plan không làm mất entry archive. Các JSON/nguồn lời và subtitle có sẵn giữ nguyên byte khi di chuyển.

Chạy website cục bộ bằng `python3 -m http.server 8000 --bind 127.0.0.1`. Test R2 thật: `node tests/r2-live.cjs`; test phụ đề/backup/WebM: `node tests/vietnamese-captions-editor.cjs`. Các test đọc ảnh/WAV cục bộ cần restore trước. Chỉ kiểm tra phù hợp thay đổi, không render lại MP4 khi chỉ sửa tài liệu.

**Chờ người dùng:** góp ý/video tiếp theo; nếu sửa bản người dùng đã chỉnh, cần backup. Không còn bước CORS/khôi phục Pages đang chờ. Chưa có yêu cầu mới về chủ đề, video hay viết lại Git history.
