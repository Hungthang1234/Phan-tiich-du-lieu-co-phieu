# Thông Số Kỹ Thuật Các Mô Hình Dự báo Xu hướng Cổ phiếu

## 1. Bảng Thông Số Kỹ Thuật (Hyperparameters)

### Bảng 1: Logistic Regression (Baseline Model)

| Thông số | Giá trị | Mô tả |
|---------|--------|-------|
| Solver | lbfgs | Thuật toán tối ưu hóa cho bài toán phân loại đa lớp |
| Max iterations | 1000 | Số lần lặp tối đa để hội tụ |
| Random state | 42 | Hạt ngẫu nhiên để tái lập kết quả |
| Multi-class | multinomial | Chiến lược xử lý với 3 lớp (Tăng/Đi ngang/Giảm) |
| Penalty | L2 | Chính quy hóa L2 để tránh overfitting |
| C parameter | 1.0 | Nghịch đảo của độ mạnh chính quy (mặc định) |
| N_jobs | -1 | Sử dụng tất cả nhân xử lý |

---

### Bảng 2: XGBoost (Main Model)

| Thông số | Giá trị | Mô tả |
|---------|--------|-------|
| N_estimators | 100 | Số lượng cây quyết định trong ensemble |
| Max_depth | 5 | Độ sâu tối đa của mỗi cây (kiểm soát độ phức tạp) |
| Learning_rate | 0.1 | Hệ số thu nhỏ (tốc độ học) để cải thiện tổng quát hóa |
| Subsample | 1.0 | Tỷ lệ mẫu đào tạo dùng cho mỗi cây |
| Colsample_bytree | 1.0 | Tỷ lệ feature dùng cho mỗi cây |
| Objective | multi:softprob | Hàm mục tiêu cho phân loại đa lớp (xác suất) |
| Eval_metric | mlogloss | Chỉ số đánh giá multi-class logarithmic loss |
| Random_state | 42 | Hạt ngẫu nhiên để tái lập kết quả |
| N_jobs | -1 | Sử dụng tất cả nhân xử lý |
| Verbosity | 0 | Không hiển thị log chi tiết |

---

## 2. Mô tả Lý do Chọn Cấu hình Tham số

### Logistic Regression

Logistic Regression được chọn làm mô hình baseline do độ đơn giản, khả năng diễn giải cao và tốc độ huấn luyện nhanh, phù hợp cho bài toán phân loại xu hướng ba lớp với dữ liệu chuỗi thời gian. Thuật toán lbfgs được ưa thích vì tính ổn định với bài toán đa lớp, trong khi chính quy hóa L2 với C=1.0 (mặc định) giúp ngăn chặn overfitting mà không quá kiểm soát độ linh hoạt của mô hình. Số lần lặp tối đa 1000 đủ để thuật toán hội tụ trên tập dữ liệu kích thước trung bình (5.928 mẫu huấn luyện). Hạt ngẫu nhiên được cố định để đảm bảo tính tái lập khi thực hiện các thí nghiệm khác nhau.

### XGBoost

XGBoost được chọn làm mô hình chính do khả năng xử lý các mối quan hệ phi tuyến và tương tác đặc trưng phức tạp trong dữ liệu tài chính. Độ sâu cây tối đa được đặt ở 5 để cân bằng giữa độ phức tạp mô hình và khả năng tổng quát hóa, tránh tình trạng overfitting trên tập huấn luyện nhỏ. Hệ số học 0.1 được sử dụng để làm giảm tốc độ học, cho phép thuật toán Gradient Boosting hội tụ mượt mà hơn và cải thiện hiệu suất trên tập kiểm tra. Các tham số subsample và colsample_bytree được giữ ở 1.0 do kích thước tập dữ liệu và số lượng đặc trưng không quá lớn (20 đặc trưng), giảm nhu cầu lấy mẫu con để tránh underfitting. Hàm mục tiêu multi:softprob tạo ra xác suất cho từng lớp, cho phép xác định ngưỡng quyết định tùy chỉnh khi triển khai chiến lược giao dịch.

---

