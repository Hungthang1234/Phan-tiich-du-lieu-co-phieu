# Hướng dẫn Chạy Pipeline Phân Tích Dữ Liệu & Dự Báo Xu Hướng Cổ Phiếu VN30

## Mục lục
1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt](#cài-đặt)
3. [Chạy Pipeline](#chạy-pipeline)
4. [Cấu trúc dự án](#cấu-trúc-dự-án)
5. [Kết quả & Output](#kết-quả--output)

---

## Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Hệ điều hành**: Windows, Linux, macOS
- **Bộ nhớ**: >= 4 GB RAM
- **Dung lượng**: >= 2 GB (cho dữ liệu + mô hình + biểu đồ)

---

## Cài đặt

### 1. Download/Tải dự án
- Tải file zip từ GitHub hoặc source
- Giải nén vào thư mục bất kỳ (VD: `C:\my_projects\KLTN`)

### 2. Kiểm tra Python đã cài chưa
```bash
python --version
```
Nếu chưa cài, download từ [python.org](https://www.python.org/downloads/) (bản 3.8+)

### 3. Cài đặt các package cần thiết
Mở Command Prompt tại thư mục dự án:
```bash
pip install -r requirements.txt
```

**Hoặc cài thủ công:**
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
```

### 4. Chuẩn bị dữ liệu
- Đặt các file CSV vào thư mục `data/raw/`:
  - `FPT.csv`, `HPG.csv`, `VCB.csv`, `MWG.csv`, `ACB.csv`
  - `VNINDEX.csv`, `VN30.csv`
  - (File định dạng: Date, Open, High, Low, Close, Volume)

---

## Cho Máy Khác (Nhanh & Tự Động)

**Nếu máy khác chưa cài các packages, có 2 cách:**

### Cách A: Setup + Chạy Ngay (1 click)

1. Tải folder dự án về máy khác
2. Mở File Explorer -> Thư mục dự án
3. **Double-click setup_and_run.bat**
4. Script tự động:
   - Kiểm tra Python
   - Cài đặt packages (có timeout mở rộng để tránh bị đứ)
   - Chạy pipeline

Nhanh nhất, khuyên dùng!

### Cách B: Cài Packages Riêng (nếu Cách A bị đứ)

1. **Double-click install_packages.bat** - chỉ cài packages
2. Chờ xong, sau đó **double-click run.bat** - chạy pipeline

Lợi ích: Nếu cài packages bị lỗi, bạn có thể fix riêng, rồi chạy pipeline sau

---

## Nếu Bị Đứ Khi Cài Packages

**Vấn đề:** Tải packages từ internet có khi chậm hoặc timeout

**Giải pháp:**

1. Mở Command Prompt trong thư mục dự án
2. Chạy lệnh này:
   ```bash
   pip install --default-timeout=1000 --only-binary=:all: pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
   ```
   (Chờ 3-5 phút, không bấm gì)
3. Sau khi xong, chạy: `python run_pipeline.py`

---

## Chạy Pipeline

### Cách 1: Windows - Setup Tự Động (KHUYÊN DÙNG)

**Chỉ cần 1 click để cài + chạy:**

1. **Double-click setup_and_run.bat**
2. Chờ xong kết quả
3. Bấm phím bất kỳ để đóng

### Cách 2: Windows - Chạy Nhanh (packages đã cài)

```bash
# Double-click: run.bat
# HOẶC Command Prompt:
python run_pipeline.py
```

### Cách 2.5: Xem Kết Quả Trên Web Dashboard

Sau khi chạy xong pipeline, xem kết quả trực quan trên web:

**Double-click: run_dashboard.bat**

- Tự động khởi động Flask server
- Mở trình duyệt vào `http://localhost:5000`
- Chọn mã cổ phiếu xem metrics và biểu đồ chi tiết

**Hoặc chạy thủ công:**
```bash
python dashboard_server.py
```
Rồi mở trình duyệt vào: `http://localhost:5000`

### Cách 3: Linux/Mac Terminal

```bash
# Cài packages
pip install -r requirements.txt

# Chạy pipeline
python3 run_pipeline.py
```

### Cách 4: Chạy từng bước riêng

```bash
cd src
python prepare_data.py        # Bước 1
python train_model.py         # Bước 2
python predict_price.py       # Bước 3
python backtest.py            # Bước 4
python visualize.py           # Bước 5
python visualize_by_stock.py  # Bước 6
python export_model_specs.py  # Bước 7
python export_backtest_specs.py # Bước 8
```

---

## Cấu trúc dự án

```
project/
├── data/
│   ├── raw/                    # Dữ liệu thô (CSV files)
│   │   ├── FPT.csv
│   │   ├── HPG.csv
│   │   ├── VCB.csv
│   │   ├── MWG.csv
│   │   ├── ACB.csv
│   │   ├── VNINDEX.csv
│   │   └── VN30.csv
│   └── processed/              # Dữ liệu đã xử lý
│       ├── all_stocks_prepared.csv
│       ├── train_data.csv
│       ├── val_data.csv
│       └── test_data.csv
│
├── src/
│   ├── config.py              # Cấu hình chung
│   ├── prepare_data.py        # Xử lý dữ liệu
│   ├── train_model.py         # Huấn luyện mô hình
│   ├── predict_price.py       # Dự báo giá
│   ├── backtest.py            # Backtest chiến lược
│   ├── visualize.py           # Biểu đồ tổng hợp
│   ├── visualize_by_stock.py  # Biểu đồ chi tiết
│   ├── export_model_specs.py  # Xuất bảng thông số
│   └── export_backtest_specs.py # Xuất bảng backtest
│
├── models/                     # Mô hình đã huấn luyện
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── feature_columns.pkl
│   ├── price_model.pkl
│   ├── price_scaler.pkl
│   └── price_features.pkl
│
├── plots/                      # Biểu đồ
│   ├── model_analysis/         # Confusion Matrix, Feature Importance
│   ├── trading_analysis/       # Equity Curve, Buy/Sell Signals
│   ├── price_predictions/      # Dự báo giá
│   └── by_stock/               # Biểu đồ chi tiết từng mã
│       ├── FPT/
│       ├── HPG/
│       ├── VCB/
│       ├── MWG/
│       └── ACB/
│
├── results/                    # Kết quả & bảng
│   ├── train_data.csv
│   ├── strategy_results.csv
│   ├── price_predictions.csv
│   ├── model_specifications.md    # Bảng thông số mô hình
│   ├── Model_Specifications.xlsx
│   ├── Backtest_Specifications.xlsx
│   └── [các file CSV khác]
│
├── run_pipeline.py            # Script Python chạy toàn bộ
├── run_pipeline.bat           # Script Windows (double-click)
├── run_pipeline.sh            # Script Linux/Mac (bash)
├── setup_and_run.bat          # Script Windows setup + run (double-click)
├── install_packages.bat       # Script Windows cài packages (double-click)
├── run.bat                    # Script Windows chạy pipeline (double-click)
├── README.md                  # File này
└── requirements.txt           # Danh sách package
```

---

## Kết quả & Output

Pipeline sẽ tạo ra các file/thư mục sau:

### 1. **Dữ liệu xử lý** (`data/processed/`)
- `train_data.csv`: Dữ liệu huấn luyện (2015-2020)
- `val_data.csv`: Dữ liệu validation (2021-2022)
- `test_data.csv`: Dữ liệu test/backtest (2023-2024)

### 2. **Mô hình** (`models/`)
- `model.pkl`: Mô hình dự báo xu hướng (Logistic Regression)
- `price_model.pkl`: Mô hình dự báo giá (Linear Regression)
- `scaler.pkl`, `price_scaler.pkl`: Scaler cho chuẩn hóa

### 3. **Biểu đồ** (`plots/`)

#### `model_analysis/`
- `confusion_matrix.png` - Ma trận nhầm lẫn
- `feature_importance.png` - Top 15 feature quan trọng
- `model_performance_summary.png` - So sánh MAE/RMSE/MAPE

#### `trading_analysis/`
- `equity_curve.png` - Đường giá trị tài khoản
- `buy_sell_signals.png` - Buy/Sell signals

#### `price_predictions/`
- `price_prediction_linear_regression.png` - Tổng thể
- `price_prediction_FPT.png`, `HPG.png`, v.v. - Từng mã

#### `by_stock/FPT/` (tương tự cho HPG, VCB, MWG, ACB)
- `01_FPT_price_actual_vs_predicted.png` - Giá thực vs dự đoán
- `02_FPT_prediction_error_vnd.png` - Sai số (VND)
- `03_FPT_prediction_error_percent.png` - Sai số (%)
- `04_FPT_buy_sell_signals.png` - Tín hiệu giao dịch
- `05_FPT_probability.png` - Xác suất dự báo
- `FPT_equity_curve.png` - Equity curve

### 4. **Kết quả & Bảng** (`results/`)

#### File CSV
- `strategy_results.csv` - Kết quả backtest chiến lược
- `buy_hold_results.csv` - Kết quả buy & hold
- `comparison.csv` - So sánh hai chiến lược
- `price_predictions.csv` - Dự báo giá chi tiết

#### File bảng thông số (cho luận văn)
- `Model_Specifications.xlsx` - Excel với 4 sheet
- `Backtest_Specifications.xlsx` - Excel backtest config
- `model_specifications.md` - Markdown (copy vào luận văn)
- `*.csv` - Các bảng riêng lẻ

### 5. **Web Dashboard** (`dashboard.html`, `dashboard_server.py`)

Sau khi chạy pipeline, xem kết quả trực quan trên web:

- **Chạy**: Double-click `run_dashboard.bat` (hoặc `python dashboard_server.py`)
- **Truy cập**: `http://localhost:5000`
- **Tính năng**:
  - Chọn mã cổ phiếu từ dropdown
  - Xem metrics: Tổng lợi nhuận, Max Drawdown, Sharpe Ratio
  - So sánh hiệu suất chiến lược ML vs Buy & Hold
  - 6 biểu đồ chi tiết cho mỗi mã:
    - Giá thực tế vs dự đoán
    - Sai số dự báo (VND & %)
    - Tín hiệu mua/bán
    - Xác suất dự báo
    - Equity curve

---

## Kỳ vọng Kết quả

Sau khi chạy xong, bạn sẽ có:

1. Mô hình được huấn luyện với độ chính xác ~39.58% (Logistic Regression)
2. Dự báo giá với MAPE ~0.47%
3. Backtest kết quả so sánh chiến lược ML vs Buy & Hold
4. Biểu đồ chi tiết cho từng mã cổ phiếu
5. Bảng thông số sẵn sàng copy vào luận văn

---

## Lưu ý

- **Lần chạy đầu tiên**: Chạy đầy đủ tất cả 8 bước, mất ~2-5 phút tuỳ cấu hình máy
- **Lần chạy tiếp theo**: Có thể chạy từng bước riên lẻ nếu chỉ muốn cập nhật phần nào đó
- **Dữ liệu**: Đảm bảo các file CSV trong `data/raw/` (FPT.csv, HPG.csv, VCB.csv, MWG.csv, ACB.csv, v.v.)
- **Unicode**: Nếu gặp lỗi encoding trên Windows, đảm bảo Command Prompt mở với UTF-8

---

## Xử lý Lỗi

### Lỗi: "Python not found"
```bash
# Cài Python từ python.org hoặc
# Thêm Python vào PATH
```

### Lỗi: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
# hoặc
pip install --default-timeout=1000 --only-binary=:all: pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
```

### Lỗi: "Dữ liệu không tìm thấy"
- Kiểm tra folder `data/raw/` có các file CSV: FPT.csv, HPG.csv, VCB.csv, MWG.csv, ACB.csv, VNINDEX.csv, VN30.csv
- Đảm bảo tên file đúng (phân biệt HOA/thường)

### Lỗi: "Encoding"
- Thêm dòng này vào đầu script Python:
```python
# -*- coding: utf-8 -*-
```

---

## Liên hệ & Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Python version: `python --version` (>= 3.8)
2. Các package cần thiết: `pip list | grep -E "pandas|sklearn|xgboost"`
3. Dữ liệu trong `data/raw/`

---

**Chúc bạn thành công!**
