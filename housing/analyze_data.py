import pandas as pd

# CSV dosyasını oku
df = pd.read_csv('housing/turkiye_ev_fiyatlari.csv')

print("=== TÜRKİYE EV FİYAT VERİ SETİ ANALİZİ ===\n")

print("Veri seti bilgileri:")
print(f"Satır sayısı: {len(df):,}")
print(f"Sütun sayısı: {len(df.columns)}")

print("\nSütunlar:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\nVeri tipleri:")
print(df.dtypes)

print("\nEksik değerler:")
print(df.isnull().sum())

print("\nFiyat istatistikleri:")
print(df['fiyat_tl'].describe())

print("\nŞehir dağılımı:")
print(df['sehir'].value_counts())

print("\nEv tipi dağılımı:")
print(df['ev_tipi'].value_counts())

print("\nOrtalama fiyatlar (şehir bazında):")
city_avg = df.groupby('sehir')['fiyat_tl'].mean().sort_values(ascending=False)
for city, price in city_avg.items():
    print(f"{city}: {price:,.0f} TL")

print(f"\nVeri seti başarıyla oluşturuldu ve 'housing/turkiye_ev_fiyatlari.csv' dosyasına kaydedildi!") 