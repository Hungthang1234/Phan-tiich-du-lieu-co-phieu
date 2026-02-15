# -*- coding: utf-8 -*-
# prepare_data.py - Chuẩn hóa dữ liệu và tạo feature

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
import warnings
warnings.filterwarnings('ignore')

from config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, 
    VN30_STOCKS, MARKET_INDICES,
    SMA_PERIODS, EMA_PERIODS, RSI_PERIOD,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BB_PERIOD, BB_STD, ATR_PERIOD, VOLUME_MA_PERIOD,
    THRESHOLD_UP, THRESHOLD_DOWN,
    TRAIN_START, TRAIN_END, VAL_START, VAL_END, TEST_START, TEST_END
)


def load_raw_data(symbol):
    """Load raw CSV data cho 1 mã"""
    file_path = RAW_DATA_DIR / f"{symbol}.csv"
    if not file_path.exists():
        print(f"Cảnh báo: Không tìm thấy file {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    return df


def add_technical_indicators(df):
    """Thêm chỉ báo kỹ thuật vào dataframe"""
    
    # SMA
    for period in SMA_PERIODS:
        df[f'SMA_{period}'] = df['close'].rolling(window=period).mean()
    
    # EMA
    for period in EMA_PERIODS:
        df[f'EMA_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema_fast = df['close'].ewm(span=MACD_FAST, adjust=False).mean()
    ema_slow = df['close'].ewm(span=MACD_SLOW, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_SIGNAL'] = df['MACD'].ewm(span=MACD_SIGNAL, adjust=False).mean()
    df['MACD_HIST'] = df['MACD'] - df['MACD_SIGNAL']
    
    # Bollinger Bands
    df['BB_MA'] = df['close'].rolling(window=BB_PERIOD).mean()
    df['BB_STD'] = df['close'].rolling(window=BB_PERIOD).std()
    df['BB_UPPER'] = df['BB_MA'] + (df['BB_STD'] * BB_STD)
    df['BB_LOWER'] = df['BB_MA'] - (df['BB_STD'] * BB_STD)
    
    # ATR
    df['TR'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift()),
            abs(df['low'] - df['close'].shift())
        )
    )
    df['ATR_14'] = df['TR'].rolling(window=ATR_PERIOD).mean()
    
    # Volume ratio
    df['VOLUME_MA'] = df['volume'].rolling(window=VOLUME_MA_PERIOD).mean()
    df['VOLUME_RATIO'] = df['volume'] / df['VOLUME_MA']
    
    return df


def add_market_features(df, market_df, market_name):
    """Thêm feature từ chỉ số thị trường"""
    market_df_copy = market_df[['date', 'close']].copy()
    market_df_copy.rename(columns={'close': f'{market_name}_close'}, inplace=True)
    
    # Return ngày
    market_df_copy[f'{market_name}_return'] = market_df_copy[f'{market_name}_close'].pct_change()
    
    # Volatility (std của return 20 phiên)
    market_df_copy[f'{market_name}_volatility'] = \
        market_df_copy[f'{market_name}_return'].rolling(window=20).std()
    
    # Merge vào df
    df = df.merge(market_df_copy, on='date', how='left')
    return df


def add_labels(df):
    """Thêm nhãn xu hướng (label)"""
    df['future_return'] = df['close'].shift(-1) / df['close'] - 1
    
    df['label'] = 0  # Đi ngang
    df.loc[df['future_return'] > THRESHOLD_UP, 'label'] = 1    # Tăng
    df.loc[df['future_return'] < THRESHOLD_DOWN, 'label'] = -1  # Giảm
    
    return df


def add_time_period(df):
    """Thêm cột chỉ ra train/val/test period"""
    df['period'] = 'unknown'
    
    train_mask = (df['date'] >= TRAIN_START) & (df['date'] <= TRAIN_END)
    val_mask = (df['date'] >= VAL_START) & (df['date'] <= VAL_END)
    test_mask = (df['date'] >= TEST_START) & (df['date'] <= TEST_END)
    
    df.loc[train_mask, 'period'] = 'train'
    df.loc[val_mask, 'period'] = 'val'
    df.loc[test_mask, 'period'] = 'test'
    
    return df


def prepare_stock_data(symbol):
    """Xử lý đầy đủ dữ liệu 1 mã cổ phiếu"""
    print(f"Đang xử lý {symbol}...")
    
    # Load dữ liệu thô
    df = load_raw_data(symbol)
    if df is None:
        return None
    
    # Thêm chỉ báo kỹ thuật
    df = add_technical_indicators(df)
    
    # Load và thêm feature thị trường
    vnindex_df = load_raw_data('VNINDEX')
    vn30_df = load_raw_data('VN30')
    
    if vnindex_df is not None:
        df = add_market_features(df, vnindex_df, 'VNINDEX')
    
    if vn30_df is not None:
        df = add_market_features(df, vn30_df, 'VN30')
    
    # Thêm nhãn
    df = add_labels(df)
    
    # Thêm period
    df = add_time_period(df)
    
    # Thêm cột symbol
    df['symbol'] = symbol
    
    # Loại bỏ dòng có NaN ở feature quan trọng
    df = df.dropna(subset=['label', 'close'])
    
    # Điền giá trị NaN cho feature bằng forward fill rồi backward fill
    feature_cols = [col for col in df.columns if col not in ['date', 'symbol', 'period', 'label', 'future_return', 
                                                               'open', 'high', 'low', 'close', 'volume', 'TR', 'BB_MA', 'BB_STD']]
    df[feature_cols] = df[feature_cols].ffill().bfill()
    
    # Loại bỏ dòng còn lại có NaN
    df = df.dropna()
    
    return df


def main():
    """Main pipeline chuẩn hóa dữ liệu"""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    all_dfs = []
    
    # Xử lý từng mã cổ phiếu
    for symbol in VN30_STOCKS:
        df = prepare_stock_data(symbol)
        if df is not None:
            all_dfs.append(df)
    
    if all_dfs:
        # Gộp tất cả dữ liệu
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_df = combined_df.sort_values(['symbol', 'date']).reset_index(drop=True)
        
        # Lưu file đầy đủ
        combined_df.to_csv(PROCESSED_DATA_DIR / "all_stocks_prepared.csv", index=False)
        print(f"Lưu: {PROCESSED_DATA_DIR / 'all_stocks_prepared.csv'}")
        
        # Thống kê chi tiết
        print("\n" + "="*80)
        print("THỐNG KÊ CHI TIẾT DỮ LIỆU")
        print("="*80)
        print(f"Tổng dòng dữ liệu: {len(combined_df)}")
        print(f"Các mã cổ phiếu: {sorted(combined_df['symbol'].unique().tolist())}")
        print(f"Khoảng thời gian: {combined_df['date'].min()} đến {combined_df['date'].max()}")
        print(f"\nSố cột (features): {len(combined_df.columns)}")
        print(f"Tên các cột: {list(combined_df.columns)}")
        
        print(f"\n--- PHÂN BỐ LABEL ---")
        label_dist = combined_df['label'].value_counts().sort_index()
        label_names = {-1: 'Giảm', 0: 'Đi ngang', 1: 'Tăng'}
        for label, count in label_dist.items():
            pct = (count / len(combined_df)) * 100
            print(f"  {label_names.get(label, 'Unknown')} ({label}): {count} ({pct:.2f}%)")
        
        print(f"\n--- PHÂN BỐ PERIOD ---")
        period_dist = combined_df['period'].value_counts()
        for period, count in period_dist.items():
            pct = (count / len(combined_df)) * 100
            print(f"  {period}: {count} ({pct:.2f}%)")
        
        print(f"\n--- PHÂN BỐ THEO MÃ CỔ PHIẾU ---")
        symbol_dist = combined_df['symbol'].value_counts().sort_values(ascending=False)
        for symbol, count in symbol_dist.items():
            pct = (count / len(combined_df)) * 100
            print(f"  {symbol}: {count} ({pct:.2f}%)")
        
        print(f"\n--- PHÂN BỐ THEO CẬP NHẬT ---")
        for period in ['train', 'val', 'test']:
            period_df = combined_df[combined_df['period'] == period]
            print(f"  {period.upper()}:")
            print(f"    Tổng: {len(period_df)}")
            print(f"    Thời gian: {period_df['date'].min()} đến {period_df['date'].max()}")
            print(f"    Label: {period_df['label'].value_counts().to_dict()}")
        
        # Lưu riêng từng giai đoạn
        for period in ['train', 'val', 'test']:
            period_df = combined_df[combined_df['period'] == period]
            period_df.to_csv(PROCESSED_DATA_DIR / f"{period}_data.csv", index=False)
            print(f"\nLưu: {PROCESSED_DATA_DIR / f'{period}_data.csv'} ({len(period_df)} dòng)")
    else:
        print("Không có dữ liệu để xử lý!")


if __name__ == '__main__':
    main()
