# Bàn giao nhanh Credit Studio

Cập nhật **2026-10-23**, múi giờ Asia/Saigon. Đây là trạng thái hiện tại; ghi chú lịch sử trong PROJECT_HANDOFF.md có thể mô tả các bước chưa hoàn thành ở thời điểm cũ.




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
