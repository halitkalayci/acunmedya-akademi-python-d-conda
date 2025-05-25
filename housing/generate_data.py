import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Rastgele seed ayarla
np.random.seed(42)
random.seed(42)

# Türkiye şehirleri ve ortalama m2 fiyatları (TL)
cities_prices = {
    'İstanbul': {'min': 8000, 'max': 25000, 'avg': 15000},
    'Ankara': {'min': 4000, 'max': 12000, 'avg': 7000},
    'İzmir': {'min': 5000, 'max': 15000, 'avg': 8500},
    'Antalya': {'min': 6000, 'max': 18000, 'avg': 10000},
    'Bursa': {'min': 3500, 'max': 10000, 'avg': 6000},
    'Adana': {'min': 2500, 'max': 8000, 'avg': 4500},
    'Gaziantep': {'min': 2000, 'max': 7000, 'avg': 4000},
    'Konya': {'min': 2200, 'max': 6500, 'avg': 3800},
    'Mersin': {'min': 2800, 'max': 8500, 'avg': 5000},
    'Kayseri': {'min': 2000, 'max': 6000, 'avg': 3500},
    'Eskişehir': {'min': 2500, 'max': 7500, 'avg': 4200},
    'Diyarbakır': {'min': 1800, 'max': 5500, 'avg': 3000},
    'Samsun': {'min': 2200, 'max': 6800, 'avg': 3800},
    'Denizli': {'min': 2000, 'max': 6200, 'avg': 3500},
    'Şanlıurfa': {'min': 1500, 'max': 4500, 'avg': 2800}
}

# Semtler (her şehir için)
districts = [
    'Merkez', 'Çankaya', 'Beşiktaş', 'Kadıköy', 'Üsküdar', 'Şişli', 'Beyoğlu',
    'Kartal', 'Maltepe', 'Pendik', 'Ataşehir', 'Bağcılar', 'Bahçelievler',
    'Bakırköy', 'Zeytinburnu', 'Fatih', 'Eminönü', 'Beylikdüzü', 'Avcılar',
    'Küçükçekmece', 'Büyükçekmece', 'Silivri', 'Çatalca', 'Arnavutköy'
]

# Ev tipleri
house_types = ['Daire', 'Villa', 'Müstakil Ev', 'Dubleks', 'Tripleks', 'Rezidans']

# Isıtma tipleri
heating_types = ['Doğalgaz', 'Kombi', 'Merkezi', 'Klima', 'Soba', 'Yerden Isıtma']

# Bina yaşları
building_ages = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '30+']

# Kat sayıları
floor_counts = list(range(1, 21))  # 1-20 arası kat

# Banyo sayıları
bathroom_counts = [1, 2, 3, 4, 5]

# Balkon durumu
balcony_options = ['Var', 'Yok']

# Otopark durumu
parking_options = ['Var', 'Yok', 'Kapalı Otopark', 'Açık Otopark']

# Site içi durumu
site_options = ['Evet', 'Hayır']

# Eşyalı durumu
furnished_options = ['Eşyalı', 'Eşyasız', 'Yarı Eşyalı']

