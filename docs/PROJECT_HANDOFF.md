# Bàn giao Credit Studio cho phiên chat tiếp theo

Cập nhật: 2026-10-21. Đây là ghi chú tiếp nối công việc, không phải bản sao toàn bộ lịch sử chat. Kiểm tra trạng thái Git và các thay đổi mới trước khi thực hiện.

## Mục tiêu và quyết định đã chốt

- Người dùng giao tiếp bằng tiếng Việt, làm video YouTube tài chính cho khán giả Mỹ; lời đọc bằng tiếng Anh Mỹ.
- Người dùng cung cấp âm thanh (có thể do AI đọc). Trợ lý chuẩn bị lời thoại, hình ảnh, phân cảnh, dựng video và bản duyệt chỉnh được trong Credit Studio; người dùng sửa tiểu tiết trước bản xuất cuối.
- Phong cách đã chọn: nhân vật nét vẽ 2D, biểu đồ và biểu tượng đơn giản. Nhân vật Alex có tóc nâu sẫm, áo kem xắn tay, quần xanh teal; nền kem, nét than, xanh tiền, coral cho chi phí và điểm nhấn vàng.
- **Giữ Times New Roman cho toàn bộ chữ**, bao gồm giao diện, chữ trong hình và phụ đề. Website có font serif dự phòng khi thiết bị thiếu font; bản MP4 hiện có được dựng bằng Times New Roman thực.
- **Bố cục thẻ biểu tượng + nhãn:** người dùng góp ý từ ô “Taxes”: những lần dựng sau cần căn giữa cả biểu tượng và chữ theo chiều ngang trong từng ô, giữ khoảng cách giữa hình/chữ và lề cân đối, đồng đều giữa các ô. Đây là yêu cầu áp dụng cho lần sau; chưa thay bố cục hay xuất lại video hiện tại chỉ từ góp ý này.
- **Không cắt/che nhân vật ngoài ý muốn:** người dùng chỉ lỗi ở cảnh “PLAN AROUND WHAT ARRIVES” (ảnh `02b`): đỉnh đầu/tóc Alex bị vùng nền của tiêu đề che ngang. Các lần dựng sau kiểm tra vùng crop, mép khung và lớp nền/chữ chồng lên hình; giữ đầu, tay, chân đầy đủ khi không chủ đích cắt cận. Xem khung tổng hợp lúc vào cảnh, giữa và cuối cảnh, không chỉ kiểm tra chữ có tràn hay không. Lỗi này đã được ghi nhận, chưa sửa bản dựng/MP4 hiện tại vì người dùng đang góp ý cho lần sau.
- Dùng online, quản lý nhiều dự án qua một địa chỉ: https://tai23082004l02-svg.github.io/Credit_Studio/ . Không yêu cầu người dùng nhớ các URL công cụ riêng.

## Website và lưu dữ liệu

Ứng dụng tĩnh HTML/CSS/JavaScript, không có backend hay tài khoản. GitHub Pages triển khai từ nhánh `main`, thư mục gốc. Push vào `main` kích hoạt triển khai; kiểm tra kết quả GitHub Actions trước khi khẳng định bản sửa đã lên website.

Trang chủ có danh sách dự án và các tab Tổng quan, Dựng video, Hình ảnh, Âm thanh & tài liệu. Có tạo dự án, tìm kiếm, đổi tên, thêm tệp và sao lưu/khôi phục `.credit.json`. `/video/` và `/design/` vẫn mở trực tiếp được nhưng là công cụ bên trong luồng chung.

**Dự án tự tạo, bản sửa và tệp tải lên qua website lưu trong IndexedDB của trình duyệt đó; không tự đồng bộ lên GitHub hoặc thiết bị khác.** Chat mới không truy cập được những bản sửa này chỉ bằng việc đọc repo. Khi cần chúng, người dùng dùng **Sao lưu dự án** rồi cung cấp tệp `.credit.json`. Khôi phục tạo dự án riêng, không ghi đè dự án hiện có. Tài nguyên xuất bản sẵn vẫn được tham chiếu từ website.

`projects.json` đăng ký các dự án xuất bản. Dự án tài chính hiện có ID ổn định `finance-001`. Mỗi dự án mới cần thư mục riêng trong `videos/` và mục đăng ký riêng. Giữ khả năng đọc bản sao lưu, dữ liệu IndexedDB và các khóa localStorage cũ.

## Kho đạo cụ dùng chung

