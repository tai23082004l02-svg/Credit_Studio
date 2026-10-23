# Audio gốc video 005

Đã nhận qua chat: **You find a house you can f.wav**, 27.189.644 byte /566,45 giây, PCM s16le /24 kHz /mono. SHA-256 `9586941c972c26238f808a0c6c3ad0a5416f53f0e2ba07410a45e6c6f27c619c`. Giữ nguyên byte nguồn.

WAV gốc và full MP3 đã được upload qua GitHub Actions lên R2, tải lại xác minh SHA-256; public Range/CORS và public full hash đều qua. Xem source.json và storage/manifest.json. Credential trong môi trường chat vẫn401, nhưng credential Actions hoạt động; không cần gửi lại khóa hoặc WAV.

review/voiceover.mp3 là dẫn xuất hai-pass loudnorm, không cắt nội dung/thay tốc độ; −16,84 LUFS /−1,69 dBTP. Không có nhạc. Các excerpt trong samples/project.json là bản style cũ giữ nguyên. File WAV/MP3 local được gitignore; phục hồi bằng `python3 tools/restore-media.py videos/005-mortgage-payment/audio/` và tương tự review/voiceover.mp3.

Bản sửa Studio sống trong IndexedDB, cần .credit.json/JSON khi bàn giao; audio gốc không thay bằng audio đã xử lý.
