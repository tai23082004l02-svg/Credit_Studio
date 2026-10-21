# Bàn giao Credit Studio cho phiên chat tiếp theo

Cập nhật: 2026-10-21. Đây là ghi chú tiếp nối công việc, không phải bản sao toàn bộ lịch sử chat. Kiểm tra trạng thái Git và các thay đổi mới trước khi thực hiện.

## Mục tiêu và quyết định đã chốt

- Người dùng giao tiếp bằng tiếng Việt, làm video YouTube tài chính cho khán giả Mỹ; lời đọc bằng tiếng Anh Mỹ.
- Người dùng cung cấp âm thanh (có thể do AI đọc). Trợ lý chuẩn bị lời thoại, hình ảnh, phân cảnh, dựng video và bản duyệt chỉnh được trong Credit Studio; người dùng sửa tiểu tiết trước bản xuất cuối.
- Phong cách đã chọn: nhân vật nét vẽ 2D, biểu đồ và biểu tượng đơn giản. Nhân vật Alex có tóc nâu sẫm, áo kem xắn tay, quần xanh teal; nền kem, nét than, xanh tiền, coral cho chi phí và điểm nhấn vàng.
- **Giữ Times New Roman cho toàn bộ chữ**, bao gồm giao diện, chữ trong hình và phụ đề. Website có font serif dự phòng khi thiết bị thiếu font; bản MP4 hiện có được dựng bằng Times New Roman thực.
- Dùng online, quản lý nhiều dự án qua một địa chỉ: https://tai23082004l02-svg.github.io/Credit_Studio/ . Không yêu cầu người dùng nhớ các URL công cụ riêng.

## Website và lưu dữ liệu

Ứng dụng tĩnh HTML/CSS/JavaScript, không có backend hay tài khoản. GitHub Pages triển khai từ nhánh `main`, thư mục gốc. Push vào `main` kích hoạt triển khai; kiểm tra kết quả GitHub Actions trước khi khẳng định bản sửa đã lên website.

Trang chủ có danh sách dự án và các tab Tổng quan, Dựng video, Hình ảnh, Âm thanh & tài liệu. Có tạo dự án, tìm kiếm, đổi tên, thêm tệp và sao lưu/khôi phục `.credit.json`. `/video/` và `/design/` vẫn mở trực tiếp được nhưng là công cụ bên trong luồng chung.

**Dự án tự tạo, bản sửa và tệp tải lên qua website lưu trong IndexedDB của trình duyệt đó; không tự đồng bộ lên GitHub hoặc thiết bị khác.** Chat mới không truy cập được những bản sửa này chỉ bằng việc đọc repo. Khi cần chúng, người dùng dùng **Sao lưu dự án** rồi cung cấp tệp `.credit.json`. Khôi phục tạo dự án riêng, không ghi đè dự án hiện có. Tài nguyên xuất bản sẵn vẫn được tham chiếu từ website.

`projects.json` đăng ký các dự án xuất bản. Dự án tài chính hiện có ID ổn định `finance-001`. Mỗi dự án mới cần thư mục riêng trong `videos/` và mục đăng ký riêng. Giữ khả năng đọc bản sao lưu, dữ liệu IndexedDB và các khóa localStorage cũ.

## Video đầu tiên: trạng thái thực tế

Tên: **Why You Feel Broke on a $100,000 Salary**.

Thư mục: `videos/001-100k-salary/`.

- `script.md`: lời thoại tiếng Anh chia 8 phần. Các con số là ví dụ minh họa, không phải kết quả thuế phổ quát.
- `audio/Why You Feel Broke on a $100,000 Salary.wav`: âm thanh gốc do người dùng cung cấp, dài khoảng 486,75 giây (8 phút 6,75 giây), PCM mono 24 kHz. **Bảo toàn tệp gốc.**
- `images/scenes/`: 16 ảnh cảnh PNG; `images/sheets/`: 3 bảng tài nguyên nhân vật/đồ vật có nền trong suốt.
- `projects/`: 16 thiết kế JSON có ảnh nền và lớp chữ/số chỉnh được; `artwork.json` và `storyboard.md` mô tả bộ hình/phân cảnh. Ảnh cảnh là ảnh phẳng, không phải mọi chi tiết đều tách lớp.
- `intro/project.json`: bản dựng mở đầu **40,5 giây**, 1920×1080, 30 fps, 8 cảnh có lớp nhân vật/đồ vật/chữ và chuyển động đơn giản.
- `intro/voiceover.mp3`, `alignment.json`, `captions.vtt`: đoạn âm thanh dẫn xuất, mốc từ tự động và 14 đoạn phụ đề. Xem `intro/README.md` để biết thời điểm cụ thể.
- `exports/intro-v01.mp4`: bản duyệt H.264/AAC 40,5 giây, Times New Roman, chưa thêm nhạc nền.

