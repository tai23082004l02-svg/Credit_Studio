# Bàn giao nhanh Credit Studio

Cập nhật **2026-10-23**, múi giờ Asia/Saigon. Đây là trạng thái hiện tại; ghi chú lịch sử trong PROJECT_HANDOFF.md có thể mô tả các bước chưa hoàn thành ở thời điểm cũ.



## Video 005 — kịch bản Mortgage Payment v01 đã duyệt (2026-10-23)

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

Kho chung: **89 mục = 75 đạo cụ + 14 tư thế Alex**. Có thay đạo cụ trong trình dựng, giữ vị trí, khung kích thước, thời gian và hiệu ứng; timeline, audio, undo/redo, xuất WebM.

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
