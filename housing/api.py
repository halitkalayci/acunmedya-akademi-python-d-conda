"""
Türkiye Ev Fiyat Tahmini API
FastAPI kullanarak eğitilen Random Forest modelini web üzerinden erişilebilir hale getirir.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import pickle
import numpy as np
import pandas as pd
from typing import List, Optional
import os
import uvicorn

# FastAPI uygulaması oluştur
app = FastAPI(
    title="Türkiye Ev Fiyat Tahmini API",
    description="Random Forest modeli kullanarak Türkiye'deki ev fiyatlarını tahmin eden API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global değişkenler
model = None
label_encoders = None
feature_names = None
categorical_values = None

def load_model_components():
    """Model ve gerekli bileşenleri yükle"""
    global model, label_encoders, feature_names, categorical_values
    
    try:
        # Modeli yükle
        with open('model/random_forest_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Label encoder'ları yükle
        with open('model/label_encoders.pkl', 'rb') as f:
            label_encoders = pickle.load(f)
        
        # Özellik isimlerini yükle
        with open('model/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        # Kategorik değerleri yükle
        with open('model/categorical_values.pkl', 'rb') as f:
            categorical_values = pickle.load(f)
            
        print("✅ Model bileşenleri başarıyla yüklendi")
        
    except FileNotFoundError as e:
        print(f"❌ Model dosyaları bulunamadı: {e}")
        print("   Önce 'python train_and_save_model.py' komutunu çalıştırın.")
        raise
    except Exception as e:
        print(f"❌ Model yükleme hatası: {e}")
        raise

# Pydantic modelleri
class EvBilgileri(BaseModel):
    """Ev bilgileri için veri modeli"""
    sehir: str = Field(..., description="Şehir adı")
    semt: str = Field(..., description="Semt adı")
    ev_tipi: str = Field(..., description="Ev tipi (Daire, Villa, vb.)")
    oda_sayisi: str = Field(..., description="Oda sayısı")
    net_metrekare: float = Field(..., gt=0, description="Net metrekare (m²)")
    brut_metrekare: float = Field(..., gt=0, description="Brüt metrekare (m²)")
    bina_yasi: str = Field(..., description="Bina yaşı")
    bulundugu_kat: str = Field(..., description="Bulunduğu kat")
    kat_sayisi: int = Field(..., gt=0, description="Kat sayısı")
    banyo_sayisi: int = Field(..., gt=0, description="Banyo sayısı")
    balkon: str = Field(..., description="Balkon durumu")
    isitma_tipi: str = Field(..., description="Isıtma tipi")
    otopark: str = Field(..., description="Otopark durumu")
    site_ici: str = Field(..., description="Site içi durumu")
    esyali_durum: str = Field(..., description="Eşyalı durumu")

class TahminSonucu(BaseModel):
    """Tahmin sonucu için veri modeli"""
    tahmin_fiyat: float = Field(..., description="Tahmini fiyat (TL)")
    tahmin_fiyat_formatted: str = Field(..., description="Formatlanmış tahmini fiyat")
    tahmin_bilgileri: dict = Field(..., description="Tahmin hakkında bilgiler")

class ModelBilgileri(BaseModel):
    """Model bilgileri için veri modeli"""
    algoritma_tipi: str
    ozellik_sayisi: int
    desteklenen_sehirler: List[str]
    desteklenen_ev_tipleri: List[str]

# API endpoint'leri
@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında model bileşenlerini yükle"""
    load_model_components()

@app.get("/", summary="Ana Sayfa")
async def ana_sayfa():
    """API ana sayfası"""
    return {
        "mesaj": "Türkiye Ev Fiyat Tahmini API'sine hoş geldiniz!",
        "dokumantasyon": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }

@app.get("/health", summary="Sağlık Kontrolü")
async def saglik_kontrolu():
    """API'nin çalışır durumda olup olmadığını kontrol et"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklenmedi")
    
    return {
        "durum": "sağlıklı",
        "model_yuklendi": model is not None,
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.get("/model-info", response_model=ModelBilgileri, summary="Model Bilgileri")
async def model_bilgileri():
    """Model hakkında bilgi ver"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklenmedi")
    
    return ModelBilgileri(
        algoritma_tipi="Random Forest Regressor",
        ozellik_sayisi=len(feature_names),
        desteklenen_sehirler=categorical_values.get('sehir', [])[:20],  # İlk 20 şehir
        desteklenen_ev_tipleri=categorical_values.get('ev_tipi', [])
    )

@app.get("/kategorik-degerler", summary="Kategorik Değerler")
async def kategorik_degerler():
    """Tüm kategorik alanlar için geçerli değerleri listele"""
    if categorical_values is None:
        raise HTTPException(status_code=503, detail="Kategorik değerler yüklenmedi")
    
    return categorical_values

