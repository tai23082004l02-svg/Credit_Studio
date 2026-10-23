# Video 005 — Your Mortgage Payment Is Only the Beginning

**Bản duyệt đầy đủ v01: 88 cảnh /9 phút 26,45 giây**, chờ người dùng duyệt. Đồ họa nhiều lớp giấy kem/đỏ trầm/sage, **Times New Roman**, bốn nhóm minh họa Jamie; 40 lớp chuyển động nội dung trong 19 cảnh, cùng các thẻ hiện theo lời đọc.

[Mở bản dựng trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-005&tab=video) · [Tổng quan và MP4](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-005) · [MP4 v01](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/a7a917bc941d1ba28419b3f552d6a412207d6b076b7c4a133084bb5a32c5cf6e.mp4) · [JSON chỉnh được](review/project.json) · [Timecode/giới hạn](review/README.md).

Kịch bản v01 đã duyệt, 1241 từ /8 phần; giữ nguyên lời thoại và WAV gốc 566,45 giây /27.189.644 byte. MP3 dùng cho bản dựng đã chuẩn hóa âm lượng, không cắt lời hoặc thay tốc độ. WAV/MP3 được Actions đưa lên R2, tải lại xác minh SHA-256 và kiểm tra public Range/CORS; không commit audio lớn vào Git. [Metadata nguồn](audio/source.json).

Một bản dựng chính ở review/project.json; **samples/project.json (3 cảnh /86,8 giây) giữ nguyên byte**. Khi mở finance-005, bản mẫu cũ đã chỉnh được lưu nguyên vẹn vào **Bản lưu trước cập nhật** trong cùng giao dịch IndexedDB trước khi mở review. Lịch sử tải JSON được và có trong .credit.json. Không reset sửa hiện tại trên review, revision lạ hoặc bản khôi phục. Review mới dựng từ tài nguyên repo, chưa ghép các sửa riêng của người dùng trong trình duyệt; muốn tiếp tục từ chúng cần backup.

- [Kịch bản](script.md), [lời đọc](narration.txt), [nguồn/phép tính](sources.md).
- [Storyboard](storyboard.md), [88 cảnh](review/shot-plan.json), [chuyển động](review/motion-plan.json), [phụ đề EN](review/captions.vtt), [kiểm tra bố cục](review/layout-validation.json).
- [Audio gốc](audio/README.md), [source/hash/crop map minh họa](images/image-generation.json).

Chuyển động gồm ngân sách 1517→2017 bills và 2267 gồm repair savings, cash75000→4000/downpayment60000 sang equity, 12 lần chuyển250 thành3000, quỹ500 so với bill3000/gap2500, principal/interest tháng đầu và lịch amortization nén. Số/thanh dùng cùng mốc; không cộng trùng escrow hoặc repair expense. Giữ ví dụ hư cấu và giả định6,5% fixed nominal /30 năm; không gán mức này cho thị trường hiện tại hoặc khuyến nghị chung. Không thêm thu nhập, giá nhà tăng, nhạc nền hay rig khớp nhân vật.

Bốn nhóm Jamie dùng trong timeline và kho93 mục: nhận chìa khóa, hóa đơn, máy giặt, so sánh giấy tờ. Giữ source AI và crop map, không upscale hoặc cắt đầu/tay/chân/góc bàn/cạnh máy giặt. Chữ/số là lớp native, không nằm trong PNG. Năm PNG mới vẫn ở GitHub; tài nguyên archive cũ vẫn ở R2, sáu pin cũ giữ nguyên.

Để dựng lại, phục hồi đúng media bằng tools/restore-media.py trước. tools/build-mortgage-review.py chặn ghi đè project đã có; tools/render-intro.cjs dùng tên xuất mới. Duyệt sửa nhỏ trong Studio; không xuất full sau mỗi sửa nhỏ, không làm thêm bộ16 hình hoặc bảng96 giây.
