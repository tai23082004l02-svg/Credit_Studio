# Audio gốc video006

Đã nhận `tts_20261023_125715_dda159.wav`: **25.705.244 byte /535,525 giây**, PCM s16le /24kHz /mono, giữ nguyên byte. SHA-256 `c26b2cd58cb7b9f7cd9dce14954c7668eabb699145499bb46125f6c8a93e45c5`.

WAV và full MP3 được upload R2 qua Actions, tải lại S3 và public kiểm tra SHA-256/Range/CORS. Metadata/run tại source.json. MP3 dẫn xuất loudnorm hai-pass, không cắt lời/đổi tốc độ: −16,85 LUFS /−1,67 dBTP; nguồn −27,29 LUFS. Không nhạc. Local media gitignore; dùng tools/restore-media.py để phục hồi đúng đường dẫn khi dựng lại.

Alignment tự động:1068/1115 token khớp trực tiếp; khác biệt số/cách viết được nội suy, không phải xác nhận thủ công từng từ. WAV, script/narration và metadata số liệu gốc được bảo toàn.
