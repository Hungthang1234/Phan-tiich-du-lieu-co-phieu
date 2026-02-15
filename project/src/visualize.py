# -*- coding: utf-8 -*-
# visualize.py - Vẽ các biểu đồ phân tích

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

# Fix matplotlib for UTF-8
import matplotlib
matplotlib.use('Agg')
# Use simple fonts that work on Windows without Vietnamese text
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.max_open_warning'] = 0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import xgboost as xgb

from config import (
    PROCESSED_DATA_DIR, PROJECT_ROOT,
    PROB_THRESHOLD_BUY, PROB_THRESHOLD_SELL,
    INITIAL_CAPITAL, TRANSACTION_COST
)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_models_and_data():
    """Load mô hình và dữ liệu"""
    model_dir = PROJECT_ROOT / "models"
    
    with open(model_dir / "model.pkl", 'rb') as f:
        trend_model = pickle.load(f)
    
    with open(model_dir / "scaler.pkl", 'rb') as f:
        scaler = pickle.load(f)
    
    with open(model_dir / "feature_columns.pkl", 'rb') as f:
        features = pickle.load(f)
    
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    return trend_model, scaler, features, test_df


def plot_confusion_matrix(model, scaler, features, test_df):
    """Vẽ Confusion Matrix"""
    print("Vẽ Confusion Matrix...")
    
    X_test = scaler.transform(test_df[features])
    y_test = np.array(test_df['label'].values, dtype=int) + 1  # Convert to (0, 1, 2)
    
    y_pred = model.predict(X_test)
    
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Giảm (-1)', 'Đi ngang (0)', 'Tăng (1)'])
    disp.plot(cmap='Blues', values_format='d')
    plt.title('Confusion Matrix - Dự báo xu hướng')
    plt.tight_layout()
    
    plot_dir = PROJECT_ROOT / "plots" / "model_analysis"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / "confusion_matrix.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / 'confusion_matrix.png'}")
    plt.close()


def plot_feature_importance(model, features):
    """Vẽ Feature Importance"""
    print("Vẽ Feature Importance...")
    
    # Kiểm tra xem model có feature importance không
    if not hasattr(model, 'feature_importances_') and not hasattr(model, 'get_booster'):
        print("Cảnh báo: Mô hình không có feature importance")
        return
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    else:
        # Cho XGBoost
        try:
            importances = model.feature_importances_
        except Exception:
            print("Cảnh báo: Không thể lấy feature importance")
            return
    
    # Sort
    indices = np.argsort(importances)[::-1][:15]  # Top 15
    
    plt.figure(figsize=(12, 6))
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Độ quan trọng')
    plt.title('Top 15 Feature Quan Trọng Nhất')
    plt.tight_layout()
    
    plot_dir = PROJECT_ROOT / "plots" / "model_analysis"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / "feature_importance.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / 'feature_importance.png'}")
    plt.close()


