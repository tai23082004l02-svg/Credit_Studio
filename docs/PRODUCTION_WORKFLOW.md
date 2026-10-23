# Quy trình sản xuất video đã chốt

## Hướng hình ảnh mới nhất — ảnh nguyên cảnh

Theo mẫu người dùng gửi và quyết định2026-10-23: mỗi cảnh là một ảnh hoạt hình hoàn chỉnh với nhân vật nhất quán, bối cảnh và đạo cụ; chia cảnh theo audio, chuyển ảnh và pan nhẹ. Không mặc định tách bộ phận nhân vật/đạo cụ hoặc dựng thẻ thông tin kiểu cũ. Chữ và số chính là lớp native để sửa chính xác. Sheet có thể đóng gói nhiều cảnh, giữ ảnh nguồn và crop toàn cảnh. Giữ Times New Roman và mọi bản cũ. Đây là thay đổi hướng hình ảnh; không cần duyệt hình trung gian.

Đầu ra theo yêu cầu từng dự án: video007 chỉ bàn giao bản dựng chỉnh được trên Studio, **không xuất MP4**. Các hướng dẫn MP4 bên dưới chỉ áp dụng khi MP4 nằm trong đầu ra được yêu cầu.


Áp dụng mặc định cho video mới từ **2026-10-23**, theo quyết định của người dùng: cùng chọn chủ đề; trợ lý chuẩn bị lời đọc, người dùng tạo audio; trợ lý tự quyết và thực hiện toàn bộ phần hình ảnh, chuyển động và dựng. Quy trình này thay bước chờ người dùng duyệt storyboard, phong cách, cảnh mẫu hoặc từng hình trong quy trình trước.

## Trình tự và trách nhiệm

1. **Cùng chọn chủ đề.** Thống nhất nội dung chính và những yêu cầu riêng nếu có.
2. **Trợ lý chuẩn bị kịch bản và lời đọc tiếng Anh Mỹ.** Kiểm tra nguồn, số liệu, phép tính và phạm vi ví dụ trước khi gửi; bàn giao `script.md`, `narration.txt` sạch để thu/TTS và `sources.md`. Không mặc định tạo audio thay người dùng.
3. **Người dùng tạo và gửi audio gốc.** Trợ lý giữ nguyên nguồn, ghi metadata/hash, tạo bản âm thanh dẫn xuất khi cần và căn cảnh theo giọng đọc thật. Khi đang chờ audio, có thể chuẩn bị storyboard ngắn và thử bố cục nội bộ.
4. **Trợ lý tự sản xuất toàn bộ hình và bản dựng.** Tự chọn phong cách phù hợp chủ đề, tạo hoặc dùng lại minh họa/đạo cụ, quyết định bố cục, phân cảnh và chuyển động; không dừng xin duyệt hình hoặc cảnh mẫu. Thử nghiệm nội bộ chỉ làm khi giúp kiểm tra chất lượng, không bắt buộc có 2–3 cảnh mẫu cho mỗi video.
5. **Trợ lý tự kiểm tra và bàn giao video hoàn chỉnh.** Kiểm tra nội dung, bố cục, crop, chuyển động, đồng bộ tiếng và tệp xuất; xuất MP4 ở mốc hoàn thành, lưu media mới trên R2 sau khi xác minh, đưa một bản dựng chính chỉnh được lên Studio và cập nhật bàn giao. Người dùng có thể xem thành phẩm và góp ý sau; không cần duyệt trung gian để tiếp tục sản xuất. Đăng trong Credit Studio theo luồng hiện tại, không tự đăng lên YouTube hoặc dịch vụ bên ngoài.

## Tiêu chuẩn tiếp tục áp dụng

- Trao đổi bằng tiếng Việt; nội dung video hướng khán giả Mỹ bằng tiếng Anh; **Times New Roman** cho chữ, số và phụ đề.
- Không làm sẵn bộ 16 ảnh, bảng hình im lặng 96 giây hoặc nhiều thiết kế trùng nội dung. Tạo tài nguyên đúng nhu cầu; ưu tiên đồ họa động chỉnh được trong Studio, không dùng Runway trong quy trình hiện tại.
- Khi dùng sheet, giữ nguồn/toạ độ cắt, chừa lề an toàn và kiểm tra từng hình trong cảnh; giữ đủ góc, cạnh, đầu, tay, chân. Kiểm tra lúc vào, giữa và ra; hình/nhãn trong thẻ căn giữa và không bị lớp chữ hoặc nền che.
- Thanh và số tiền phải đồng bộ, phép tính và phạm vi ví dụ phải chính xác. Tự kiểm tra cả hình lẫn audio trong MP4; bỏ vòng duyệt trung gian không có nghĩa là bỏ kiểm tra chất lượng.
- Xem sửa nhỏ trong Studio hoặc đoạn trích; không xuất MP4 đầy đủ sau mỗi chỉnh sửa nhỏ. Giữ một bản dựng chính, dùng tên phiên bản mới khi xuất tiếp.
- Bảo toàn WAV gốc, nguồn hình, JSON, bản xuất và backup cũ. Bản sửa riêng ở IndexedDB: nhận `.credit.json` hoặc JSON trước nếu cần tiếp tục từ bản người dùng đã sửa; không ghi đè bằng bản repo. Giữ cơ chế archive draft khi nâng cấp.
- Không đưa media đã archive trở lại GitHub, không viết lại lịch sử Git. Giữ sáu pin local cũ; media mới chỉ đăng ký R2 sau khi upload và xác minh hash/đọc công khai thành công.

## Ước tính thời gian

Kỳ vọng khoảng **20–35% ít thời gian sản xuất thực tế hơn** (mốc tham khảo khoảng 30%); nếu tính cả thời gian chờ duyệt, tổng thời gian có thể giảm **40–60%**. Đây là ước tính trao đổi, chưa phải kết quả đo hoặc cam kết thời hạn. Không rút ngắn bằng cách bỏ kiểm tra nội dung, chất lượng hoặc bảo toàn dữ liệu.