Bản mở đầu kết thúc sau câu “before you buy a single thing”, trước “Meet Alex.” Người dùng đã đánh giá tốt bản duyệt và yêu cầu đổi font, sau đó gộp công cụ quản lý. **Ngày 2026-10-21 đã dựng tiếp toàn bộ thành bản duyệt đầy đủ; xem cập nhật bên dưới.** Chuyển động hiện là fade/slide/pop/drift của các lớp; chưa có rig khớp nhân vật.

## Cập nhật bản dựng đầy đủ — 2026-10-21

Người dùng đã yêu cầu dựng tiếp. Đã dựng toàn bộ **486,75 giây / 64 cảnh**, nối nguyên 8 cảnh intro với 56 cảnh mới. Bản duyệt chỉnh được: `review/project.json`; nguồn âm thanh MP3 toàn bộ: `review/voiceover.mp3`; mốc nhận dạng: `review/alignment.json`; phụ đề: `review/captions.vtt`. Tất cả nằm trong `videos/001-100k-salary/`. `review/README.md` có bảng timecode từng cảnh. Bản MP4 để duyệt: `exports/full-review-v01.mp4` (1920×1080, 30 fps, Times New Roman, lời đọc gốc, chưa nhạc nền). WAV và bản intro cũ được bảo toàn.

`projects.json` vẫn dùng ID `finance-001`, trỏ bản video và MP4 đầy đủ. Trang chủ/Tổng quan xem MP4 mới, tab Dựng video chỉnh timeline. Đã sửa lỗi người dùng thấy Tổng quan 8 phút nhưng trình dựng chỉ 40,5 giây: ưu tiên bản lưu intro cũ, và thông báo mở bản mới bị ẩn trên mobile.

Trình dựng nay tự chuyển riêng `finance-001` từ revision `intro-v01` sang `full-review-v01`. Trước khi chuyển, lưu nguyên vẹn bản cũ vào document slot `history-<uuid>` trong cùng giao dịch IndexedDB với việc thay main; lỗi giao dịch không được làm mất bản cũ. Mục **Bản lưu trước cập nhật** tải từng JSON cũ, hiển thị cả trên điện thoại; `.credit.json` chứa cả lịch sử. Giữ localStorage gốc. Các bản cùng revision full được giữ nguyên khi reload, không tạo thêm lịch sử hoặc reset sửa đổi. Nếu không tải được bản mới, vẫn mở bản cũ. Dự án khác, bản khôi phục và revision khác không tự chuyển. Module/iframe đã đổi tham số phiên bản để bỏ cache ứng dụng cũ.

Các cảnh mới kết hợp nhân vật/đạo cụ tách lớp, thẻ chữ/số, biểu đồ ngân sách đúng tỉ lệ và ảnh cảnh có sẵn. Một số cảnh dùng ảnh tổng thể, không phải mọi chi tiết của ảnh đều chỉnh riêng được. Mốc từ tự động bằng faster-whisper base.en được ánh xạ lại script để giữ đúng chữ; có sai số ở mức từ. Các nhóm đạo cụ quan trọng xuất hiện theo mốc câu. Phụ đề mặc định tắt trong MP4; bật được trong Studio. Chưa có rig khớp hoặc nhạc nền.

Công cụ tái tạo: `tools/build-full-video.py` đọc script, mốc nhận dạng và tài nguyên, tạo lại JSON/VTT/timecode; không chỉnh WAV hay intro. Không chạy lại nếu có bản sửa tay chưa sao lưu. Dựng MP4 bằng `tools/render-intro.cjs` với đầu vào `review/project.json` và đường dẫn xuất mới.

