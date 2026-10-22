# Phân cảnh hình — Living Alone

8 phần lời thoại, mỗi phần có một minh họa collage (`a`) và một bảng thông tin (`b`). Có 16 thiết kế JSON chỉnh riêng và PNG 1920×1080. **Chưa có giọng đọc; chưa có timecode thật hoặc MP4.** `storyboard/project.json` là bảng duyệt hình im lặng **16 × 6 = 96 giây**, revision `living-artwork-board-v01`, không phải thời lượng video đầy đủ.

| Phần | Minh họa | Bảng thông tin / điểm cần giữ | Hướng chuyển động khi nhận WAV |
|---|---|---|---|
| 01 · The keys | Chìa khóa trong căn hộ buổi tối | 4 nhóm: rent, utilities, internet, groceries; không gán số giả | Chìa khóa và hóa đơn rời xuất hiện theo lời kể |
| 02 · One front door | Hai căn hộ cắt lớp, một và hai phòng ngủ | $1.800 + $60 = $1.860; $2.400/2 + $60/2 = $1.230/người; chênh $630/tháng = $7.560/năm | Cộng số theo từng khoản; hai thanh cùng thang $1.860, độ dài tỉ lệ 1.860 và 1.230 |
| 03 · What changed | Nhà, hợp đồng trống và mũi tên ẩn dụ | BLS rent CPI +4,3%, 12 tháng hết 12/2024; Census 38,5 triệu hộ một người / 29% hộ, năm 2024 | Hiện từng dữ kiện có nguồn/năm; không biến ảnh mũi tên thành biểu đồ có dữ liệu giả |
| 04 · Smaller bills | Tủ lạnh, internet, thực phẩm, hộp dọn nhà | Tách recurring / variable / upfront; deposit có thể hoàn lại nhưng giữ cash | Hóa đơn định kỳ lặp lại; nhóm move-in hiện riêng, không cộng trùng |
| 05 · One income | Bàn làm việc trống và cửa nhà | 2 × $1.860 = $3.720 chỉ rent + internet; chưa đủ emergency fund | Lịch hiện hai tháng, cùng hóa đơn; không gọi đây là toàn bộ sinh hoạt |
| 06 · Privacy | Nhân vật hư cấu đọc sách trong ghế đỏ trầm | $630 là chênh tiền nhà/internet trong ví dụ, không phải định giá chung cho sự riêng tư | Đạo cụ ghế rời, chữ rest/safety/quiet; không chuyển động vào vùng tóc/tay/chân |
| 07 · Plan for one | Sổ, máy tính, chìa khóa, quỹ dự phòng | Full monthly cost / move-in cash / bare-bones budget | Các mục checklist hiện theo lời; không đặt một mục tiêu quỹ chung cho mọi người |
| 08 · Room to stay | Căn hộ sáng, chìa khóa và lọ tiền | Home / honest plan / people to call | Gọi lại chìa khóa mở đầu; kết bằng khoảng thở và kết nối hỗ trợ |

## Sheet và đạo cụ

- `images/originals/household.png`, `planning.png`: hai sheet nguồn AI được chỉnh lại khoảng cách sau khi kiểm tra bản thử; giữ nguyên pixel nguồn đã chọn.
- `images/sheets/household.png`, `planning.png`: atlas trong suốt **4 × 2 ô**, mỗi ô 512×448 px; các bản `*-guide.png` có đường ô, nhãn Times New Roman và nền giấy kem.
- `images/cutouts/`: **16 PNG rời**, lấy đủ vùng alpha của từng đạo cụ + khoảng đệm 32 px mỗi phía; không nâng độ phân giải nội dung.
- `images/crop-map.json`: `sourceCrop` / `sourceArtCrop` dùng tọa độ sheet nguồn; `crop` / `artBounds` dùng tọa độ atlas đóng gói. Không hoán đổi hai hệ.
- ID dùng chung `solo4-*`, nhóm **Nhà ở · Collage**. Giữ 73 mục cũ; tổng kho 89 mục = 75 đạo cụ và 14 tư thế Alex.

## Quy tắc bố cục và bảo toàn

Chữ/số Times New Roman là lớp chỉnh riêng. Tiêu đề nằm ngoài vùng ảnh, không dùng panel che tóc. Ảnh được fit giữ tỉ lệ; nhân vật ngồi trong 06a giữ trọn đầu, tay và hai chân. Các khung nội thất có cận cảnh đồ đạc có chủ đích; không lấy ảnh nội thất làm nguồn cắt đạo cụ. Hình và nhãn trong thẻ đạo cụ căn giữa, lề cân đối.

Hình ảnh là minh họa AI theo phong cách tài liệu, không phải ảnh tư liệu thật. Nhãn số tiền: **Illustrative example — not national averages**. Năm và đơn vị của dữ liệu lịch sử giữ đúng [nguồn](sources.md).

Minh họa `a` vẫn là một lớp ảnh tổng thể, chưa tách mọi vật thể. Các đạo cụ PNG rời và bảng `b` đã sẵn sàng để dựng chuyển động theo audio; chưa rig khớp hoặc nhạc nền. Sau khi nhận WAV, lưu bảng 96 giây cũ và tạo review theo audio với revision/tệp xuất mới, không ghi đè sửa riêng trong IndexedDB.
