"""
Türkiye Ev Fiyat Tahmini API Test Scripti
API'nin çalışıp çalışmadığını test eder ve örnek kullanımları gösterir.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_health():
    """API sağlık kontrolü"""
    print("🔍 API Sağlık Kontrolü...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ API çalışıyor")
            print(f"   📊 Yanıt: {response.json()}")
        else:
            print(f"   ❌ API hatası: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ API'ye bağlanılamıyor. API'nin çalıştığından emin olun.")
        return False
    return True

def test_model_info():
    """Model bilgilerini test et"""
    print("\n📊 Model Bilgileri...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Model bilgileri alındı")
            print(f"   🤖 Model Tipi: {data['algoritma_tipi']}")
            print(f"   📈 Özellik Sayısı: {data['ozellik_sayisi']}")
            print(f"   🏙️ Desteklenen Şehirler: {', '.join(data['desteklenen_sehirler'][:5])}...")
            print(f"   🏠 Desteklenen Ev Tipleri: {', '.join(data['desteklenen_ev_tipleri'])}")
        else:
            print(f"   ❌ Hata: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_kategorik_degerler():
    """Kategorik değerleri test et"""
    print("\n📋 Kategorik Değerler...")
    try:
        response = requests.get(f"{BASE_URL}/kategorik-degerler")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Kategorik değerler alındı")
            for key, values in data.items():
                print(f"   📝 {key}: {len(values)} farklı değer")
        else:
            print(f"   ❌ Hata: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_ornek_veri():
    """Örnek veri endpoint'ini test et"""
    print("\n📄 Örnek Veri...")
    try:
        response = requests.get(f"{BASE_URL}/ornek-veri")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Örnek veriler alındı")
            for key, ev in data.items():
                print(f"   🏠 {key}: {ev['sehir']}, {ev['ev_tipi']}, {ev['oda_sayisi']}")
        else:
            print(f"   ❌ Hata: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_tekil_tahmin():
    """Tekil ev fiyat tahmini test et"""
    print("\n🔮 Tekil Ev Fiyat Tahmini...")
    
    # Örnek ev verisi
    ev_bilgileri = {
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
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tahmin",
            json=ev_bilgileri,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Tahmin başarılı")
            print(f"   🏠 Ev: {ev_bilgileri['sehir']}, {ev_bilgileri['ev_tipi']}, {ev_bilgileri['net_metrekare']}m²")
            print(f"   💰 Tahmini Fiyat: {data['tahmin_fiyat_formatted']}")
            print(f"   📊 Model: {data['tahmin_bilgileri']['algoritma_tipi']}")
        else:
            print(f"   ❌ Hata: {response.status_code}")
            print(f"   📄 Detay: {response.text}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_toplu_tahmin():
    """Toplu ev fiyat tahmini test et"""
    print("\n🔮 Toplu Ev Fiyat Tahmini...")
    
    # Birden fazla ev verisi
    ev_listesi = [
        {
            "sehir": "İstanbul",
            "semt": "Beşiktaş",
            "ev_tipi": "Daire",
            "oda_sayisi": "2+1",
            "net_metrekare": 90.0,
            "brut_metrekare": 110.0,
            "bina_yasi": "0-5",
            "bulundugu_kat": "3",
            "kat_sayisi": 6,
            "banyo_sayisi": 1,
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
            "brut_metrekare": 250.0,
            "bina_yasi": "0-5",
            "bulundugu_kat": "Bahçe Katı",
            "kat_sayisi": 3,
            "banyo_sayisi": 3,
            "balkon": "Var",
            "isitma_tipi": "Merkezi",
            "otopark": "Var",
            "site_ici": "Evet",
            "esyali_durum": "Eşyasız"
        }
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/toplu-tahmin",
            json=ev_listesi,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Toplu tahmin başarılı")
            print(f"   📊 Toplam Ev: {data['toplam_ev']}")
            print(f"   ✅ Başarılı: {data['basarili_tahmin']}")
            print(f"   ❌ Hatalı: {data['hatali_tahmin']}")
            
            for sonuc in data['sonuclar']:
                if 'tahmin' in sonuc:
                    ev = sonuc['ev_bilgileri']
                    tahmin = sonuc['tahmin']
                    print(f"   🏠 {ev['sehir']}, {ev['ev_tipi']}: {tahmin['tahmin_fiyat_formatted']}")
                else:
                    print(f"   ❌ Hata: {sonuc['hata']}")
        else:
            print(f"   ❌ Hata: {response.status_code}")
            print(f"   📄 Detay: {response.text}")
    except Exception as e:
        print(f"   ❌ Hata: {e}")

def test_hata_durumu():
    """Hata durumlarını test et"""
    print("\n⚠️ Hata Durumu Testi...")
    
    # Geçersiz veri ile test
    gecersiz_ev = {
        "sehir": "GeçersizŞehir",
        "semt": "GeçersizSemt",
        "ev_tipi": "Daire",
        "oda_sayisi": "3+1",
        "net_metrekare": 120.0,
        "bulundugu_kat": "5",
        "bina_yasi": "5-10 Yıl",
        "balkon": "Var",
        "isitma_tipi": "Kombi",
        "otopark": "Var",
        "site_ici": "Evet",
        "esyali_durum": "Boş"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tahmin",
            json=gecersiz_ev,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            print("   ✅ Hata durumu doğru şekilde yakalandı")
            print(f"   📄 Hata mesajı: {response.json()['detail']}")
        else:
            print(f"   ⚠️ Beklenmeyen yanıt: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Test hatası: {e}")

def main():
    """Ana test fonksiyonu"""
    print("🧪 Türkiye Ev Fiyat Tahmini API Test Scripti")
    print("=" * 50)
    
    # API'nin çalışıp çalışmadığını kontrol et
    if not test_api_health():
        print("\n❌ API çalışmıyor. Önce API'yi başlatın:")
        print("   python api.py")
        return
    
    # Diğer testleri çalıştır
    test_model_info()
    test_kategorik_degerler()
    test_ornek_veri()
    test_tekil_tahmin()
    test_toplu_tahmin()
    test_hata_durumu()
    
    print(f"\n🎉 Tüm testler tamamlandı!")
    print(f"📖 API Dokümantasyonu: {BASE_URL}/docs")
    print(f"🔄 API Durumu: {BASE_URL}/health")

if __name__ == "__main__":
    main() 