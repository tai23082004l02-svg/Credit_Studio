# Video 001 — Why You Feel Broke on a $100,000 Salary

- Khán giả: người xem Mỹ, ngôn ngữ tiếng Anh.
- Phong cách: nhân vật nét vẽ 2D, nền sáng, kết hợp biểu đồ.
- Thời lượng thực tế: 486,75 giây (8 phút 06,75 giây), theo WAV đã nhận.
- [Lời thoại](script.md): 8 đoạn; không đọc tiêu đề đoạn.
- [Audio](audio/): nơi tải giọng đọc MP3/WAV lên.
- [Ảnh mẫu phong cách](../../assets/samples/finance-hand-drawn-2d.png).
- [Xem toàn bộ bộ hình](index.html) · [Trang xem online](https://tai23082004l02-svg.github.io/Credit_Studio/videos/001-100k-salary/).
- [Phân cảnh và hướng chuyển động](storyboard.md).
- [Duyệt và chỉnh toàn bộ video](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-001&tab=video) · [MP4 đầy đủ](exports/full-review-v01.mp4) · [MP4 mở đầu cũ 40,5 giây](exports/intro-v01.mp4).

Mở [không gian dự án chung](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-001) để quản lý bản dựng, cảnh ảnh, audio và lời thoại cùng một chỗ. Chọn **Hình ảnh → Chỉnh cảnh trong dự án** để sửa trực tiếp, mỗi cảnh có bản lưu riêng. **Sao lưu dự án** giữ cả bản video, các cảnh đã sửa và tệp bạn thêm vào trình duyệt.

## Bản duyệt đầy đủ

Đã nối toàn bộ lời đọc thành **64 cảnh, dài 8 phút 06,75 giây**, giữ nguyên 8 cảnh mở đầu. Đây là bản duyệt v01 để sửa tiểu tiết trước bản xuất cuối.

- [Mở dựng video trong dự án](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-001&tab=video).
- [MP4 đầy đủ v01](exports/full-review-v01.mp4), 1920×1080, 30 fps, có lời đọc gốc, chưa có nhạc nền.
- `review/project.json`: bản dựng đầy đủ với các lớp chữ, số, đạo cụ và cảnh ảnh.
- `review/voiceover.mp3`: dẫn xuất toàn bộ WAV gốc, không cắt bỏ nội dung.
- `review/alignment.json` và `review/captions.vtt`: nhận dạng mốc từ và phụ đề đối chiếu script; có sai số căn từ tự động.
- [Danh sách timecode 64 cảnh](review/README.md).

Nếu trình duyệt vẫn mở bản cũ, dùng **Sao lưu dự án** trước, rồi chọn **Mở bản dựng mới** trong tab Dựng video (hoặc **Bản gốc**). Bản lưu cục bộ không tự bị ghi đè. MP4 ở Tổng quan là bản đã xuất trên GitHub; các chỉnh sửa mới trong trình duyệt cần xuất lại.

Các đoạn mới kết hợp nhân vật/đạo cụ riêng với ảnh cảnh đã có. Phần ngân sách tăng dần theo từng khoản, có biểu đồ đúng tỉ lệ; các cảnh dùng ảnh tổng thể chỉ chỉnh chữ và toàn bộ lớp ảnh, chưa tách mọi chi tiết bên trong. Giữ Times New Roman. Có thể bật phụ đề trong Studio, bản MP4 mặc định không chèn phụ đề.

Dựng lại dữ liệu: `python3 tools/build-full-video.py`. Dựng MP4 với đường dẫn xuất mới theo hướng dẫn README gốc, thay đầu vào bằng `videos/001-100k-salary/review/project.json`. Không chạy lại công cụ tạo dữ liệu nếu đang giữ bản sửa thủ công chưa sao lưu.

## Bản duyệt mở đầu

Đã dựng đoạn 0–40,5 giây, gồm 8 cảnh, kết sau câu “before you buy a single thing”, trước “Meet Alex”. Đây là bản để duyệt phong cách và nhịp, chưa phải toàn bộ video.

- `intro/project.json`: dự án video với các lớp chữ, nhân vật, đạo cụ và thời điểm xuất hiện.
- `intro/props.png`: bảng đạo cụ nền trong suốt bổ sung cho điện thoại ngân hàng, đồ ăn mang về và lốp xe xẹp.
- `intro/voiceover.mp3`: bản cắt 40,5 giây từ WAV; tệp WAV gốc được giữ nguyên.
- `intro/alignment.json`: mốc từ nhận dạng bằng faster-whisper base.en, đã so với phần mở đầu của lời thoại. Mốc tự động có sai số, cần nghe khi duyệt.
- `intro/captions.vtt`: phụ đề tiếng Anh cho đoạn mở đầu.
- `exports/intro-v01.mp4`: bản MP4 xem thử 1920×1080, 30 fps, có giọng đọc; không có nhạc nền.

Trong [Credit Studio Video](../../video/), chọn cảnh ở thanh bên hoặc timeline; phát/tạm dừng, tua, chỉnh chữ/màu/vị trí/kích thước/thời lượng và kiểu xuất hiện. Các tư thế và đạo cụ của cả 8 cảnh là lớp ảnh riêng, lấy từ vùng ảnh trong bảng tài nguyên; chữ, điện thoại, đồ ăn và lốp xe có thể chỉnh riêng. Các nét bên trong một tư thế/đạo cụ chưa được tách tiếp và chưa có chuyển động khớp tay/chân.

Bản sửa tự lưu trong trình duyệt. **Lưu JSON** để gửi bản sửa lại; các sửa đổi không tự đẩy lên GitHub. **Xuất WebM** tạo video từ bản đang chỉnh, theo thời gian thực; giữ tab mở khi xuất. **MP4 bản nháp gốc** luôn là bản gốc, không tự chứa các sửa đổi mới. Dùng Chrome hoặc Edge mới để xuất WebM; có thể bật phụ đề tiếng Anh trong phần xem trước và bản xuất.

Chữ trong video, phụ đề, giao diện và các dự án cảnh hiện dùng Times New Roman. Website ưu tiên font có sẵn trên thiết bị và dùng font serif dự phòng nếu thiếu. MP4 đã được dựng lại bằng Times New Roman thực tế. Hình mẫu có chữ vẽ tay đã nằm trong PNG tham khảo không phải lớp chữ của bản dựng.

Đổi thời lượng hoặc thứ tự cảnh sẽ làm thay đổi nhịp với audio; hãy tua và nghe lại. Thay audio sẽ bỏ phụ đề cũ để tránh hiển thị lời không khớp. Dự án JSON lưu đường dẫn tài nguyên của kho mã (hoặc nhúng audio khi tải từ máy), nên mở bằng website này hoặc một bản sao đầy đủ của kho mã.

## Bộ hình

- `images/scenes/`: 16 ảnh cảnh chính, hai cảnh cho mỗi phần lời thoại.
- `images/sheets/`: 3 bảng PNG nền trong suốt, gồm 4 tư thế Alex và 24 nhóm đạo cụ.
- `projects/`: 16 dự án JSON, mở bằng nút **Mở dự án** trong Credit Studio để sửa chữ và số.
- `artwork.json`: danh sách cảnh, câu bắt đầu trong lời thoại, vị trí lớp chữ và liên kết tệp.

Ảnh cảnh gốc là PNG 1672 × 941, bố cục gần 16:9. Trang dự án là 1920 × 1080; ảnh gốc không được nâng độ phân giải hoặc chỉnh sửa trong bước đóng gói. Nhân vật và đồ vật trong mỗi ảnh cảnh là một lớp ảnh, chưa tách riêng. Các bảng tài nguyên là PNG nền trong suốt, chưa tách từng vật thể hoặc gắn khớp hoạt hình.

Chữ và số tài chính được giữ riêng trong JSON để sửa được và tránh sai số trong ảnh tạo sinh. Mở trang xem bộ hình để thấy phiên bản có lớp chữ; PNG gốc chưa có các lớp chữ đó.

Để đóng gói lại JSON sau khi cập nhật lớp chữ trong `artwork.json`, chạy `python3 tools/build-video-projects.py` từ thư mục gốc kho mã. Lệnh chỉ đóng gói ảnh và chữ, không tạo lại hoặc sửa ảnh.

## Trạng thái

Đã có bộ hình, công cụ chỉnh video và bản duyệt đầy đủ 64 cảnh / 486,75 giây. Chờ người dùng duyệt và yêu cầu chỉnh tiểu tiết; giữ nguyên WAV gốc và MP4 mở đầu.

## Quy trình bàn giao

1. Tạo giọng đọc từ `script.md`, đọc phần tiếng Anh, bỏ qua tiêu đề.
2. Tải audio vào thư mục `audio/`, commit lên GitHub.
3. Báo trong cuộc trò chuyện sau khi tải xong để kiểm tra và bắt đầu căn cảnh.
4. Sau này giữ hình, dự án dựng và bản xuất trong thư mục riêng của video này khi có các tệp thực tế.

Các số liệu trong lời thoại là tình huống minh họa, không phải mức thuế hay chi phí áp dụng cho mọi người.
