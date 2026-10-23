# Video 005 — Your Mortgage Payment Is Only the Beginning

**Tiền trả góp nhà mới chỉ là phần bắt đầu.**

## Trạng thái thực tế

**Kịch bản v01 đã được duyệt ngày 2026-10-23** (1241 từ / 8 phần). Đã nhận WAV **566,45 giây / 27.189.644 byte**, giữ nguyên gốc. Đã có **ba cảnh mẫu có giọng đọc / 86,8 giây**, **phong cách đã được người dùng chốt ngày2026-10-23**; **chưa phải bản video đầy đủ**.

[Mở ba cảnh mẫu trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-005&tab=video) · [JSON chỉnh được](samples/project.json) · [Nguồn audio](audio/source.json) · [Mốc ba đoạn trích](samples/excerpts.json).

Mẫu gồm calculator, ngân sách sở hữu, cash và equity. Dùng audio trích từ giọng đọc thật, không phải bảng hình96 giây; thời lượng toàn bộ WAV là 9 phút26,45 giây. Bản mẫu tự chứa audio montage và hình trong JSON; không có MP4 public ở bước này.

**Lưu trữ audio gốc:** môi trường chat hiện trả HTTP401 khi gọi R2 có xác thực, nên chưa upload/xác minh WAV mới hoặc thêm mapping manifest. File gốc được giữ local và gitignore; upload chat là nguồn bàn giao, không có bản R2 đã xác minh. Không đưa WAV27 MB lên GitHub và không ảnh hưởng tài nguyên R2 cũ.

- [Kịch bản có chia phần](script.md).
- [Lời đọc thuần để TTS](narration.txt).
- [Nguồn và phép tính](sources.md).
- [Storyboard ngắn và kế hoạch ba cảnh mẫu](storyboard.md).
- [Bàn giao audio](audio/README.md).

`finance-005` đã đăng ký trong projects.json và trỏ **bản mẫu thật**, không khai báo audio/MP4/cover chưa tồn tại. Các dự án001–004 giữ nguyên.

## Hướng triển khai

Dùng đồ họa động nhiều lớp, Times New Roman. Đề xuất tiếp tục nền giấy kem/đỏ trầm với minh họa nhà ở tách lớp; không bắt buộc dùng Alex hoặc ảnh collage cố định. Phong cách ba cảnh mẫu đã được người dùng chốt; không hỏi duyệt lại. Đã tạo thêm bốn nhóm minh họa Jamie để dùng trong bản đầy đủ, không làm sẵn16 ảnh.

Nhịp kể: khoản trả vay → ngân sách sở hữu → escrow không cộng trùng → tiền sau nhận nhà → sửa chữa đến sớm → equity khác tiền mặt → thử ngân sách → kết.

Lời thoại đã được duyệt và audio gốc đã nhận. Triển khai theo phong cách đã chốt; chia cảnh/thời điểm chính thức theo audio thật. Tạo hình và đạo cụ đúng nhu cầu, dùng lại kho chung. Không tạo bảng hình im lặng 96 giây. Duyệt sửa nhỏ trực tiếp trong Studio hoặc bằng đoạn ngắn; chỉ xuất MP4 đầy đủ ở mốc duyệt.

## Các điểm phải bảo toàn

- Ví dụ hư cấu, không gọi là giá nhà/lãi suất hiện tại, trung bình toàn Mỹ, hoặc khoản vay được chào bán. 6,5% là lãi suất danh nghĩa giả định, không phải APR.
- Không cộng trùng thuế/bảo hiểm đã bao gồm trong escrow; phí HOA tính riêng trong ví dụ.
- Khoản để dành sửa chữa là tiền chuyển vào savings, không phải toàn bộ chi phí đã tiêu; không cộng lại khoản sửa từ cùng quỹ.
- Tiền gốc và down payment không phải toàn bộ chi phí mất đi; equity không đồng nghĩa tiền mặt, giá nhà không được đảm bảo tăng.
- 20% down/no mortgage insurance chỉ là giả định khoản vay conventional này, không phải yêu cầu chung để mua nhà.
- Hướng dẫn dùng sheet: cần lề ô an toàn, giữ nguồn/toạ độ, kiểm tra từng ảnh sau cắt và trong cảnh, đủ góc/cạnh/đầu/tay/chân.
- Bảo toàn audio gốc và mọi bản xuất/JSON sau này; nếu tiếp tục từ sửa riêng trong Studio phải nhận .credit.json/JSON trước.
- Media archive vẫn ở R2; không đưa lại lên GitHub hoặc thay manifest cho bước viết kịch bản.

## Hình minh họa mới

Đã tạo bốn nhóm Jamie: [nhận chìa khóa](../../library/props/jamie-mortgage/keys.png), [xem hóa đơn](../../library/props/jamie-mortgage/bills.png), [kiểm tra máy giặt](../../library/props/jamie-mortgage/repair.png), [so sánh giấy tờ](../../library/props/jamie-mortgage/compare.png). Xem trong [Kho đạo cụ](https://tai23082004l02-svg.github.io/Credit_Studio/?view=props), nhóm **Nhân vật · Jamie**. Giữ source sheet tại images/sources/, prompt/hash và map cắt tại images/. Không đặt chữ/số vào ảnh; mỗi nhóm là lớp ảnh riêng, chưa rig khớp nhân vật.

Các PNG mới được giữ trên GitHub để dùng được ngay; R2 chưa xác minh upload mới. Không thay hoặc khôi phục lại bất kỳ media archive nào.
