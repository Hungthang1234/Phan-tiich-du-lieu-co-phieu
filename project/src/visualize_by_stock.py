# -*- coding: utf-8 -*-
# visualize_by_stock.py - Vẽ biểu đồ riêng cho từng mã cổ phiếu

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

from config import (
    PROCESSED_DATA_DIR, PROJECT_ROOT,
    PROB_THRESHOLD_BUY, PROB_THRESHOLD_SELL,
    INITIAL_CAPITAL
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
    
    with open(model_dir / "price_model.pkl", 'rb') as f:
        price_model = pickle.load(f)
    
    with open(model_dir / "price_scaler.pkl", 'rb') as f:
        price_scaler = pickle.load(f)
    
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    price_predictions = pd.read_csv(PROJECT_ROOT / "results" / "price_predictions.csv")
    
    return trend_model, scaler, features, price_model, price_scaler, test_df, price_predictions


def plot_stock_comprehensive(symbol, trend_model, scaler, features, price_model, 
                            price_scaler, test_df, price_predictions):
    """Vẽ biểu đồ toàn diện cho 1 mã cổ phiếu - tách riêng từng biểu đồ"""
    
    print(f"Vẽ biểu đồ cho {symbol}...")
    
    # Filter dữ liệu cho symbol
    symbol_test_df = test_df[test_df['symbol'] == symbol].reset_index(drop=True)
    symbol_price_pred = price_predictions[price_predictions['Symbol'] == symbol]
    
    plot_dir = PROJECT_ROOT / "plots" / "by_stock" / symbol
    plot_dir.mkdir(parents=True, exist_ok=True)
    
    # ===== Plot 1: Giá thực tế vs dự đoán =====
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(symbol_test_df.index, symbol_test_df['close'], label='Giá thực tế', 
            linewidth=2.5, marker='o', markersize=4, color='blue')
    
    y_pred_values = symbol_price_pred.sort_values('Date')['Predicted_Close'].values
    if len(y_pred_values) == len(symbol_test_df):
        ax.plot(symbol_test_df.index, y_pred_values, label='Giá dự đoán', 
               linewidth=2.5, marker='s', markersize=4, color='red', linestyle='--', alpha=0.8)
    
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Giá (VND)', fontsize=11)
    ax.set_title(f'{symbol} - Giá Thực tế vs Dự đoán', fontweight='bold', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_dir / f"01_{symbol}_price_actual_vs_predicted.png", dpi=300, bbox_inches='tight')
    print(f"  Lưu: {plot_dir / f'01_{symbol}_price_actual_vs_predicted.png'}")
    plt.close()
    
    # ===== Plot 2: Sai số dự đoán (VND) =====
    fig, ax = plt.subplots(figsize=(14, 6))
    errors = symbol_price_pred.sort_values('Date')['Error'].values
    colors = ['red' if e < 0 else 'green' for e in errors]
    ax.bar(range(len(errors)), errors, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Sai số (VND)', fontsize=11)
    ax.set_title(f'{symbol} - Sai số Dự đoán (VND)', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(plot_dir / f"02_{symbol}_prediction_error_vnd.png", dpi=300, bbox_inches='tight')
    print(f"  Lưu: {plot_dir / f'02_{symbol}_prediction_error_vnd.png'}")
    plt.close()
    
    # ===== Plot 3: Sai số dự đoán (%) =====
    fig, ax = plt.subplots(figsize=(14, 6))
    error_pct = symbol_price_pred.sort_values('Date')['Error_Percent'].values
    colors = ['red' if e < 0 else 'green' for e in error_pct]
    ax.bar(range(len(error_pct)), error_pct, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Sai số (%)', fontsize=11)
    ax.set_title(f'{symbol} - Sai số Dự đoán (%)', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(plot_dir / f"03_{symbol}_prediction_error_percent.png", dpi=300, bbox_inches='tight')
    print(f"  Lưu: {plot_dir / f'03_{symbol}_prediction_error_percent.png'}")
    plt.close()
    
    # ===== Plot 4: Buy/Sell Signals + Giá =====
    fig, ax = plt.subplots(figsize=(14, 6))
    X_test = scaler.transform(symbol_test_df[features])
    proba = trend_model.predict_proba(X_test)
    prob_up = proba[:, 1] if proba.shape[1] > 1 else proba[:, 0]
    
    symbol_test_df['prob_up'] = prob_up
    symbol_test_df['signal'] = 0
    symbol_test_df.loc[prob_up > PROB_THRESHOLD_BUY, 'signal'] = 1
    symbol_test_df.loc[prob_up < PROB_THRESHOLD_SELL, 'signal'] = -1
    
    ax.plot(symbol_test_df.index, symbol_test_df['close'], label='Giá đóng cửa', 
            linewidth=2.5, color='black', marker='o', markersize=3)
    
    buy_signals = symbol_test_df[symbol_test_df['signal'] == 1]
    ax.scatter(buy_signals.index, buy_signals['close'], color='green', marker='^', 
               s=200, label='BUY Signal', zorder=5, edgecolors='darkgreen', linewidth=2)
    
    sell_signals = symbol_test_df[symbol_test_df['signal'] == -1]
    ax.scatter(sell_signals.index, sell_signals['close'], color='red', marker='v', 
               s=200, label='SELL Signal', zorder=5, edgecolors='darkred', linewidth=2)
    
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Giá (VND)', fontsize=11)
    ax.set_title(f'{symbol} - Buy/Sell Signals', fontweight='bold', fontsize=12)
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_dir / f"04_{symbol}_buy_sell_signals.png", dpi=300, bbox_inches='tight')
    print(f"  Lưu: {plot_dir / f'04_{symbol}_buy_sell_signals.png'}")
    plt.close()
    
    # ===== Plot 5: Probability của mô hình =====
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(symbol_test_df.index, prob_up, label='Xác suất tăng', linewidth=2.5, 
           color='purple', marker='o', markersize=3)
    ax.axhline(y=PROB_THRESHOLD_BUY, color='green', linestyle='--', linewidth=2,
              label=f'Buy threshold ({PROB_THRESHOLD_BUY})')
    ax.axhline(y=PROB_THRESHOLD_SELL, color='red', linestyle='--', linewidth=2,
              label=f'Sell threshold ({PROB_THRESHOLD_SELL})')
    ax.fill_between(range(len(prob_up)), PROB_THRESHOLD_BUY, 1, alpha=0.15, color='green', label='BUY zone')
    ax.fill_between(range(len(prob_up)), 0, PROB_THRESHOLD_SELL, alpha=0.15, color='red', label='SELL zone')
    
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Xác suất', fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_title(f'{symbol} - Xác suất Dự báo Xu hướng', fontweight='bold', fontsize=12)
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_dir / f"05_{symbol}_probability.png", dpi=300, bbox_inches='tight')
    print(f"  Lưu: {plot_dir / f'05_{symbol}_probability.png'}")
    plt.close()


def plot_stock_equity_curve(symbol, test_df):
    """Vẽ Equity Curve cho từng mã cổ phiếu"""
    
    symbol_df = test_df[test_df['symbol'] == symbol].reset_index(drop=True)
    
    # Tính equity curve cho Buy & Hold
    entry_price = symbol_df.iloc[0]['close']
    portfolio_values = []
    
    for i in range(len(symbol_df)):
        close_price = symbol_df.iloc[i]['close']
        portfolio_value = INITIAL_CAPITAL * (close_price / entry_price)
        portfolio_values.append(portfolio_value)
    
    # Vẽ
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(range(len(portfolio_values)), portfolio_values, linewidth=2.5, 
           marker='o', markersize=4, color='blue', label='Buy & Hold')
    ax.axhline(y=INITIAL_CAPITAL, color='red', linestyle='--', linewidth=1.5, 
              label='Initial Capital')
    ax.fill_between(range(len(portfolio_values)), INITIAL_CAPITAL, portfolio_values, 
                   alpha=0.2, color='blue')
    
    ax.set_xlabel('Ngày giao dịch', fontsize=11)
    ax.set_ylabel('Giá trị tài khoản (VND)', fontsize=11)
    ax.set_title(f'{symbol} - Equity Curve (Buy & Hold)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Tính chỉ số
    final_value = portfolio_values[-1]
    total_return = (final_value - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100
    max_drawdown = min([(v - max(portfolio_values[:i+1])) / max(portfolio_values[:i+1]) * 100 
                       for i, v in enumerate(portfolio_values)])
    
    stats_text = f'Final Value: {final_value:,.0f} VND\nReturn: {total_return:.2f}%\nMax DD: {max_drawdown:.2f}%'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    plot_dir = PROJECT_ROOT / "plots" / "by_stock" / symbol
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / f"{symbol}_equity_curve.png", dpi=300, bbox_inches='tight')
    print(f"Lưu: {plot_dir / f'{symbol}_equity_curve.png'}")
    plt.close()


def main():
    """Main pipeline"""
    print("=== VẼ BIỂU ĐỒ RIÊNG CHO TỪNG MÃ CỔ PHIẾU ===\n")
    
    # Load data
    trend_model, scaler, features, price_model, price_scaler, test_df, price_predictions = load_models_and_data()
    
    symbols = test_df['symbol'].unique()
    
    for symbol in symbols:
        print(f"\nXử lý {symbol}...")
        
        try:
            plot_stock_comprehensive(symbol, trend_model, scaler, features, price_model, 
                                   price_scaler, test_df, price_predictions)
        except Exception as e:
            print(f"Lỗi vẽ comprehensive plots cho {symbol}: {e}")
        
        try:
            plot_stock_equity_curve(symbol, test_df)
        except Exception as e:
            print(f"Lỗi vẽ equity curve cho {symbol}: {e}")
    
    print("\n=== HOÀN TẤT ===")
    print(f"Tất cả biểu đồ riêng đã lưu trong: {PROJECT_ROOT / 'plots' / 'by_stock'}")


if __name__ == '__main__':
    main()
