> WAV gốc đã chuyển sang [R2](https://pub-ae346874928c47ce9628da16abea661c.r2.dev/credit-studio/media/d824b5830079a818da3c2c46a37dc377fac9de2baf70ee91c871546b2637b65e.wav), giữ nguyên byte. Để dựng cục bộ: `python3 tools/restore-media.py videos/002-monthly-payment-trap/audio/` từ gốc repo.

# Giọng đọc video 002

Đã nhận `monthly-payment-trap-voiceover.wav`: PCM 16-bit, mono 24 kHz, **495,475 giây**. Giữ nguyên tệp gốc, không cắt hoặc ghi đè.

Bản dựng đầy đủ: `../review/project.json`, 79 cảnh; MP4: `../exports/full-review-v01.mp4`. Audio dùng trong Studio là MP3 dẫn xuất `../review/voiceover.mp3`, nâng âm lượng bằng loudnorm, không đổi tốc độ hoặc bỏ nội dung. Bảng hình `../storyboard/project.json` vẫn là bản tĩnh 96 giây cũ, không phải video theo audio.
