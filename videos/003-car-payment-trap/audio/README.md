> WAV gốc đã chuyển sang [R2](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/e0d47280389d7f6592b3bd6bed5f1b41389b29088da07c14522ac13258888938.wav), giữ nguyên byte. Để dựng cục bộ: `python3 tools/restore-media.py videos/003-car-payment-trap/audio/` từ gốc repo.

# Giọng đọc video 003

Đã nhận `tts_20261022_115123_7124d9.wav`: 522,2 giây, PCM 16-bit / 24 kHz / mono. Giữ nguyên bản ghi gốc. SHA-256: `e0d47280389d7f6592b3bd6bed5f1b41389b29088da07c14522ac13258888938`.

Bản dựng dùng `../review/voiceover.mp3`, dẫn xuất chuẩn hóa âm lượng, không đổi tốc độ hoặc cắt lời. Không ghi đè bản gốc khi thay giọng đọc; dùng tên phiên bản mới. Audio dùng câu chuyển thời gian cũ; phần trade-in được ghi rõ là ví dụ riêng trong bản dựng. Xem `../review/narration.md` cho văn bản đối chiếu audio.
