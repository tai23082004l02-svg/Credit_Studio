# Nguồn và phép tính — Mortgage Payment v01

Ngày đối chiếu nguồn công khai: **2026-10-23 (Asia/Saigon)**.
Không dùng thống kê thị trường hiện tại; không khẳng định lãi suất hoặc giá nào là trung bình năm 2026.

## Nguồn chính thức và phạm vi dùng

1. [CFPB — Figure out how much you want to spend](https://www.consumerfinance.gov/owning-a-home/prepare/figure-out-how-much-you-want-to-spend/).
   Dùng cho việc tính toàn bộ ngân sách sở hữu: khoản vay, thuế, bảo hiểm, HOA nếu có, utilities, upkeep và tiền còn lại sau mua. Đối chiếu các phần Budget for new or changed expenses và Determine your down payment. Kịch bản không dùng tỉ lệ bảo trì hay mức quỹ dự phòng chung của nguồn làm quy tắc bắt buộc.
2. [CFPB — Principal and interest versus total monthly payment](https://www.consumerfinance.gov/ask-cfpb/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment-en-1941/).
   Dùng cho escrow, thuế/bảo hiểm có thể đã nằm trong khoản gửi servicer, HOA thường riêng, tổng thu có thể đổi dù principal/interest theo khoản vay fixed-rate thông thường ổn định. Không cộng khoản escrow và hóa đơn của cùng kỳ hai lần.
3. [CFPB — How does paying down a mortgage work?](https://www.consumerfinance.gov/ask-cfpb/how-does-paying-down-a-mortgage-work-en-1943/).
   Dùng cho phân biệt principal/interest, phần giảm dư nợ và equity. Phần equity không phải phép dự báo giá nhà; không gọi toàn bộ tiền trả vay là tiền mất đi hoặc toàn bộ là khoản tiết kiệm.
4. [CFPB — Loan Estimate explainer](https://www.consumerfinance.gov/owning-a-home/loan-estimate/).
   Dùng cho đọc Projected Payments, khoản không escrow, closing costs và estimated cash to close. So sánh cùng phạm vi chi phí và điều kiện vay.
5. [CFPB — Closing Disclosure explainer](https://www.consumerfinance.gov/owning-a-home/closing-disclosure/).
   Dùng cho kiểm tra số cuối cùng; phân biệt fees, prepaids, initial escrow và cash to close có điều chỉnh deposit/credits. Không gọi mọi khoản cash to close là phí mất đi.

Nội dung lời thoại là diễn giải mới, không trích nguyên văn các trang. Chủ đề là giáo dục tài chính, không kết luận mua/thuê bên nào luôn thắng, không dự báo giá nhà, không đề xuất sản phẩm hay khoản vay cá nhân.

## Ví dụ hư cấu thống nhất: Jamie

Tất cả giá/chi phí bên dưới là giả định biên tập. Lấy báo giá bảo hiểm, thuế địa phương và hồ sơ property thật nếu áp dụng ngoài video.

| Biến | Giá trị | Giới hạn |
| --- | ---: | --- |
| Giá mua | $300,000 | Hư cấu, không trung bình thị trường |
| Down payment | $60,000 = 20% | Không nói ai cũng cần 20% |
| Principal | $240,000 | Không cộng financed fees |
| Lãi suất | 6.5%/năm | Nominal interest, không APR/báo giá |
| Kỳ hạn | 360 tháng | Standard fully amortizing fixed-rate |
| Principal + interest | $1,516.963256…/tháng | Hiển thị/lời đọc làm tròn $1,517 |
| Property tax | $300/tháng tương đương $3,600/năm | Giả định, không quy tắc tăng thuế |
| Homeowners insurance | $125/tháng tương đương $1,500/năm | Giả định, không cam kết coverage |
| HOA | $75/tháng | Chỉ property ví dụ có HOA |
| Mortgage insurance | $0 | Giả định conventional, 20% down |
| Bills subtotal | $2,017/tháng | Dùng PI đã làm tròn; gồm HOA, trước utilities |
| Repair savings | $250/tháng | Tiền giữ trong savings, không chi phí đã trả |
| Housing allocation | $2,267/tháng | Bills + repair savings, trước utilities |
| So với PI | +$750/tháng | 300 + 125 + 75 + 250, không gọi tất cả là phí |
| First-month interest | $1,300 | 240,000 × .065 / 12 |
| First-month principal | $216.963256… | Làm tròn $217; không dùng cho mọi tháng |

Công thức kiểm tra: r = .065 / 12; n = 360; M = 240000 × r / (1 − (1+r)^(-n)).
Thuế/bảo hiểm được tính một lần; nếu hiển thị payment qua escrow thì nhóm PI + tax + insurance = $1,942, HOA riêng $75. Không gọi $2,267 là khoản gửi lender. Thanh tích lũy có các mốc 1517 → 1817 → 1942 → 2017 → 2267; đoạn cuối phân biệt màu/nhãn SAVED FOR REPAIRS.

## Cash sau mua và thời điểm sửa chữa

- Savings ban đầu $75,000 − down payment $60,000 − other closing amounts $9,000 = $6,000.
- Trừ moving/essentials $2,000 → $4,000 còn lại.
- $9,000 là tổng giả định gồm phí, prepaids và initial escrow funding; giả định không credits hoặc earlier deposits. Không thêm prepaid tax/insurance lần nữa như một phí riêng; mô hình này không lập sổ cái escrow theo ngày. Không khẳng định closing cost luôn bằng 3%.
- Down payment chuyển một phần tài sản từ cash sang equity, không minh họa bằng thùng rác.
- Quỹ sửa $250 × 12 = $3,000 trước rút tiền/lãi; sau hai lần chuyển chỉ $500. Hóa đơn $3,000 trong ví dụ không phải báo giá máy nước nóng/mái nhà thực tế. Quỹ phải đủ tiền trước khi trả, không vẽ thành âm nếu chưa có nguồn bù.
- So sánh “month 2” và “12 monthly transfers” là hai mốc để giải thích timing, không phải hai lần tiêu cùng một khoản. Không cộng repair expense lần nữa vào allocation đã gồm chính tiền chuyển vào quỹ.
- $4,000 là tiền mặt trong câu chuyện, không gọi là quỹ dự phòng đủ cho bất kỳ ai; cần xét toàn bộ chi tiêu/thu nhập/rủi ro.

## Hướng dẫn hình và kiểm tra sau khi có audio

Giữ nhãn FICTIONAL EXAMPLE ở cảnh số liệu, ASSUMED 6.5% FIXED INTEREST / 30 YEARS ở cảnh khoản vay. Hiện đầy đủ giả định lúc thiết lập ví dụ, không chỉ giấu trong mô tả. Tiền gốc và phần lưu savings có nhãn riêng với bills. Bars/counters dùng cùng thang, cùng keyframes; không đưa giá trị lên trước cue lời đọc.
