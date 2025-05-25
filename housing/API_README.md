# Türkiye Ev Fiyat Tahmini API

Bu API, Random Forest makine öğrenmesi modeli kullanarak Türkiye'deki ev fiyatlarını tahmin eden bir web servisidir.

## 🚀 Kurulum ve Başlatma

### 1. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Modeli Eğitin ve Kaydedin
```bash
python train_and_save_model.py
```

### 3. API'yi Başlatın
```bash
python api.py
```

API varsayılan olarak `http://localhost:8000` adresinde çalışacaktır.

## 📖 API Dokümantasyonu

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Durumu**: http://localhost:8000/health

## 🔗 Endpoint'ler

### 1. Ana Sayfa
```
GET /
```
API hakkında genel bilgi döndürür.

### 2. Sağlık Kontrolü
```
GET /health
```
API'nin çalışır durumda olup olmadığını kontrol eder.

### 3. Model Bilgileri
```
GET /model-info
```
Kullanılan model hakkında bilgi verir.

**Örnek Yanıt:**
```json
{
  "algoritma_tipi": "Random Forest Regressor",
  "ozellik_sayisi": 12,
  "desteklenen_sehirler": ["İstanbul", "Ankara", "İzmir", ...],
  "desteklenen_ev_tipleri": ["Daire", "Villa", "Müstakil Ev", ...]
}
```

### 4. Kategorik Değerler
```
GET /kategorik-degerler
```
Tüm kategorik alanlar için geçerli değerleri listeler.

### 5. Örnek Veri
```
GET /ornek-veri
```
API'yi test etmek için örnek ev verilerini döndürür.

### 6. Ev Fiyat Tahmini
```
POST /tahmin
```
Tek bir ev için fiyat tahmini yapar.

**İstek Gövdesi:**
```json
{
  "sehir": "İstanbul",
  "semt": "Kadıköy",
  "ev_tipi": "Daire",
  "oda_sayisi": "3+1",
  "net_metrekare": 120.0,
  "bulundugu_kat": "5",
  "bina_yasi": "6-10",
  "balkon": "Var",
  "isitma_tipi": "Kombi",
  "otopark": "Var",
  "site_ici": "Evet",
  "esyali_durum": "Boş"
}
```

**Yanıt:**
```json
{
  "tahmin_fiyat": 2500000.0,
  "tahmin_fiyat_formatted": "2,500,000 TL",
  "tahmin_bilgileri": {
    "algoritma_tipi": "Random Forest",
    "ozellik_sayisi": 12,
    "tahmin_timestamp": "2024-01-15T10:30:00"
  }
}
```

### 7. Toplu Ev Fiyat Tahmini
```
POST /toplu-tahmin
```
Birden fazla ev için fiyat tahmini yapar (maksimum 100 ev).

**İstek Gövdesi:**
```json
[
  {
    "sehir": "İstanbul",
    "semt": "Beşiktaş",
    "ev_tipi": "Daire",
    "oda_sayisi": "2+1",
    "net_metrekare": 90.0,
    "bulundugu_kat": "3",
    "bina_yasi": "0-5",
    "balkon": "Var",
    "isitma_tipi": "Merkezi",
    "otopark": "Var",
    "site_ici": "Evet",
    "esyali_durum": "Eşyalı"
  },
  {
    "sehir": "Ankara",
    "semt": "Çankaya",
    "ev_tipi": "Villa",
    "oda_sayisi": "4+1",
    "net_metrekare": 200.0,
    "bulundugu_kat": "Bahçe Katı",
    "bina_yasi": "0-5",
    "balkon": "Var",
    "isitma_tipi": "Merkezi",
    "otopark": "Var",
    "site_ici": "Evet",
    "esyali_durum": "Boş"
  }
]
```

## 📝 Veri Alanları