Người dùng làm rõ yêu cầu là **kho đạo cụ**, không phải kho audio/video tổng hợp. R2 đã kết nối và kiểm tra đọc/ghi thành công ngày 2026-10-21; tài nguyên đang xuất bản vẫn ở GitHub, chưa chuyển sang R2. Đã thêm nút **Kho đạo cụ** trong đầu trang Studio, route `?view=props` hoặc `?view=props&project=<id>`. Có 31 mục (27 đạo cụ + 4 tư thế Alex trong nhóm **Nhân vật**: vui mừng, lo lắng, suy nghĩ, giới thiệu), tìm kiếm tiếng Việt có/không dấu hoặc từ khóa tiếng Anh, lọc nhóm, xem trước hình và nhãn căn giữa, tải PNG riêng đúng vùng cắt/độ phân giải gốc, chọn dự án video và cảnh rồi thêm lớp ảnh độc lập vào cảnh đó.

Nhân vật dùng chung đầy đủ đầu/tay/chân từ sprite sheet Alex gốc, giữ nền trong suốt. Tải PNG riêng hoặc thêm vào cảnh như các đạo cụ khác; không tạo thêm nhân vật mới ở đợt bổ sung này. Đã kiểm tra 31 mục hiển thị, lọc 4 nhân vật, tìm nhiều từ như “Alex lo lắng”, tải PNG Alex — Giới thiệu đủ 536×769 px và thêm thành lớp riêng vào đúng cảnh; các kiểm tra kho khác vẫn qua.

Danh mục: `library/props/catalog.json`. Ảnh hiện có được tham chiếu từ các sprite sheet gốc trong `videos/001-100k-salary/`; không nhân bản/di chuyển ảnh đang dùng. Đạo cụ mới tải lên `library/props/` (PNG trong suốt ưu tiên, JPG/WebP cũng hỗ trợ), tên không dấu/không khoảng trắng; người dùng báo sau khi commit để trợ lý chạy `python3 tools/index-props.py`, bổ sung tên/nhóm/tags, kiểm tra rồi push. Upload chưa tự đăng ký vào danh mục. ID/đường dẫn đã dùng phải giữ ổn định; phiên bản mới dùng tên tệp riêng.

`assets/js/prop-library.js` kiểm tra dữ liệu, xem trước, xuất PNG và thêm lớp vào cảnh. Video engine nhận thêm nguồn ảnh `library/props/...`. Không thêm login, API ghi GitHub từ website hoặc đồng bộ dự án online. Bản dựng thêm đạo cụ vẫn lưu riêng trong trình duyệt; backup chứa tham chiếu tài nguyên đã xuất bản. Đọc `library/props/README.md` khi tiếp tục mở rộng kho.

Đã kiểm tra: 8 unit test, `tests/prop-library.cjs`, `tests/project-workspaces.cjs`, `tests/video-editor.cjs` đều qua. Kiểm tra kho bao gồm 27 vùng cắt hiện đúng, tìm không dấu/lọc nhóm, PNG tải đúng kích thước, thêm vào đúng cảnh và mở đúng cảnh đó, reload giữ lớp mới, không đổi cảnh khác/audio, thêm PNG mới từ đường dẫn library/props, từ chối nguồn/vùng cắt lỗi, mobile và công cụ lập danh mục giữ ID khi chạy lại.

### Thay đạo cụ ngay trong trình dựng

Chọn lớp ảnh rồi **Chỉnh phần tử → Thay đạo cụ** để mở hộp chọn ngay trong trình dựng. Có tìm nhiều từ/không dấu, lọc nhóm (gồm Nhân vật), hình và tên căn giữa. Chọn mẫu thay toàn bộ lớp ảnh đó, giữ ID lớp, thứ tự lớp, x/y/w/h, enter/effect/opacity/drift, thời lượng cảnh và audio. Ảnh mới giữ đúng tỉ lệ trong khung cũ, không kéo méo. Ảnh tổng thể chỉ thay được toàn bộ lớp, không tự tách vật thể bên trong.

`replaceProp` trong `assets/js/prop-library.js` tạo tham chiếu tài nguyên riêng cho lớp mới; giữ tài nguyên cũ nếu còn cảnh/lớp khác dùng, thu hồi tham chiếu không dùng để tránh tăng mãi. Trình dựng tải ảnh trước khi thay, dùng lịch sử Hoàn tác/Làm lại và lưu dự án hiện tại; không sửa JSON/MP4 xuất bản gốc. Hủy hoặc lỗi tải danh mục giữ bản đang chỉnh. Phím tắt trình dựng không tác động cảnh khi hộp chọn mở.

