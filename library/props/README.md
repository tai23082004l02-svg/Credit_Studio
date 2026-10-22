# Kho đạo cụ dùng chung

[Mở kho trong Credit Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?view=props).

Kho dành cho nhân vật, nhà, xe, tiền, hóa đơn, đồ ăn và các vật thể dùng lại ở nhiều video. Hiện có **89 mục: 75 đạo cụ và 14 tư thế Alex** trong nhóm **Nhân vật**. Video 004 thêm 16 đạo cụ photographic collage trong nhóm **Nhà ở · Collage**, ID `solo4-*`; 73 mục vẽ tay trước đó giữ nguyên. Chúng được đăng ký bằng vùng cắt trong `catalog.json`, trỏ về sheet gốc hoặc sheet sản xuất đã căn ô; không sao chép hoặc di chuyển ảnh đang dùng trong video. Các mẫu collage có PNG rời, sheet trong suốt và bản hướng dẫn tại `videos/004-living-alone/images/`; không dùng tọa độ nguồn để cắt atlas đóng gói.

## Đưa đạo cụ mới vào kho

1. Mở thư mục này trên GitHub, chọn **Add file → Upload files**.
2. Tải PNG nền trong suốt (ưu tiên), JPG hoặc WebP. Đặt tên như `red-car-02.png`; tên tệp không dấu, không khoảng trắng. Mỗi phiên bản mới dùng tên riêng để giữ các video cũ.
3. Commit lên `main`, rồi báo trợ lý cập nhật kho. Upload trên GitHub chưa tự đăng ký tệp vào danh mục.
4. Trợ lý chạy `python3 tools/index-props.py`, bổ sung tên tiếng Việt, nhóm và từ khóa trong `catalog.json`, kiểm tra hình rồi commit/push. GitHub Pages sẽ cập nhật kho.

Để thay một đạo cụ/nhân vật đang có, mở **Dựng video**, chọn lớp ảnh, bấm **Thay đạo cụ** rồi chọn mẫu trong kho. Giữ nguyên vị trí, khung kích thước và hiệu ứng của lớp; hoàn tác/làm lại được. Lớp dùng chung ở cảnh khác không bị thay theo.

Trong Studio, bấm **Kho đạo cụ**, tìm theo tên/từ khóa, chọn dự án video và cảnh rồi **Thêm vào cảnh**. Một lớp đạo cụ riêng được đặt giữa khung; chỉnh vị trí/kích thước trong trình dựng. **Tải PNG** tải riêng đạo cụ ở độ phân giải vùng ảnh gốc, giữ nền trong suốt nếu ảnh nguồn có.

Kho đã xuất bản trên GitHub có thể xem ở mọi máy. Việc thêm đạo cụ vào bản đang dựng vẫn lưu trong trình duyệt; dùng **Sao lưu dự án** để bàn giao các chỉnh sửa. Không có đồng bộ dự án online hay kết nối R2 trong thay đổi này. Tài nguyên ở repo công khai có thể được xem/tải công khai.

## Danh mục

`catalog.json` có `version: 1` và danh sách `items`. Mỗi mục gồm `id` ổn định, `name`, `category`, `tags`, `src`; `crop` tùy chọn là `[x,y,width,height]` theo pixel nguồn. Ảnh được phép lấy từ `videos/<slug>/...` hoặc `library/props/...`. Giữ ID, tên tệp và đường dẫn đã sử dụng. Đạo cụ mới nên là một tệp riêng; khi dùng sprite sheet, kiểm tra vùng cắt không dính vật thể bên cạnh hoặc mất nét của chính vật thể.

Mỗi lần dựng, kiểm tra bố cục và toàn bộ đường viền của nhân vật/đạo cụ, kể cả các lớp nền/chữ có thể che lên chúng. Các góp ý của người dùng về căn giữa và không che đầu nhân vật được lưu trong `AGENTS.md` và bản bàn giao.