| Alan | Tip | Açıklama | Örnek Değerler |
|------|-----|----------|----------------|
| `sehir` | string | Şehir adı | "İstanbul", "Ankara", "İzmir" |
| `semt` | string | Semt adı | "Kadıköy", "Çankaya", "Konak" |
| `ev_tipi` | string | Ev tipi | "Daire", "Villa", "Müstakil Ev" |
| `oda_sayisi` | string | Oda sayısı | "1+1", "2+1", "3+1", "4+1", "5+1" |
| `net_metrekare` | float | Net metrekare | 50.0, 120.0, 200.0 |
| `bulundugu_kat` | string | Bulunduğu kat | "1", "5", "10", "Bahçe Katı" |
| `bina_yasi` | string | Bina yaşı | "0-5", "6-10", "11-15" |
| `balkon` | string | Balkon durumu | "Var", "Yok" |
| `isitma_tipi` | string | Isıtma tipi | "Kombi", "Merkezi", "Klima" |
| `otopark` | string | Otopark durumu | "Var", "Yok" |
| `site_ici` | string | Site içi durumu | "Evet", "Hayır" |
| `esyali_durum` | string | Eşyalı durumu | "Eşyalı", "Boş" |

## 🧪 Test Etme

API'yi test etmek için test scriptini çalıştırın:

```bash
python test_api.py
```

Bu script şunları test eder:
- API sağlık kontrolü
- Model bilgileri
- Kategorik değerler
- Tekil tahmin
- Toplu tahmin
- Hata durumları

## 📱 Kullanım Örnekleri

### Python ile Kullanım

```python
import requests

# API base URL
BASE_URL = "http://localhost:8000"

# Ev bilgileri
ev_bilgileri = {
    "sehir": "İstanbul",
    "semt": "Kadıköy",
    "ev_tipi": "Daire",
    "oda_sayisi": "3+1",
    "net_metrekare": 120.0,
    "bulundugu_kat": "5",
    "bina_yasi": "6-10",
    "balkon": "Var",
    "isitma_tipi": "Kombi",
    "otopark": "Var",
    "site_ici": "Evet",
    "esyali_durum": "Boş"
}

# Tahmin isteği gönder
response = requests.post(
    f"{BASE_URL}/tahmin",
    json=ev_bilgileri
)

if response.status_code == 200:
    sonuc = response.json()
    print(f"Tahmini Fiyat: {sonuc['tahmin_fiyat_formatted']}")
else:
    print(f"Hata: {response.status_code}")
```

### cURL ile Kullanım

```bash
curl -X POST "http://localhost:8000/tahmin" \
     -H "Content-Type: application/json" \
     -d '{
       "sehir": "İstanbul",
       "semt": "Kadıköy",
       "ev_tipi": "Daire",
       "oda_sayisi": "3+1",
       "net_metrekare": 120.0,
       "bulundugu_kat": "5",
       "bina_yasi": "6-10",
       "balkon": "Var",
       "isitma_tipi": "Kombi",
       "otopark": "Var",
       "site_ici": "Evet",
       "esyali_durum": "Boş"
     }'
```

### JavaScript ile Kullanım

```javascript
const evBilgileri = {
  sehir: "İstanbul",
  semt: "Kadıköy",
  ev_tipi: "Daire",
  oda_sayisi: "3+1",
  net_metrekare: 120.0,
  bulundugu_kat: "5",
  bina_yasi: "6-10",
  balkon: "Var",
  isitma_tipi: "Kombi",
  otopark: "Var",
  site_ici: "Evet",
  esyali_durum: "Boş"
};

fetch('http://localhost:8000/tahmin', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(evBilgileri)
})
.then(response => response.json())
.then(data => {
  console.log('Tahmini Fiyat:', data.tahmin_fiyat_formatted);
})
.catch(error => {
  console.error('Hata:', error);
});
```

## ⚠️ Hata Kodları

| Kod | Açıklama |
|-----|----------|
| 200 | Başarılı |
| 400 | Geçersiz veri |
| 503 | Model yüklenmedi |
| 500 | Sunucu hatası |

## 🔧 Yapılandırma

API'yi farklı port veya host'ta çalıştırmak için `api.py` dosyasının sonundaki `uvicorn.run()` parametrelerini değiştirin:

```python
uvicorn.run(
    "api:app",
    host="0.0.0.0",  # Tüm IP'lerden erişim için
    port=8080,       # Farklı port için
    reload=True,
    log_level="info"
)
```

## 📊 Model Performansı

Model, Random Forest algoritması kullanılarak eğitilmiştir ve şu performans metriklerine sahiptir:
- **R² Score**: Model doğruluğu
- **MAE (Mean Absolute Error)**: Ortalama mutlak hata
- **RMSE (Root Mean Square Error)**: Kök ortalama kare hatası

Detaylı model performansı için `python train_and_save_model.py` komutunu çalıştırın.

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 