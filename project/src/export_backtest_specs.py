# -*- coding: utf-8 -*-
# Xuất bảng thông số backtest sang Excel

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

# Bảng 5: Vốn và chu kỳ
capital_config = {
    'Thông số': ['Vốn ban đầu', 'Giai đoạn backtest', 'Tần suất giao dịch', 'Số lệnh tối đa'],
    'Giá trị': ['100 đơn vị (%)', '2023-01-01 → 2024-12-31', 'Hàng ngày (EOD)', '1 lệnh mở'],
    'Mô tả': [
        'Chuẩn hóa để so sánh hiệu suất giữa các cổ phiếu khác nhau',
        'Dữ liệu thực tế 2 năm gần nhất để đánh giá kỹ năng tiên đoán trên thị trường mới',
        'Khớp lệnh vào cuối ngày giao dịch, tại giá đóng cửa',
        'Tại mỗi thời điểm chỉ nắm giữ 1 vị thế trên 1 mã cổ phiếu (fully invested hoặc fully cash)'
    ]
}

# Bảng 6: Ngưỡng tín hiệu
signal_config = {
    'Thông số': [
        'Ngưỡng vào lệnh MUA',
        'Ngưỡng vào lệnh BÁN',
        'Vùng trung tính',
        'Loại tín hiệu'
    ],
    'Giá trị': [
        'Xác suất ≥ 0.60',
        'Xác suất < 0.40',
        '0.40 ≤ Xác suất < 0.60',
        'Nhị phân (0/1)'
    ],
    'Mô tả': [
        'Khi mô hình dự báo xác suất tăng ≥ 60%, tín hiệu mua (giữ vị thế)',
        'Khi xác suất tăng < 40%, tín hiệu bán (không giữ vị thế, chuyển sang cash)',
        'Khi xác suất nằm trong khoảng này, duy trì vị thế hiện tại (không hành động)',
        'Chỉ có 2 trạng thái: nắm giữ cổ phiếu (1) hoặc không nắm giữ (0)'
    ]
}

# Bảng 7: Cơ chế khớp lệnh
execution_config = {
    'Thông số': [
        'Giá khớp lệnh',
        'Cơ chế khớp',
        'Chi phí giao dịch (Phí)',
        'Ảnh hưởng phí',
        'Slippage'
    ],
    'Giá trị': [
        'Giá đóng cửa (EOD Close)',
        'T+0 (giả lập)',
        '0.30% / lần',
        'Trừ khỏi vốn giao dịch',
        'Không tính'
    ],
    'Mô tả': [
        'Lệnh được xử lý vào cuối phiên giao dịch (16:00) tại giá chính thức đóng cửa',
        'Giả định lệnh khớp ngay trong ngày; thực tế HOSE là T+2 nhưng được đơn giản hóa cho khả thi',
        'Tổng 0.30% cho mỗi vòng giao dịch (mua + bán) bao gồm phí môi giới (~0.10%) + thuế GTGT (~0.10%) + phí khác',
        'Phí được tính và trừ vào vốn hiện có trước khi mua (giảm lượng cổ phiếu có thể mua)',
        'Giả định không có sự trượt giá do thực hiện lệnh (điều kiện lý tưởng)'
    ]
}

# Bảng 8: So sánh benchmark
benchmark_config = {
    'Chiến lược': ['Chiến lược dự báo (ML)', 'Buy & Hold (BH)', 'Outperformance'],
    'Mô tả': [
        'Dựa trên tín hiệu từ mô hình Logistic Regression',
        'Mua vào ngày đầu tiên và giữ đến hết giai đoạn',
        'Lợi nhuận ML - Lợi nhuận BH'
    ],
    'Mục đích': [
        'Đánh giá hiệu suất của mô hình ML khi triển khai thực tế',
        'Benchmark tiêu chuẩn để so sánh; phản ánh chiến lược đầu tư thụ động',
        'Độ vượt trội của mô hình so với buy & hold; nếu âm = mô hình thua buy & hold'
    ]
}

# Tạo DataFrame
df_capital = pd.DataFrame(capital_config)
df_signal = pd.DataFrame(signal_config)
df_exec = pd.DataFrame(execution_config)
df_bench = pd.DataFrame(benchmark_config)

# Lưu thành Excel bổ sung (chế độ append nếu file cũ tồn tại)
excel_file = results_dir / "Backtest_Specifications.xlsx"

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df_capital.to_excel(writer, sheet_name='Capital & Period', index=False)
    df_signal.to_excel(writer, sheet_name='Signal Thresholds', index=False)
    df_exec.to_excel(writer, sheet_name='Execution & Fees', index=False)
    df_bench.to_excel(writer, sheet_name='Benchmark', index=False)

print(f"✓ Lưu file: {excel_file}")

# Lưu thành CSV riêng
df_capital.to_csv(results_dir / "05_backtest_capital_period.csv", index=False, encoding='utf-8-sig')
df_signal.to_csv(results_dir / "06_backtest_signal_thresholds.csv", index=False, encoding='utf-8-sig')
df_exec.to_csv(results_dir / "07_backtest_execution_fees.csv", index=False, encoding='utf-8-sig')
df_bench.to_csv(results_dir / "08_backtest_benchmark.csv", index=False, encoding='utf-8-sig')

print("✓ Lưu file CSV:")
print("  - 05_backtest_capital_period.csv")
print("  - 06_backtest_signal_thresholds.csv")
print("  - 07_backtest_execution_fees.csv")
print("  - 08_backtest_benchmark.csv")

print("\n=== TÓM TẮT ===")
print(f"Tất cả bảng backtest đã lưu trong: {results_dir}")
