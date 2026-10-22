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

## Bản duyệt đầy đủ v01 hiện tại

**98 cảnh · 522,2 giây (8 phút 42,2 giây) · 1920×1080 / 30 fps.** Chờ người dùng duyệt, chưa phải bản cuối.

- [MP4 v01](exports/full-review-v01.mp4) · [Dự án chỉnh được](review/project.json) · [Timecode](review/README.md) · [Kiểm tra thực tế](review/validation.json).
- WAV gốc `audio/tts_20261022_115123_7124d9.wav` giữ nguyên; `review/voiceover.mp3` là bản dẫn xuất chuẩn hóa âm lượng, không đổi tốc độ hoặc cắt lời.
- 27 lớp chuyển động nội dung trong 14 cảnh, cùng các thẻ xuất hiện theo lời đọc: thanh tổng chi phí xe, bảng tiết kiệm 12 tháng, lịch và dư nợ theo công thức trả góp, phong bì nợ đi sang khoản vay mới. Chữ Times New Roman; không nhạc nền hoặc rig khớp.
- `review/alignment.json`: mốc từ tự động, `review/captions.vtt`: phụ đề bật được trong Studio; MP4 mặc định không chèn phụ đề. Có sai số căn từ tự động.
- Audio dùng câu chuyển thời gian cũ “A couple of years pass”; giữ nguyên lời đọc và ghi rõ phần trade-in là **ví dụ giả định riêng**, không phải số dư hai năm của khoản vay trước. Văn bản đối chiếu audio nằm ở `review/narration.md`; script dự định vẫn giữ bản đã chỉnh.
- Bảng 96 giây, 16 thiết kế/ảnh và sheet trước đây giữ nguyên. Studio lưu draft bảng hình đã chỉnh vào **Bản lưu trước cập nhật** trước khi mở review; bản đó tải JSON được và nằm trong `.credit.json`. Các sửa đổi trên review v01 được giữ khi reload.

Vào **Chỉnh phần tử → Chuyển động nội dung** để sửa mốc, giá trị và nhịp của từng lớp. Vị trí/thời gian audio giữ nguyên khi xem/tua và xuất. Bản dựng này dựa trên tài nguyên repo, chưa ghép các sửa riêng trong IndexedDB; nếu cần tiếp tục từ sửa đó, cung cấp `.credit.json` hoặc JSON.

Tạo lại dữ liệu: `python3 tools/build-car-payment-video.py`. Mặc định chặn ghi đè; chỉ `--force` sau khi sao lưu sửa tay. Công cụ không sửa WAV/MP4. Xuất bằng `tools/render-intro.cjs` với tên mới; giữ v01 cho lần xuất sau.

## Số liệu minh họa

$35,000 vay ở APR 8% / 72 tháng cho payment khoảng $614/tháng; tổng khoảng $44,200 và interest khoảng $9,200, giả định fixed rate và không thêm financed fees. Các số đã làm tròn; không lấy $614 làm số chưa làm tròn để kiểm tra tổng chính xác. Payment + insurance + gas + upkeep/registration dùng ví dụ 614 + 180 + 160 + 90 = 1,044; 12,528/năm được đọc và hiển thị gần $12,500. Negative equity: 28,000 − 23,000 = 5,000; 30,000 + 5,000 = 35,000 trước tax/fees, tùy lender. 200 × 12 = 2,400.

## Tiếp theo

Người dùng duyệt MP4 v01 và gửi góp ý kèm timecode. Nếu đã chỉnh trong Studio, gửi bản sao lưu trước khi tiếp tục từ sửa đó. Giữ bản WAV gốc và dùng tên v02 cho lần xuất tiếp theo. Chưa thêm nhạc nền hoặc rig khớp.

Bản sửa trong Studio nằm ở IndexedDB, không tự lên GitHub. Nếu đã chỉnh, tải **Sao lưu dự án .credit.json** hoặc JSON trước khi nhờ trợ lý tiếp tục từ bản đó. Các video 001/002 và bản xuất trước giữ nguyên.

Đóng gói lại bằng `node tools/build-car-payment-artwork.cjs`; mặc định chặn ghi đè. Chỉ dùng `--force` sau khi sao lưu sửa tay. Công cụ không tạo lại ảnh AI hoặc sửa WAV; cần máy chủ cục bộ và Times New Roman đã cài. Dùng FONTCONFIG_FILE theo README gốc nếu dựng trong môi trường cloud. Xem `artwork-validation.json` cho kiểm tra thực tế.