Bước tiếp theo: người dùng xem **bản duyệt đầy đủ v01**, cung cấp các chi tiết cần sửa (tốt nhất kèm timecode). Nếu đã sửa trong trình duyệt, cần nhận `.credit.json` hoặc JSON video trước khi trợ lý tiếp tục từ các sửa đổi đó. Chưa coi bản duyệt là bản cuối đã được người dùng duyệt.

## Mã nguồn và kiểm tra

- `index.html`, `assets/js/hub.js`, `assets/css/hub.css`: trang quản lý và điều hướng chung.
- `assets/js/workspace-store.js`: IndexedDB, danh mục, sao lưu/khôi phục, chuyển dữ liệu cũ.
- `design/index.html`, `assets/js/app.js`, `assets/js/design-model.js`: trình ảnh và kiểm tra dữ liệu thiết kế.
- `video/editor.js`, `video/engine.js`, `video/webm.js`: trình video, bộ vẽ dùng chung và xuất WebM.
- `tools/build-video-projects.py`, `tools/build-intro-project.py`, `tools/build-full-video.py`: tạo lại thiết kế/bản intro từ cấu hình; đọc hướng dẫn trước khi chạy vì có thể thay JSON hiện có.
- `tools/render-intro.cjs`: dựng MP4 từ JSON bằng bộ vẽ dùng chung, Playwright và FFmpeg; dùng đường dẫn xuất mới để giữ bản cũ.

Đọc README để chạy máy chủ, kiểm tra và dựng MP4. Ứng dụng không cần thư viện production. Bộ kiểm tra trình duyệt/công cụ MP4 cần Playwright, Chromium và FFmpeg. Font cục bộ ở môi trường trước nằm ngoài repo tại `/workspace/shared/credit-studio-fonts`; máy mới cần kiểm tra lại, không giả định tệp đó luôn tồn tại. Không đưa tệp font độc quyền vào website/repo.

Đã kiểm tra ở lần triển khai gộp công cụ: 8 bài unit test cho engine/WebM; bộ Playwright `tests/video-editor.cjs` và `tests/project-workspaces.cjs` (tách dữ liệu dự án, lưu lại, âm thanh, xuất WebM, sao lưu/khôi phục và mobile); MP4 thực bằng FFmpeg/ffprobe. GitHub Pages triển khai thành công cho commit `0f542fa`; tài nguyên online đã đối chiếu qua HTTPS. Đây là kết quả của phiên trước, không thay cho kiểm tra phù hợp với thay đổi mới.

Kiểm tra bản đầy đủ ngày 2026-10-21: 8 unit test và cả hai bộ Playwright đã qua, gồm bảo toàn/sao lưu bản sửa cũ, hủy mở bản mới, xác nhận mở và reload bản đầy đủ. Kiểm tra thực tế toàn bộ bố cục chữ bằng Times New Roman, tua audio ở 8 phần, phát đoạn kết, timeline và mobile đã qua. MP4 đã giải mã toàn bộ bằng FFmpeg không lỗi; âm thanh đối chiếu WAV ở giây 10/200/480 có tương quan >0,9999. MP4 dài 486,766667 giây do làm tròn khung 30 fps; audio/timeline 486,75 giây. Xem `review/validation.json` và `review/source.json`. Trạng thái triển khai cần kiểm tra theo commit mới nhất trên GitHub Actions.

Kiểm tra bản sửa mở video: Playwright tái hiện bản intro đã chỉnh trong localStorage/IndexedDB rồi xác nhận tự mở 64 cảnh; JSON cũ được tải lại nguyên vẹn, backup chứa main mới và lịch sử, sửa bản đầy đủ rồi reload vẫn giữ, lịch sử không nhân đôi. Kiểm tra mở trực tiếp `/video/` chỉ có localStorage, lỗi mạng tải bản mới và thử lại thành công. Không cần dựng lại MP4 vì chỉ sửa cách chọn bản dự án.

## Cách tiếp tục trong chat mới

Chọn/đính kèm repo `tai23082004l02-svg/Credit_Studio`, yêu cầu đọc `AGENTS.md`, tài liệu này và README. Chat mới không tự nhớ lịch sử chat cũ. Nếu chưa có quyền truy cập repo, cần kết nối/chọn repo trước. Nếu công việc phụ thuộc bản sửa chỉ có trên trình duyệt, cung cấp bản sao lưu dự án; chỉ GitHub là chưa đủ.
