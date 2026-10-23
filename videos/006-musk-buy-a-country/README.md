# Video006 — Could Elon Musk Buy a Country?

**Đã hoàn thành toàn bộ hình và bản dựng theo audio v01:55 cảnh /8 phút55,525 giây. MP4 đang xuất, chưa khai báo bản xuất public.**

[Mở thư viện hình trong Studio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-006&tab=images) · [Mở bản dựng có audio](https://tai23082004l02-svg.github.io/Credit_Studio/?project=finance-006&tab=video) · [JSON chính](review/project.json) · [Kiểm tra hình](images/validation.json).

## Hình và bối cảnh

- **7 bối cảnh AI**: Lisbon/Tagus, công nghiệp, tài chính, khu dân cư, bệnh viện, trường/đường sắt, không gian công quyền. Không dùng nền trắng/giấy kem xuyên suốt. Đây là minh họa biên tập, không phải ảnh tư liệu hay dự án Musk thực hiện.
- **4 tư thế Musk tách nền**: đứng, hướng tay, suy nghĩ, cầm hồ sơ. Musk là **đối tượng được nói đến, không phải narrator**; giọng kể ngoài, không quote tưởng tượng, giọng giả Musk hoặc lip-sync. Giữ đầy đủ tóc/tay/giày/góc hồ sơ và40px padding, crop map xác nhận bảo toàn pixel nhìn thấy. Không upscale PNG khi cắt.
- **1 bản đồ native** theo Natural Earth110m, outline phần lục địa; số liệu áp dụng toàn Bồ Đào Nha, gồm đảo. Giữ nguồn/license ở images/portugal-mainland.geo.json.
- **13 PNG khung chính lấy từ timeline thực**, không phải bộ16 ảnh hoặc storyboard96 giây. Chỉ có một project JSON chính; link “Chỉnh cảnh” mở đúng clip trong Studio, không nhân bản thiết kế JSON. visuals.json quản lý preview/source/cutout.
- Chữ, số, panel và đồ thị Times New Roman native, độc lập với PNG. Nền ảnh giữ tỉ lệ và có crop cover có chủ ý; nhân vật/map không bị cắt/che. **14 lớp chuyển động nội dung trong11 cảnh**, cùng55 lớp pan nền và timed reveals.

## Audio và nội dung

WAV nhận qua chat **535,525 giây /25.705.244 byte**, giữ nguyên SHA; MP3 loudnorm dẫn xuất, không cắt/thay tốc độ, không nhạc. [Nguồn audio](audio/source.json). ASR1068/1115 từ khớp trực tiếp;149 cue EN mặc định tắt, có sai số căn từ tự động. Script/narration1115 từ và data-snapshot giữ nguyên.

Forbes snapshot2026-10-01 $936B; Portugal GDP2025~$346.64B và population10,804,871. GDP không phải national wealth, public budget hoặc giá mua cả nước. Model $108B/round dùng rounded population10.8M; giả định936B đã cash, bỏ taxes/returns/inflation/population/admin →8round đầy đủ, còn72B, không đủround9. Không gán model cho kế hoạch thực của Musk/chính phủ.

- [Lời đọc](narration.txt) · [Kịch bản gốc](script.md) · [Nguồn/phép tính](sources.md) · [Mốc dữ liệu](data-snapshot.json).
- [Timecode55 cảnh](review/shot-plan.json) · [Kế hoạch chuyển động](review/motion-plan.json) · [Phụ đề](review/captions.vtt).
- [Prompt/hash/source hình](images/image-generation.json) · [Map cắt](images/musk-crop-map.json) · [Kiểm tra bố cục](review/layout-validation.json).

Nguồn AI, WAV/MP3, cutout/map và preview được lưu R2, authenticated và public full hash/Range/CORS đều verified; các media local đều gitignore. Giữ toàn bộ208 mapping/sáu pin cũ,5 dự án cũ và catalog93 mục. Sửa riêng IndexedDB không tự lên Git; nhận .credit.json/JSON trước khi tiếp tục từ chúng. Không viết lại lịch sử hoặc đưa media archive vào main.

Công cụ: tools/extract-musk-character.cjs, tools/build-musk-review.py, tools/build-musk-gallery.cjs đều chặn ghi đè. Phục hồi media từ R2 trước khi chạy builder; giữ bản cũ và dùng version mới.
