# Credit Studio

Trình thiết kế đồ họa cục bộ với giao diện tiếng Việt, lấy cảm hứng từ Canva. Không cần tài khoản, API hay cài thư viện.

## Dùng online

Địa chỉ website: https://tai23082004l02-svg.github.io/Credit_Studio/

Website được triển khai bằng GitHub Pages từ thư mục gốc của nhánh `main`.
Sau khi commit và push thay đổi lên `main`, GitHub Pages sẽ cập nhật website.
Thiết kế và ảnh vẫn được xử lý trong trình duyệt của bạn. Dữ liệu tự lưu gắn với trình duyệt và địa chỉ website; dùng nút **Lưu dự án** để sao lưu JSON hoặc chuyển thiết kế từ localhost sang website.

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

Bản này hỗ trợ một trang thiết kế; chưa có cộng tác, kho tài nguyên trực tuyến, chỉnh ảnh nâng cao hoặc đầy đủ tính năng Canva. Localhost của môi trường đám mây khác với localhost của máy cá nhân: tải/clone dự án về máy trước để chạy tại đó.

## Kiểm tra cú pháp

```sh
node --check app.js
```
