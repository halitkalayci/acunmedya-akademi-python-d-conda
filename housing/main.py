# Indexing

# Context => Prompt içerisinde bağlamı daraltmak için kullanılır.

# `` => Back Tick

# Türkiye Ev Fiyat Tahmini Projesi
# Bu proje, Türkiye'deki ev fiyatlarını tahmin etmek için makine öğrenmesi modelleri geliştirir.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = ['DejaVu Sans']

def load_and_explore_data():
    """Veri setini yükle ve keşifsel analiz yap"""
    print("🏠 Türkiye Ev Fiyat Tahmini Projesi")
    print("=" * 50)
    
    # Veri setini yükle
    df = pd.read_csv('turkiye_ev_fiyatlari.csv')
    
    print(f"📊 Veri Seti Bilgileri:")
    print(f"   • Satır sayısı: {len(df):,}")
    print(f"   • Sütun sayısı: {len(df.columns)}")
    print(f"   • Eksik değer: {df.isnull().sum().sum()}")
    
    print(f"\n💰 Fiyat İstatistikleri:")
    print(f"   • Minimum: {df['fiyat_tl'].min():,} TL")
    print(f"   • Maksimum: {df['fiyat_tl'].max():,} TL")
    print(f"   • Ortalama: {df['fiyat_tl'].mean():,.0f} TL")
    print(f"   • Medyan: {df['fiyat_tl'].median():,.0f} TL")
    
    return df

def preprocess_data(df):
    """Veri ön işleme"""
    print("\n🔧 Veri Ön İşleme...")
    
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
    
    print("   ✅ Kategorik değişkenler encode edildi")
    
    return df_processed, label_encoders

def train_models(X_train, X_test, y_train, y_test):
    """Modelleri eğit ve değerlendir"""
    print("\n🤖 Model Eğitimi...")
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n   📈 {name} eğitiliyor...")
        
        # Modeli eğit
        model.fit(X_train, y_train)
        
        # Tahmin yap
        y_pred = model.predict(X_test)
        
        # Metrikleri hesapla
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'predictions': y_pred
        }
        
        print(f"      • MAE: {mae:,.0f} TL")
        print(f"      • RMSE: {rmse:,.0f} TL")
        print(f"      • R² Score: {r2:.4f}")
    
    return results

def visualize_results(results, y_test):
    """Sonuçları görselleştir"""
    print("\n📊 Sonuçlar görselleştiriliyor...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Türkiye Ev Fiyat Tahmini - Model Sonuçları', fontsize=16, fontweight='bold')
    
    # Model karşılaştırması
    model_names = list(results.keys())
    mae_scores = [results[name]['mae'] for name in model_names]
    r2_scores = [results[name]['r2'] for name in model_names]
    
    # MAE karşılaştırması
    axes[0, 0].bar(model_names, mae_scores, color=['skyblue', 'lightcoral'])
    axes[0, 0].set_title('Mean Absolute Error (MAE)')
    axes[0, 0].set_ylabel('MAE (TL)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # R² karşılaştırması
    axes[0, 1].bar(model_names, r2_scores, color=['lightgreen', 'orange'])
    axes[0, 1].set_title('R² Score')
    axes[0, 1].set_ylabel('R² Score')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Gerçek vs Tahmin (Random Forest)
    rf_pred = results['Random Forest']['predictions']
    axes[1, 0].scatter(y_test, rf_pred, alpha=0.6, color='purple')
    axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[1, 0].set_xlabel('Gerçek Fiyat (TL)')
    axes[1, 0].set_ylabel('Tahmin Edilen Fiyat (TL)')
    axes[1, 0].set_title('Random Forest: Gerçek vs Tahmin')
    
    # Hata dağılımı
    rf_errors = y_test - rf_pred
    axes[1, 1].hist(rf_errors, bins=50, alpha=0.7, color='gold')
    axes[1, 1].set_xlabel('Hata (TL)')
    axes[1, 1].set_ylabel('Frekans')
    axes[1, 1].set_title('Random Forest: Hata Dağılımı')
    
    plt.tight_layout()
    plt.savefig('model_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("   ✅ Grafikler 'model_results.png' dosyasına kaydedildi")

def main():
    """Ana fonksiyon"""
    try:
        # Veri yükleme ve keşif
        df = load_and_explore_data()
        
        # Veri ön işleme
        df_processed, label_encoders = preprocess_data(df)
        
        # Özellikler ve hedef değişken
        X = df_processed.drop('fiyat_tl', axis=1)
        y = df_processed['fiyat_tl']
        
        # Eğitim-test ayrımı
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"\n📚 Eğitim-Test Ayrımı:")
        print(f"   • Eğitim seti: {len(X_train):,} örnek")
        print(f"   • Test seti: {len(X_test):,} örnek")
        
        # Model eğitimi
        results = train_models(X_train, X_test, y_train, y_test)
        
        # Sonuçları görselleştir
        visualize_results(results, y_test)
        
        # En iyi modeli belirle
        best_model_name = max(results.keys(), key=lambda x: results[x]['r2'])
        best_model = results[best_model_name]
        
        print(f"\n🏆 En İyi Model: {best_model_name}")
        print(f"   • R² Score: {best_model['r2']:.4f}")
        print(f"   • RMSE: {best_model['rmse']:,.0f} TL")
        
        print(f"\n✅ Proje başarıyla tamamlandı!")
        print(f"   📁 Veri seti: turkiye_ev_fiyatlari.csv")
        print(f"   📊 Sonuçlar: model_results.png")
        
    except FileNotFoundError:
        print("❌ Hata: 'turkiye_ev_fiyatlari.csv' dosyası bulunamadı!")
        print("   Önce 'python generate_data.py' komutunu çalıştırın.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()