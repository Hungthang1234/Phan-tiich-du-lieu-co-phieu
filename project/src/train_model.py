# -*- coding: utf-8 -*-
# train_model.py - Huấn luyện mô hình dự báo

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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except:
    XGB_AVAILABLE = False
    print("Cảnh báo: XGBoost chưa được cài đặt")

from config import (
    PROCESSED_DATA_DIR, PROJECT_ROOT,
    RANDOM_STATE, VERBOSE
)


def get_feature_columns(df):
    """Lấy danh sách feature (loại bỏ label, date, symbol, v.v.)"""
    exclude_cols = ['date', 'symbol', 'period', 'label', 'future_return', 
                    'open', 'high', 'low', 'close', 'volume', 'TR', 'BB_MA', 'BB_STD']
    features = [col for col in df.columns if col not in exclude_cols]
    return features


def train_baseline_model(X_train, y_train, X_val, y_val):
    """Huấn luyện Logistic Regression"""
    print("\n=== LOGISTIC REGRESSION (BASELINE) ===")
    
    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Đánh giá
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    
    print(f"Accuracy (Validation): {acc:.4f}")
    print(f"\nClassification Report:\n{classification_report(y_val, y_pred)}")
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_val, y_pred)}")
    
    return model


def train_xgboost_model(X_train, y_train, X_val, y_val):
    """Huấn luyện XGBoost"""
    if not XGB_AVAILABLE:
        print("XGBoost chưa được cài đặt. Bỏ qua.")
        return None
    
    print("\n=== XGBOOST ===")
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbosity=1 if VERBOSE else 0
    )
    
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    
    # Đánh giá
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    
    print(f"Accuracy (Validation): {acc:.4f}")
    print(f"\nClassification Report:\n{classification_report(y_val, y_pred)}")
    print(f"\nConfusion Matrix:\n{confusion_matrix(y_val, y_pred)}")
    
    return model


def main():
    """Main pipeline huấn luyện"""
    print("Đang tải dữ liệu...")
    
    # Load dữ liệu
    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train_data.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val_data.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test_data.csv")
    
    print(f"Train: {len(train_df)} dòng")
    print(f"Validation: {len(val_df)} dòng")
    print(f"Test: {len(test_df)} dòng")
    
    # Lấy feature columns
    features = get_feature_columns(train_df)
    print(f"\nSố feature: {len(features)}")
    print(f"Features: {features[:10]}...")  # In 10 cái đầu
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_df[features])
    X_val = scaler.transform(val_df[features])
    X_test = scaler.transform(test_df[features])
    
    y_train = np.array(train_df['label'].values, dtype=int)
    y_val = np.array(val_df['label'].values, dtype=int)
    y_test = np.array(test_df['label'].values, dtype=int)
    
    # Convert label (-1, 0, 1) → (0, 1, 2) cho XGBoost
    y_train = y_train + 1
    y_val = y_val + 1
    y_test = y_test + 1
    
    print(f"X_train shape: {X_train.shape}")
    unique, counts = np.unique(y_train, return_counts=True)
    print(f"y_train distribution: {dict(zip(unique, counts))}")
    
    # Huấn luyện các mô hình
    models = {}
    
    # 1. Baseline: Logistic Regression
    lr_model = train_baseline_model(X_train, y_train, X_val, y_val)
    models['logistic_regression'] = lr_model
    
    # 2. XGBoost
    xgb_model = train_xgboost_model(X_train, y_train, X_val, y_val)
    if xgb_model:
        models['xgboost'] = xgb_model
    
    # Đánh giá trên test set
    print("\n" + "="*80)
    print("ĐÁNH GIÁ MÔ HÌNH TRÊN TEST SET")
    print("="*80)
    for name, model in models.items():
        print(f"\n{name.upper()}:")
        y_pred = model.predict(X_test)
        
        # Classification metrics
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"  Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"  Confusion Matrix:\n{cm}")
        
        # Per-class performance
        print(f"  Per-class metrics:")
        for i in range(cm.shape[0]):
            if cm[i].sum() > 0:
                class_acc = cm[i, i] / cm[i].sum()
                print(f"    Class {i}: {class_acc:.4f}")
    
    # Lưu model và scaler
    model_dir = PROJECT_ROOT / "models"
    model_dir.mkdir(exist_ok=True)
    
    best_model = models.get('xgboost', models['logistic_regression'])
    
    print(f"\n--- Lưu mô hình ---")
    print(f"Mô hình được chọn: {type(best_model).__name__}")
    
    with open(model_dir / "model.pkl", 'wb') as f:
        pickle.dump(best_model, f)
    
    with open(model_dir / "scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    
    with open(model_dir / "feature_columns.pkl", 'wb') as f:
        pickle.dump(features, f)
    
    print(f"Lưu: {model_dir / 'model.pkl'}")
    print(f"Lưu: {model_dir / 'scaler.pkl'}")
    print(f"Lưu: {model_dir / 'feature_columns.pkl'}")


if __name__ == '__main__':
    main()
