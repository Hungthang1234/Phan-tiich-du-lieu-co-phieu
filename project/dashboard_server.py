# -*- coding: utf-8 -*-
# dashboard_server.py - Web server để phục vụ dashboard

import sys
import os
import io
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Đường dẫn dự án
PROJECT_ROOT = Path(__file__).parent
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"
PLOTS_DIR = PROJECT_ROOT / "plots"

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    """Lấy danh sách mã cổ phiếu"""
    try:
        strategy_df = pd.read_csv(RESULTS_DIR / "strategy_results.csv")
        symbols = strategy_df['symbol'].tolist()
        return jsonify({'symbols': symbols})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/<symbol>', methods=['GET'])
def get_symbol_data(symbol):
    """Lấy dữ liệu cho một mã cổ phiếu"""
    try:
        strategy_df = pd.read_csv(RESULTS_DIR / "strategy_results.csv")
        buyhold_df = pd.read_csv(RESULTS_DIR / "buy_hold_results.csv")
        comparison_df = pd.read_csv(RESULTS_DIR / "comparison.csv")
        
        strategy = strategy_df[strategy_df['symbol'] == symbol].iloc[0].to_dict()
        buyhold = buyhold_df[buyhold_df['symbol'] == symbol].iloc[0].to_dict()
        comparison = comparison_df[comparison_df['Symbol'] == symbol].iloc[0].to_dict()
        
        return jsonify({
            'strategy': strategy,
            'buyhold': buyhold,
            'comparison': comparison
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/all-results', methods=['GET'])
def get_all_results():
    """Lấy toàn bộ kết quả"""
    try:
        strategy_df = pd.read_csv(RESULTS_DIR / "strategy_results.csv")
        buyhold_df = pd.read_csv(RESULTS_DIR / "buy_hold_results.csv")
        comparison_df = pd.read_csv(RESULTS_DIR / "comparison.csv")
        
        return jsonify({
            'strategy': strategy_df.to_dict('records'),
            'buyhold': buyhold_df.to_dict('records'),
            'comparison': comparison_df.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plots/<symbol>', methods=['GET'])
def get_symbol_plots(symbol):
    """Lấy đường dẫn biểu đồ cho một mã"""
    try:
        plots_dir = PLOTS_DIR / "by_stock" / symbol
        if not plots_dir.exists():
            return jsonify({'error': 'Không tìm thấy biểu đồ'}), 404
        
        # Giải thích cho mỗi loại plot
        plot_descriptions = {
            'price': 'Giá thực tế vs giá dự đoán - so sánh độ chính xác của mô hình',
            'error_vnd': 'Lỗi dự đoán tính bằng VND - sai số tuyệt đối',
            '03': 'Lỗi dự đoán tính bằng % - sai số tương đối trên tổng giá',
            'signals': 'Tín hiệu mua/bán từ chiến lược ML - điểm vào/ra giao dịch',
            '05': 'Xác suất tăng giá từ mô hình - độ tin cậy của tín hiệu (0-1)',
            'equity': 'Đường lợi nhuận tích lũy - hiệu suất chiến lược theo thời gian'
        }
        
        plots = []
        for plot_file in sorted(plots_dir.glob('*.png')):
            name = plot_file.stem
            # Tìm description dựa trên tên file - kiểm tra từ khóa chính
            description = 'Biểu đồ chi tiết'
            for key, desc in plot_descriptions.items():
                if key in name.lower() or name.startswith(key):
                    description = desc
                    break
            
            plots.append({
                'name': name,
                'path': f'/plots/by_stock/{symbol}/{plot_file.name}',
                'description': description
            })
        
        return jsonify({'plots': plots})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/plots/<path:filepath>', methods=['GET'])
def serve_plot(filepath):
    """Phục vụ file biểu đồ"""
    try:
        file_path = PLOTS_DIR / filepath
        if file_path.exists():
            return send_file(file_path, mimetype='image/png')
        return jsonify({'error': 'File không tồn tại'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard.html', methods=['GET'])
def serve_dashboard():
    """Phục vụ dashboard HTML"""
    try:
        dashboard_path = PROJECT_ROOT / "dashboard.html"
        if dashboard_path.exists():
            return send_file(dashboard_path, mimetype='text/html')
        return jsonify({'error': 'Dashboard không tồn tại'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Trang chủ - redirect đến dashboard"""
    return '''
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Dashboard</title>
            <script>
                window.location.href = '/dashboard.html';
            </script>
        </head>
        <body>
            <p>Redirecting to dashboard...</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    print("\n" + "="*80)
    print("DASHBOARD SERVER")
    print("="*80)
    print("\nMở trình duyệt và vào: http://localhost:5000")
    print("Nhấn Ctrl+C để dừng server\n")
    
    app.run(debug=False, port=5000, host='127.0.0.1')
