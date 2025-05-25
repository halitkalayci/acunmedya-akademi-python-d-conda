import pickle

# Kategorik değerleri kontrol et
with open('model/categorical_values.pkl', 'rb') as f:
    categorical_values = pickle.load(f)

print("Kategorik Değerler:")
for key, values in categorical_values.items():
    print(f"  {key}: {values}")

print("\n" + "="*50)

# Özellik isimlerini kontrol et
with open('model/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

print("Özellik İsimleri:")
for i, name in enumerate(feature_names):
    print(f"  {i+1}. {name}") 