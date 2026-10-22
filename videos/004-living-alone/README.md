# Video 004 — Why Living Alone Has Become So Expensive

Người dùng đã chốt chủ đề tài chính và phong cách phim tài liệu tài chính thu nhỏ: nền giấy kem, ảnh cắt ghép có viền, đỏ trầm, chữ Times New Roman. Khán giả Mỹ, lời thoại tiếng Anh Mỹ. Không áp mặc định Alex vẽ tay của ba video trước vào toàn bộ bộ hình mới; Alex trong lời thoại là nhân vật ngân sách hư cấu.

- [Lời thoại v01](script.md): 8 phần; người dùng đã yêu cầu triển khai hình từ bản này.
- [Chỉ lời đọc để copy vào TTS](narration.txt): bỏ toàn bộ tiêu đề và ghi chú.
- [Nguồn và phép tính](sources.md): tách dữ liệu lịch sử khỏi tình huống giả định.
- [Nơi bàn giao âm thanh](audio/README.md).

Lời đọc có khoảng **1.279 từ**, dự kiến **8–10 phút** (khoảng 8,3–8,8 phút ở 145–155 từ/phút, chưa tính khoảng nghỉ); thời lượng thật phụ thuộc audio.

## Bộ hình v01 đã có

[Mở trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-004&tab=images) · [Xem toàn bộ hình](https://tai23082004l02-svg.github.io/Credit_Studio/videos/004-living-alone/) · [Phân cảnh và cách cắt](storyboard.md) · [Kết quả kiểm tra](artwork-validation.json).

- **16 khung PNG 1920×1080 và 16 thiết kế JSON chỉnh được**: 8 minh họa collage mới + 8 bảng thông tin. Ảnh nguồn ở `images/illustrations/`, thiết kế ở `projects/`, bản khung xuất ở `images/scenes/`.
- **2 sheet trong suốt 4×2 ô**, bản hướng dẫn có nhãn, **16 đạo cụ PNG rời** có lề trong suốt 32 px. `images/crop-map.json` ghi cả hệ tọa độ nguồn và atlas.
- `image-generation.json` ghi nguồn tạo sinh, prompt/ghi chú và SHA-256; bản nguồn đã chọn giữ nguyên. Hình AI chỉ để minh họa, không phải chứng cứ ảnh tư liệu.
- **finance-004** được đăng ký trên trang chủ. `storyboard/project.json` là bảng hình im lặng **96 giây**, revision `living-artwork-board-v01`; chưa căn thời gian lời đọc, chưa có MP4 hoặc audio. Các lớp thẻ/chữ/số/đạo cụ chỉnh riêng; minh họa `a` mỗi cảnh vẫn là một ảnh tổng thể.
- Times New Roman thực, vùng tiêu đề tách khỏi minh họa, nhân vật 06a không bị che/cắt đầu, tay hoặc chân. Thẻ hình và nhãn căn giữa. 16 đạo cụ mới có trong kho chung, tổng 89 mục.

Đóng gói lại: `node tools/build-living-alone-artwork.cjs`, cần server cục bộ và font theo README gốc. Mặc định chặn ghi đè; chỉ dùng `--force` sau khi sao lưu sửa tay. Công cụ cắt/đóng gói nguồn đã tạo, không gọi lại AI hoặc sửa audio. Kiểm tra: `node tests/living-alone-artwork.cjs`.

Tiếp theo: người dùng duyệt hình, cung cấp WAV gốc trong `audio/`, rồi căn dựng đầy đủ với chuyển động theo lời kể. Chưa nhạc nền hoặc rig khớp. Giữ mọi tài nguyên video 001–003. Các sửa riêng trong Studio lưu ở IndexedDB; nhận `.credit.json`/JSON trước khi cần tiếp tục từ chúng.