Kiểm tra: `tests/replace-prop.cjs` qua — thay nhân vật/đạo cụ, giữ hình học/chuyển động/audio/cảnh khác và tham chiếu dùng chung, undo/redo/reload, hủy/lỗi danh mục, mobile, thay nhiều lần không tăng tài nguyên thừa. 8 unit test engine/WebM cũng qua.

## Video đầu tiên: trạng thái thực tế

Tên: **Why You Feel Broke on a $100,000 Salary**.

Thư mục: `videos/001-100k-salary/`.

- `script.md`: lời thoại tiếng Anh chia 8 phần. Các con số là ví dụ minh họa, không phải kết quả thuế phổ quát.
- `audio/Why You Feel Broke on a $100,000 Salary.wav`: âm thanh gốc do người dùng cung cấp, dài khoảng 486,75 giây (8 phút 6,75 giây), PCM mono 24 kHz. **Bảo toàn tệp gốc.**
- `images/scenes/`: 16 ảnh cảnh PNG; `images/sheets/`: 3 bảng tài nguyên nhân vật/đồ vật có nền trong suốt.
- `projects/`: 16 thiết kế JSON có ảnh nền và lớp chữ/số chỉnh được; `artwork.json` và `storyboard.md` mô tả bộ hình/phân cảnh. Ảnh cảnh là ảnh phẳng, không phải mọi chi tiết đều tách lớp.
- `intro/project.json`: bản dựng mở đầu **40,5 giây**, 1920×1080, 30 fps, 8 cảnh có lớp nhân vật/đồ vật/chữ và chuyển động đơn giản.
- `intro/voiceover.mp3`, `alignment.json`, `captions.vtt`: đoạn âm thanh dẫn xuất, mốc từ tự động và 14 đoạn phụ đề. Xem `intro/README.md` để biết thời điểm cụ thể.
- `exports/intro-v01.mp4`: bản duyệt H.264/AAC 40,5 giây, Times New Roman, chưa thêm nhạc nền.

Bản mở đầu kết thúc sau câu “before you buy a single thing”, trước “Meet Alex.” Người dùng đã đánh giá tốt bản duyệt và yêu cầu đổi font, sau đó gộp công cụ quản lý. **Ngày 2026-10-21 đã dựng tiếp toàn bộ thành bản duyệt đầy đủ; xem cập nhật bên dưới.** Chuyển động hiện là fade/slide/pop/drift của các lớp; chưa có rig khớp nhân vật.

## Cập nhật bản dựng đầy đủ — 2026-10-21

Người dùng đã yêu cầu dựng tiếp. Đã dựng toàn bộ **486,75 giây / 64 cảnh**, nối nguyên 8 cảnh intro với 56 cảnh mới. Bản duyệt chỉnh được: `review/project.json`; nguồn âm thanh MP3 toàn bộ: `review/voiceover.mp3`; mốc nhận dạng: `review/alignment.json`; phụ đề: `review/captions.vtt`. Tất cả nằm trong `videos/001-100k-salary/`. `review/README.md` có bảng timecode từng cảnh. Bản MP4 để duyệt: `exports/full-review-v01.mp4` (1920×1080, 30 fps, Times New Roman, lời đọc gốc, chưa nhạc nền). WAV và bản intro cũ được bảo toàn.

`projects.json` vẫn dùng ID `finance-001`, trỏ bản video và MP4 đầy đủ. Trang chủ/Tổng quan xem MP4 mới, tab Dựng video chỉnh timeline. Đã sửa lỗi người dùng thấy Tổng quan 8 phút nhưng trình dựng chỉ 40,5 giây: ưu tiên bản lưu intro cũ, và thông báo mở bản mới bị ẩn trên mobile.

Trình dựng nay tự chuyển riêng `finance-001` từ revision `intro-v01` sang `full-review-v01`. Trước khi chuyển, lưu nguyên vẹn bản cũ vào document slot `history-<uuid>` trong cùng giao dịch IndexedDB với việc thay main; lỗi giao dịch không được làm mất bản cũ. Mục **Bản lưu trước cập nhật** tải từng JSON cũ, hiển thị cả trên điện thoại; `.credit.json` chứa cả lịch sử. Giữ localStorage gốc. Các bản cùng revision full được giữ nguyên khi reload, không tạo thêm lịch sử hoặc reset sửa đổi. Nếu không tải được bản mới, vẫn mở bản cũ. Dự án khác, bản khôi phục và revision khác không tự chuyển. Module/iframe đã đổi tham số phiên bản để bỏ cache ứng dụng cũ.

