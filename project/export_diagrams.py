#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
export_diagrams.py - Xuất sơ đồ vận hành ra ảnh PNG
"""

import sys
import os
import io
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

# Tạo thư mục output
PROJECT_ROOT = Path(__file__).parent.parent
DIAGRAMS_DIR = PROJECT_ROOT / "diagrams"
DIAGRAMS_DIR.mkdir(exist_ok=True)

# Cấu hình font
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("Đang tạo sơ đồ vận hành...")
print(f"Output: {DIAGRAMS_DIR}")

# ═══════════════════════════════════════════════════════════════════════════════
# SƠ ĐỒ 1: KIẾN TRÚC TỔNG THỂ
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Title
ax.text(5, 11.5, 'KIẾN TRÚC HỆ THỐNG DỰ ÁN', ha='center', fontsize=16, weight='bold')

# Dữ liệu thực
box1 = FancyBboxPatch((3, 9.5), 4, 1, boxstyle="round,pad=0.1", 
                       edgecolor='blue', facecolor='lightblue', linewidth=2.5)
ax.add_patch(box1)
ax.text(5, 10.2, 'DỮ LIỆU THỰC', ha='center', va='center', fontsize=12, weight='bold')
ax.text(5, 9.8, '2015-2024 (13,520 records)', ha='center', va='center', fontsize=9)

# Arrow
arrow = FancyArrowPatch((5, 9.5), (5, 8.5), arrowstyle='->', mutation_scale=35, linewidth=3, color='#1f77b4', connectionstyle="arc3")
ax.add_patch(arrow)

# Pipeline
box2 = FancyBboxPatch((2, 7.5), 6, 1, boxstyle="round,pad=0.1", 
                       edgecolor='green', facecolor='lightgreen', linewidth=2.5)
ax.add_patch(box2)
ax.text(5, 8.2, 'PIPELINE XỬ LÝ', ha='center', va='center', fontsize=12, weight='bold')
ax.text(5, 7.8, '8 Bước: Chuẩn bị → Huấn luyện → Backtest → Xuất kết quả', ha='center', va='center', fontsize=9)

# Arrow
arrow = FancyArrowPatch((5, 7.5), (5, 5.5), arrowstyle='->', mutation_scale=35, linewidth=3, color='#1f77b4', connectionstyle="arc3")
ax.add_patch(arrow)

# Dashboard box - larger
dashboard_box = FancyBboxPatch((1.5, 4), 7, 1.3, boxstyle="round,pad=0.15", 
                               edgecolor='darkgreen', facecolor='#90EE90', linewidth=2.5)
ax.add_patch(dashboard_box)
ax.text(5, 5, 'WEB DASHBOARD', ha='center', va='center', fontsize=13, weight='bold')
ax.text(5, 4.5, 'localhost:5000 - Xem kết quả trực quan', ha='center', va='center', fontsize=10)

# Output details at bottom
output_box = FancyBboxPatch((1, 1.5), 8, 2, boxstyle="round,pad=0.1", 
                            edgecolor='#666666', facecolor='#F5F5F5', linewidth=1.5, linestyle='--')
ax.add_patch(output_box)
ax.text(5, 3.2, 'KẾT QUẢ ĐẦU RA:', ha='center', va='center', fontsize=11, weight='bold')
ax.text(5, 2.7, '• 30 biểu đồ (6 plot × 5 cổ phiếu)', ha='center', va='center', fontsize=9)
ax.text(5, 2.3, '• 3 file Excel (model specs, backtest results, predictions)', ha='center', va='center', fontsize=9)
ax.text(5, 1.9, '• CSV chi tiết và thống kê', ha='center', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / '01_kien_truc_tong_the.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: 01_kien_truc_tong_the.png")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SƠ ĐỒ 2: PIPELINE 8 BƯỚC
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(8, 9.5, 'PIPELINE 8 BƯỚC CHI TIẾT', ha='center', fontsize=16, weight='bold')

steps_detail = [
    (1, 'BƯỚC 1\nChuẩn bị\nDữ liệu', 'blue'),
    (3, 'BƯỚC 2\nHuấn luyện\nPhân loại', 'green'),
    (5, 'BƯỚC 3\nDự báo\nGiá', 'orange'),
    (7, 'BƯỚC 4\nBacktest\nChiến lược', 'red'),
    (9, 'BƯỚC 5\nBiểu đồ\nTổng hợp', 'purple'),
    (11, 'BƯỚC 6\nBiểu đồ\nChi tiết', 'brown'),
    (13, 'BƯỚC 7\nXuất\nModel', 'cyan'),
    (15, 'BƯỚC 8\nXuất\nBacktest', 'magenta'),
]

for i, (x, label, color) in enumerate(steps_detail):
    # Box
    box = FancyBboxPatch((x-0.7, 7), 1.4, 1.5, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color, alpha=0.7, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, 7.75, label, ha='center', va='center', fontsize=8, weight='bold', color='white')
    
    # Arrow to next
    if i < len(steps_detail) - 1:
        arrow = FancyArrowPatch((x+0.7, 7.75), (steps_detail[i+1][0]-0.7, 7.75), 
                                arrowstyle='->', mutation_scale=15, linewidth=2, color='black')
        ax.add_patch(arrow)

# Outputs below
outputs_detail = [
    (1, 'processed/\ntrain_data.csv'),
    (3, 'model.pkl\nscaler.pkl'),
    (5, 'price_model.pkl'),
    (7, 'strategy_\nresults.csv'),
    (9, '10 plots'),
    (11, '30 plots'),
    (13, 'Excel\nModel'),
    (15, 'Excel\nBacktest'),
]

for x, label in outputs_detail:
    box = FancyBboxPatch((x-0.6, 5.2), 1.2, 1, boxstyle="round,pad=0.05", 
                          edgecolor='gray', facecolor='lightyellow', linewidth=1)
    ax.add_patch(box)
    ax.text(x, 5.7, label, ha='center', va='center', fontsize=7)
    
    # Arrow from step to output
    arrow = FancyArrowPatch((x, 7), (x, 6.2), arrowstyle='->', mutation_scale=12, linewidth=1, color='gray', linestyle='--')
    ax.add_patch(arrow)

# Add metrics at bottom
metrics = [
    ('Accuracy\n39.58%', 1),
    ('MAPE\n0.47%', 3),
    ('Return\n3.70%', 7),
    ('Sharpe\n0.37', 9),
]

y_metrics = 3.5
for label, x in metrics:
    ax.text(x, y_metrics, label, ha='center', va='center', fontsize=8, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Timeline
ax.text(8, 2.5, 'TỔNG THỜI GIAN: 5-7 phút (lần đầu)', ha='center', fontsize=11, weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / '02_pipeline_8_buoc.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: 02_pipeline_8_buoc.png")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SƠ ĐỒ 3: FLOW DỮ LIỆU
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

ax.text(5, 11.5, 'FLOW DỮ LIỆU', ha='center', fontsize=14, weight='bold')

# Input
input_box = FancyBboxPatch((2, 10.5), 6, 0.8, boxstyle="round,pad=0.1", 
                            edgecolor='blue', facecolor='lightblue', linewidth=2)
ax.add_patch(input_box)
ax.text(5, 10.9, 'DỮ LIỆU THỰC (2015-2024)\n5 mã cổ phiếu, 13,520 bản ghi', 
        ha='center', va='center', fontsize=9, weight='bold')

# Arrow
arrow = FancyArrowPatch((5, 10.5), (5, 9.7), arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
ax.add_patch(arrow)

# Processing
proc_box = FancyBboxPatch((1.5, 8.5), 7, 1, boxstyle="round,pad=0.1", 
                           edgecolor='green', facecolor='lightgreen', linewidth=2)
ax.add_patch(proc_box)
ax.text(5, 9.2, 'PROCESSING LAYER', ha='center', va='center', fontsize=10, weight='bold')
ax.text(5, 8.8, 'Feature Engineering (20 indicators) → Normalization → Split Data', 
        ha='center', va='center', fontsize=8)

# Arrow
arrow = FancyArrowPatch((5, 8.5), (5, 7.7), arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
ax.add_patch(arrow)

# Three branches
branches = [
    (1.5, 'Classification\nModel\n(Train)', 'orange'),
    (5, 'Regression\nModel\n(Train)', 'orange'),
    (8.5, 'Backtest\nStrategy', 'red'),
]

for x, label, color in branches:
    box = FancyBboxPatch((x-0.8, 6.5), 1.6, 1, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor=color, alpha=0.7, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, 7, label, ha='center', va='center', fontsize=8, weight='bold')
    
    # Arrow down
    arrow = FancyArrowPatch((x, 6.5), (x, 5.7), arrowstyle='->', mutation_scale=15, linewidth=1.5, color='gray')
    ax.add_patch(arrow)

# Outputs
outputs_flow = [
    (1.5, 'model.pkl\nscaler.pkl', 'yellow'),
    (5, 'price_model.pkl\nprice_scaler.pkl', 'yellow'),
    (8.5, 'CSV Results\nMetrics', 'lightyellow'),
]

for x, label, color in outputs_flow:
    box = FancyBboxPatch((x-0.8, 5.2), 1.6, 0.8, boxstyle="round,pad=0.05", 
                          edgecolor='gray', facecolor=color, linewidth=1)
    ax.add_patch(box)
    ax.text(x, 5.6, label, ha='center', va='center', fontsize=7)

# Arrow to final layer
arrow = FancyArrowPatch((5, 5.2), (5, 4.4), arrowstyle='->', mutation_scale=20, linewidth=2, color='black')
ax.add_patch(arrow)

# Final output
final_box = FancyBboxPatch((1, 3.6), 8, 0.6, boxstyle="round,pad=0.1", 
                            edgecolor='purple', facecolor='plum', linewidth=2)
ax.add_patch(final_box)
ax.text(5, 3.9, 'VISUALIZATION LAYER: 50+ Plots, Excel, Web Dashboard', 
        ha='center', va='center', fontsize=9, weight='bold')

# Data stats
stats_y = 2.5
ax.text(1, stats_y+0.5, 'Train Set', ha='center', fontsize=8, weight='bold')
ax.text(1, stats_y, '6,760 rows\n(50%)', ha='center', fontsize=7)

ax.text(3.5, stats_y+0.5, 'Validation Set', ha='center', fontsize=8, weight='bold')
ax.text(3.5, stats_y, '2,710 rows\n(20%)', ha='center', fontsize=7)

ax.text(6, stats_y+0.5, 'Test Set', ha='center', fontsize=8, weight='bold')
ax.text(6, stats_y, '4,050 rows\n(30%)', ha='center', fontsize=7)

ax.text(8.5, stats_y+0.5, 'Total', ha='center', fontsize=8, weight='bold')
ax.text(8.5, stats_y, '13,520 rows\n(100%)', ha='center', fontsize=7, 
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# Models used
ax.text(5, 0.8, 'MODELS: Logistic Regression (39.58%) | Linear Regression (MAPE 0.47%)', 
        ha='center', fontsize=8, weight='bold')

plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / '03_flow_du_lieu.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: 03_flow_du_lieu.png")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SƠ ĐỒ 4: BACKTEST RESULT COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(14, 8))

stocks = ['FPT', 'HPG', 'VCB', 'MWG', 'ACB', 'TRUNG BÌNH']
ml_returns = [36.73, -31.49, 5.74, -0.19, 7.71, 3.70]
bh_returns = [160.04, 51.37, 29.62, 40.40, 61.02, 68.49]

x = np.arange(len(stocks))
width = 0.35

bars1 = ax.bar(x - width/2, ml_returns, width, label='ML Strategy', color='orange', alpha=0.8)
bars2 = ax.bar(x + width/2, bh_returns, width, label='Buy & Hold', color='green', alpha=0.8)

ax.set_ylabel('Return (%)', fontsize=11, weight='bold')
ax.set_title('Backtest Results: ML Strategy vs Buy & Hold (2023-2024)', fontsize=13, weight='bold')
ax.set_xticks(x)
ax.set_xticklabels(stocks, fontsize=10)
ax.legend(fontsize=10)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / '04_backtest_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: 04_backtest_comparison.png")
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SƠ ĐỒ 5: MODEL COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(12, 6))

models = ['Logistic\nRegression\n(CHỌN)', 'XGBoost', 'Random\nForest']
accuracy = [39.58, 35.22, 37.50]
colors_models = ['green', 'orange', 'blue']

bars = ax.bar(models, accuracy, color=colors_models, alpha=0.7, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Accuracy (%)', fontsize=11, weight='bold')
ax.set_title('Classification Models Comparison', fontsize=13, weight='bold')
ax.set_ylim(0, 50)
ax.axhline(y=33.33, color='red', linestyle='--', linewidth=2, label='Random Baseline (33.33%)')
ax.grid(axis='y', alpha=0.3)
ax.legend(fontsize=10)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%', ha='center', va='bottom', fontsize=10, weight='bold')

plt.tight_layout()
plt.savefig(DIAGRAMS_DIR / '05_model_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: 05_model_comparison.png")
plt.close()

print("\n" + "="*60)
print("HOÀN TẤT!")
print("="*60)
print("\nTất cả sơ đồ đã được xuất thành công!")
print(f"Thư mục: {DIAGRAMS_DIR}")
print("\nFile được tạo:")
print("  1. 01_kien_truc_tong_the.png - Kiến trúc hệ thống")
print("  2. 02_pipeline_8_buoc.png - Pipeline 8 bước")
print("  3. 03_flow_du_lieu.png - Flow dữ liệu")
print("  4. 04_backtest_comparison.png - So sánh backtest")
print("  5. 05_model_comparison.png - So sánh các mô hình")
print("\n✓ Sử dụng trong luận văn!")