## 3. Kết quả Đánh giá Mô hình trên Tập Test

| Chỉ số | Logistic Regression | XGBoost |
|-------|---------------------|---------|
| Accuracy | 0.3958 (39.58%) | 0.3522 (35.22%) |
| Precision (Macro) | 0.40 | 0.35 |
| Recall (Macro) | 0.34 | 0.33 |
| F1-Score (Weighted) | 0.3937 | 0.3365 |

**Ghi chú:** Logistic Regression cho kết quả tốt hơn XGBoost trên tập test, phản ánh đặc điểm của dữ liệu thị trường chứng khoán Việt Nam trong giai đoạn 2023-2024 có thể phụ thuộc vào các mối quan hệ tuyến tính hoặc dữ liệu chứa nhiều nhiễu làm XGBoost dễ overfit. Mô hình Logistic Regression được chọn cho giai đoạn backtest chiến lược giao dịch.

---

## 4. Cấu hình Tiền xử lý Dữ liệu

| Bước xử lý | Phương pháp | Mục đích |
|-----------|-----------|---------|
| Chuẩn hóa đặc trưng | StandardScaler | Đưa tất cả đặc trưng về cùng tỷ lệ (trung bình 0, độ lệch chuẩn 1) |
| Điền NaN | Forward Fill → Backward Fill | Xử lý các giá trị bị thiếu trong chuỗi thời gian |
| Chia tập dữ liệu | Theo thời gian (không shuffle) | Bảo tồn tính chất chuỗi thời gian; tránh data leakage |

---

# II. THIẾT LẬP BACKTEST CHIẾN LƯỢC GIAO DỊCH

## 1. Bảng Thông Số Cấu hình Backtest

### Bảng 5: Thông Số Vốn và Chu kỳ Kiểm định

| Thông số | Giá trị | Mô tả |
|---------|--------|-------|
| Vốn ban đầu | 100 đơn vị (%) | Chuẩn hóa để so sánh hiệu suất giữa các cổ phiếu khác nhau |
| Giai đoạn backtest | 2023-01-01 → 2024-12-31 | Dữ liệu thực tế 2 năm gần nhất để đánh giá kỹ năng tiên đoán trên thị trường mới |
| Tần suất giao dịch | Hàng ngày (EOD) | Khớp lệnh vào cuối ngày giao dịch, tại giá đóng cửa |
| Số lệnh tối đa | 1 lệnh mở | Tại mỗi thời điểm chỉ nắm giữ 1 vị thế trên 1 mã cổ phiếu (fully invested hoặc fully cash) |

---

### Bảng 6: Quy Tắc Vào/Ra Lệnh (Ngưỡng Tín hiệu)

| Thông số | Giá trị | Mô tả |
|---------|--------|-------|
| Ngưỡng vào lệnh MUA | Xác suất ≥ 0.60 | Khi mô hình dự báo xác suất tăng ≥ 60%, tín hiệu mua (giữ vị thế) |
| Ngưỡng vào lệnh BÁN | Xác suất < 0.40 | Khi xác suất tăng < 40%, tín hiệu bán (không giữ vị thế, chuyển sang cash) |
| Vùng trung tính | 0.40 ≤ Xác suất < 0.60 | Khi xác suất nằm trong khoảng này, duy trì vị thế hiện tại (không hành động) |
| Loại tín hiệu | Nhị phân (0/1) | Chỉ có 2 trạng thái: nắm giữ cổ phiếu (1) hoặc không nắm giữ (0) |

---

### Bảng 7: Cơ Chế Khớp Lệnh và Phí Giao Dịch

