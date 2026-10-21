# Credit Studio

Không gian quản lý dự án video và thiết kế ảnh với giao diện tiếng Việt. Không cần tài khoản, API hay cài thư viện.

## Tiếp tục ở phiên chat mới

Chọn repo này trong chat mới rồi yêu cầu đọc [AGENTS.md](AGENTS.md) và [bản bàn giao dự án](docs/PROJECT_HANDOFF.md). Tài liệu ghi các quyết định đã chốt, vị trí tài nguyên, tiến độ thực tế và phần còn lại. Chat mới không tự nhớ lịch sử chat; các bản sửa chỉ lưu trong trình duyệt cần **Sao lưu dự án** và cung cấp tệp nếu muốn trợ lý tiếp tục từ chúng.

## Dùng online

Địa chỉ website: https://tai23082004l02-svg.github.io/Credit_Studio/

Website được triển khai bằng GitHub Pages từ thư mục gốc của nhánh `main`.
Sau khi commit và push thay đổi lên `main`, GitHub Pages sẽ cập nhật website.
Địa chỉ chính mở trang **Dự án của bạn**. Tạo dự án mới hoặc chọn dự án hiện có, rồi chuyển giữa **Tổng quan**, **Dựng video**, **Hình ảnh**, **Âm thanh & tài liệu** trên cùng trang. `/video/` và `/design/` là các công cụ bên trong, vẫn mở riêng được nếu cần; không cần nhớ các đường dẫn này để sử dụng.

