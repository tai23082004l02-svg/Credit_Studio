# Credit Studio

Không gian quản lý dự án video và thiết kế ảnh với giao diện tiếng Việt. Không cần tài khoản, API hay cài thư viện.

## Tiếp tục ở phiên chat mới

Chọn repo này trong chat mới rồi yêu cầu đọc [AGENTS.md](AGENTS.md), [bàn giao nhanh hiện tại](docs/NEXT_CHAT.md) và [bản bàn giao chi tiết](docs/PROJECT_HANDOFF.md). Tài liệu ghi các quyết định đã chốt, vị trí tài nguyên, tiến độ thực tế và phần còn lại. Chat mới không tự nhớ lịch sử chat; các bản sửa chỉ lưu trong trình duyệt cần **Sao lưu dự án** và cung cấp tệp nếu muốn trợ lý tiếp tục từ chúng.

## Dùng online

Địa chỉ website: https://tai23082004l02-svg.github.io/Credit_Studio/

Website được triển khai bằng GitHub Pages từ thư mục gốc của nhánh `main`.
Sau khi commit và push thay đổi lên `main`, GitHub Pages sẽ cập nhật website.
Địa chỉ chính mở trang **Dự án của bạn**. Tạo dự án mới hoặc chọn dự án hiện có, rồi chuyển giữa **Tổng quan**, **Dựng video**, **Hình ảnh**, **Âm thanh & tài liệu** trên cùng trang. `/video/` và `/design/` là các công cụ bên trong, vẫn mở riêng được nếu cần; không cần nhớ các đường dẫn này để sử dụng.

