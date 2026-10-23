# Ba cảnh mẫu Mortgage v01

**86,8 giây /3 cảnh có giọng đọc**, chờ duyệt phong cách. Không phải bản đầy đủ566,45 giây.

[Mở trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-005&tab=video). Bản dựng chính: project.json. Chỉ có một bản dựng mẫu chỉnh được; PNG căn nhà và MP3 montage trích audio nằm trong data URL, nên mẫu không phụ thuộc upload R2 đang vướng401. Nguồn vector: house.svg. Không có ảnh cảnh hoặc thiết kế JSON trùng nội dung.

- Calculator: WAV12,55–25,08 giây, số mở đầu xấp xỉ1500.
- Monthly allocation: WAV80,95–123,12 giây, bar/counter cùng scale2267; tiền giữ cho sửa chữa khác bills.
- Cash/equity: WAV222,92–255,02 giây, cash75000→4000; down payment60000 vẫn thành equity, không vào thùng rác.

Các đoạn không liền nhau trong WAV; chỉ nối để duyệt thiết kế và chuyển động, không thay lời đọc nguồn. Chưa có phụ đề hoặc nhạc. Giữ Times New Roman; kiểm tra font thực và số liệu trong validation.json. Mẫu có16 lớp animation trong2 cảnh; nhà là một lớp ảnh từ SVG, chưa có nhân vật/rig.

Tạo lại (sau khi đã có timing và MP3 dẫn xuất): `node tools/build-mortgage-samples.cjs normalized.mp3 production/script-timing.json work/new-scratch`. Builder chặn ghi đè project.json; nếu đã có sửa trong Studio, nhận backup trước, không chạy đè bản chỉnh. Full WAV không được nhúng vào JSON hoặc commit GitHub.

Tiếp theo: người dùng duyệt phong cách, rồi tạo tài nguyên/chia cảnh đầy đủ theo audio. Khi bản review thay thế mẫu trong finance-005, phải giữ bản chỉnh hiện tại bằng backup/archive. MP4 thử chỉ ở work, chưa publish MP4 hoặc full review.
