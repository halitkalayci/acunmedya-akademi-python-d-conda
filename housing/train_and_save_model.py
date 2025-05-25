"""
Türkiye Ev Fiyat Tahmini Modeli - Eğitim ve Kaydetme
Bu script modeli eğitir ve API'de kullanmak üzere kaydeder.
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """Veri setini yükle ve ön işleme yap"""
    print("📊 Veri yükleniyor ve işleniyor...")
    
    # Veri setini yükle
    df = pd.read_csv('turkiye_ev_fiyatlari.csv')
    
    # Kategorik değişkenleri encode et
    categorical_columns = ['sehir', 'semt', 'ev_tipi', 'oda_sayisi', 'bina_yasi', 
                          'balkon', 'isitma_tipi', 'otopark', 'site_ici', 'esyali_durum']
    
    df_processed = df.copy()
    label_encoders = {}
    
    for col in categorical_columns:
        le = LabelEncoder()
        df_processed[col] = le.fit_transform(df_processed[col])
        label_encoders[col] = le
    
    # Bulunduğu kat sütununu işle (Bahçe Katı = 0)
    df_processed['bulundugu_kat'] = df_processed['bulundugu_kat'].replace('Bahçe Katı', 0)
    df_processed['bulundugu_kat'] = pd.to_numeric(df_processed['bulundugu_kat'])
    
    print(f"   ✅ {len(df)} satır veri işlendi")
    
    return df_processed, label_encoders, df

def train_model(df_processed):
    """Random Forest modelini eğit"""
    print("🌲 Random Forest modeli eğitiliyor...")
    
    # Özellikler ve hedef değişken
    X = df_processed.drop('fiyat_tl', axis=1)
    y = df_processed['fiyat_tl']
    
    # Eğitim-test ayrımı
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Hiperparametre optimizasyonu
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf_grid = RandomForestRegressor(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(
        rf_grid, param_grid, cv=3, 
        scoring='neg_mean_absolute_error', 
        n_jobs=-1, verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    # En iyi model
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    # Model metrikleri
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"   🏆 Model Performansı:")
    print(f"      • MAE: {mae:,.0f} TL")
    print(f"      • RMSE: {rmse:,.0f} TL")
    print(f"      • R² Score: {r2:.4f}")
    print(f"      • En iyi parametreler: {grid_search.best_params_}")
    
    return best_model, X.columns.tolist()

def save_model_and_encoders(model, label_encoders, feature_names, original_df):
    """Modeli ve encoder'ları kaydet"""
    print("💾 Model ve encoder'lar kaydediliyor...")
    
    # Model klasörü oluştur
    os.makedirs('model', exist_ok=True)
    
    # Modeli kaydet
    with open('model/random_forest_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Label encoder'ları kaydet
    with open('model/label_encoders.pkl', 'wb') as f:
        pickle.dump(label_encoders, f)
    
    # Özellik isimlerini kaydet
    with open('model/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    # Kategorik değişkenlerin benzersiz değerlerini kaydet (API validasyonu için)
    categorical_values = {}
    categorical_columns = ['sehir', 'semt', 'ev_tipi', 'oda_sayisi', 'bina_yasi', 
                          'balkon', 'isitma_tipi', 'otopark', 'site_ici', 'esyali_durum']
    
    for col in categorical_columns:
        categorical_values[col] = sorted(original_df[col].unique().tolist())
    
    # Bulundugu_kat için özel değerler
    kat_values = sorted([str(x) for x in original_df['bulundugu_kat'].unique() if x != 'Bahçe Katı'])
    kat_values.append('Bahçe Katı')
    categorical_values['bulundugu_kat'] = kat_values
    
    with open('model/categorical_values.pkl', 'wb') as f:
        pickle.dump(categorical_values, f)
    
    print(f"   ✅ Model dosyaları 'model/' klasörüne kaydedildi:")
    print(f"      • random_forest_model.pkl")
    print(f"      • label_encoders.pkl")
    print(f"      • feature_names.pkl")
    print(f"      • categorical_values.pkl")

def main():
    """Ana fonksiyon"""
    try:
        # Veri yükleme ve ön işleme
        df_processed, label_encoders, original_df = load_and_preprocess_data()
        
        # Model eğitimi
        model, feature_names = train_model(df_processed)
        
        # Model ve encoder'ları kaydet
        save_model_and_encoders(model, label_encoders, feature_names, original_df)
        
        print(f"\n🎉 Model başarıyla eğitildi ve kaydedildi!")
        print(f"   Artık 'python api.py' komutu ile API'yi başlatabilirsiniz.")
        
    except FileNotFoundError:
        print("❌ Hata: 'turkiye_ev_fiyatlari.csv' dosyası bulunamadı!")
        print("   Önce 'python generate_data.py' komutunu çalıştırın.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main() 