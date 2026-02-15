import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set Vietnamese font
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Create figure
fig, ax = plt.subplots(figsize=(14, 18), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 24)
ax.axis('off')

# Title
ax.text(5, 23.5, 'SƠ ĐỒ QUY TRÌNH - TỪNG BƯỚC', 
        ha='center', va='top', fontsize=18, fontweight='bold')
ax.text(5, 22.8, 'Dự báo xu hướng và giá cổ phiếu bằng Machine Learning',
        ha='center', va='top', fontsize=11, style='italic')

# Input
input_box = FancyBboxPatch((2, 21.5), 6, 0.8, boxstyle="round,pad=0.1", 
                           edgecolor='darkblue', facecolor='lightblue', linewidth=2)
ax.add_patch(input_box)
ax.text(5, 21.9, '📥 DỮ LIỆU ĐẦU VÀO (5 file CSV cổ phiếu 2015-2024)',
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow down
arrow = FancyArrowPatch((5, 21.5), (5, 20.8), arrowstyle='->', 
                        mutation_scale=25, linewidth=2.5, color='black')
ax.add_patch(arrow)

# Step 1
step1_box = FancyBboxPatch((1.5, 19.5), 7, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='orange', facecolor='lightyellow', linewidth=2)
ax.add_patch(step1_box)
ax.text(5, 20.4, 'BƯỚC 1: CHUẨN BỊ DỮ LIỆU', ha='center', va='center', 
        fontsize=11, fontweight='bold')
ax.text(5, 19.9, '• Tính chỉ báo kỹ thuật  • Tạo nhãn phân loại  • Chia train/val/test',
        ha='center', va='center', fontsize=9)

# Arrow down
arrow = FancyArrowPatch((5, 19.5), (5, 18.8), arrowstyle='->', 
                        mutation_scale=25, linewidth=2.5, color='black')
ax.add_patch(arrow)

# Step 2 & 3 (parallel)
# Step 2
step2_box = FancyBboxPatch((0.5, 17.5), 4, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='green', facecolor='lightgreen', linewidth=2)
ax.add_patch(step2_box)
ax.text(2.5, 18.4, 'BƯỚC 2: PHÂN LOẠI', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(2.5, 17.9, 'Logistic Regression\n(Tăng/Giảm)',
        ha='center', va='center', fontsize=8)

# Arrow from 1 to 2
arrow = FancyArrowPatch((3.5, 19.5), (2.5, 18.7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='green')
ax.add_patch(arrow)

# Step 3
step3_box = FancyBboxPatch((5.5, 17.5), 4, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='blue', facecolor='lightcyan', linewidth=2)
ax.add_patch(step3_box)
ax.text(7.5, 18.4, 'BƯỚC 3: DỰ BÁO GIÁ', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(7.5, 17.9, 'Linear Regression\n(Giá tương lai)',
        ha='center', va='center', fontsize=8)

# Arrow from 1 to 3
arrow = FancyArrowPatch((6.5, 19.5), (7.5, 18.7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='blue')
ax.add_patch(arrow)

# Arrow down from 2 to 4
arrow = FancyArrowPatch((2.5, 17.5), (3.5, 16.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='green')
ax.add_patch(arrow)

# Arrow down from 3 to 4
arrow = FancyArrowPatch((7.5, 17.5), (6.5, 16.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='blue')
ax.add_patch(arrow)

# Step 4
step4_box = FancyBboxPatch((1.5, 15.5), 7, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='red', facecolor='lightcoral', linewidth=2)
ax.add_patch(step4_box)
ax.text(5, 16.4, 'BƯỚC 4: BACKTEST CHIẾN LƯỢC', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(5, 15.9, '• Kết hợp 2 mô hình  • Tạo tín hiệu mua/bán  • Tính lợi nhuận',
        ha='center', va='center', fontsize=9)

# Arrow down
arrow = FancyArrowPatch((5, 15.5), (5, 14.8), arrowstyle='->', 
                        mutation_scale=25, linewidth=2.5, color='black')
ax.add_patch(arrow)

# Step 5 & 6 (parallel)
# Step 5
step5_box = FancyBboxPatch((0.5, 13.5), 4, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='purple', facecolor='plum', linewidth=2)
ax.add_patch(step5_box)
ax.text(2.5, 14.4, 'BƯỚC 5: VẼ BIỂU ĐỒ', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(2.5, 13.9, 'Giá dự đoán, Lỗi,\nXác suất',
        ha='center', va='center', fontsize=8)

# Arrow from 4 to 5
arrow = FancyArrowPatch((3.5, 15.5), (2.5, 14.7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='purple')
ax.add_patch(arrow)

# Step 6
step6_box = FancyBboxPatch((5.5, 13.5), 4, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='brown', facecolor='wheat', linewidth=2)
ax.add_patch(step6_box)
ax.text(7.5, 14.4, 'BƯỚC 6: VẼ BACKTEST', ha='center', va='center',
        fontsize=10, fontweight='bold')
ax.text(7.5, 13.9, 'Tín hiệu mua/bán,\nĐường lợi nhuận',
        ha='center', va='center', fontsize=8)

# Arrow from 4 to 6
arrow = FancyArrowPatch((6.5, 15.5), (7.5, 14.7), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='brown')
ax.add_patch(arrow)

# Arrow down from 5 to 7
arrow = FancyArrowPatch((2.5, 13.5), (3.5, 12.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='purple')
ax.add_patch(arrow)

# Arrow down from 6 to 7
arrow = FancyArrowPatch((7.5, 13.5), (6.5, 12.8), arrowstyle='->', 
                        mutation_scale=20, linewidth=2, color='brown')
ax.add_patch(arrow)

# Step 7
step7_box = FancyBboxPatch((1.5, 11.5), 7, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='darkgreen', facecolor='lightgreen', linewidth=2)
ax.add_patch(step7_box)
ax.text(5, 12.4, 'BƯỚC 7: XUẤT KẾT QUẢ', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(5, 11.9, '• Excel thông số mô hình  • Excel backtest  • CSV dự đoán',
        ha='center', va='center', fontsize=9)

# Arrow down
arrow = FancyArrowPatch((5, 11.5), (5, 10.8), arrowstyle='->', 
                        mutation_scale=25, linewidth=2.5, color='black')
ax.add_patch(arrow)

# Step 8
step8_box = FancyBboxPatch((1.5, 9.5), 7, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='darkred', facecolor='salmon', linewidth=2)
ax.add_patch(step8_box)
ax.text(5, 10.4, 'BƯỚC 8: XUẤT SƠ ĐỒ KIẾN TRÚC', ha='center', va='center',
        fontsize=11, fontweight='bold')
ax.text(5, 9.9, '• Sơ đồ hệ thống  • Pipeline  • Flow dữ liệu  • So sánh',
        ha='center', va='center', fontsize=9)

# Arrow down
arrow = FancyArrowPatch((5, 9.5), (5, 8.8), arrowstyle='->', 
                        mutation_scale=25, linewidth=2.5, color='black')
ax.add_patch(arrow)

# Output
output_box = FancyBboxPatch((1.5, 7.5), 7, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='darkblue', facecolor='lightblue', linewidth=2)
ax.add_patch(output_box)
ax.text(5, 8.4, '📊 KẾT QUẢ ĐẦU RA',
        ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(5, 7.9, 'Biểu đồ • Excel • Sơ đồ PNG • CSV • Web Dashboard',
        ha='center', va='center', fontsize=9)

# Summary section
summary_y = 6.5
ax.text(5, summary_y, 'TÓMLƯỢC KẾT QUẢ', ha='center', va='top', 
        fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

summary_text = [
    '📊 Dữ liệu: 5 cổ phiếu VN30 (2015-2024, 13,520 records)',
    '🤖 Mô hình: Logistic (39.58%) + Linear Regression (0.47% MAPE)',
    '📈 Backtest: +3.70% (so với B&H +68.49%, thị trường bull)',
    '📁 Output: 30 biểu đồ + 3 Excel + 5 PNG sơ đồ + Web Dashboard',
]

for i, text in enumerate(summary_text):
    ax.text(0.5, summary_y - 0.4 - i*0.35, text, fontsize=9, va='top')

plt.tight_layout()
plt.savefig(r'c:\Users\ASUS\Desktop\KLTN\diagrams\06_so_do_quy_trinh.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print('✓ Saved: 06_so_do_quy_trinh.png')
plt.close()

# Create a simpler diagram - just flow without details
fig, ax = plt.subplots(figsize=(12, 16), dpi=150)
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# Title
ax.text(5, 19.5, 'QUY TRÌNH 8 BƯỚC',
        ha='center', va='top', fontsize=16, fontweight='bold')

# Simple boxes for each step
steps = [
    (18.5, 'BƯỚC 1\nCHUẨN BỊ DỮ LIỆU', 'lightblue'),
    (17.0, 'BƯỚC 2\nPHÂN LOẠI', 'lightgreen'),
    (15.5, 'BƯỚC 3\nDỰ BÁO GIÁ', 'lightcyan'),
    (14.0, 'BƯỚC 4\nBACKTEST', 'lightcoral'),
    (12.5, 'BƯỚC 5\nVẼ BIỂU ĐỒ 1', 'plum'),
    (11.0, 'BƯỚC 6\nVẼ BIỂU ĐỒ 2', 'wheat'),
    (9.5, 'BƯỚC 7\nXUẤT KẾT QUẢ', 'lightgreen'),
    (8.0, 'BƯỚC 8\nXUẤT SƠ ĐỒ', 'salmon'),
]

for i, (y, label, color) in enumerate(steps):
    box = FancyBboxPatch((2, y-0.35), 6, 0.7, boxstyle="round,pad=0.05",
                         edgecolor='black', facecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(5, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Arrow to next step
    if i < len(steps) - 1:
        arrow = FancyArrowPatch((5, y-0.35), (5, steps[i+1][0]+0.35),
                               arrowstyle='->', mutation_scale=20, linewidth=2)
        ax.add_patch(arrow)

# Output at the bottom
output_y = 6.5
ax.text(5, output_y, '📊 KẾT QUẢ: Biểu đồ + Excel + Sơ đồ PNG + Dashboard',
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', edgecolor='black', linewidth=2))

plt.tight_layout()
plt.savefig(r'c:\Users\ASUS\Desktop\KLTN\diagrams\07_quy_trinh_don_gian.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('✓ Saved: 07_quy_trinh_don_gian.png')
plt.close()

print('\n' + '='*50)
print('HOÀN TẤT!')
print('='*50)
print('Sơ đồ quy trình đã được xuất:')
print('  1. 06_so_do_quy_trinh.png')
print('  2. 07_quy_trinh_don_gian.png')
