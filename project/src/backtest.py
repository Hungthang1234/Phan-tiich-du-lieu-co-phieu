# -*- coding: utf-8 -*-
# backtest.py - Backtesting chiến lược giao dịch

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
import numpy as np
from pathlib import Path
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler

from config import (
    PROCESSED_DATA_DIR, PROJECT_ROOT,
    TRANSACTION_COST, INITIAL_CAPITAL,
    PROB_THRESHOLD_BUY, PROB_THRESHOLD_SELL
)


def load_model_and_data():
    """Load model, scaler, và dữ liệu test"""
    model_dir = PROJECT_ROOT / "models"
    
    with open(model_dir / "model.pkl", 'rb') as f:
        model = pickle.load(f)
    
    with open(model_dir / "scaler.pkl", 'rb') as f:
        scaler = pickle.load(f)
    
    with open(model_dir / "feature_columns.pkl", 'rb') as f:
        features = pickle.load(f)
    
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    return model, scaler, features, test_df


def generate_trading_signals(model, scaler, features, test_df):
    """Tạo tín hiệu giao dịch từ mô hình"""
    X_test = scaler.transform(test_df[features])
    
    # Lấy xác suất dự báo
    proba = model.predict_proba(X_test)
    
    # Mô hình có 3 class: 0 (giảm), 1 (tăng), 2 (đi ngang)
    # Lấy xác suất của class 1 (tăng)
    prob_up = proba[:, 1]
    
    # Sử dụng phân vị để tạo signal linh hoạt
    # Thay vì fixed thresholds, dùng percentile
    threshold_buy = np.percentile(prob_up, 66)    # Top 33% = BUY
    threshold_sell = np.percentile(prob_up, 33)   # Bottom 33% = SELL
    
    signals = np.zeros(len(test_df))
    signals[prob_up > threshold_buy] = 1    # Mua/Giữ
    signals[prob_up < threshold_sell] = -1  # Bán/Không giữ
    
    test_df['prob_up'] = prob_up
    test_df['signal'] = signals
    
    # Debug: In số lượng signal
    buy_count = np.sum(signals > 0)
    sell_count = np.sum(signals < 0)
    hold_count = np.sum(signals == 0)
    print(f"Signal - Mua: {buy_count}, Bán: {sell_count}, Chờ: {hold_count} (thresholds: {threshold_sell:.4f} / {threshold_buy:.4f})")
    
    return test_df


def backtest_strategy(df):
    """Chạy backtest chiến lược"""
    print("\n=== BACKTEST CHIẾN LỰC GIAO DỊCH ===\n")
    
    results = []
    
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].reset_index(drop=True)
        
        # Khởi tạo biến
        position = 0  # 0 = không nắm giữ, 1 = nắm giữ
        cash = INITIAL_CAPITAL
        portfolio_value = INITIAL_CAPITAL
        entry_price = None
        
        daily_values = [INITIAL_CAPITAL]
        daily_returns = [0]
        trades = []  # Lưu thông tin giao dịch
        
        for i in range(len(symbol_df)):
            row = symbol_df.iloc[i]
            close_price = row['close']
            signal = row['signal']
            
            # Vào lệnh mua
            if signal == 1 and position == 0:
                entry_price = close_price
                cash_used = cash / (1 + TRANSACTION_COST)
                position = cash_used / entry_price
                cash = 0
                trades.append({'date': row['date'], 'action': 'BUY', 'price': entry_price})
                
            # Vào lệnh bán
            elif signal == -1 and position > 0:
                revenue = position * close_price * (1 - TRANSACTION_COST)
                exit_price = close_price
                cash = revenue
                position = 0
                trades.append({'date': row['date'], 'action': 'SELL', 'price': exit_price})
            
            # Cập nhật giá trị portfolio
            if position > 0:
                portfolio_value = position * close_price + cash
            else:
                portfolio_value = cash
            
            daily_values.append(portfolio_value)
            daily_returns.append((portfolio_value - daily_values[-2]) / daily_values[-2])
        
        # Nếu cuối kỳ vẫn nắm giữ, tự động bán
        if position > 0:
            last_price = symbol_df.iloc[-1]['close']
            revenue = position * last_price * (1 - TRANSACTION_COST)
            cash = revenue
            position = 0
            portfolio_value = cash
            trades.append({'date': symbol_df.iloc[-1]['date'], 'action': 'SELL', 'price': last_price})
        
        # Tính toán chỉ số
        total_return = (daily_values[-1] - INITIAL_CAPITAL) / INITIAL_CAPITAL
        
        # Max drawdown
        cum_returns = np.cumprod([1 + r for r in daily_returns])
        running_max = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        # Sharpe ratio (giả sử risk-free rate = 0)
        daily_returns_arr = np.array(daily_returns[1:])
        sharpe = np.mean(daily_returns_arr) / (np.std(daily_returns_arr) + 1e-6) * np.sqrt(252)
        
        # Win rate
        winning_trades = sum(1 for t in trades if t['action'] == 'SELL' and t.get('profit', 0) > 0)
        total_trades = len([t for t in trades if t['action'] == 'SELL'])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        results.append({
            'symbol': symbol,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'final_value': daily_values[-1],
            'num_trades': len(trades) // 2,  # Số cặp buy-sell
            'win_rate': win_rate
        })
        
        print(f"{symbol}:")
        print(f"  Tổng lợi nhuận: {total_return*100:.2f}%")
        print(f"  Max Drawdown: {max_drawdown*100:.2f}%")
        print(f"  Sharpe Ratio: {sharpe:.4f}")
        print(f"  Giá trị cuối: {daily_values[-1]:.2f}")
        print(f"  Số lần giao dịch: {len(trades)}")
        print()
    
    results_df = pd.DataFrame(results)
    return results_df