[Mở dự án tài chính hiện tại](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-001). Có bản duyệt đầy đủ 8 phút 06,75 giây (64 cảnh), 16 cảnh ảnh, audio và lời thoại. [Hướng dẫn và giới hạn bản dựng](videos/001-100k-salary/README.md#bản-duyệt-đầy-đủ).

## Quản lý và lưu dự án

- **Tạo dự án**: bắt đầu video mới (một cảnh trắng, chưa có giọng đọc) hoặc thiết kế ảnh.
- Mỗi dự án giữ bản dựng video, thiết kế tự do, từng cảnh đã sửa và tệp đính kèm riêng. Có thể tìm theo tên và lọc Video/Thiết kế ảnh.
- Trong **Hình ảnh**, chọn **Chỉnh cảnh trong dự án** để sửa một cảnh có sẵn; không cần tải JSON qua lại.
- Trong **Âm thanh & tài liệu**, thêm ảnh, audio hoặc TXT/MD, tối đa 25 MiB/tệp. Có thể dùng audio làm giọng đọc, thêm PNG/JPEG/WebP vào video hoặc mở ảnh để thiết kế.
- **Sao lưu dự án** tải một tệp `.credit.json` gồm các bản sửa và tệp mới đã thêm. **Mở bản sao lưu** khôi phục thành một dự án riêng, không ghi đè dự án hiện có. Cũng nhận JSON riêng từ trình ảnh hoặc video.
- Dự án mới và các bản sửa được lưu trong trình duyệt hiện tại bằng IndexedDB; không tự đồng bộ sang máy khác hoặc GitHub. Tài nguyên đã xuất bản vẫn lấy từ website. Sao lưu để chuyển máy, bảo vệ khi xóa dữ liệu trình duyệt hoặc gửi bản sửa lại.
- Dữ liệu của hai trình chỉnh cũ được chuyển sang từng dự án một lần; các khóa localStorage cũ được giữ nguyên để bảo toàn dữ liệu.

Để xuất bản dự án tiếp theo cho mọi thiết bị, thêm tài nguyên vào thư mục riêng trong `videos/` và đăng ký trong `projects.json`. Giữ `id` dự án ổn định. Trang chủ tự hiển thị các mục đã đăng ký. Riêng dự án tài chính đầu tiên, bản intro v01 cũ được lưu vào **Bản lưu trước cập nhật** rồi chuyển sang bản đầy đủ. Bản lưu cũ có trong Sao lưu dự án và tải JSON riêng được; các sửa đổi trên bản đầy đủ được giữ khi mở lại. Những bản khác vẫn được giữ và hiện thông báo khi có bản xuất bản khác.

## Bố trí thư mục

```text
index.html                         Trang quản lý dự án chung
projects.json                      Danh mục dự án đã xuất bản
assets/
  css/hub.css                      Giao diện quản lý dự án
  css/style.css                    Giao diện trình chỉnh sửa
  js/app.js                        Logic trình chỉnh sửa
  js/hub.js                        Điều hướng trang quản lý chung
  js/workspace-store.js             Lưu từng dự án và sao lưu/khôi phục
  samples/                         Ảnh tham khảo phong cách
design/                            Trình chỉnh ảnh, có thể nhúng vào dự án
video/                             Trình chỉnh video và bộ dựng canvas
tests/                             Kiểm tra timeline, xuất video và thao tác trình duyệt
tools/                             Đóng gói dự án và dựng MP4
videos/
  001-100k-salary/
    README.md                      Thông tin và tiến độ video đầu tiên
    script.md                      Lời thoại tiếng Anh, chia 8 đoạn
    audio/                         Tải giọng đọc MP3/WAV vào đây
    images/                        16 cảnh và 3 bảng tài nguyên
    projects/                      16 trang JSON chỉnh chữ trong Studio
    storyboard.md                  Phân cảnh và hướng chuyển động
    index.html                     Trang xem bộ hình
    intro/                         Bản mở đầu 40,5 giây được giữ lại
    review/                        Bản dựng đầy đủ, audio dẫn xuất và phụ đề
    exports/                       MP4 bản mở đầu và bản duyệt đầy đủ
```

Mỗi video tiếp theo sẽ có thư mục riêng dưới `videos/` để không lẫn tài nguyên.
Thư mục hình, dự án dựng và bản xuất sẽ được thêm vào từng video khi có các tệp đó.

[Xem bộ hình video đầu tiên](https://tai23082004l02-svg.github.io/Credit_Studio/videos/001-100k-salary/) · [Phân cảnh](videos/001-100k-salary/storyboard.md).

## Gửi âm thanh cho video đầu tiên

Mở [thư mục audio trên GitHub](https://github.com/tai23082004l02-svg/Credit_Studio/tree/main/videos/001-100k-salary/audio), chọn **Add file → Upload files**, tải tệp lên rồi chọn **Commit changes** vào nhánh `main`.

Xem [hướng dẫn đặt tên và dung lượng](videos/001-100k-salary/audio/README.md). Thư mục này để bàn giao âm thanh; chưa tự nhập âm thanh vào trình chỉnh sửa.

## Chạy trên máy của bạn

Cài Python 3, mở terminal trong thư mục dự án rồi chạy:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Windows: `py -m http.server 8000 --bind 127.0.0.1`.

Mở **http://localhost:8000** trên chính máy chạy lệnh. Dừng bằng Ctrl+C.

## Tính năng

- Thêm chữ, hình chữ nhật, hình tròn và ảnh PNG/JPEG/WebP/GIF (tối đa 15 MB).
- Kéo phần tử để di chuyển; bảng bên phải chỉnh vị trí, kích thước, màu, chữ, độ hiển thị và thứ tự lớp.
- Hai mẫu có sẵn; trang trắng với kích thước tùy chọn (100–4096 px).
- Xuất PNG; lưu/mở dự án JSON để tiếp tục chỉnh sửa.
- Tự lưu trong trình duyệt khi bộ nhớ khả dụng. Lưu JSON để sao lưu lâu dài.
- Ctrl/Cmd+Z: hoàn tác; Ctrl/Cmd+Shift+Z: làm lại; Delete: xóa; phím mũi tên: di chuyển (Shift: 10 px).

Văn bản xuống dòng bằng Enter; kích thước hộp chữ là vùng chọn, nội dung không tự ngắt dòng theo chiều rộng. Ảnh GIF xuất PNG dưới dạng ảnh tĩnh. Ảnh được xử lý trong trình duyệt, không gửi lên máy chủ.

Trình chỉnh ảnh hỗ trợ một trang; trình chỉnh video hỗ trợ cảnh và các lớp chữ/ảnh/khối màu. Chưa có cộng tác, chỉnh ảnh nâng cao, chuyển động khớp nhân vật hoặc đầy đủ tính năng Canva. Localhost của môi trường đám mây khác với localhost của máy cá nhân: tải/clone dự án về máy trước để chạy tại đó.

## Kiểm tra cú pháp

```sh
node --check assets/js/app.js
node --check assets/js/hub.js
node --test tests/video-engine.mjs tests/video-webm.mjs
```

Kiểm tra trình duyệt (cần Playwright + Chromium và FFmpeg, máy chủ cục bộ đang chạy):

```sh
node tests/video-editor.cjs
node tests/project-workspaces.cjs
```

## Dựng MP4 từ dự án video

Website chạy không cần thư viện. Công cụ dựng MP4 cục bộ cần Node.js, Playwright 1.62.1 với Chromium và FFmpeg có libx264/AAC. Công cụ dùng chung bộ vẽ với phần xem trước để giữ hình và thời điểm giống nhau.

Sau khi khởi động máy chủ cục bộ theo hướng dẫn phía trên:

```sh
node tools/render-intro.cjs videos/001-100k-salary/intro/project.json /tmp/intro-review.mp4
```

Có thể thay đối số đầu bằng JSON đã lưu từ trình chỉnh video. Không ghi đè tệp xuất cũ trừ khi chọn đường dẫn mới hoặc đặt `CREDIT_STUDIO_OVERWRITE=1`. Đặt `CREDIT_STUDIO_URL` nếu máy chủ dùng địa chỉ khác. Chạy `python3 tools/build-intro-project.py` chỉ khi muốn tạo lại dự án mở đầu từ cấu hình trong công cụ; lệnh sẽ thay thế `intro/project.json` và `intro/captions.vtt`.

Font hiện dùng là Times New Roman cho chữ và phụ đề. Khi dựng MP4 cần có font này trên máy; kiểm tra bằng `fc-match 'Times New Roman'` trên Linux. Trong môi trường đám mây đã chuẩn bị font tại `/workspace/shared/credit-studio-fonts`; dùng tiền tố `FONTCONFIG_FILE=/workspace/shared/credit-studio-fonts/fonts.conf` khi chạy lệnh dựng. Website dùng Times New Roman cục bộ và font serif dự phòng nếu thiết bị thiếu font.
