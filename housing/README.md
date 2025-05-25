# Türkiye Ev Fiyat Tahmini Projesi

Bu proje, Türkiye'deki ev fiyatlarını tahmin etmek için makine öğrenmesi modelleri geliştirmeyi amaçlamaktadır.

## 📊 Veri Seti Özellikleri

- **Toplam Kayıt Sayısı**: 15.000 satır
- **Özellik Sayısı**: 16 sütun
- **Veri Formatı**: CSV
- **Eksik Değer**: Yok

### 🏠 Veri Seti Sütunları

1. **sehir**: Evin bulunduğu şehir (15 farklı şehir)
2. **semt**: Evin bulunduğu semt/ilçe
3. **ev_tipi**: Ev türü (Daire, Villa, Müstakil Ev, Dubleks, Tripleks, Rezidans)
4. **oda_sayisi**: Oda + salon sayısı (1+0, 1+1, 2+1, 3+1, 4+1, 5+1, 4+2, 5+2)
5. **net_metrekare**: Net kullanım alanı (m²)
6. **brut_metrekare**: Brüt alan (m²)
7. **bina_yasi**: Binanın yaşı (0-5, 6-10, 11-15, 16-20, 21-25, 26-30, 30+)
8. **bulundugu_kat**: Evin bulunduğu kat
9. **kat_sayisi**: Binanın toplam kat sayısı
10. **banyo_sayisi**: Banyo sayısı (1-5)
11. **balkon**: Balkon durumu (Var/Yok)
12. **isitma_tipi**: Isıtma sistemi türü
13. **otopark**: Otopark durumu
14. **site_ici**: Site içinde olup olmadığı
15. **esyali_durum**: Eşyalı durumu
16. **fiyat_tl**: Ev fiyatı (Türk Lirası) - **Hedef değişken**

### 🏙️ Şehirler ve Ortalama Fiyatlar

| Şehir | Ortalama Fiyat (TL) |
|-------|-------------------|
| İstanbul | 4.501.122 |
| Antalya | 3.459.156 |
| İzmir | 2.500.000+ |
| Ankara | 2.000.000+ |
| Bursa | 1.800.000+ |

## 🚀 Kurulum

### Gereksinimler

```bash
pip install -r requirements.txt
```

### Veri Setini Oluşturma

```bash
python generate_data.py
```

### Veri Analizi

```bash
python analyze_data.py
```

## 📁 Dosya Yapısı

```
housing/
├── turkiye_ev_fiyatlari.csv    # Ana veri seti
├── generate_data.py            # Veri oluşturma scripti
├── analyze_data.py             # Veri analiz scripti
├── requirements.txt            # Python kütüphaneleri
├── README.md                   # Bu dosya
└── main.py                     # Ana proje dosyası
```

## 🎯 Proje Hedefleri

1. **Veri Ön İşleme**: Kategorik değişkenlerin kodlanması, özellik mühendisliği
2. **Keşifsel Veri Analizi**: Görselleştirmeler ve istatistiksel analizler
3. **Model Geliştirme**: Farklı makine öğrenmesi algoritmalarının denenmesi
4. **Model Değerlendirme**: Performans metrikleri ile model karşılaştırması
5. **Hiperparametre Optimizasyonu**: En iyi model parametrelerinin bulunması

## 🔧 Kullanılacak Algoritmalar

- **Linear Regression**: Temel regresyon modeli
- **Random Forest**: Ensemble öğrenme
- **Gradient Boosting**: XGBoost, LightGBM
- **Support Vector Regression**: SVR
- **Neural Networks**: Derin öğrenme yaklaşımları

## 📈 Değerlendirme Metrikleri

- **MAE (Mean Absolute Error)**: Ortalama mutlak hata
- **MSE (Mean Squared Error)**: Ortalama kare hata
- **RMSE (Root Mean Squared Error)**: Kök ortalama kare hata
- **R² Score**: Belirleme katsayısı
- **MAPE (Mean Absolute Percentage Error)**: Ortalama mutlak yüzde hata

## 🎨 Veri Görselleştirme

- Fiyat dağılımları
- Şehir bazında fiyat karşılaştırmaları
- Ev özelliklerinin fiyata etkisi
- Korelasyon matrisleri
- Feature importance grafikleri

## 📝 Notlar

- Veri seti tamamen sentetik olarak oluşturulmuştur
- Gerçek piyasa verilerine dayalı mantıklı fiyatlandırma kullanılmıştır
- Tüm özellikler ev fiyatını etkileyecek şekilde modellenmiştir
- Veri seti makine öğrenmesi eğitimi için optimize edilmiştir

## 🤝 Katkıda Bulunma

Bu proje eğitim amaçlı geliştirilmiştir. Önerileriniz ve katkılarınız için lütfen iletişime geçin.

## 📄 Lisans

Bu proje eğitim amaçlı olarak geliştirilmiştir ve açık kaynak kodludur. 