from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

# Model ve Tokenizer'ı belirle
model_name = "savasy/bert-base-turkish-sentiment-cased"
save_directory = "./src/model_files"  # Senin logundaki klasör yolu

print(f"⏳ '{model_name}' modeli indiriliyor... (440 MB)")
print("Bu işlem internet hızına göre 1-5 dakika sürebilir. Lütfen bekleyin...")

# Klasör yoksa oluştur
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# İndir ve kaydet
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"✅ BAŞARILI! Dosyalar '{save_directory}' klasörüne kaydedildi.")
# "Silebilirsin" mesajını sildim ki kafa karışmasın :)
print("Bu dosya projenin bir parçasıdır, silmeyiniz.")