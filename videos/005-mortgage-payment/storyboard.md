# Storyboard ngắn — Mortgage Payment v01

Đây là kế hoạch nội dung toàn bộ, **chưa chốt timecode hoặc clip count cho full video**. Đã có WAV566,45 giây và bản ba cảnh mẫu samples/project.json /86,8 giây để duyệt phong cách. Audio thật sẽ quyết định điểm cắt; một phần lời thoại có thể chia nhiều shot. Không tạo bảng im lặng 96 giây hoặc bộ 16 ảnh cố định.

## Phong cách đã chốt

Đồ họa tài chính nhiều lớp, nền giấy kem, nét than/đỏ trầm, Times New Roman. Dùng căn nhà, tài liệu, tiền và các phần có thể di chuyển độc lập; không bắt buộc đưa Alex vẽ tay vào. Chữ/số tách khỏi ảnh. Người dùng đã chốt phong cách qua ba cảnh mẫu ngày2026-10-23. Minh họa mới Jamie trong images/ và library/props/jamie-mortgage/ tiếp tục bảng màu này.

| Phần | Câu chuyện hình | Chuyển động phục vụ giải thích |
| --- | --- | --- |
| 01 | Căn nhà và con số trên calculator | Khung nhìn mở rộng từ LOAN PAYMENT sang LIFE AROUND IT; chưa hiện tổng chi trước lời |
| 02 | Ngân sách tách lớp | Các đoạn PI/tax/insurance/HOA xuất hiện; bar + counter đồng bộ 1517→1817→1942→2017; savings riêng đưa allocation lên2267 |
| 03 | Đường đi escrow | Tiền chia vào tax/insurance qua escrow; gộp cùng bill để giải thích không cộng hai lần; HOA ở ngoài |
| 04 | Sổ tiền mặt và phần sở hữu nhà | 75000→15000→6000→4000; $60000 di chuyển sang equity, không biến mất như phí; $9000 có ba nhóm closing |
| 05 | Lịch và quỹ sửa chữa | Hai lần $250 thành500; bill3000 xuất hiện; chỉ ra gap2500; riêng mốc12 transfers thành3000, không tự bù gap trước đó |
| 06 | Payment tách principal/interest | First month:1300 interest,217 principal; equity và checking hiển thị hai nơi khác nhau; không giả lập giá tăng |
| 07 | Ngân sách quanh căn nhà | Checklist housing/utility/food/transport/debt/saving; chỉ minh họa thay đổi định tính khi không có giả định số, không tạo income giả |
| 08 | Ngôi nhà và khoảng thở | Các mục repair/saving/life còn chỗ quanh nhà; kết thúc bằng THE ROOM YOU HAVE LEFT |

## Ba cảnh mẫu đã tạo — người dùng đã chốt phong cách

1. Mở đầu: căn nhà và calculator, thử tỷ lệ hình, Times New Roman và nhịp mở khung.
2. Monthly allocation: thử stacked bar/counter, bills vs saved money, căn giữa icon/label.
3. Cash vs equity: thử chuyển $60000 sang nhà, giữ góc/cạnh/nhân vật và phân biệt tiền mặt.

Không tạo thêm thiết kế ảnh riêng giống hệt frame video. Khi có mẫu, dùng một bản dựng mẫu chỉnh được; render ngắn để duyệt khi cần, không gọi là full review. Sau audio, chuyển tài nguyên cần dùng sang bản dựng chính; tránh duy trì hai bản nội dung giống nhau.

## Điều kiện chất lượng

- Nhãn FICTIONAL EXAMPLE; số dùng USD, đúng phép tính và phạm vi trong sources.md.
- Kho chung dùng lại khi phù hợp. Nếu cần sheet mới: ô đủ lề, kiểm tra alpha/crop từng ảnh, không lẹm góc/cạnh hoặc dính ô bên cạnh; giữ nguồn/crop map. Không tạo đạo cụ chưa dùng.
- Căn giữa hình/nhãn trong thẻ. Kiểm tra đầu/tay/chân, crop và chồng lớp lúc vào/giữa/ra.
- Animation deterministic khi tua và xuất; bar/number dùng cùng nhịp và scale. Chưa thêm nhạc nền hoặc rig khớp nếu chưa có quyết định.
- Thời lượng và điểm xuất hiện chốt theo WAV, không theo phỏng đoán từ số từ.
