# Video 001 — Why You Feel Broke on a $100,000 Salary

- Khán giả: người xem Mỹ, ngôn ngữ tiếng Anh.
- Phong cách: nhân vật nét vẽ 2D, nền sáng, kết hợp biểu đồ.
- Thời lượng dự kiến: 6–8 phút, cần đo lại theo tệp giọng đọc thực tế.
- [Lời thoại](script.md): 8 đoạn; không đọc tiêu đề đoạn.
- [Audio](audio/): nơi tải giọng đọc MP3/WAV lên.
- [Ảnh mẫu phong cách](../../assets/samples/finance-hand-drawn-2d.png).
- [Xem toàn bộ bộ hình](index.html) · [Trang xem online](https://tai23082004l02-svg.github.io/Credit_Studio/videos/001-100k-salary/).
- [Phân cảnh và hướng chuyển động](storyboard.md).

## Bộ hình

- `images/scenes/`: 16 ảnh cảnh chính, hai cảnh cho mỗi phần lời thoại.
- `images/sheets/`: 3 bảng PNG nền trong suốt, gồm 4 tư thế Alex và 24 nhóm đạo cụ.
- `projects/`: 16 dự án JSON, mở bằng nút **Mở dự án** trong Credit Studio để sửa chữ và số.
- `artwork.json`: danh sách cảnh, câu bắt đầu trong lời thoại, vị trí lớp chữ và liên kết tệp.

Ảnh cảnh gốc là PNG 1672 × 941, bố cục gần 16:9. Trang dự án là 1920 × 1080; ảnh gốc không được nâng độ phân giải hoặc chỉnh sửa trong bước đóng gói. Nhân vật và đồ vật trong mỗi ảnh cảnh là một lớp ảnh, chưa tách riêng. Các bảng tài nguyên là PNG nền trong suốt, chưa tách từng vật thể hoặc gắn khớp hoạt hình.

Chữ và số tài chính được giữ riêng trong JSON để sửa được và tránh sai số trong ảnh tạo sinh. Mở trang xem bộ hình để thấy phiên bản có lớp chữ; PNG gốc chưa có các lớp chữ đó.

Để đóng gói lại JSON sau khi cập nhật lớp chữ trong `artwork.json`, chạy `python3 tools/build-video-projects.py` từ thư mục gốc kho mã. Lệnh chỉ đóng gói ảnh và chữ, không tạo lại hoặc sửa ảnh.

## Trạng thái

Đã có lời thoại, ảnh tham khảo, 16 cảnh, 3 bảng tài nguyên, 16 dự án chỉnh chữ và phân cảnh. Đã nhận tệp WAV trong `audio/`; chưa đối chiếu nội dung, căn thời gian hoặc dựng video.
Credit Studio hiện là trình chỉnh ảnh một trang; timeline, âm thanh và xuất video chưa được triển khai.

## Quy trình bàn giao

1. Tạo giọng đọc từ `script.md`, đọc phần tiếng Anh, bỏ qua tiêu đề.
2. Tải audio vào thư mục `audio/`, commit lên GitHub.
3. Báo trong cuộc trò chuyện sau khi tải xong để kiểm tra và bắt đầu căn cảnh.
4. Sau này giữ hình, dự án dựng và bản xuất trong thư mục riêng của video này khi có các tệp thực tế.

Các số liệu trong lời thoại là tình huống minh họa, không phải mức thuế hay chi phí áp dụng cho mọi người.
