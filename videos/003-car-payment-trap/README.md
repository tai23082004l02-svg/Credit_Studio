# Video 003 — Your Car Payment Is Keeping You Broke

Khán giả Mỹ; lời thoại tiếng Anh; Alex và đồ họa vẽ tay 2D; chữ Times New Roman.

- [Mở dự án trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-003).
- [Bộ hình online](https://tai23082004l02-svg.github.io/Credit_Studio/videos/003-car-payment-trap/) · [Lời thoại](script.md) · [Phân cảnh](storyboard.md).
- `images/illustrations/`: 8 PNG minh họa gốc mới, chưa có chữ/số tài chính.
- `images/originals/`: 2 sheet nguồn tạo sinh, giữ nguyên; `images/sheets/`: 2 sheet đóng gói có ô đều, khoảng đệm và bản guide Times New Roman.
- `images/cutouts/`: 12 PNG mới tách sẵn (8 đạo cụ + 4 Alex); `images/reused/`: 6 PNG dẫn xuất từ kho cũ, không đăng ký trùng mục.
- `images/crop-map.json`: sourceCrop, cell crop và artBounds; không dùng tọa độ source để cắt atlas đã đóng gói.
- `projects/`: 16 thiết kế có lớp chữ/số/ảnh riêng; `images/scenes/`: 16 bản PNG xem nhanh qua cùng renderer Studio.
- `storyboard/project.json`: bảng 16 cảnh × 6 giây, **không có audio, chưa căn lời đọc**, revision `car-artwork-board-v01`. Không phải video hoàn chỉnh và chưa có MP4.

## Số liệu minh họa

$35,000 vay ở APR 8% / 72 tháng cho payment khoảng $614/tháng; tổng khoảng $44,200 và interest khoảng $9,200, giả định fixed rate và không thêm financed fees. Các số đã làm tròn; không lấy $614 làm số chưa làm tròn để kiểm tra tổng chính xác. Payment + insurance + gas + upkeep/registration dùng ví dụ 614 + 180 + 160 + 90 = 1,044; 12,528/năm được đọc và hiển thị gần $12,500. Negative equity: 28,000 − 23,000 = 5,000; 30,000 + 5,000 = 35,000 trước tax/fees, tùy lender. 200 × 12 = 2,400.

## Tiếp theo

Tạo giọng đọc từ `script.md`, bỏ tiêu đề đoạn và hướng dẫn tiếng Việt. Lưu WAV hoặc MP3 vào `audio/`, commit lên GitHub rồi báo để bắt đầu căn cảnh và chuyển động theo audio thật. Giữ bản ghi gốc. Chưa thêm nhạc nền hoặc rig khớp.

Bản sửa trong Studio nằm ở IndexedDB, không tự lên GitHub. Nếu đã chỉnh, tải **Sao lưu dự án .credit.json** hoặc JSON trước khi nhờ trợ lý tiếp tục từ bản đó. Các video 001/002 và bản xuất trước giữ nguyên.

Đóng gói lại bằng `node tools/build-car-payment-artwork.cjs`; mặc định chặn ghi đè. Chỉ dùng `--force` sau khi sao lưu sửa tay. Công cụ không tạo lại ảnh AI hoặc sửa WAV; cần máy chủ cục bộ và Times New Roman đã cài. Dùng FONTCONFIG_FILE theo README gốc nếu dựng trong môi trường cloud. Xem `artwork-validation.json` cho kiểm tra thực tế.
