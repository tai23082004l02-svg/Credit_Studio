# Kết nối kho tài nguyên R2

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
