# Video 002 — The Monthly Payment Trap: How “Affordable” Keeps You Broke

[Mở dự án trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-002) · [Xem toàn bộ hình](https://tai23082004l02-svg.github.io/Credit_Studio/videos/002-monthly-payment-trap/) · [Lời thoại](script.md) · [Phân cảnh](storyboard.md).

## Trạng thái

Đã chuẩn bị trọn bộ hình cho 8 phần lời thoại: **16 khung hình 1920×1080**, gồm 8 cảnh minh họa gốc và 8 bố cục thông tin dựng từ lớp riêng. Có 16 dự án ảnh chỉnh được, 3 sheet nền trong suốt, 3 bản hướng dẫn sheet có ô/nhãn, **6 tư thế Alex và 24 đạo cụ mới**, 30 PNG tách sẵn và tọa độ cắt. Đã đăng ký dự án `finance-002`, giữ nguyên dự án `finance-001`.

**Đã nhận WAV và dựng bản duyệt đầy đủ v01: 495,475 giây (8 phút 15,475 giây), 79 cảnh.** [Mở bản dựng trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-002&tab=video) · [MP4 đầy đủ v01](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/67f69d7d870311eb7258fa56a06580329b576378ae3420c8307722efb20e6489.mp4) · [Timecode 79 cảnh](review/README.md).

WAV gốc ở `audio/monthly-payment-trap-voiceover.wav` được giữ nguyên. `review/voiceover.mp3` là bản dẫn xuất đã nâng âm lượng, khoảng −16,7 LUFS, không đổi tốc độ hoặc cắt nội dung. Chưa thêm nhạc nền, chưa rig chuyển động khớp. Đây là bản duyệt để góp ý, chưa phải bản cuối đã duyệt.

`storyboard/project.json` vẫn giữ nguyên bảng hình tĩnh cũ 16 cảnh × 6 giây = 96 giây để tham khảo; `review/project.json` mới là bản dựng theo audio. Khi Studio nhận bản đầy đủ, bảng hình cũ trong trình duyệt được lưu nguyên vẹn vào **Bản lưu trước cập nhật** trước khi chuyển; bản sao lưu `.credit.json` chứa cả lịch sử. Các chỉnh sửa trên revision đầy đủ được giữ khi reload.

## Tệp và mức chỉnh sửa

- `script.md`: lời thoại tiếng Anh đã được người dùng chấp thuận, giữ nguyên 8 phần.
- `artwork.json`: 16 khung hình, câu bắt đầu, liên kết thiết kế và hướng chuyển động.
- `images/illustrations/`: 8 PNG minh họa gốc được tạo mới theo Alex và bảng màu hiện có; hình trong mỗi PNG là ảnh tổng thể.
- `images/scenes/`: 16 PNG khung hoàn chỉnh để xem/tải, có chữ Times New Roman và các phép tính được dựng bằng lớp riêng trước khi xuất.
- `projects/`: 16 JSON thiết kế ảnh; chữ/số và các lớp của cảnh thông tin chỉnh riêng được. Ảnh minh họa tổng thể chưa tách mọi nét thành khớp.
- `images/sources/`: 3 sheet nguyên bản tạo sinh được giữ lại.
- `images/sheets/`: 3 atlas sản xuất đã đưa từng mục vào ô đều có khoảng đệm; 3 `*-guide.png` có viền ô, số và tên để tìm nhanh. Chỉ dùng atlas PNG trong suốt hoặc PNG riêng khi dựng; bản guide có nhãn không phải sprite nền trong suốt.
- `images/cutouts/`: 30 PNG riêng; giữ pixel của vùng cắt nguồn, thêm 32 px khoảng đệm trong suốt mỗi phía, không nâng độ phân giải nội dung.
- `images/crop-map.json`: tọa độ `[x, y, width, height]` theo pixel, gốc ở góc trái trên; chứa ô trên atlas, vùng nét và vùng cắt trên sheet nguồn.
- `asset-layout.json`: cấu hình cảnh, nguồn, phép cắt để tái tạo các tệp dẫn xuất.
- `storyboard/project.json`: bảng hình 16 cảnh dùng bộ vẽ Studio, chưa audio, không phải video cuối.
- `audio/`: WAV gốc đã nhận, giữ nguyên 24 kHz mono 16-bit.
- `review/`: dự án 79 cảnh, audio MP3 dẫn xuất, mốc từ, phụ đề, timecode và kiểm tra bản dựng.
- `exports/full-review-v01.mp4`: MP4 duyệt 1920×1080, 30 fps, H.264/AAC.

30 mục mới có ID ổn định `mpt-*`, được thêm vào Kho đạo cụ chung bằng tham chiếu atlas. Các ID/đường dẫn cũ được giữ. Tổng kho hiện 61 mục: 51 đạo cụ, 10 tư thế Alex. Có thể tải PNG riêng ở thư viện này hoặc tải một ô qua Kho đạo cụ.

## Quy tắc bố cục

Times New Roman cho mọi lớp chữ và bản hướng dẫn. Tiêu đề nằm ở phần trên; vùng minh họa của 8 cảnh vẽ nằm hoàn toàn từ y=254 trở xuống, không có tấm nền phủ lên đầu nhân vật. Ảnh luôn giữ tỉ lệ. Các thẻ căn giữa cả hình và từng dòng nhãn; khoảng cách trong nhóm đồng đều. PNG tách sẵn và atlas giữ đủ tóc, tay, giày.

Ở giai đoạn dựng chuyển động tiếp theo, tiếp tục kiểm tra khung tổng hợp lúc vào, giữa và ra cảnh: khoảng đệm hiện tại không cho phép tùy ý zoom/crop hoặc kéo tiêu đề đè lên nhân vật.

## Kiểm tra số liệu

- Điện thoại: $37.50 × 24 = $900, chỉ khi không có lãi/phí.
- $525 + $37.50 + $90 + $120 + $45 = $817.50 trong tháng minh họa. BNPL là tổng các kỳ đến hạn trong tháng này, không phải khoản cố định mãi mãi; đăng ký dịch vụ có thể hủy không đồng nghĩa với dư nợ vay.
- Ví dụ tài trợ: $75 × 24 = $1,800; $60 × 36 = $2,160; ít hơn $15/tháng nhưng tổng cao hơn $360 và lâu thêm 12 tháng. Không phải đề nghị vay thực tế.
- Chi phí sửa xe $600 là khoản bất ngờ riêng, không gộp vào $817.50.
- Các đường lịch ở ảnh 04a là ẩn dụ; dùng 04b cho số tiền/kỳ hạn chính xác.

## Tái tạo

Không chạy lại trên thiết kế đã sửa mà chưa sao lưu. Website không cần thư viện; công cụ tạo atlas/PNG cần Node, Playwright/Chromium, máy chủ cục bộ và Times New Roman có bản quyền sử dụng hợp lệ trên máy dựng.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Chuẩn bị font in đậm tại `work/monthly-payment-trap/timesbd.ttf` (tệp tạm, không commit). Chạy `node tools/build-monthly-payment-artwork.cjs`; khi tệp dẫn xuất đã tồn tại, phải sao lưu rồi mới dùng `--force`. `CREDIT_STUDIO_URL` thay địa chỉ máy chủ, `CREDIT_CHROMIUM` chọn Chromium khi cần. Atlas được đóng gói bằng browser canvas; pixel nguồn được giữ và không đưa font độc quyền lên GitHub.

## Dựng lại bản video

Không dùng công cụ tạo hình để tái tạo bản dựng. `python3 tools/build-monthly-payment-video.py` đọc script, mốc nhận dạng, asset-layout và tài nguyên có sẵn để tạo bản review; mặc định chặn ghi đè, chỉ dùng `--force` sau khi sao lưu bản sửa tay. Dựng MP4 bằng `tools/render-intro.cjs` theo README gốc, đầu vào `review/project.json`, chọn tên xuất mới để bảo toàn v01.

## Bước tiếp theo

Người dùng xem bản duyệt đầy đủ và gửi góp ý kèm timecode. Nhận `.credit.json` hoặc JSON video nếu người dùng đã sửa trong Studio trước khi tiếp tục từ bản sửa đó. Khi chỉnh chuyển động, tiếp tục kiểm tra nhân vật lúc vào/giữa/ra cảnh, giữ font Times New Roman và căn giữa hình/nhãn; bản xuất tiếp theo dùng tên mới.
