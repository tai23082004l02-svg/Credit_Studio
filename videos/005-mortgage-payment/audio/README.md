# Giọng đọc video 005

Trạng thái: **đã nhận audio gốc qua chat**, tên `You find a house you can f.wav`, 566,45 giây, 27.189.644 byte, PCM s16le/24kHz/mono. SHA-256 và thông tin đối chiếu tại [source.json](source.json). Không cần người dùng upload lại nếu bản local còn nguyên hash.

R2 authenticated HEAD từ môi trường chat trả HTTP401: chưa có upload/hash-verify source trên R2, manifest cũ giữ nguyên. File local exact đã gitignore, không commit WAV27 MB. Ba cảnh mẫu chứa audio montage dẫn xuất trực tiếp trong JSON để duyệt; không thay thế việc lưu WAV gốc.

**Kịch bản v01 đã được người dùng duyệt ngày 2026-10-23.** Dùng nguyên nội dung [narration.txt](../narration.txt) để thu/TTS tiếng Anh Mỹ; không đọc tiêu đề hoặc ghi chú trong [script.md](../script.md). Tệp này chỉ chứa lời đọc, không có heading hoặc ghi chú. Khoảng 1241 từ; thời lượng thật phụ thuộc giọng/tốc độ, không ép thành mốc dự kiến bằng cách cắt hoặc đổi tốc độ nguồn.

Gửi WAV/MP3 gốc qua chat hoặc bàn giao theo phương thức phù hợp dung lượng. Giữ tên nguồn; khi nhận sẽ đo thời lượng, format, SHA-256, căn lời và dựng theo audio thật. Audio đã thêm chỉ trong Studio cần .credit.json có tệp đính kèm hoặc gửi riêng WAV/MP3.

Không đưa media archive trở lại GitHub. Nếu thêm media mới vào R2, copy và kiểm tra hash, cập nhật manifest theo docs/R2_SETUP.md trước khi bỏ bản local; không log khóa. Giữ nguyên nguồn, tạo bản dẫn xuất và tên xuất mới, không ghi đè nguồn.
