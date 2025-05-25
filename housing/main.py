# Indexing

# Context => Prompt içerisinde bağlamı daraltmak için kullanılır.

# `` => Back Tick

# Türkiye Ev Fiyat Tahmini Projesi - Random Forest Modeli
# Bu proje, Random Forest algoritması kullanarak Türkiye'deki ev fiyatlarını tahmin eder.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = ['DejaVu Sans']

def load_and_explore_data():
    """Veri setini yükle ve keşifsel analiz yap"""
    print("🌲 Random Forest ile Türkiye Ev Fiyat Tahmini")
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

def train_random_forest(X_train, X_test, y_train, y_test):
    """Random Forest modelini eğit ve optimize et"""
    print("\n🌲 Random Forest Model Eğitimi...")
    
    # Temel Random Forest modeli
    print("   📈 Temel Random Forest modeli eğitiliyor...")
    rf_basic = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_basic.fit(X_train, y_train)
    
    # Temel model tahminleri
    y_pred_basic = rf_basic.predict(X_test)
    
    # Temel model metrikleri
    mae_basic = mean_absolute_error(y_test, y_pred_basic)
    rmse_basic = np.sqrt(mean_squared_error(y_test, y_pred_basic))
    r2_basic = r2_score(y_test, y_pred_basic)
    
    print(f"      • MAE: {mae_basic:,.0f} TL")
    print(f"      • RMSE: {rmse_basic:,.0f} TL")
    print(f"      • R² Score: {r2_basic:.4f}")
    
    # Hiperparametre optimizasyonu
    print("\n   🔍 Hiperparametre optimizasyonu yapılıyor...")
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
    rf_best = grid_search.best_estimator_
    y_pred_best = rf_best.predict(X_test)
    
    # En iyi model metrikleri
    mae_best = mean_absolute_error(y_test, y_pred_best)
    rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))
    r2_best = r2_score(y_test, y_pred_best)
    
    print(f"\n   🏆 En İyi Random Forest Modeli:")
    print(f"      • En iyi parametreler: {grid_search.best_params_}")
    print(f"      • MAE: {mae_best:,.0f} TL")
    print(f"      • RMSE: {rmse_best:,.0f} TL")
    print(f"      • R² Score: {r2_best:.4f}")
    
    return {
        'basic_model': rf_basic,
        'best_model': rf_best,
        'basic_predictions': y_pred_basic,
        'best_predictions': y_pred_best,
        'basic_metrics': {'mae': mae_basic, 'rmse': rmse_basic, 'r2': r2_basic},
        'best_metrics': {'mae': mae_best, 'rmse': rmse_best, 'r2': r2_best},
        'best_params': grid_search.best_params_
    }

def analyze_feature_importance(model, feature_names):
    """Özellik önemini analiz et"""
    print("\n📊 Özellik Önem Analizi...")
    
    # Özellik önemlerini al
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print("\n   🔝 En Önemli 10 Özellik:")
    for i, (_, row) in enumerate(feature_importance_df.head(10).iterrows(), 1):
        print(f"      {i:2d}. {row['feature']}: {row['importance']:.4f}")
    
    return feature_importance_df