[Mở dự án tài chính hiện tại](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-001). Có bản duyệt chuyển động v03 dài 8 phút 06,75 giây (88 cảnh), 20 thiết kế ảnh, audio và lời thoại. [Hướng dẫn và giới hạn bản dựng](videos/001-100k-salary/README.md#bản-duyệt-chuyển-động-v03-hiện-tại).

## Quản lý và lưu dự án

- **Tạo dự án**: bắt đầu video mới (một cảnh trắng, chưa có giọng đọc) hoặc thiết kế ảnh.
- Mỗi dự án giữ bản dựng video, thiết kế tự do, từng cảnh đã sửa và tệp đính kèm riêng. Có thể tìm theo tên và lọc Video/Thiết kế ảnh.
- Trong **Hình ảnh**, chọn **Chỉnh cảnh trong dự án** để sửa một cảnh có sẵn; không cần tải JSON qua lại.
- Trong **Âm thanh & tài liệu**, thêm ảnh, audio hoặc TXT/MD, tối đa 25 MiB/tệp. Có thể dùng audio làm giọng đọc, thêm PNG/JPEG/WebP vào video hoặc mở ảnh để thiết kế.
- **Sao lưu dự án** tải một tệp `.credit.json` gồm các bản sửa và tệp mới đã thêm. **Mở bản sao lưu** khôi phục thành một dự án riêng, không ghi đè dự án hiện có. Cũng nhận JSON riêng từ trình ảnh hoặc video.
- Dự án mới và các bản sửa được lưu trong trình duyệt hiện tại bằng IndexedDB; không tự đồng bộ sang máy khác hoặc GitHub. Tài nguyên đã xuất bản vẫn lấy từ website. Sao lưu để chuyển máy, bảo vệ khi xóa dữ liệu trình duyệt hoặc gửi bản sửa lại.
- Dữ liệu của hai trình chỉnh cũ được chuyển sang từng dự án một lần; các khóa localStorage cũ được giữ nguyên để bảo toàn dữ liệu.

Để xuất bản dự án tiếp theo cho mọi thiết bị, thêm tài nguyên vào thư mục riêng trong `videos/` và đăng ký trong `projects.json`. Giữ `id` dự án ổn định. Trang chủ tự hiển thị các mục đã đăng ký. Riêng dự án tài chính đầu tiên, bản intro v01, bản đầy đủ v01 hoặc v02 cũ được lưu nguyên vẹn vào **Bản lưu trước cập nhật** rồi chuyển sang v03. Bản lưu cũ có trong Sao lưu dự án và tải JSON riêng được; các sửa đổi trên v03 được giữ khi mở lại. Video 002–004 cũng lưu bảng hình 96 giây cũ vào lịch sử trước khi mở bản review theo WAV. Các revision khác và dự án khôi phục vẫn được giữ, hiện thông báo khi có bản xuất bản khác.

## Tài nguyên được lưu trên R2

Đã chuyển **198 tệp / 620,33 MB** khỏi nhánh `main` sang R2: toàn bộ WAV, MP3, MP4 và 180 PNG. Đủ 204 bản gốc đã được tải lại kiểm tra SHA-256 trên R2; 6 PNG (8,89 MB) vẫn giữ trên GitHub vì đường dẫn R2 công khai của chúng tải không ổn định. Studio tự chọn nguồn bằng [manifest](storage/manifest.json), đã bật và kiểm tra CORS thực tế. Không đổi đường dẫn trong JSON bản dựng hoặc bản sửa IndexedDB.

[Audio/video gốc và cách tải lại](storage/README.md). Ví dụ trước khi dựng lại video 004: `python3 tools/restore-media.py videos/004-living-alone/`. Các bản khôi phục được gitignore để tránh đưa file lớn trở lại repo. Khi chạy kiểm tra cần đọc media cục bộ, khôi phục đúng thư mục hoặc dùng `--all`; kiểm tra R2 thật: `node tests/r2-live.cjs`.

Cây tệp hiện tại giảm khoảng 620 MB; **lịch sử Git vẫn giữ các bản cũ**, không force-push trong lần này. Repo hiện Public, GitHub Pages đã được người dùng bật lại từ main /; trang chủ và manifest đã kiểm tra HTTP 200.

## Kho đạo cụ dùng chung

Bấm **Kho đạo cụ** ở đầu Studio hoặc [mở kho online](https://tai23082004l02-svg.github.io/Credit_Studio/?view=props). Hiện có 93 mục: 75 đạo cụ, 14 tư thế Alex trong nhóm **Nhân vật** và 4 nhóm minh họa trong **Nhân vật · Jamie**. Video 004 bổ sung 16 đạo cụ ảnh cắt ghép trong nhóm **Nhà ở · Collage**, giữ các mẫu vẽ tay cũ. Tìm theo tên/từ khóa, lọc nhóm, tải PNG riêng hoặc chọn dự án + cảnh rồi **Thêm vào cảnh**. Hình và nhãn được căn giữa; đạo cụ thêm vào video là lớp ảnh riêng.

Trong **Dựng video**, chọn lớp ảnh/nhân vật trên khung xem hoặc danh sách **Các lớp**, bấm **Thay đạo cụ** trong **Chỉnh phần tử**, rồi tìm/lọc mẫu thay thế. Thao tác giữ vị trí, khung kích thước, thời điểm và hiệu ứng; có Hoàn tác/Làm lại và tự lưu. Chỉ thay lớp đang chọn, không đổi các cảnh khác đang dùng cùng hình. Nếu lớp là ảnh cảnh tổng thể, thao tác thay cả ảnh đó.

Đưa PNG/JPG/WebP mới vào [thư mục library/props trên GitHub](https://github.com/tai23082004l02-svg/Credit_Studio/tree/main/library/props), commit rồi báo trợ lý cập nhật danh mục. Chạy `python3 tools/index-props.py` để đăng ký tệp mới, bổ sung tên/nhóm/từ khóa trong `library/props/catalog.json`, kiểm tra rồi push. [Hướng dẫn chi tiết](library/props/README.md). Tài nguyên cũ được tham chiếu, không nhân bản hoặc di chuyển.

Kho đã xuất bản dùng được trên mọi máy. Việc thêm đạo cụ vào bản dựng vẫn là bản sửa lưu trong trình duyệt và cần Sao lưu dự án để bàn giao. Đã sao chép và đối chiếu 204 tệp sang R2. Studio đã dùng R2 cho tài nguyên đã chuyển; xem [hướng dẫn R2](docs/R2_SETUP.md).

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

## Video thứ hai — Monthly Payment Trap

[Mở dự án video 002](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-002) · [Xem bộ hình](videos/002-monthly-payment-trap/) · [Hướng dẫn](videos/002-monthly-payment-trap/README.md). Có 16 khung hình (8 minh họa + 8 bố cục thông tin chỉnh riêng), 3 sheet trong suốt có ô đều, bản hướng dẫn đánh số, 30 PNG tách sẵn và tọa độ cắt. Tiêu đề và số dùng Times New Roman, nằm ngoài vùng minh họa. Đã nhận WAV và dựng **79 cảnh / 495,475 giây**, [MP4 duyệt v01](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/67f69d7d870311eb7258fa56a06580329b576378ae3420c8307722efb20e6489.mp4), chữ Times New Roman, audio dẫn xuất được nâng âm lượng, chưa nhạc nền. Bản dựng chỉnh được ở `review/project.json`; bảng hình 96 giây trước đó vẫn được giữ. [Timecode và trạng thái](videos/002-monthly-payment-trap/review/README.md).

## Video thứ tư — Living Alone

Video 004 **Why Living Alone Has Become So Expensive** dùng phong cách tài liệu tài chính với ảnh cắt ghép/nền giấy kem/đỏ trầm, vẫn dùng Times New Roman. [Mở bản dựng](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-004&tab=video) · [MP4 duyệt v01](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/76c1cf191f35563ef717fbe93fe85f9a61c4d18099743fc06f20f09f7697d5f9.mp4) · [Bộ hình](videos/004-living-alone/) · [Lời thoại](videos/004-living-alone/script.md) · [Nguồn/phép tính](videos/004-living-alone/sources.md). Đã nhận WAV qua chat và dựng **91 cảnh / 577,5 giây (9 phút 37,5 giây)**, có **29 lớp chuyển động nội dung trong 15 cảnh** và các thẻ hiện theo lời. WAV, 16 thiết kế ảnh, 2 sheet, 16 đạo cụ rời và bảng hình 96 giây cũ được giữ. Bản duyệt chờ người dùng, chưa phải bản cuối; chưa nhạc nền hoặc rig khớp. [Timecode và trạng thái](videos/004-living-alone/review/README.md).

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
node tests/prop-library.cjs
node tests/replace-prop.cjs
```

## Dựng MP4 từ dự án video

Website chạy không cần thư viện. Công cụ dựng MP4 cục bộ cần Node.js, Playwright 1.62.1 với Chromium và FFmpeg có libx264/AAC. Công cụ dùng chung bộ vẽ với phần xem trước để giữ hình và thời điểm giống nhau.

Sau khi khởi động máy chủ cục bộ theo hướng dẫn phía trên:

```sh
node tools/render-intro.cjs videos/001-100k-salary/intro/project.json /tmp/intro-review.mp4
```

Có thể thay đối số đầu bằng JSON đã lưu từ trình chỉnh video. Không ghi đè tệp xuất cũ trừ khi chọn đường dẫn mới hoặc đặt `CREDIT_STUDIO_OVERWRITE=1`. Đặt `CREDIT_STUDIO_URL` nếu máy chủ dùng địa chỉ khác. Chạy `python3 tools/build-intro-project.py` chỉ khi muốn tạo lại dự án mở đầu từ cấu hình trong công cụ; lệnh sẽ thay thế `intro/project.json` và `intro/captions.vtt`.

Font hiện dùng là Times New Roman cho chữ và phụ đề. Khi dựng MP4 cần có font này trên máy; kiểm tra bằng `fc-match 'Times New Roman'` trên Linux. Trong môi trường đám mây đã chuẩn bị font tại `/workspace/shared/credit-studio-fonts`; dùng tiền tố `FONTCONFIG_FILE=/workspace/shared/credit-studio-fonts/fonts.conf` khi chạy lệnh dựng. Website dùng Times New Roman cục bộ và font serif dự phòng nếu thiết bị thiếu font.

## Phụ đề trong trình dựng

Trên khung xem của trình dựng, bật **Phụ đề** và chọn **Tiếng Anh / Tiếng Việt**. Chọn ngôn ngữ tự bật phụ đề, được lưu cùng bản chỉnh và dùng khi xuất WebM. Hiện video 004 có 155 đoạn dịch tiếng Việt; các video chưa dịch vẫn dùng tiếng Anh. Bổ sung bản dịch vào draft đã lưu chỉ khi mốc và chữ tiếng Anh khớp, giữ nguyên timeline và các sửa riêng. MP4 bản duyệt gốc giữ nguyên.

## Chuyển động nội dung trong video

Trong **Chỉnh phần tử → Chuyển động nội dung**, chọn thanh tăng/giảm, di chuyển ngang/dọc hoặc số thay đổi. Chỉnh mốc `giây: giá trị`, nhịp chuyển và định dạng số. Studio và các bản xuất dùng cùng trạng thái theo thời gian, hỗ trợ tua ngược, hoàn tác/làm lại và lưu JSON. [Hướng dẫn bản v03](videos/001-100k-salary/review-v03/README.md). Kiểm tra: `node --test tests/video-motion.mjs` và `node tests/video-motion-editor.cjs`.

## Video thứ ba — Car Payment Trap

[Your Car Payment Is Keeping You Broke](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-003) đã có [16 thiết kế ảnh](videos/003-car-payment-trap/), 8 minh họa, 2 sheet có ô cắt/guide và 12 PNG mới (8 đạo cụ, 4 tư thế Alex). Chữ/số Times New Roman chỉnh riêng trong Studio. [Lời thoại](videos/003-car-payment-trap/script.md) đã lưu; đã nhận WAV và dựng **98 cảnh / 522,2 giây**, [MP4 duyệt v01](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/73bcec8142e0d7d4ace61f1313618998346d793d9aba7e43f7ee757275c79237.mp4), có chuyển động chi phí, dư nợ vay, lịch và dòng tiền. Bảng hình 96 giây cũ được giữ nguyên. [Timecode và kiểm tra](videos/003-car-payment-trap/review/README.md). [Hướng dẫn](videos/003-car-payment-trap/README.md).

## Video thứ năm — Mortgage Payment (đã nhận audio, duyệt phong cách)

Đề xuất **Your Mortgage Payment Is Only the Beginning**: [kịch bản tiếng Anh](videos/005-mortgage-payment/script.md), [lời đọc thuần để TTS](videos/005-mortgage-payment/narration.txt), [nguồn và phép tính](videos/005-mortgage-payment/sources.md), [storyboard ngắn](videos/005-mortgage-payment/storyboard.md). Kịch bản v01 1241 từ /8 phần đã duyệt; đã nhận WAV **9 phút26,45 giây** và có [ba cảnh mẫu chỉnh được trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-005&tab=video), **86,8 giây audio trích / chưa phải bản đầy đủ**. Người dùng đã chốt phong cách; đã bổ sung bốn minh họa Jamie cho bản đầy đủ, xem trong Kho đạo cụ → Nhân vật · Jamie. WAV mới giữ nguyên local và gitignore; upload R2 từ môi trường chat đang vướng HTTP401, chưa cập nhật manifest. [Trạng thái và nguồn](videos/005-mortgage-payment/README.md).