@app.post("/tahmin", response_model=TahminSonucu, summary="Ev Fiyat Tahmini")
async def ev_fiyat_tahmini(ev_bilgileri: EvBilgileri):
    """Verilen ev bilgilerine göre fiyat tahmini yap"""
    if model is None or label_encoders is None:
        raise HTTPException(status_code=503, detail="Model veya encoder'lar yüklenmedi")
    
    try:
        # Giriş verilerini dict'e çevir
        input_data = ev_bilgileri.dict()
        
        # Kategorik değerleri validate et
        if categorical_values:
            for field_name, value in input_data.items():
                if field_name in categorical_values:
                    if str(value) not in categorical_values[field_name]:
                        valid_values = ", ".join(categorical_values[field_name][:10])
                        if len(categorical_values[field_name]) > 10:
                            valid_values += "..."
                        raise HTTPException(
                            status_code=400,
                            detail=f"{field_name} için geçersiz değer: {value}. Geçerli değerler: {valid_values}"
                        )
        
        # Kategorik değişkenleri encode et
        categorical_columns = ['sehir', 'semt', 'ev_tipi', 'oda_sayisi', 'bina_yasi', 
                              'balkon', 'isitma_tipi', 'otopark', 'site_ici', 'esyali_durum']
        
        for col in categorical_columns:
            if col in input_data:
                try:
                    input_data[col] = label_encoders[col].transform([input_data[col]])[0]
                except ValueError as e:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"{col} için geçersiz değer: {ev_bilgileri.dict()[col]}"
                    )
        
        # Bulunduğu kat özel işlemi
        if input_data['bulundugu_kat'] == 'Bahçe Katı':
            input_data['bulundugu_kat'] = 0
        else:
            try:
                input_data['bulundugu_kat'] = int(input_data['bulundugu_kat'])
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Geçersiz kat değeri: {ev_bilgileri.bulundugu_kat}"
                )
        
        # Özellik sırasını doğru şekilde düzenle
        feature_values = []
        for feature in feature_names:
            if feature in input_data:
                feature_values.append(input_data[feature])
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Eksik özellik: {feature}"
                )
        
        # Tahmin yap
        X_input = np.array(feature_values).reshape(1, -1)
        tahmin = model.predict(X_input)[0]
        
        # Sonucu formatla
        tahmin_formatted = f"{tahmin:,.0f} TL"
        
        return TahminSonucu(
            tahmin_fiyat=float(tahmin),
            tahmin_fiyat_formatted=tahmin_formatted,
            tahmin_bilgileri={
                "algoritma_tipi": "Random Forest",
                "ozellik_sayisi": len(feature_names),
                "tahmin_timestamp": pd.Timestamp.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/toplu-tahmin", summary="Toplu Ev Fiyat Tahmini")
async def toplu_ev_fiyat_tahmini(ev_listesi: List[EvBilgileri]):
    """Birden fazla ev için fiyat tahmini yap"""
    if len(ev_listesi) > 100:
        raise HTTPException(status_code=400, detail="Maksimum 100 ev için tahmin yapılabilir")
    
    sonuclar = []
    for i, ev in enumerate(ev_listesi):
        try:
            sonuc = await ev_fiyat_tahmini(ev)
            sonuclar.append({
                "index": i,
                "ev_bilgileri": ev.dict(),
                "tahmin": sonuc.dict()
            })
        except HTTPException as e:
            sonuclar.append({
                "index": i,
                "ev_bilgileri": ev.dict(),
                "hata": e.detail
            })
    
    return {
        "toplam_ev": len(ev_listesi),
        "basarili_tahmin": len([s for s in sonuclar if "tahmin" in s]),
        "hatali_tahmin": len([s for s in sonuclar if "hata" in s]),
        "sonuclar": sonuclar
    }

@app.get("/ornek-veri", summary="Örnek Veri")
async def ornek_veri():
    """API'yi test etmek için örnek veri döndür"""
    return {
        "ornek_ev_1": {
            "sehir": "İstanbul",
            "semt": "Kadıköy",
            "ev_tipi": "Daire",
            "oda_sayisi": "3+1",
            "net_metrekare": 120.0,
            "brut_metrekare": 140.0,
            "bina_yasi": "6-10",
            "bulundugu_kat": "5",
            "kat_sayisi": 8,
            "banyo_sayisi": 2,
            "balkon": "Var",
            "isitma_tipi": "Kombi",
            "otopark": "Var",
            "site_ici": "Evet",
            "esyali_durum": "Eşyasız"
        },
        "ornek_ev_2": {
            "sehir": "Ankara",
            "semt": "Çankaya",
            "ev_tipi": "Villa",
            "oda_sayisi": "4+1",
            "net_metrekare": 200.0,
            "brut_metrekare": 250.0,
            "bina_yasi": "0-5",
            "bulundugu_kat": "Bahçe Katı",
            "kat_sayisi": 3,
            "banyo_sayisi": 3,
            "balkon": "Var",
            "isitma_tipi": "Merkezi",
            "otopark": "Var",
            "site_ici": "Evet",
            "esyali_durum": "Eşyalı"
        }
    }

if __name__ == "__main__":
    # Model dosyalarının varlığını kontrol et
    if not os.path.exists('model/random_forest_model.pkl'):
        print("❌ Model dosyaları bulunamadı!")
        print("   Önce 'python train_and_save_model.py' komutunu çalıştırın.")
        exit(1)
    
    print("🚀 Türkiye Ev Fiyat Tahmini API başlatılıyor...")
    print("📖 Dokümantasyon: http://localhost:8000/docs")
    print("🔄 API Durumu: http://localhost:8000/health")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 