| Thông số | Giá trị | Mô tả |
|---------|--------|-------|
| Giá khớp lệnh | Giá đóng cửa (EOD Close) | Lệnh được xử lý vào cuối phiên giao dịch (16:00) tại giá chính thức đóng cửa |
| Cơ chế khớp | T+0 (giả lập) | Giả định lệnh khớp ngay trong ngày; thực tế HOSE là T+2 nhưng được đơn giản hóa cho khả thi |
| Chi phí giao dịch (Phí) | 0.30% / lần | Tổng 0.30% cho mỗi vòng giao dịch (mua + bán) bao gồm phí môi giới (~0.10%) + thuế GTGT (~0.10%) + phí khác |
| Ảnh hưởng phí | Trừ khỏi vốn giao dịch | Phí được tính và trừ vào vốn hiện có trước khi mua (giảm lượng cổ phiếu có thể mua) |
| Slippage | Không tính | Giả định không có sự trượt giá do thực hiện lệnh (điều kiện lý tưởng) |

---

### Bảng 8: Chiến Lược So Sánh (Benchmark)

| Chiến lược | Mô tả | Mục đích |
|-----------|-------|---------|
| Chiến lược dự báo (ML) | Dựa trên tín hiệu từ mô hình Logistic Regression | Đánh giá hiệu suất của mô hình ML khi triển khai thực tế |
| Buy & Hold (BH) | Mua vào ngày đầu tiên và giữ đến hết giai đoạn | Benchmark tiêu chuẩn để so sánh; phản ánh chiến lược đầu tư thụ động |
| Outperformance | Lợi nhuận ML - Lợi nhuận BH | Độ vượt trội của mô hình so với buy & hold; nếu âm = mô hình thua buy & hold |

---

## 2. Mô tả Lý do Chọn Cấu hình Backtest

### Giai đoạn và Vốn

Giai đoạn kiểm định từ 2023-2024 được chọn vì đây là dữ liệu thị trường gần nhất, phản ánh điều kiện kinh tế-chính trị mới nhất của Việt Nam sau các biến động 2020-2022. Vốn ban đầu được chuẩn hóa thành 100 đơn vị (%) để dễ so sánh hiệu suất giữa các cổ phiếu khác nhau (tránh ảnh hưởng của mức giá tuyệt đối). Chiến lược fully invested hoặc fully cash được áp dụng nhằm đơn giản hóa logic ra quyết định và tránh vấn đề quản lý danh mục phức tạp với nhiều vị thế cùng lúc.

### Ngưỡng Tín hiệu và Cơ Chế Khớp Lệnh

Ngưỡng xác suất 0.60 và 0.40 được chọn dựa trên cân bằng giữa tính chủ động của tín hiệu (không quá khắt khe) và độ ổn định của chiến lược (tránh whipsaw). Khớp lệnh tại giá đóng cửa phản ánh thực tế nhà đầu tư cá nhân không thể khớp lệnh ngay trong phiên mà chỉ có thể vào lệnh tại EOD hoặc sàn đóng. Giả định T+0 được sử dụng để đơn giản hóa (thực tế HOSE là T+2 tương ứng 2 ngày làm việc), tuy nhiên ảnh hưởng của điều này là hạn chế do tần suất giao dịch không quá cao trên dữ liệu hàng ngày.

### Chi Phí Giao Dịch

Mức phí 0.30% mỗi vòng giao dịch bao gồm phí môi giới (~0.10%) và thuế GTGT (~0.10%) theo quy định hiện hành của Sở Giao dịch Chứng khoán Tp.HCM (HOSE) cho nhà đầu tư cá nhân. Phí được tính trực tiếp vào vốn giao dịch có sẵn, mô phỏng tình huống thực tế khi nhà đầu tư phải trả phí từ tài khoản. Việc không tính slippage (trượt giá) là một giả định lý tưởng để đơn giản hóa, nhưng có thể được bổ sung trong các nghiên cứu tiến hơn khi có dữ liệu intraday chi tiết.

### So Sánh Benchmark

Chiến lược Buy & Hold được chọn làm benchmark tiêu chuẩn vì nó đại diện cho chiến lược đầu tư thụ động, không cần kỹ năng dự báo, và là mục tiêu so sánh hợp lý cho bất kỳ chiến lược chủ động nào. Độ vượt trội (outperformance) được tính trực tiếp dưới dạng sai khác lợi nhuận (%), giúp nhà nghiên cứu đánh giá giá trị thực tế của mô hình ML trong bối cảnh thị trường chứng khoán Việt Nam.