Các cảnh mới kết hợp nhân vật/đạo cụ tách lớp, thẻ chữ/số, biểu đồ ngân sách đúng tỉ lệ và ảnh cảnh có sẵn. Một số cảnh dùng ảnh tổng thể, không phải mọi chi tiết của ảnh đều chỉnh riêng được. Mốc từ tự động bằng faster-whisper base.en được ánh xạ lại script để giữ đúng chữ; có sai số ở mức từ. Các nhóm đạo cụ quan trọng xuất hiện theo mốc câu. Phụ đề mặc định tắt trong MP4; bật được trong Studio. Chưa có rig khớp hoặc nhạc nền.

Công cụ tái tạo: `tools/build-full-video.py` đọc script, mốc nhận dạng và tài nguyên, tạo lại JSON/VTT/timecode; không chỉnh WAV hay intro. Không chạy lại nếu có bản sửa tay chưa sao lưu. Dựng MP4 bằng `tools/render-intro.cjs` với đầu vào `review/project.json` và đường dẫn xuất mới.

Bước tiếp theo: người dùng xem **bản duyệt đầy đủ v01**, cung cấp các chi tiết cần sửa (tốt nhất kèm timecode). Nếu đã sửa trong trình duyệt, cần nhận `.credit.json` hoặc JSON video trước khi trợ lý tiếp tục từ các sửa đổi đó. Chưa coi bản duyệt là bản cuối đã được người dùng duyệt.

## Mã nguồn và kiểm tra

- `index.html`, `assets/js/hub.js`, `assets/css/hub.css`: trang quản lý và điều hướng chung.
- `assets/js/workspace-store.js`: IndexedDB, danh mục, sao lưu/khôi phục, chuyển dữ liệu cũ.
- `design/index.html`, `assets/js/app.js`, `assets/js/design-model.js`: trình ảnh và kiểm tra dữ liệu thiết kế.
- `video/editor.js`, `video/engine.js`, `video/webm.js`: trình video, bộ vẽ dùng chung và xuất WebM.
- `tools/build-video-projects.py`, `tools/build-intro-project.py`, `tools/build-full-video.py`: tạo lại thiết kế/bản intro từ cấu hình; đọc hướng dẫn trước khi chạy vì có thể thay JSON hiện có.
- `tools/render-intro.cjs`: dựng MP4 từ JSON bằng bộ vẽ dùng chung, Playwright và FFmpeg; dùng đường dẫn xuất mới để giữ bản cũ.

Đọc README để chạy máy chủ, kiểm tra và dựng MP4. Ứng dụng không cần thư viện production. Bộ kiểm tra trình duyệt/công cụ MP4 cần Playwright, Chromium và FFmpeg. Font cục bộ ở môi trường trước nằm ngoài repo tại `/workspace/shared/credit-studio-fonts`; máy mới cần kiểm tra lại, không giả định tệp đó luôn tồn tại. Không đưa tệp font độc quyền vào website/repo.

Đã kiểm tra ở lần triển khai gộp công cụ: 8 bài unit test cho engine/WebM; bộ Playwright `tests/video-editor.cjs` và `tests/project-workspaces.cjs` (tách dữ liệu dự án, lưu lại, âm thanh, xuất WebM, sao lưu/khôi phục và mobile); MP4 thực bằng FFmpeg/ffprobe. GitHub Pages triển khai thành công cho commit `0f542fa`; tài nguyên online đã đối chiếu qua HTTPS. Đây là kết quả của phiên trước, không thay cho kiểm tra phù hợp với thay đổi mới.

Kiểm tra bản đầy đủ ngày 2026-10-21: 8 unit test và cả hai bộ Playwright đã qua, gồm bảo toàn/sao lưu bản sửa cũ, hủy mở bản mới, xác nhận mở và reload bản đầy đủ. Kiểm tra thực tế toàn bộ bố cục chữ bằng Times New Roman, tua audio ở 8 phần, phát đoạn kết, timeline và mobile đã qua. MP4 đã giải mã toàn bộ bằng FFmpeg không lỗi; âm thanh đối chiếu WAV ở giây 10/200/480 có tương quan >0,9999. MP4 dài 486,766667 giây do làm tròn khung 30 fps; audio/timeline 486,75 giây. Xem `review/validation.json` và `review/source.json`. Trạng thái triển khai cần kiểm tra theo commit mới nhất trên GitHub Actions.

