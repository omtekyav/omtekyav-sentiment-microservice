from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os
import shutil

# 🌍 MULTILINGUAL MODEL (TR/EN/DE/FR/ES)
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
save_directory = "./src/model_files"

print(f"🌍 Multilingual model indiriliyor: {model_name}")
print("⏳ Bu işlem internet hızına göre 2-5 dakika sürebilir...")

# Eski model varsa temizle
if os.path.exists(save_directory):
    try:
        shutil.rmtree(save_directory)
        print("🧹 Eski model dosyaları temizlendi")
    except Exception as e:
        print(f"⚠️ Temizleme hatası (devam ediliyor): {e}")

# Klasör oluştur
os.makedirs(save_directory, exist_ok=True)

# İndir ve kaydet
try:
    print("📥 Tokenizer indiriliyor...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print("📥 Model indiriliyor...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    print("💾 Kaydediliyor...")
    tokenizer.save_pretrained(save_directory)
    model.save_pretrained(save_directory)
    
    print(f"✅ MODEL HAZIR! Dosyalar: {save_directory}")
    print("🌍 Desteklenen diller: TR, EN, DE, FR, ES, NL")
    
except Exception as e:
    print(f"❌ İndirme hatası: {e}")
    raise