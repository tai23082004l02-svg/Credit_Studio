# Video 004 — Why Living Alone Has Become So Expensive

Người dùng đã chốt chủ đề tài chính và phong cách phim tài liệu tài chính thu nhỏ: nền giấy kem, ảnh cắt ghép có viền, đỏ trầm, chữ Times New Roman. Khán giả Mỹ, lời thoại tiếng Anh Mỹ. Không áp mặc định Alex vẽ tay của ba video trước vào toàn bộ bộ hình mới; Alex trong lời thoại là nhân vật ngân sách hư cấu.

- [Lời thoại v01](script.md): 8 phần; người dùng đã yêu cầu triển khai hình từ bản này.
- [Chỉ lời đọc để copy vào TTS](narration.txt): bỏ toàn bộ tiêu đề và ghi chú.
- [Nguồn và phép tính](sources.md): tách dữ liệu lịch sử khỏi tình huống giả định.
- [Nơi bàn giao âm thanh](audio/README.md).

Lời đọc có khoảng **1.279 từ**. Đã nhận WAV dài **577,5 giây (9 phút 37,5 giây)** qua chat và dựng theo thời lượng thực tế.

## Bản duyệt đầy đủ v01

**91 cảnh · 577,5 giây · 1920×1080 / 30 fps**, chờ người dùng duyệt, chưa phải bản cuối.

- [Mở bản dựng trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-004&tab=video) · [MP4 v01](exports/full-review-v01.mp4) · [Timecode](review/README.md) · [Kiểm tra thực tế](review/validation.json).
- Dự án chỉnh được `review/project.json`, revision `living-alone-review-v01`. **29 lớp chuyển động nội dung trong 15 cảnh**, cùng các thẻ hiện theo lời đọc: chia rent/internet, thanh và số đồng bộ, chênh $630/tháng thành $7.560/năm, lịch hai tháng $3.720, tỷ lệ hộ, phong bì thu nhập và đặt cọc.
- WAV gốc `audio/tts_20261022_133142_ba54ee.wav`, **27.720.044 byte**, PCM 16-bit / 24 kHz / mono, giữ nguyên. `review/voiceover.mp3` là dẫn xuất chuẩn hóa âm lượng; không cắt nội dung hoặc đổi tốc độ, chưa nhạc nền.
- Nét collage và chữ Times New Roman giữ đúng bộ hình. Minh họa tổng thể vẫn là một lớp ảnh; đạo cụ, chữ/số và thanh chỉnh riêng. Chưa rig khớp nhân vật.
- `review/alignment.json`, `captions.vtt`, `shot-plan.json`, `motion-plan.json`, `source.json` ghi căn từ và nguồn. Mốc từ tự động có nội suy token số và sai số mức từ. Phụ đề mặc định tắt trong MP4, bật được ở Studio.
- Trước khi chuyển bản bảng hình cũ sang review, Studio lưu draft cũ nguyên vẹn vào **Bản lưu trước cập nhật**; tải JSON được và có trong `.credit.json`. Các sửa trên review, revision lạ và dự án khôi phục được giữ. Chưa ghép các sửa riêng của người dùng chỉ có trong IndexedDB.

Tạo lại dữ liệu: `python3 tools/build-living-alone-video.py`, mặc định chặn ghi đè; chỉ `--force` sau khi sao lưu sửa tay. Công cụ không ghi đè WAV, bộ hình hoặc MP4. Xuất theo `tools/render-intro.cjs` với tên tệp mới; giữ v01 cho lần xuất sau.

## Bộ hình v01 đã có

[Mở trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-004&tab=images) · [Xem toàn bộ hình](https://tai23082004l02-svg.github.io/Credit_Studio/videos/004-living-alone/) · [Phân cảnh và cách cắt](storyboard.md) · [Kết quả kiểm tra](artwork-validation.json).

- **16 khung PNG 1920×1080 và 16 thiết kế JSON chỉnh được**: 8 minh họa collage mới + 8 bảng thông tin. Ảnh nguồn ở `images/illustrations/`, thiết kế ở `projects/`, bản khung xuất ở `images/scenes/`.
- **2 sheet trong suốt 4×2 ô**, bản hướng dẫn có nhãn, **16 đạo cụ PNG rời** có lề trong suốt 32 px. `images/crop-map.json` ghi cả hệ tọa độ nguồn và atlas.
- `image-generation.json` ghi nguồn tạo sinh, prompt/ghi chú và SHA-256; bản nguồn đã chọn giữ nguyên. Hình AI chỉ để minh họa, không phải chứng cứ ảnh tư liệu.
- **finance-004** được đăng ký trên trang chủ, nay mở review đầy đủ ở trên. `storyboard/project.json` vẫn là bảng hình im lặng **96 giây** cũ, revision `living-artwork-board-v01`, chỉ dùng duyệt bố cục trước audio. Các lớp thẻ/chữ/số/đạo cụ chỉnh riêng; minh họa `a` mỗi cảnh vẫn là một ảnh tổng thể.
- Times New Roman thực, vùng tiêu đề tách khỏi minh họa, nhân vật 06a không bị che/cắt đầu, tay hoặc chân. Thẻ hình và nhãn căn giữa. 16 đạo cụ mới có trong kho chung, tổng 89 mục.

Đóng gói lại: `node tools/build-living-alone-artwork.cjs`, cần server cục bộ và font theo README gốc. Mặc định chặn ghi đè; chỉ dùng `--force` sau khi sao lưu sửa tay. Công cụ cắt/đóng gói nguồn đã tạo, không gọi lại AI hoặc sửa audio. Kiểm tra: `node tests/living-alone-artwork.cjs`.

Tiếp theo: người dùng duyệt MP4 v01, góp ý kèm timecode. Giữ mọi tài nguyên video 001–003 và các bản cũ. Các sửa riêng trong Studio lưu ở IndexedDB; nhận `.credit.json`/JSON trước khi cần tiếp tục từ chúng.

## Kế hoạch dựng và nguồn nhận audio

Sau lần chưa tìm thấy audio trên main, người dùng gửi WAV trực tiếp qua chat vì tệp lớn. Đã lưu nguyên bản vào `audio/`, giữ tên gốc và hash; không cần người dùng tải lại qua giao diện GitHub.

Đã dùng [91 cảnh và mốc lời kể](edit-plan.json) làm cơ sở căn theo WAV. Tệp này là kế hoạch, không phải JSON video để nhập Studio; bản dựng thật ở `review/project.json`, mốc thực tế ở `review/shot-plan.json`. Bảng hình 96 giây và các thiết kế gốc giữ nguyên.
