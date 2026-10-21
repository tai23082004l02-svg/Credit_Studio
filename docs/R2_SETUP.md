# Điền thông tin kết nối R2

Tệp mẫu không có khóa: [`.env.r2.example`](../.env.r2.example).

Trong môi trường làm việc hiện tại đã chuẩn bị tệp riêng `/workspace/.credit-studio/r2.env`, nằm ngoài thư mục website/kho Git và chỉ chủ sở hữu có quyền đọc/ghi. Điền Access Key ID, Secret Access Key, S3 API endpoint và tên bucket vào đó. Không thay đổi tên biến ở bên trái dấu `=`.

Endpoint có dạng `https://<account-id>.r2.cloudflarestorage.com`; dùng đúng địa chỉ Cloudflare cung cấp, không thêm tên bucket vào cuối. Bucket dự kiến là `credit-studio`.

Không điền khóa thật vào tệp mẫu trên GitHub hoặc tệp nằm trong thư mục website, kể cả khi tệp đó đã được `.gitignore` bỏ qua: máy chủ tĩnh vẫn có thể phục vụ tệp ngoài ý muốn. Nếu lưu trên máy cá nhân, giữ tệp đã điền ở thư mục riêng ngoài bản sao website. Không gửi tệp chứa khóa vào chat.

Sau khi người dùng điền tệp trong môi trường, trợ lý chỉ kiểm tra sự hiện diện của giá trị (không in khóa), rồi thử kết nối R2. Hiện chưa có khóa và chưa xác minh kết nối. Các lệnh kết nối sau này phải đọc biến theo định dạng key=value, không thực thi tệp cấu hình như mã shell.

Tệp riêng trên đĩa không thay thế Secrets của môi trường và không bảo đảm tồn tại ở phiên/môi trường khác. Secrets là cách cấu hình dùng lâu dài; chat mới cần kiểm tra cấu hình hiện có trước khi yêu cầu điền lại.
