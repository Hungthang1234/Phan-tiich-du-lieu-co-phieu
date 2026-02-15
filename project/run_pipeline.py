#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_pipeline.py - Script chạy toàn bộ pipeline phân tích dữ liệu và dự báo xu hướng cổ phiếu
Một lần nhấp = Tự động chạy tất cả các bước từ chuẩn hóa dữ liệu đến backtest
"""

import sys
import os
import io
import subprocess
from pathlib import Path
import time
from datetime import datetime

# Fix encoding cho Windows
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Thêm src vào path
project_root = Path(__file__).parent  # project/
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Tạo thư mục logs nếu không tồn tại
logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

# Màu sắc cho output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """In header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_step(step_num, text):
    """In bước"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}[BƯỚC {step_num}]{Colors.ENDC} {text}")

def print_success(text):
    """In thành công"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """In lỗi"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    """In thông tin"""
    print(f"{Colors.OKCYAN}{text}{Colors.ENDC}")

def run_script(script_name, description):
    """Chạy một script Python"""
    script_path = src_dir / f"{script_name}.py"
    
    if not script_path.exists():
        print_error(f"Script không tồn tại: {script_path}")
        return False
    
    print_step("", description)
    print_info(f"Đang chạy: {script_path}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(src_dir),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"{description} - Hoàn tất!\n")
            return True
        else:
            print_error(f"{description} - Lỗi!")
            return False
    
    except Exception as e:
        print_error(f"{description} - Lỗi: {str(e)}")
        return False

def check_required_modules():
    """Kiểm tra xem có các module cần thiết chưa"""
    required_modules = ['pandas', 'numpy', 'sklearn', 'xgboost', 'matplotlib', 'seaborn', 'openpyxl', 'flask', 'flask_cors']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    return missing_modules

def main():
    """Main pipeline"""
    
    # Kiểm tra packages
    missing = check_required_modules()
    if missing:
        print_header("LỖI: THIẾU CÁC THƯ VIỆN CẦN THIẾT")
        print_error(f"Các package sau chưa được cài đặt: {', '.join(missing)}")
        print(f"\n{Colors.WARNING}{Colors.BOLD}CÁCH FIX:{Colors.ENDC}")
        print(f"{Colors.WARNING}1. Chạy file 'setup_and_run.bat' (nếu lần đầu){Colors.ENDC}")
        print(f"{Colors.WARNING}2. Hoặc chạy 'install_packages.bat' để chỉ cài packages{Colors.ENDC}")
        print(f"{Colors.WARNING}3. Xem chi tiết trong README.md{Colors.ENDC}\n")
        return 1
    
    # Tạo timestamp cho log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"pipeline_{timestamp}.log"
    
    print_header("PIPELINE PHÂN TÍCH DỮ LIỆU & DỰ BÁO XU HƯỚNG CỔ PHIẾU VN30")
    
    # Thông báo quan trọng
    print(f"{Colors.WARNING}{Colors.BOLD}[THÔNG BÁO QUAN TRỌNG]{Colors.ENDC}")
    print(f"{Colors.WARNING}1. Nếu lần đầu chạy, vui lòng chạy 'setup_and_run.bat' hoặc 'install_packages.bat' trước!{Colors.ENDC}")
    print(f"{Colors.WARNING}2. Mô hình này là dự báo xu hướng (tăng/giảm), độ chính xác ~39% - KHÔNG PHải dự đoán giá chính xác{Colors.ENDC}")
    print(f"{Colors.WARNING}3. Kết quả backtest cho thấy chiến lược này KHÔNG luôn thắng hơn mua & nắm giữ{Colors.ENDC}")
    print(f"{Colors.WARNING}4. Sử dụng kết quả này chỉ cho mục đích học tập và nghiên cứu{Colors.ENDC}\n")
    
    print_info("Chương trình sẽ chạy tự động tất cả các bước xử lý, huấn luyện, dự báo, và backtest")
    print_info(f"Thư mục dự án: {project_root}")
    print_info(f"Log file: {log_file}\n")
    
    # Danh sách các bước
    steps = [
        (1, "prepare_data", "Bước 1: Chuẩn hóa dữ liệu & Tạo feature kỹ thuật"),
        (2, "train_model", "Bước 2: Huấn luyện mô hình dự báo xu hướng"),
        (3, "predict_price", "Bước 3: Dự báo giá & Đánh giá (MAE, RMSE, MAPE)"),
        (4, "backtest", "Bước 4: Backtest chiến lược giao dịch"),
        (5, "visualize", "Bước 5: Vẽ biểu đồ tổng hợp"),
        (6, "visualize_by_stock", "Bước 6: Vẽ biểu đồ chi tiết theo từng mã"),
        (7, "export_model_specs", "Bước 7: Xuất bảng thông số mô hình"),
        (8, "export_backtest_specs", "Bước 8: Xuất bảng thông số backtest"),
    ]
    
    results = {}
    total_steps = len(steps)
    success_count = 0
    
    start_time = time.time()
    
    # Ghi vào log file
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Pipeline Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Project: {project_root}\n")
        f.write("="*80 + "\n\n")
    
    for step_num, script, description in steps:
        success = run_script(script, description)
        results[script] = success
        if success:
            success_count += 1
        
        # Ghi kết quả vào log file
        with open(log_file, 'a', encoding='utf-8') as f:
            status = "SUCCESS" if success else "FAILED"
            f.write(f"[{status}] {description}\n")
        
        time.sleep(1)  # Delay giữa các bước
    
    elapsed_time = time.time() - start_time
    
    # Tóm tắt kết quả
    print_header("TÓM TẮT KẾT QUẢ")
    
    for script, success in results.items():
        status = f"{Colors.OKGREEN}✓ THÀNH CÔNG{Colors.ENDC}" if success else f"{Colors.FAIL}✗ THẤT BẠI{Colors.ENDC}"
        print(f"{script:.<40} {status}")
    
    print(f"\n{Colors.BOLD}Tổng cộng:{Colors.ENDC} {success_count}/{total_steps} bước hoàn tất")
    print(f"{Colors.BOLD}Thời gian:{Colors.ENDC} {elapsed_time:.1f} giây\n")
    
    # Ghi tóm tắt vào log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"Summary: {success_count}/{total_steps} steps completed\n")
        f.write(f"Total time: {elapsed_time:.1f} seconds\n")
        f.write(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Kết quả cuối cùng
    if success_count == total_steps:
        print_header("TOÀN BỘ PIPELINE HOÀN TẤT THÀNH CÔNG")
        print_success("Tất cả bước đã chạy thành công!")
        print_info("\nCác file kết quả được lưu trong:")
        print_info(f"  - Dữ liệu: {project_root}/data/processed/")
        print_info(f"  - Mô hình: {project_root}/models/")
        print_info(f"  - Biểu đồ: {project_root}/plots/")
        print_info(f"  - Kết quả: {project_root}/results/")
        print_info(f"  - Log: {log_file}")
        return 0
    else:
        print_header("PIPELINE GẶP LỖI")
        print_error(f"Có {total_steps - success_count} bước không thành công!")
        print_info(f"Xem chi tiết tại: {log_file}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
