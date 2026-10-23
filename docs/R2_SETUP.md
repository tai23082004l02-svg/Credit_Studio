# Kết nối kho tài nguyên R2

## Media mới từ môi trường chat — 2026-10-23

Credential của chat vẫn trả401, nhưng credential GitHub Actions đọc/ghi hoạt động. WAV gốc và MP3 full video005 đã được chuyển, tải lại xác minh full SHA-256 qua S3 trong [run39902713876](https://github.com/tai23082004l02-svg/Credit_Studio/actions/runs/39902713876); tiếp tục kiểm tra public full hash, Range206 và CORS độc lập trong chat. Không còn cần người dùng gửi lại audio hoặc khóa.

Khi upload release bị401, dùng `tools/stage-video-media.py work/media-map.json`: map v1 gồm assets/path/filename/size/sha256; tạo Git blob tạm theo chunk8MiB, **không tạo tree/commit/branch chứa media**. Chạy workflow `r2-staged-media.yml` với map_blob SHA. Worker tải/ghép bytes, kiểm tra hash, PUT object content-addressed nếu thiếu, không ghi đè object khác metadata; tải lại toàn bộ qua S3 và kiểm tra public Range/CORS. Sau run success, kiểm tra public full SHA-256 trước khi thêm manifest. Chỉ dùng cho media mới được phép xuất bản, không chép lại media archive cũ.

Map/blob cache local nằm trong work/media-staging/, không chứa credential. Không dùng Actions artifact download trong môi trường hiện tại: redirect Azure trả403; trạng thái run và public hash là bằng chứng kiểm tra. Không in signed URL, token hoặc body lỗi. Giữ sáu local:true cũ và toàn bộ mapping cũ; file mới được ignore trước khi commit. Các ghi chú401/pending ở phần lịch sử bên dưới mô tả thời điểm trước khi dùng Actions này.

## Trạng thái mới nhất — 2026-10-23: đã dọn main

Người dùng đã lưu CORS trong giao diện Cloudflare. GET Range trả 206 và Access-Control-Allow-Origin chính xác cho Pages và localhost. **Manifest enabled:true**. Có sáu PNG public GET timeout dù bản sao S3 đã được kiểm tra đúng byte; giữ các bản này trong GitHub, đánh dấu `local:true` và resolver dùng nguồn cùng origin. Không tự chuyển các pin này sang R2 khi plan/sync lại.

Đã gỡ **198 media / 620.325.763 byte** khỏi main: 180 PNG, 4 WAV gốc, 6 MP3, 8 MP4. Giữ 6 PNG / 8.891.621 byte. Đủ 204 bản trên R2 đã qua tải lại SHA-256 qua [Actions run 39889738423](https://github.com/tai23082004l02-svg/Credit_Studio/actions/runs/39889738423). Khi đó copy/verify qua, CORS API bị 403; CORS nay đã được lưu thủ công. Workflow sync bỏ bước sửa CORS để không yêu cầu quyền quản trị bucket.

**Kiểm tra sau khi gỡ file cục bộ:** `tests/r2-live.cjs` qua cả 4 editor/audio/MP4 và 4 gallery, đủ 89 đạo cụ, tải PNG, canvas export không bị taint. Mọi request media về origin Studio chỉ là sáu PNG được giữ; phần còn lại đọc R2 thật, không mock. Đã đọc đủ 180 PNG công khai và kiểm tra hash/CORS; sáu PNG timeout giữ lại. 18 WAV/MP3/MP4 đều trả Range 206/CORS đúng. `plan()` giữ nguyên đủ 204 entry sau khi source rời Git. Restore ảnh mẫu từ R2 đúng SHA-256; bản thử đã xóa. JSON/draft/revision không thay đổi. 19 unit tests và vietnamese-captions-editor qua sau khi gỡ source: WebM thật có audio, 155 cue EN/VI, giữ draft đã sửa, backup/reload, mobile, legacy và offline fallback.

Phục hồi file phục vụ builder/test: `python3 tools/restore-media.py videos/004-living-alone/` hoặc `--all`. Tệp khôi phục được ignore theo từng đường dẫn cũ. Không đổi SHA/byte bản gốc hoặc xóa object R2. [Danh mục](../storage/README.md). Khi thêm media mới, đăng ký và copy/verify trên R2 trước khi gỡ bản Git, giữ manifest đủ mapping; không chạy builder cần WAV/PNG trước khi restore. JSON thiết kế nhúng ảnh vẫn giữ vì là tài liệu chỉnh sửa.

Cây tệp main giảm khoảng 620 MB, lịch sử Git không được viết lại nên dung lượng repo Git phía GitHub chưa giảm tương ứng. Sau khi dọn, người dùng đã chuyển repo về Public và bật lại Pages main /. Đã kiểm tra Pages built, trang chủ và manifest online HTTP 200; R2 enabled:true.

## Chẩn đoán bằng GitHub Actions

Đã chạy ngày **2026-10-23**: [run 39889380000](https://github.com/tai23082004l02-svg/Credit_Studio/actions/runs/39889380000) **success**. ListObjectsV2 xác thực HTTP 200; đọc một phần object xác thực HTTP 206. Cấu hình Actions hoạt động, còn nguồn cấu hình môi trường chat hiện trả 401; chưa xác định nguyên nhân chênh lệch. Chưa thử ghi/xóa, chưa bật manifest hoặc xác minh CORS trong trình duyệt.

Workflow `.github/workflows/r2-diagnostic.yml` chạy thủ công tại **Actions → Diagnose R2 access → Run workflow**. Cấu hình **Settings → Secrets and variables → Actions**: secrets `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`, `R2_BUCKET` (hai mục cuối cũng nhận repository variables; bucket mặc định `credit-studio`). Biến trong môi trường chat không tự chuyển sang Actions. Không đưa khóa vào YAML hoặc log.

Tác vụ chỉ ListObjectsV2 và đọc tối đa 64 byte của một object; không ghi/xóa, không thay manifest hoặc dữ liệu Studio. Báo thiếu biến, lỗi định dạng, HTTP 401/403/404 hoặc lỗi mạng; không in khóa, endpoint, object key hay thông báo lỗi thô. Thành công chỉ xác nhận quyền đọc, chưa xác nhận quyền ghi.

## Trạng thái — 2026-10-21

Bucket `credit-studio` đã nhận **26 tệp / 128.215.675 byte**. Đã tải lại toàn bộ qua S3 và đối chiếu SHA-256 với bản gốc: tất cả khớp. Địa chỉ công khai: `https://pub-ae346874928c47ce9628da16abea661c.r2.dev/`.

**Chưa bật sử dụng R2 trên website:** đang chờ người dùng lưu CORS trong Cloudflare và kiểm tra thực tế bằng trình duyệt. `storage/manifest.json` hiện có `enabled: false`; Studio tiếp tục dùng GitHub Pages. Các tệp gốc chưa bị xóa nên dung lượng website GitHub chưa giảm. R2 lưu tài nguyên; bản sửa của người dùng vẫn nằm trong IndexedDB và cần Sao lưu dự án để bàn giao.

## Thông tin kết nối

Bốn biến môi trường trực tiếp của Codex: `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`, `R2_BUCKET`. Tệp mẫu [`.env.r2.example`](../.env.r2.example) không chứa khóa. Tệp riêng `/workspace/.credit-studio/r2.env` vẫn trống khóa và không phải nguồn kết nối hiện tại. Môi trường mới cần kiểm tra sự hiện diện của biến, không in giá trị.

`tools/r2-storage.py` dùng thư viện chuẩn Python và ký S3 SigV4, region `auto`. Ngoài cặp khóa S3, công cụ chấp nhận cặp token value/token ID đã được nhập trong môi trường: chuẩn hóa trong bộ nhớ theo [hướng dẫn Cloudflare](https://developers.cloudflare.com/r2/api/tokens/), Access Key ID = token ID, Secret Access Key = SHA-256(token value). **Không yêu cầu người dùng nhập lại khi cấu hình hiện tại hoạt động.**

Endpoint S3 là HTTPS do Cloudflare cấp, không thêm tên bucket vào cuối. Không đưa khóa vào repo, website, chat, log hoặc bản bàn giao. Token cũ từng xuất hiện trong lịch sử Git đã được người dùng thông báo thu hồi; đã xác nhận danh tính S3 mới khác danh tính bị lộ trước khi chép tài nguyên. Bản hiện tại của tệp mẫu đã được làm trống; lịch sử Git chưa viết lại.

## CORS còn cần hoàn tất

Cloudflare → R2 Object Storage → Overview → **credit-studio** → **Settings** → **CORS Policy** → Add/Edit. Dán cấu hình trong [`storage/cors.json`](../storage/cors.json); nếu đã có quy tắc khác, giữ chúng và thêm quy tắc Studio. Token hiện có quyền đọc/ghi object nhưng không sửa cấu hình CORS của bucket; không cần cấp token quản trị để làm bước này.

Sau khi Save, kiểm tra phản hồi có `Access-Control-Allow-Origin` cho origin website và máy chủ thử nghiệm. Lúc kiểm tra hiện tại, tải công khai với User-Agent trình duyệt và Range được HTTP 206 nhưng chưa có header CORS. Chưa coi đây là lỗi khóa. R2 có thể chặn User-Agent mặc định của urllib với mã 1010; kiểm tra công khai dùng User-Agent trình duyệt, không tắt xác minh TLS.

Chỉ bật `enabled: true` sau khi xác nhận tải ảnh, crop đạo cụ, canvas xuất PNG, phát/tua audio và MP4 trên R2 hoạt động. `r2.dev` phù hợp bước thử ban đầu; dùng tên miền riêng khi triển khai phục vụ thường xuyên.

## Công cụ và cách tiếp tục

```sh
python tools/r2-storage.py check
python tools/r2-storage.py plan
python tools/r2-storage.py sync
python tools/r2-storage.py verify
```

`check` tạo rồi xóa đúng tệp thử riêng; `sync` chép media được Git theo dõi và đăng ký vào manifest; không xóa tệp gốc. Object dùng tên theo SHA-256, có metadata hash và cache immutable. Dừng khi object đã có không khớp metadata, không ghi đè. Chỉ chạy `cors` nếu được cấp quyền phù hợp; cấu hình UI là đủ cho token hiện tại.

Đường dẫn trong JSON dự án vẫn tương đối và ổn định. `assets/js/media-storage.js` chỉ chuyển các tệp được đăng ký trong manifest sang R2 khi bật; JSON dự án và ảnh data URL giữ nguyên. Thiết kế ảnh cũ có thể vẫn nhúng PNG trong JSON. Không xóa nguồn hoặc bản xuất cũ chỉ vì đã chép sang R2.

Kiểm tra đã qua: đối chiếu 26 tệp S3; 10 unit test; kiểm tra trình duyệt R2 mô phỏng cho kho đạo cụ/trình dựng/audio/MP4/thư viện ảnh và xuất canvas; bộ kiểm tra dự án, sao lưu/khôi phục và mobile; trình dựng với audio, sửa cảnh, undo/redo và xuất WebM có âm thanh. Bước xuất WebM timeout ở lần đầu, đã chạy lại thành công. Kiểm tra CORS và trình duyệt với R2 thật còn chờ.