Kiểm tra bản sửa mở video: Playwright tái hiện bản intro đã chỉnh trong localStorage/IndexedDB rồi xác nhận tự mở 64 cảnh; JSON cũ được tải lại nguyên vẹn, backup chứa main mới và lịch sử, sửa bản đầy đủ rồi reload vẫn giữ, lịch sử không nhân đôi. Kiểm tra mở trực tiếp `/video/` chỉ có localStorage, lỗi mạng tải bản mới và thử lại thành công. Không cần dựng lại MP4 vì chỉ sửa cách chọn bản dự án.

## Cách tiếp tục trong chat mới

R2 đã kết nối thành công ngày 2026-10-21. Môi trường hiện có đủ `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`, `R2_BUCKET` dưới dạng biến môi trường trực tiếp (nguồn vault), không phải bí mật proxy. Đã thử S3 SigV4 với region `auto`: ListObjectsV2 HTTP 200 (bucket trống), PUT tệp thử 200, GET 200 và đối chiếu đúng nội dung, DELETE 204 để dọn tệp thử. Không lưu giá trị khóa trong repo/log/chat. Tệp riêng `/workspace/.credit-studio/r2.env` vẫn chỉ là mẫu chưa có khóa; nguồn đang dùng là biến môi trường. Chat mới phải kiểm tra các biến có mặt và thử quyền cần dùng, không giả định thông tin phiên cũ tự được truyền sang môi trường khác.

Đã chép và xác minh 26 tệp (128.215.675 byte) lên R2; các bản gốc GitHub được giữ. Public URL, manifest, công cụ và trạng thái mới nhất nằm trong `docs/R2_SETUP.md`. `storage/manifest.json` hiện **enabled: false** vì chờ người dùng lưu CORS và kiểm tra trình duyệt với R2 thật. Đã chuẩn bị bộ phân giải đường dẫn cho kho đạo cụ, trình dựng, audio, MP4 và thư viện ảnh; JSON dự án giữ đường dẫn cũ. Kiểm tra mô phỏng R2 và unit test đã qua; không nhầm với đã kiểm tra thực tế hoặc đã giảm dung lượng GitHub. Bản sửa vẫn lưu trong trình duyệt.

Chọn/đính kèm repo `tai23082004l02-svg/Credit_Studio`, yêu cầu đọc `AGENTS.md`, tài liệu này và README. Chat mới không tự nhớ lịch sử chat cũ. Nếu chưa có quyền truy cập repo, cần kết nối/chọn repo trước. Nếu công việc phụ thuộc bản sửa chỉ có trên trình duyệt, cung cấp bản sao lưu dự án; chỉ GitHub là chưa đủ.

## R2: token thay thế và bước đang chờ

Người dùng đã thông báo thu hồi token cũ và thay khóa. Đã xác nhận danh tính S3 mới khác danh tính từng lộ trước khi di chuyển. Không dùng lại khóa từ lịch sử Git. Công cụ tự chuẩn hóa token value/token ID theo tài liệu Cloudflare; hai biến khóa hiện tại hoạt động, không yêu cầu nhập lại. Chỉ log tên biến/trạng thái.

Người dùng đang tìm **CORS Policy** trong tab Settings của bucket `credit-studio`, không phải Settings tài khoản. Đã gửi cấu hình cho origin GitHub Pages và `http://127.0.0.1:8002`; chi tiết trong `storage/cors.json`. Quyền token hiện tại không sửa CORS qua API (403), nên thực hiện trên UI; không yêu cầu khóa quản trị. Sau khi người dùng lưu, kiểm tra header, trình duyệt R2 thật rồi mới bật manifest, triển khai và kiểm tra website online.

## Video 002 — Bộ hình Monthly Payment Trap (2026-10-21)

Người dùng đã chấp thuận lời thoại **The Monthly Payment Trap: How “Affordable” Keeps You Broke** và yêu cầu tạo toàn bộ hình, sheet đẹp/dễ cắt và đưa lên GitHub. Đã thêm `videos/002-monthly-payment-trap/`, giữ nguyên lời thoại 8 phần khoảng 1.101 từ trong `script.md`, `storyboard.md`, README và hướng dẫn audio. ID ổn định `finance-002` được đăng ký trong `projects.json`; có thể mở từ trang chủ như dự án 001.