def plot_equity_curve():
    """Vẽ Equity Curve (đường giá trị tài khoản theo thời gian)"""
    print("Vẽ Equity Curve...")
    
    # Load kết quả backtest
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    # Tính equity curve cho từng chiến lược
    symbols = test_df['symbol'].unique()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Equity Curve - So sánh Chiến lược vs Buy & Hold', fontsize=16, fontweight='bold')
    
    for idx, symbol in enumerate(symbols):
        ax = axes[idx // 2, idx % 2]
        
        symbol_df = test_df[test_df['symbol'] == symbol].reset_index(drop=True)
        
        # Tính equity curve cho strategy
        position = 0
        cash = INITIAL_CAPITAL
        portfolio_values_strategy = [INITIAL_CAPITAL]
        
        for i in range(len(symbol_df)):
            row = symbol_df.iloc[i]
            close_price = row['close']
            
            # Giả sử signal từ backtest
            if i == 0:
                position = 0
            
            # Update portfolio value
            if position > 0:
                portfolio_value = position * close_price + cash
            else:
                portfolio_value = cash
            
            portfolio_values_strategy.append(portfolio_value)
        
        # Tính equity curve cho Buy & Hold
        entry_price = symbol_df.iloc[0]['close']
        portfolio_values_buy_hold = []
        
        for i in range(len(symbol_df) + 1):
            if i == 0:
                portfolio_values_buy_hold.append(INITIAL_CAPITAL)
            else:
                close_price = symbol_df.iloc[i-1]['close']
                portfolio_values_buy_hold.append(INITIAL_CAPITAL * (close_price / entry_price))
        
        # Plot
        ax.plot(portfolio_values_strategy, label='Chiến lược', linewidth=2, marker='o', markersize=3)
        ax.plot(portfolio_values_buy_hold, label='Buy & Hold', linewidth=2, marker='s', markersize=3)
        ax.axhline(y=INITIAL_CAPITAL, color='red', linestyle='--', alpha=0.5, label='Initial Capital')
        ax.set_title(f'{symbol}', fontweight='bold')
        ax.set_xlabel('Ngày giao dịch')
        ax.set_ylabel('Giá trị tài khoản (VND)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_dir = PROJECT_ROOT / "plots" / "trading_analysis"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / "equity_curve.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / 'equity_curve.png'}")
    plt.close()


def plot_buy_sell_signals():
    """Vẽ Buy/Sell Signals trên biểu đồ giá"""
    print("Vẽ Buy/Sell Signals...")
    
    model_dir = PROJECT_ROOT / "models"
    
    with open(model_dir / "model.pkl", 'rb') as f:
        model = pickle.load(f)
    
    with open(model_dir / "scaler.pkl", 'rb') as f:
        scaler = pickle.load(f)
    
    with open(model_dir / "feature_columns.pkl", 'rb') as f:
        features = pickle.load(f)
    
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    # Tạo signals
    X_test = scaler.transform(test_df[features])
    proba = model.predict_proba(X_test)
    prob_up = proba[:, 1] if proba.shape[1] > 1 else proba[:, 0]
    
    test_df['prob_up'] = prob_up
    test_df['signal'] = 0
    test_df.loc[prob_up > PROB_THRESHOLD_BUY, 'signal'] = 1    # Buy
    test_df.loc[prob_up < PROB_THRESHOLD_SELL, 'signal'] = -1  # Sell
    
    # Plot từng cổ phiếu
    symbols = test_df['symbol'].unique()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Buy/Sell Signals', fontsize=16, fontweight='bold')
    
    for idx, symbol in enumerate(symbols):
        ax = axes[idx // 2, idx % 2]
        
        symbol_df = test_df[test_df['symbol'] == symbol].reset_index(drop=True)
        
        # Plot giá
        ax.plot(symbol_df.index, symbol_df['close'], label='Giá đóng cửa', linewidth=2, color='black')
        
        # Plot buy signals
        buy_signals = symbol_df[symbol_df['signal'] == 1]
        ax.scatter(buy_signals.index, buy_signals['close'], color='green', marker='^', 
                  s=100, label='BUY Signal', zorder=5)
        
        # Plot sell signals
        sell_signals = symbol_df[symbol_df['signal'] == -1]
        ax.scatter(sell_signals.index, sell_signals['close'], color='red', marker='v', 
                  s=100, label='SELL Signal', zorder=5)
        
        ax.set_title(f'{symbol}', fontweight='bold')
        ax.set_xlabel('Ngày giao dịch')
        ax.set_ylabel('Giá đóng cửa (VND)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_dir = PROJECT_ROOT / "plots" / "trading_analysis"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / "buy_sell_signals.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / 'buy_sell_signals.png'}")
    plt.close()


def plot_model_performance_summary():
    """Vẽ tổng hợp hiệu suất mô hình"""
    print("Vẽ Model Performance Summary...")
    
    results_df = pd.read_csv(PROJECT_ROOT / "results" / "price_predictions.csv")
    
    # Tính MAE, RMSE, MAPE theo từng cổ phiếu
    performance_data = []
    
    for symbol in results_df['Symbol'].unique():
        symbol_data = results_df[results_df['Symbol'] == symbol]
        
        mae = np.mean(np.abs(symbol_data['Error']))
        rmse = np.sqrt(np.mean(symbol_data['Error'] ** 2))
        mape = np.mean(np.abs(symbol_data['Error_Percent']))
        
        performance_data.append({
            'Symbol': symbol,
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        })
    
    perf_df = pd.DataFrame(performance_data)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Model Performance by Stock', fontsize=14, fontweight='bold')
    
    # MAE
    axes[0].bar(perf_df['Symbol'], perf_df['MAE'], color='skyblue')
    axes[0].set_title('MAE (Mean Absolute Error)')
    axes[0].set_ylabel('MAE')
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # RMSE
    axes[1].bar(perf_df['Symbol'], perf_df['RMSE'], color='lightcoral')
    axes[1].set_title('RMSE (Root Mean Square Error)')
    axes[1].set_ylabel('RMSE')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # MAPE
    axes[2].bar(perf_df['Symbol'], perf_df['MAPE'], color='lightgreen')
    axes[2].set_title('MAPE (Mean Absolute Percentage Error)')
    axes[2].set_ylabel('MAPE (%)')
    axes[2].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plot_dir = PROJECT_ROOT / "plots" / "model_analysis"
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / "model_performance_summary.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / 'model_performance_summary.png'}")
    plt.close()


def main():
    """Main pipeline vẽ biểu đồ"""
    print("=== BẮT ĐẦU VẼ BIỂU ĐỒ ===\n")
    
    plot_dir = PROJECT_ROOT / "plots"
    plot_dir.mkdir(exist_ok=True)
    
    # Tạo các subfolder
    (plot_dir / "model_analysis").mkdir(exist_ok=True)
    (plot_dir / "trading_analysis").mkdir(exist_ok=True)
    (plot_dir / "price_predictions").mkdir(exist_ok=True)
    
    # Load models
    trend_model, scaler, features, test_df = load_models_and_data()
    
    # 1. Confusion Matrix
    try:
        plot_confusion_matrix(trend_model, scaler, features, test_df)
    except Exception as e:
        print(f"Lỗi vẽ Confusion Matrix: {e}")
    
    # 2. Feature Importance
    try:
        plot_feature_importance(trend_model, features)
    except Exception as e:
        print(f"Lỗi vẽ Feature Importance: {e}")
    
    # 3. Equity Curve
    try:
        plot_equity_curve()
    except Exception as e:
        print(f"Lỗi vẽ Equity Curve: {e}")
    
    # 4. Buy/Sell Signals
    try:
        plot_buy_sell_signals()
    except Exception as e:
        print(f"Lỗi vẽ Buy/Sell Signals: {e}")
    
    # 5. Model Performance Summary
    try:
        plot_model_performance_summary()
    except Exception as e:
        print(f"Lỗi vẽ Model Performance Summary: {e}")
    
    print("\n=== HOÀN TẤT ===")
    print(f"Tất cả biểu đồ đã lưu trong: {plot_dir}")


if __name__ == '__main__':
    main()
