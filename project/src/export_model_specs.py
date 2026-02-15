# -*- coding: utf-8 -*-
# Xuất bảng thông số mô hình sang Excel

# Fix encoding
import sys
import os
import io
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd

from config import PROJECT_ROOT

# Tạo file kết quả
results_dir = PROJECT_ROOT / "results"

# Bảng 1: Logistic Regression
lr_params = {
    'Thông số': ['Solver', 'Max iterations', 'Random state', 'Multi-class', 'Penalty', 'C parameter', 'N_jobs'],
    'Giá trị': ['lbfgs', '1000', '42', 'multinomial', 'L2', '1.0', '-1'],
    'Mô tả': [
        'Thuật toán tối ưu hóa cho bài toán phân loại đa lớp',
        'Số lần lặp tối đa để hội tụ',
        'Hạt ngẫu nhiên để tái lập kết quả',
        'Chiến lược xử lý với 3 lớp (Tăng/Đi ngang/Giảm)',
        'Chính quy hóa L2 để tránh overfitting',
        'Nghịch đảo của độ mạnh chính quy (mặc định)',
        'Sử dụng tất cả nhân xử lý'
    ]
}

# Bảng 2: XGBoost
xgb_params = {
    'Thông số': [
        'N_estimators', 'Max_depth', 'Learning_rate', 'Subsample', 
        'Colsample_bytree', 'Objective', 'Eval_metric', 'Random_state', 'N_jobs', 'Verbosity'
    ],
    'Giá trị': [
        '100', '5', '0.1', '1.0', 
        '1.0', 'multi:softprob', 'mlogloss', '42', '-1', '0'
    ],
    'Mô tả': [
        'Số lượng cây quyết định trong ensemble',
        'Độ sâu tối đa của mỗi cây (kiểm soát độ phức tạp)',
        'Hệ số thu nhỏ (tốc độ học) để cải thiện tổng quát hóa',
        'Tỷ lệ mẫu đào tạo dùng cho mỗi cây',
        'Tỷ lệ feature dùng cho mỗi cây',
        'Hàm mục tiêu cho phân loại đa lớp (xác suất)',
        'Chỉ số đánh giá multi-class logarithmic loss',
        'Hạt ngẫu nhiên để tái lập kết quả',
        'Sử dụng tất cả nhân xử lý',
        'Không hiển thị log chi tiết'
    ]
}

# Bảng 3: Kết quả đánh giá
eval_results = {
    'Chỉ số': ['Accuracy', 'Precision (Macro)', 'Recall (Macro)', 'F1-Score (Weighted)'],
    'Logistic Regression': ['0.3958', '0.40', '0.34', '0.3937'],
    'XGBoost': ['0.3522', '0.35', '0.33', '0.3365'],
    'Lựa chọn': ['LR (39.58% > 35.22%)', 'LR (0.40 > 0.35)', 'LR (0.34 ≈ 0.33)', 'LR (0.3937 > 0.3365)']
}

# Bảng 4: Tiền xử lý
preprocessing = {
    'Bước xử lý': ['Chuẩn hóa đặc trưng', 'Điền NaN', 'Chia tập dữ liệu'],
    'Phương pháp': ['StandardScaler', 'Forward Fill → Backward Fill', 'Theo thời gian (không shuffle)'],
    'Mục đích': [
        'Đưa tất cả đặc trưng về cùng tỷ lệ (trung bình 0, độ lệch chuẩn 1)',
        'Xử lý các giá trị bị thiếu trong chuỗi thời gian',
        'Bảo tồn tính chất chuỗi thời gian; tránh data leakage'
    ]
}

# Tạo DataFrame
df_lr = pd.DataFrame(lr_params)
df_xgb = pd.DataFrame(xgb_params)
df_eval = pd.DataFrame(eval_results)
df_prep = pd.DataFrame(preprocessing)

# Lưu thành Excel
excel_file = results_dir / "Model_Specifications.xlsx"

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df_lr.to_excel(writer, sheet_name='Logistic Regression', index=False)
    df_xgb.to_excel(writer, sheet_name='XGBoost', index=False)
    df_eval.to_excel(writer, sheet_name='Evaluation Results', index=False)
    df_prep.to_excel(writer, sheet_name='Preprocessing', index=False)

print(f"✓ Lưu file: {excel_file}")

# Lưu thành CSV riêng để tiện tham khảo
df_lr.to_csv(results_dir / "01_logistic_regression_params.csv", index=False, encoding='utf-8-sig')
df_xgb.to_csv(results_dir / "02_xgboost_params.csv", index=False, encoding='utf-8-sig')
df_eval.to_csv(results_dir / "03_evaluation_results.csv", index=False, encoding='utf-8-sig')
df_prep.to_csv(results_dir / "04_preprocessing_steps.csv", index=False, encoding='utf-8-sig')

print("✓ Lưu file CSV:")
print("  - 01_logistic_regression_params.csv")
print("  - 02_xgboost_params.csv")
print("  - 03_evaluation_results.csv")
print("  - 04_preprocessing_steps.csv")

print("\n=== TÓM TẮT ===")
print(f"Tất cả bảng đã lưu trong: {results_dir}")
