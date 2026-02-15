# -*- coding: utf-8 -*-
# predict_price.py - Dự đoán giá cổ phiếu

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
from pathlib import Path
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except:
    XGB_AVAILABLE = False

from config import (
    PROCESSED_DATA_DIR, PROJECT_ROOT,
    RANDOM_STATE, VERBOSE
)


def get_feature_columns(df):
    """Lấy danh sách feature"""
    exclude_cols = ['date', 'symbol', 'period', 'label', 'future_return', 
                    'open', 'high', 'low', 'close', 'volume', 'TR', 'BB_MA', 'BB_STD']
    features = [col for col in df.columns if col not in exclude_cols]
    return features


def mape(y_true, y_pred):
    """Tính MAPE (Mean Absolute Percentage Error)"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def train_price_model():
    """Huấn luyện mô hình dự đoán giá"""
    print("Đang tải dữ liệu...")
    
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train_data.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val_data.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    print(f"Train: {len(train_df)} dòng")
    print(f"Validation: {len(val_df)} dòng")
    print(f"Test: {len(test_df)} dòng")
    
    # Lấy feature columns
    features = get_feature_columns(train_df)
    print(f"\nSố feature: {len(features)}")
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_df[features])
    X_val = scaler.transform(val_df[features])
    X_test = scaler.transform(test_df[features])
    
    # Target: giá close
    y_train = train_df['close'].values
    y_val = val_df['close'].values
    y_test = test_df['close'].values
    
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train mean: {y_train.mean():.2f}, std: {y_train.std():.2f}")
    
    # Huấn luyện các mô hình
    models = {}
    results = {}
    
    # 1. Linear Regression
    print("\n=== LINEAR REGRESSION ===")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_val = lr_model.predict(X_val)
    
    mae_val = mean_absolute_error(y_val, y_pred_val)
    rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
    mape_val = mape(y_val, y_pred_val)
    
    print(f"Validation - MAE: {mae_val:.2f}, RMSE: {rmse_val:.2f}, MAPE: {mape_val:.2f}%")
    
    y_pred_test = lr_model.predict(X_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    mape_test = mape(y_test, y_pred_test)
    
    print(f"Test - MAE: {mae_test:.2f}, RMSE: {rmse_test:.2f}, MAPE: {mape_test:.2f}%")
    
    models['linear_regression'] = lr_model
    results['linear_regression'] = {
        'y_pred': y_pred_test,
        'mae': mae_test,
        'rmse': rmse_test,
        'mape': mape_test
    }
    
    # 2. Random Forest
    print("\n=== RANDOM FOREST ===")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_val = rf_model.predict(X_val)
    
    mae_val = mean_absolute_error(y_val, y_pred_val)
    rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
    mape_val = mape(y_val, y_pred_val)
    
    print(f"Validation - MAE: {mae_val:.2f}, RMSE: {rmse_val:.2f}, MAPE: {mape_val:.2f}%")
    
    y_pred_test = rf_model.predict(X_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    mape_test = mape(y_test, y_pred_test)
    
    print(f"Test - MAE: {mae_test:.2f}, RMSE: {rmse_test:.2f}, MAPE: {mape_test:.2f}%")
    
    models['random_forest'] = rf_model
    results['random_forest'] = {
        'y_pred': y_pred_test,
        'mae': mae_test,
        'rmse': rmse_test,
        'mape': mape_test
    }
    
    # 3. XGBoost
    if XGB_AVAILABLE:
        print("\n=== XGBOOST ===")
        xgb_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbosity=0
        )
        xgb_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        y_pred_val = xgb_model.predict(X_val)
        
        mae_val = mean_absolute_error(y_val, y_pred_val)
        rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
        mape_val = mape(y_val, y_pred_val)
        
        print(f"Validation - MAE: {mae_val:.2f}, RMSE: {rmse_val:.2f}, MAPE: {mape_val:.2f}%")
        
        y_pred_test = xgb_model.predict(X_test)
        mae_test = mean_absolute_error(y_test, y_pred_test)
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mape_test = mape(y_test, y_pred_test)
        
        print(f"Test - MAE: {mae_test:.2f}, RMSE: {rmse_test:.2f}, MAPE: {mape_test:.2f}%")
        
        models['xgboost'] = xgb_model
        results['xgboost'] = {
            'y_pred': y_pred_test,
            'mae': mae_test,
            'rmse': rmse_test,
            'mape': mape_test
        }
    
    # Lưu model tốt nhất
    best_model_name = min(results, key=lambda x: results[x]['mape'])
    best_model = models[best_model_name]
    
    print(f"\n=== MÔ HÌNH TỐT NHẤT ===")
    print(f"Model: {best_model_name}")
    print(f"MAE: {results[best_model_name]['mae']:.2f}")
    print(f"RMSE: {results[best_model_name]['rmse']:.2f}")
    print(f"MAPE: {results[best_model_name]['mape']:.2f}%")
    
    # Lưu model
    model_dir = PROJECT_ROOT / "models"
    model_dir.mkdir(exist_ok=True)
    
    with open(model_dir / "price_model.pkl", 'wb') as f:
        pickle.dump(best_model, f)
    
    with open(model_dir / "price_scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    
    with open(model_dir / "price_features.pkl", 'wb') as f:
        pickle.dump(features, f)
    
    print(f"\nLưu model vào: {model_dir / 'price_model.pkl'}")
    
    # Vẽ biểu đồ
    plot_predictions(test_df, y_test, results[best_model_name]['y_pred'], best_model_name)
    
    # Lưu kết quả
    results_df = pd.DataFrame({
        'Symbol': test_df['symbol'],
        'Date': test_df['date'],
        'Actual_Close': y_test,
        'Predicted_Close': results[best_model_name]['y_pred'],
        'Error': y_test - results[best_model_name]['y_pred'],
        'Error_Percent': ((y_test - results[best_model_name]['y_pred']) / y_test) * 100
    })
    
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    results_df.to_csv(results_dir / "price_predictions.csv", index=False)
    
    print(f"Lưu kết quả dự đoán vào: {results_dir / 'price_predictions.csv'}")


def plot_predictions(test_df, y_actual, y_pred, model_name):
    """Vẽ biểu đồ so sánh giá thực tế vs dự đoán"""
    
    plot_dir = PROJECT_ROOT / "plots" / "price_predictions"
    plot_dir.mkdir(parents=True, exist_ok=True)
    
    # Biểu đồ tổng thể
    plt.figure(figsize=(15, 6))
    plt.plot(range(len(y_actual)), y_actual, label='Giá thực tế', linewidth=2, alpha=0.7)
    plt.plot(range(len(y_pred)), y_pred, label='Giá dự đoán', linewidth=2, alpha=0.7)
    plt.xlabel('Ngày giao dịch')
    plt.ylabel('Giá đóng cửa (VND)')
    plt.title(f'Dự đoán giá - {model_name}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_dir / f"price_prediction_{model_name}.png", dpi=300)
    print(f"Lưu biểu đồ: {plot_dir / f'price_prediction_{model_name}.png'}")
    plt.close()
    
    # Biểu đồ từng cổ phiếu
    for symbol in test_df['symbol'].unique():
        mask = test_df['symbol'] == symbol
        y_actual_symbol = y_actual[mask]
        y_pred_symbol = y_pred[mask]
        
        plt.figure(figsize=(12, 5))
        plt.plot(range(len(y_actual_symbol)), y_actual_symbol, label='Giá thực tế', linewidth=2)
        plt.plot(range(len(y_pred_symbol)), y_pred_symbol, label='Giá dự đoán', linewidth=2, linestyle='--')
        plt.xlabel('Ngày giao dịch')
        plt.ylabel('Giá đóng cửa (VND)')
        plt.title(f'Dự đoán giá {symbol}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(plot_dir / f"price_prediction_{symbol}.png", dpi=300)
        print(f"Lưu biểu đồ: {plot_dir / f'price_prediction_{symbol}.png'}")
        plt.close()


if __name__ == '__main__':
    train_price_model()