def backtest_buy_hold(df):
    """Backtest chiến lược Buy & Hold"""
    print("\n" + "="*80)
    print("BACKTEST BUY & HOLD")
    print("="*80 + "\n")
    
    results = []
    
    for symbol in df['symbol'].unique():
        symbol_df = df[df['symbol'] == symbol].reset_index(drop=True)
        
        entry_price = symbol_df.iloc[0]['close']
        exit_price = symbol_df.iloc[-1]['close']
        
        # Tính lợi nhuận (sau phí giao dịch)
        entry_cost = INITIAL_CAPITAL / (1 + TRANSACTION_COST)
        exit_revenue = (entry_cost / entry_price) * exit_price * (1 - TRANSACTION_COST)
        total_return = (exit_revenue - INITIAL_CAPITAL) / INITIAL_CAPITAL
        
        # Tính Max Drawdown
        prices = symbol_df['close'].values
        cum_returns = prices / prices[0]
        running_max = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        # Sharpe Ratio
        daily_returns = np.diff(prices) / prices[:-1]
        sharpe = np.mean(daily_returns) / (np.std(daily_returns) + 1e-6) * np.sqrt(252)
        
        results.append({
            'symbol': symbol,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'final_value': exit_revenue,
            'entry_price': entry_price,
            'exit_price': exit_price
        })
        
        print(f"{symbol}:")
        print(f"  Giá mua (Entry):  {entry_price:.2f}")
        print(f"  Giá bán (Exit):   {exit_price:.2f}")
        print(f"  Tổng lợi nhuận:   {total_return*100:.2f}%")
        print(f"  Max Drawdown:     {max_drawdown*100:.2f}%")
        print(f"  Sharpe Ratio:     {sharpe:.4f}")
        print(f"  Giá trị cuối:     {exit_revenue:.2f}")
        print()
    
    results_df = pd.DataFrame(results)
    return results_df


def main():
    """Main pipeline backtest"""
    print("\n" + "="*80)
    print("BACKTEST CHIẾN LỰC GIAO DỊCH")
    print("="*80)
    print("Đang tải model và dữ liệu...")
    
    model, scaler, features, test_df = load_model_and_data()
    
    print(f"Tổng data point test: {len(test_df)}")
    print(f"Cổ phiếu: {test_df['symbol'].unique().tolist()}")
    
    # Tạo tín hiệu
    print("\nTạo tín hiệu giao dịch...")
    test_df = generate_trading_signals(model, scaler, features, test_df)
    
    # Backtest chiến lược
    print("\n" + "="*80)
    print("BACKTEST CHIẾN LỰC ML (DYNAMIC SIGNALS)")
    print("="*80 + "\n")
    strategy_results = backtest_strategy(test_df)
    
    # Backtest Buy & Hold
    buy_hold_results = backtest_buy_hold(test_df)
    
    # So sánh chi tiết
    print("\n" + "="*80)
    print("SO SÁNH CHI TIẾT")
    print("="*80)
    comparison = pd.DataFrame({
        'Symbol': strategy_results['symbol'],
        'Strategy Return (%)': strategy_results['total_return'] * 100,
        'Buy & Hold Return (%)': buy_hold_results['total_return'] * 100,
        'Outperformance (%)': (strategy_results['total_return'] - buy_hold_results['total_return']) * 100,
        'Strategy Sharpe': strategy_results['sharpe_ratio'],
        'Buy & Hold Sharpe': buy_hold_results['sharpe_ratio']
    })
    
    print(comparison.to_string(index=False))
    
    # Tổng kết
    print("\n" + "="*80)
    print("TỔNG KẾT")
    print("="*80)
    total_strategy_return = (strategy_results['total_return'].sum() / len(strategy_results)) * 100
    total_bh_return = (buy_hold_results['total_return'].sum() / len(buy_hold_results)) * 100
    
    print(f"Trung bình lợi nhuận chiến lược ML: {total_strategy_return:.2f}%")
    print(f"Trung bình lợi nhuận Buy & Hold:    {total_bh_return:.2f}%")
    print(f"Chênh lệch trung bình:              {(total_strategy_return - total_bh_return):.2f}%")
    
    wins = sum(strategy_results['total_return'] > buy_hold_results['total_return'])
    print(f"Số mã thắng chiến lược ML: {wins}/{len(strategy_results)}")
    
    # Lưu kết quả
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    
    strategy_results.to_csv(results_dir / "strategy_results.csv", index=False)
    buy_hold_results.to_csv(results_dir / "buy_hold_results.csv", index=False)
    comparison.to_csv(results_dir / "comparison.csv", index=False)
    
    print(f"\nLưu kết quả vào: {results_dir}")


if __name__ == '__main__':
    main()
