# Video 001 — Bản duyệt chuyển động v03

88 cảnh · 486,75 giây · 1920×1080 / 30 fps. Dựa trên v02 trong repo; chưa ghép các sửa riêng chỉ có trong trình duyệt.

- [Xem nhanh chuyển động 18 giây](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/baa17ce6e1687464e4e4ec484e27d3f880a3748ea4fc627b210b1dca4a6153d3.mp4) · [MP4 v03](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/91c9eec2d2d90380092377f0f2c314796adf7271725c24ff66ecd173e3caf5c3.mp4) · [Dự án chỉnh được](project.json) · [Kế hoạch chuyển động](motion-plan.json) · [Kiểm tra](validation.json).
- Giữ nguyên lời đọc, thứ tự/thời lượng 88 cảnh và audio dẫn xuất `review-v02/voiceover.mp3`. WAV và MP4/project v01/v02 giữ nguyên.
- 23 lớp chuyển động trong 11 cảnh: tiền di chuyển, số dư/thanh giảm theo sáu khoản chi và quỹ không đều, thanh phân bổ tăng tới đúng tỉ lệ, lịch nhảy 28→29→30→1 và tháng 1→2. Ngày trên lịch chỉ minh họa sự chuyển tháng.
- Số dư: 6.000→3.700→2.850→2.200→1.800→1.400→1.100→500 USD. Thanh và số dùng cùng mốc, cùng thang 6.000 USD; không tự suy diễn số tiền khác.
- Times New Roman, giữ vùng tiêu đề và nhân vật riêng; không thêm nhạc nền hay rig khớp.

## Chỉnh trong Studio

Chọn lớp → **Chuyển động nội dung**. Có thanh tăng/giảm, di chuyển ngang/dọc và số thay đổi. Mỗi dòng trong **Mốc chuyển động** là `giây: giá trị`, ví dụ `0: 6000` và `2: 3700`. Chọn nhịp êm, đều hoặc nhảy từng mốc; số hỗ trợ đô la Mỹ/số nguyên và chữ trước/sau. Có hoàn tác/làm lại, lưu JSON và xuất WebM. Với thanh, giá trị là độ rộng pixel; với vị trí, giá trị là tọa độ canvas.

Tua lấy trực tiếp trạng thái theo thời gian nên không phụ thuộc đã phát từ đầu hay chưa. Khi sửa vị trí hoặc nhân bản lớp đang di chuyển, đường chuyển động dịch cùng lớp. Đổi độ rộng thanh sẽ co/giãn toàn bộ mốc theo cùng tỉ lệ.

Studio lưu bản intro/v01/v02 đã chỉnh vào **Bản lưu trước cập nhật** trước khi mở v03. Muốn tiếp tục từ sửa đổi riêng trong bản đó, gửi `.credit.json` hoặc JSON; chúng chưa được ghép vào bản v03 xuất bản. Sửa v03 rồi reload sẽ giữ nguyên.

## Các cảnh có chuyển động nội dung

| Bắt đầu | Cảnh |
|---|---|
| 00:35.18 | Theo dòng tiền từ đầu |
| 01:49.92 | Tiền thuê nhà |
| 01:56.68 | Chi phí đi lại tổng hợp |
| 02:05.84 | Thực phẩm và ăn ngoài |
| 02:10.28 | Điện nước internet điện thoại |
| 02:13.44 | Khoản trả nợ |
| 02:18.40 | Các chi phí khác |
| 02:27.10 | Số dư sau chi cố định |
| 03:08.66 | Trừ dự trù chi phí không đều |
| 03:18.15 | Tổng hợp dòng tiền còn lại |
| 03:36.84 | Khoản trả cho chuyện đã qua |

Toàn bộ timecode còn lại giữ như [v02](../review-v02/README.md). Tạo dữ liệu bằng `python3 tools/build-salary-motion-v03.py`; mặc định chặn ghi đè. Chỉ dùng `--force` sau khi sao lưu sửa tay. Xuất MP4 bằng `tools/render-intro.cjs` với tên xuất mới.

Trạng thái: bản duyệt chờ góp ý kèm timecode, chưa phải bản cuối được người dùng chấp thuận.
