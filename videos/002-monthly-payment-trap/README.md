# Video 002 — The Monthly Payment Trap: How “Affordable” Keeps You Broke

[Mở dự án trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-002) · [Xem toàn bộ hình](https://tai23082004l02-svg.github.io/Credit_Studio/videos/002-monthly-payment-trap/) · [Lời thoại](script.md) · [Phân cảnh](storyboard.md).

## Trạng thái

Đã chuẩn bị trọn bộ hình cho 8 phần lời thoại: **16 khung hình 1920×1080**, gồm 8 cảnh minh họa gốc và 8 bố cục thông tin dựng từ lớp riêng. Có 16 dự án ảnh chỉnh được, 3 sheet nền trong suốt, 3 bản hướng dẫn sheet có ô/nhãn, **6 tư thế Alex và 24 đạo cụ mới**, 30 PNG tách sẵn và tọa độ cắt. Đã đăng ký dự án `finance-002`, giữ nguyên dự án `finance-001`.

**Chưa nhận audio, chưa có MP4 hoặc bản dựng đã căn lời đọc.** `storyboard/project.json` chỉ là bảng hình tĩnh để mở trong tab Dựng video: 16 cảnh × 6 giây = 96 giây tạm, không phải thời lượng video thật. Không suy thời lượng chính thức từ bảng hình. Script khoảng 1.101 từ; nhịp đọc thực tế sẽ quyết định thời lượng cuối.

## Tệp và mức chỉnh sửa

- `script.md`: lời thoại tiếng Anh đã được người dùng chấp thuận, giữ nguyên 8 phần.
- `artwork.json`: 16 khung hình, câu bắt đầu, liên kết thiết kế và hướng chuyển động.
- `images/illustrations/`: 8 PNG minh họa gốc được tạo mới theo Alex và bảng màu hiện có; hình trong mỗi PNG là ảnh tổng thể.
- `images/scenes/`: 16 PNG khung hoàn chỉnh để xem/tải, có chữ Times New Roman và các phép tính được dựng bằng lớp riêng trước khi xuất.
- `projects/`: 16 JSON thiết kế ảnh; chữ/số và các lớp của cảnh thông tin chỉnh riêng được. Ảnh minh họa tổng thể chưa tách mọi nét thành khớp.
- `images/sources/`: 3 sheet nguyên bản tạo sinh được giữ lại.
- `images/sheets/`: 3 atlas sản xuất đã đưa từng mục vào ô đều có khoảng đệm; 3 `*-guide.png` có viền ô, số và tên để tìm nhanh. Chỉ dùng atlas PNG trong suốt hoặc PNG riêng khi dựng; bản guide có nhãn không phải sprite nền trong suốt.
- `images/cutouts/`: 30 PNG riêng; giữ pixel của vùng cắt nguồn, thêm 32 px khoảng đệm trong suốt mỗi phía, không nâng độ phân giải nội dung.
- `images/crop-map.json`: tọa độ `[x, y, width, height]` theo pixel, gốc ở góc trái trên; chứa ô trên atlas, vùng nét và vùng cắt trên sheet nguồn.
- `asset-layout.json`: cấu hình cảnh, nguồn, phép cắt để tái tạo các tệp dẫn xuất.
- `storyboard/project.json`: bảng hình 16 cảnh dùng bộ vẽ Studio, chưa audio, không phải video cuối.
- `audio/`: chờ giọng đọc WAV/MP3, bảo toàn bản gốc khi nhận.

30 mục mới có ID ổn định `mpt-*`, được thêm vào Kho đạo cụ chung bằng tham chiếu atlas. Các ID/đường dẫn cũ được giữ. Tổng kho hiện 61 mục: 51 đạo cụ, 10 tư thế Alex. Có thể tải PNG riêng ở thư viện này hoặc tải một ô qua Kho đạo cụ.

## Quy tắc bố cục

Times New Roman cho mọi lớp chữ và bản hướng dẫn. Tiêu đề nằm ở phần trên; vùng minh họa của 8 cảnh vẽ nằm hoàn toàn từ y=254 trở xuống, không có tấm nền phủ lên đầu nhân vật. Ảnh luôn giữ tỉ lệ. Các thẻ căn giữa cả hình và từng dòng nhãn; khoảng cách trong nhóm đồng đều. PNG tách sẵn và atlas giữ đủ tóc, tay, giày.

Ở giai đoạn dựng chuyển động tiếp theo, tiếp tục kiểm tra khung tổng hợp lúc vào, giữa và ra cảnh: khoảng đệm hiện tại không cho phép tùy ý zoom/crop hoặc kéo tiêu đề đè lên nhân vật.

## Kiểm tra số liệu

- Điện thoại: $37.50 × 24 = $900, chỉ khi không có lãi/phí.
- $525 + $37.50 + $90 + $120 + $45 = $817.50 trong tháng minh họa. BNPL là tổng các kỳ đến hạn trong tháng này, không phải khoản cố định mãi mãi; đăng ký dịch vụ có thể hủy không đồng nghĩa với dư nợ vay.
- Ví dụ tài trợ: $75 × 24 = $1,800; $60 × 36 = $2,160; ít hơn $15/tháng nhưng tổng cao hơn $360 và lâu thêm 12 tháng. Không phải đề nghị vay thực tế.
- Chi phí sửa xe $600 là khoản bất ngờ riêng, không gộp vào $817.50.
- Các đường lịch ở ảnh 04a là ẩn dụ; dùng 04b cho số tiền/kỳ hạn chính xác.

## Tái tạo

Không chạy lại trên thiết kế đã sửa mà chưa sao lưu. Website không cần thư viện; công cụ tạo atlas/PNG cần Node, Playwright/Chromium, máy chủ cục bộ và Times New Roman có bản quyền sử dụng hợp lệ trên máy dựng.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Chuẩn bị font in đậm tại `work/monthly-payment-trap/timesbd.ttf` (tệp tạm, không commit). Chạy `node tools/build-monthly-payment-artwork.cjs`; khi tệp dẫn xuất đã tồn tại, phải sao lưu rồi mới dùng `--force`. `CREDIT_STUDIO_URL` thay địa chỉ máy chủ, `CREDIT_CHROMIUM` chọn Chromium khi cần. Atlas được đóng gói bằng browser canvas; pixel nguồn được giữ và không đưa font độc quyền lên GitHub.

## Bước tiếp theo

Người dùng xem bộ hình, gửi góp ý và cung cấp giọng đọc. Khi có audio: chia thêm shot từ 16 bố cục, căn các lớp theo lời đọc, kiểm tra âm lượng, phụ đề và vùng an toàn ở mọi thời điểm, xuất MP4 duyệt vào tên mới. Chưa thêm nhạc nền, chưa rig khớp nhân vật. Bản chỉnh trong trình duyệt vẫn ở IndexedDB; nhận `.credit.json` hoặc JSON trước khi tiếp tục từ các sửa đổi đó.
