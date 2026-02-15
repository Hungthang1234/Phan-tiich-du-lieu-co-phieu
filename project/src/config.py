# -*- coding: utf-8 -*-
# config.py - Cấu hình chung cho dự án

import os
from pathlib import Path

# Đường dẫn
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Danh sách mã cổ phiếu
VN30_STOCKS = ['FPT', 'HPG', 'VCB', 'MWG', 'ACB']
MARKET_INDICES = ['VNINDEX', 'VN30']

# Chia giai đoạn dữ liệu
TRAIN_START = '2015-01-01'
TRAIN_END = '2020-12-31'
VAL_START = '2021-01-01'
VAL_END = '2022-12-31'
TEST_START = '2023-01-01'
TEST_END = '2024-12-31'

# Chỉ báo kỹ thuật
SMA_PERIODS = [5, 10, 20]
EMA_PERIODS = [12, 26]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2
ATR_PERIOD = 14
VOLUME_MA_PERIOD = 20

# Nhãn (label) xu hướng
THRESHOLD_UP = 0.005      # 0.5% - MUA
THRESHOLD_DOWN = -0.005   # -0.5% - BÁN
# Label: 1 (tăng), 0 (đi ngang), -1 (giảm)

# Backtest
TRANSACTION_COST = 0.003  # 0.3% per round-trip
INITIAL_CAPITAL = 100  # 100 đơn vị (%)
PROB_THRESHOLD_BUY = 0.6   # Xác suất mua
PROB_THRESHOLD_SELL = 0.4  # Xác suất bán

# Model
TEST_SIZE = 0.2
RANDOM_STATE = 42
VERBOSE = True