def visualize_results(results, y_test, feature_importance_df):
    """Sonuçları görselleştir"""
    print("\n📊 Sonuçlar görselleştiriliyor...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Random Forest - Türkiye Ev Fiyat Tahmini Sonuçları', fontsize=16, fontweight='bold')
    
    # Model karşılaştırması (Temel vs Optimize)
    models = ['Temel RF', 'Optimize RF']
    mae_scores = [results['basic_metrics']['mae'], results['best_metrics']['mae']]
    r2_scores = [results['basic_metrics']['r2'], results['best_metrics']['r2']]
    
    # MAE karşılaştırması
    bars1 = axes[0, 0].bar(models, mae_scores, color=['lightblue', 'darkblue'])
    axes[0, 0].set_title('Mean Absolute Error (MAE)')
    axes[0, 0].set_ylabel('MAE (TL)')
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                       f'{mae_scores[i]:,.0f}', ha='center', va='bottom')
    
    # R² karşılaştırması
    bars2 = axes[0, 1].bar(models, r2_scores, color=['lightgreen', 'darkgreen'])
    axes[0, 1].set_title('R² Score')
    axes[0, 1].set_ylabel('R² Score')
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                       f'{r2_scores[i]:.4f}', ha='center', va='bottom')
    
    # Gerçek vs Tahmin (En iyi model)
    best_pred = results['best_predictions']
    axes[1, 0].scatter(y_test, best_pred, alpha=0.6, color='purple')
    axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[1, 0].set_xlabel('Gerçek Fiyat (TL)')
    axes[1, 0].set_ylabel('Tahmin Edilen Fiyat (TL)')
    axes[1, 0].set_title('Optimize RF: Gerçek vs Tahmin')
    
    # Özellik önemleri (Top 10)
    top_features = feature_importance_df.head(10)
    axes[1, 1].barh(range(len(top_features)), top_features['importance'], color='orange')
    axes[1, 1].set_yticks(range(len(top_features)))
    axes[1, 1].set_yticklabels(top_features['feature'])
    axes[1, 1].set_xlabel('Önem Skoru')
    axes[1, 1].set_title('En Önemli 10 Özellik')
    axes[1, 1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('random_forest_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("   ✅ Grafikler 'random_forest_results.png' dosyasına kaydedildi")

def make_sample_predictions(model, label_encoders, df_original):
    """Örnek tahminler yap"""
    print("\n🔮 Örnek Tahminler...")
    
    # Rastgele 5 örnek seç
    sample_indices = np.random.choice(df_original.index, 5, replace=False)
    
    for i, idx in enumerate(sample_indices, 1):
        sample = df_original.loc[idx]
        print(f"\n   🏠 Örnek {i}:")
        print(f"      • Şehir: {sample['sehir']}")
        print(f"      • Ev Tipi: {sample['ev_tipi']}")
        print(f"      • Oda Sayısı: {sample['oda_sayisi']}")
        print(f"      • Net m²: {sample['net_metrekare']}")
        print(f"      • Bina Yaşı: {sample['bina_yasi']}")
        print(f"      • Gerçek Fiyat: {sample['fiyat_tl']:,} TL")
        
        # Tahmin için veriyi hazırla
        sample_encoded = sample.copy()
        categorical_columns = ['sehir', 'semt', 'ev_tipi', 'oda_sayisi', 'bina_yasi', 
                              'balkon', 'isitma_tipi', 'otopark', 'site_ici', 'esyali_durum']
        
        for col in categorical_columns:
            sample_encoded[col] = label_encoders[col].transform([sample[col]])[0]
        
        sample_encoded['bulundugu_kat'] = 0 if sample_encoded['bulundugu_kat'] == 'Bahçe Katı' else int(sample_encoded['bulundugu_kat'])
        
        # Tahmin yap
        X_sample = sample_encoded.drop('fiyat_tl').values.reshape(1, -1)
        predicted_price = model.predict(X_sample)[0]
        
        error = abs(sample['fiyat_tl'] - predicted_price)
        error_percent = (error / sample['fiyat_tl']) * 100
        
        print(f"      • Tahmin Fiyat: {predicted_price:,.0f} TL")
        print(f"      • Hata: {error:,.0f} TL ({error_percent:.1f}%)")

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
        
        # Random Forest model eğitimi
        results = train_random_forest(X_train, X_test, y_train, y_test)
        
        # Özellik önem analizi
        feature_importance_df = analyze_feature_importance(results['best_model'], X.columns)
        
        # Sonuçları görselleştir
        visualize_results(results, y_test, feature_importance_df)
        
        # Örnek tahminler
        make_sample_predictions(results['best_model'], label_encoders, df)
        
        print(f"\n🏆 Final Sonuçlar:")
        print(f"   • En İyi R² Score: {results['best_metrics']['r2']:.4f}")
        print(f"   • En İyi RMSE: {results['best_metrics']['rmse']:,.0f} TL")
        print(f"   • En İyi MAE: {results['best_metrics']['mae']:,.0f} TL")
        print(f"   • En İyi Parametreler: {results['best_params']}")
        
        print(f"\n✅ Random Forest projesi başarıyla tamamlandı!")
        print(f"   📁 Veri seti: turkiye_ev_fiyatlari.csv")
        print(f"   📊 Sonuçlar: random_forest_results.png")
        
    except FileNotFoundError:
        print("❌ Hata: 'turkiye_ev_fiyatlari.csv' dosyası bulunamadı!")
        print("   Önce 'python generate_data.py' komutunu çalıştırın.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()