def generate_house_data(n_samples=15000):
    data = []
    
    for i in range(n_samples):
        # Şehir seç
        city = random.choice(list(cities_prices.keys()))
        city_info = cities_prices[city]
        
        # Semt seç
        district = random.choice(districts)
        
        # Ev tipi seç
        house_type = random.choice(house_types)
        
        # Oda sayısı (1+0 ile 5+2 arası)
        room_count = random.choice(['1+0', '1+1', '2+1', '3+1', '4+1', '5+1', '4+2', '5+2'])
        
        # Net metrekare (ev tipine göre)
        if house_type == 'Villa':
            net_area = random.randint(200, 500)
        elif house_type == 'Müstakil Ev':
            net_area = random.randint(120, 300)
        elif house_type == 'Dubleks' or house_type == 'Tripleks':
            net_area = random.randint(150, 350)
        elif house_type == 'Rezidans':
            net_area = random.randint(80, 250)
        else:  # Daire
            if '1+' in room_count:
                net_area = random.randint(45, 80)
            elif '2+' in room_count:
                net_area = random.randint(70, 120)
            elif '3+' in room_count:
                net_area = random.randint(100, 160)
            elif '4+' in room_count:
                net_area = random.randint(140, 200)
            else:  # 5+
                net_area = random.randint(180, 280)
        
        # Brüt metrekare (net + %10-30)
        gross_area = int(net_area * random.uniform(1.1, 1.3))
        
        # Bina yaşı
        building_age = random.choice(building_ages)
        
        # Bulunduğu kat
        if house_type in ['Villa', 'Müstakil Ev']:
            floor = 'Bahçe Katı'
        else:
            floor = random.randint(1, 15)
        
        # Kat sayısı
        if house_type in ['Villa', 'Müstakil Ev']:
            total_floors = random.choice([1, 2, 3])
        else:
            total_floors = random.choice(floor_counts)
        
        # Banyo sayısı
        bathroom_count = random.choice(bathroom_counts)
        
        # Balkon
        balcony = random.choice(balcony_options)
        
        # Isıtma tipi
        heating = random.choice(heating_types)
        
        # Otopark
        parking = random.choice(parking_options)
        
        # Site içi
        in_site = random.choice(site_options)
        
        # Eşyalı durumu
        furnished = random.choice(furnished_options)
        
        # Fiyat hesaplama (m2 fiyatı * net alan + çeşitli faktörler)
        base_price_per_m2 = random.uniform(city_info['min'], city_info['max'])
        
        # Ev tipine göre fiyat çarpanı
        type_multiplier = {
            'Daire': 1.0,
            'Villa': 1.5,
            'Müstakil Ev': 1.3,
            'Dubleks': 1.2,
            'Tripleks': 1.25,
            'Rezidans': 1.1
        }
        
        # Yaş faktörü
        age_multiplier = {
            '0-5': 1.2,
            '6-10': 1.1,
            '11-15': 1.0,
            '16-20': 0.9,
            '21-25': 0.8,
            '26-30': 0.7,
            '30+': 0.6
        }
        
        # Diğer faktörler
        site_multiplier = 1.1 if in_site == 'Evet' else 1.0
        parking_multiplier = 1.05 if 'Var' in parking else 1.0
        balcony_multiplier = 1.02 if balcony == 'Var' else 1.0
        
        # Final fiyat hesaplama
        price = (base_price_per_m2 * net_area * 
                type_multiplier[house_type] * 
                age_multiplier[building_age] * 
                site_multiplier * 
                parking_multiplier * 
                balcony_multiplier)
        
        # Rastgele varyasyon ekle (%±10)
        price *= random.uniform(0.9, 1.1)
        price = int(price)
        
        # Veriyi listeye ekle
        data.append({
            'sehir': city,
            'semt': district,
            'ev_tipi': house_type,
            'oda_sayisi': room_count,
            'net_metrekare': net_area,
            'brut_metrekare': gross_area,
            'bina_yasi': building_age,
            'bulundugu_kat': floor,
            'kat_sayisi': total_floors,
            'banyo_sayisi': bathroom_count,
            'balkon': balcony,
            'isitma_tipi': heating,
            'otopark': parking,
            'site_ici': in_site,
            'esyali_durum': furnished,
            'fiyat_tl': price
        })
    
    return pd.DataFrame(data)

# Veri setini oluştur
print("Ev fiyat verisi oluşturuluyor...")
df = generate_house_data(15000)

# CSV olarak kaydet
df.to_csv('housing/turkiye_ev_fiyatlari.csv', index=False, encoding='utf-8-sig')

print(f"Veri seti başarıyla oluşturuldu!")
print(f"Toplam satır sayısı: {len(df)}")
print(f"Sütun sayısı: {len(df.columns)}")
print("\nİlk 5 satır:")
print(df.head())
print("\nVeri seti özeti:")
print(df.describe())
print("\nFiyat istatistikleri:")
print(f"Minimum fiyat: {df['fiyat_tl'].min():,} TL")
print(f"Maksimum fiyat: {df['fiyat_tl'].max():,} TL")
print(f"Ortalama fiyat: {df['fiyat_tl'].mean():,.0f} TL")
print(f"Medyan fiyat: {df['fiyat_tl'].median():,.0f} TL") 