Đã có **16 PNG khung 1920×1080 và 16 JSON thiết kế chỉnh được**: 8 cảnh minh họa mới đúng Alex/bảng màu hiện tại, 8 bố cục thông tin có hình/chữ/số/thẻ riêng. Chữ Times New Roman thực khi xuất PNG. Tiêu đề tách ngoài vùng minh họa (y>=254), không dùng nền tiêu đề phủ lên tóc. Ảnh giữ tỉ lệ, hình và nhãn trong thẻ căn giữa. 8 ảnh minh họa vẫn là ảnh tổng thể, chưa tách mọi nét hoặc gắn khớp. `images/scenes/` có PNG hoàn chỉnh; `images/illustrations/` giữ PNG minh họa nguyên bản.

Có **3 atlas trong suốt theo ô đều**, 3 bản `*-guide.png` có viền ô/nhãn Times New Roman, **6 tư thế Alex + 24 đạo cụ**, 30 PNG riêng thêm đệm trong suốt 32 px mỗi phía; không nâng độ phân giải nội dung. `images/sources/` giữ nguyên 3 sheet tạo sinh. `images/crop-map.json` ghi `[x,y,width,height]` theo pixel, ô trên atlas và vùng cắt ở nguồn. `asset-layout.json` mô tả cấu hình; `tools/build-monthly-payment-artwork.cjs` tái tạo atlas, PNG riêng, khung PNG và JSON từ nguồn bằng browser canvas, có chặn ghi đè trừ khi dùng `--force`. Không chạy đè lên bản sửa chưa sao lưu. Font cục bộ chỉ ở `work/`, không commit font độc quyền.

Đã thêm 30 ID `mpt-*` vào Kho đạo cụ bằng vùng cắt atlas mới, giữ 31 mục cũ nguyên vẹn. Tổng kho **61 mục = 51 đạo cụ + 10 tư thế Alex**. Dự án 001, WAV, MP4 và mã ứng dụng cũ không thay đổi; các bản sửa IndexedDB của người dùng không bị đọc/ghi bởi việc bổ sung tài nguyên xuất bản này. Các test cũ được đổi từ số dự án/nhân vật cố định sang đếm danh mục để phù hợp nhiều dự án và nhân vật.

**Chưa nhận audio cho video 002; chưa có MP4 hoặc bản dựng đã căn lời đọc.** `storyboard/project.json` mở trong trình video chỉ là bảng 16 ảnh tĩnh, mỗi cảnh tạm 6 giây (96 giây để duyệt hình), revision `artwork-board-v01`, audio rỗng. Tuyệt đối không gọi đây là video hoàn chỉnh hoặc dùng 96 giây làm thời lượng thật. Thông báo trạng thái này có ở trang chủ, gallery và README.

Đã kiểm tra: 10 unit test engine/WebM/media-storage; các bộ Playwright `tests/monthly-payment-artwork.cjs`, `tests/prop-library.cjs`, `tests/replace-prop.cjs`, `tests/project-workspaces.cjs`; mở/chỉnh cảnh 002 trong Studio, tải PNG Alex, gallery/mobile, 61 đạo cụ, mọi vùng cắt/padding, tỉ lệ ảnh, phép tính và tách vùng tiêu đề. Đã xem bản tổng hợp 16 khung và sheet Alex có nhãn. Xem `videos/002-monthly-payment-trap/validation.json`. Việc kiểm tra này chỉ áp dụng bộ hình; chưa kiểm tra chuyển động/âm thanh video 002 vì chưa có bản dựng theo audio.

Bước tiếp theo: người dùng xem hình và cung cấp WAV/MP3; căn nhiều shot từ 16 bố cục và sheet, giữ khoảng đệm, kiểm tra tóc/tay/chân ở lúc vào/giữa/ra, chuẩn hóa audio dẫn xuất nếu cần nhưng bảo toàn WAV, xuất MP4 duyệt vào tên mới. Chưa nhạc nền hoặc rig khớp. Nếu người dùng đã sửa trong Studio, nhận `.credit.json`/JSON trước khi tiếp tục từ bản sửa đó. Các lỗi MP4 video 001 đã ghi nhận vẫn chưa được sửa trong đợt này.
