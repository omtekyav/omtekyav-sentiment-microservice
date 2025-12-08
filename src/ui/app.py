import os
import streamlit as st
import requests
import pandas as pd

# --- AYARLAR (DOCKER UYUMLULUĞU İÇİN KRİTİK KISIM) ---
# Docker'dan gelen 'API_URL' ortam değişkenini al. 
# Eğer yoksa (lokalde çalışıyorsan) varsayılan olarak localhost'u kullan.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1/analyze")
# İstatistik URL'sini de ana URL'den türetelim
STATS_URL = API_URL.replace("analyze", "stats")

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Sentiment AI Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- YAN MENÜ (SIDEBAR) & İSTATİSTİKLER ---
with st.sidebar:
    st.header("📊 Canlı İstatistikler")
    
    try:
        # GÜNCELLEME: Artık dinamik URL kullanıyoruz
        response = requests.get(STATS_URL)
        
        if response.status_code == 200:
            stats = response.json()
            
            # Toplam Sayı
            st.metric("Toplam Analiz", stats["Total"])
            
            # Grafik Verisi
            chart_data = {
                "Duygu": ["Pozitif", "Negatif", "Nötr"],
                "Adet": [stats["Pozitif"], stats["Negatif"], stats["Nötr"]]
            }
            df = pd.DataFrame(chart_data)
            
            # Bar Grafiği
            st.bar_chart(df.set_index("Duygu"))
            
        else:
            st.error("İstatistikler alınamadı.")
            
    except Exception as e:
        st.warning("Backend sunucusuna bağlanılamıyor.")
        st.caption(f"Hata: {e}")
        # Debug için URL'i gösterelim (Gerekirse açarsın)
        # st.caption(f"Denenen Adres: {STATS_URL}")

    st.divider()
    st.info("Bu panel, FastAPI servisine bağlıdır.")

# --- ANA EKRAN ---
st.title("🧠 Türkçe Duygu Analizi Asistanı")
st.markdown("Yapay zeka modelini (BERT) kullanarak metinlerinizi analiz edin.")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area(
        "Analiz edilecek metni giriniz:",
        placeholder="Örn: Ürün harika paketlenmiş ama kargo çok geç geldi...",
        height=150
    )
    analyze_btn = st.button("Analiz Et 🚀", type="primary", use_container_width=True)

# Mantık Kısmı
if analyze_btn:
    if not user_input.strip():
        st.warning("⚠️ Lütfen boş bir metin girmeyiniz.")
    else:
        with st.spinner("Yapay Zeka düşünüyor..."):
            try:
                # GÜNCELLEME: Artık dinamik API_URL kullanıyoruz
                response = requests.post(
                    API_URL,
                    json={"text": user_input},
                    timeout=120
                )

                if response.status_code == 200:
                    result = response.json()
                    sentiment = result["sentiment"]
                    confidence = result["confidence"]
                    
                    st.success("✅ Analiz Tamamlandı!")
                    
                    # Sonuçları yan yana göster
                    m1, m2 = st.columns(2)
                    m1.metric("Duygu", sentiment)
                    m2.metric("Güven", f"%{confidence*100:.1f}")
                    st.progress(confidence)
                    
                    st.toast("İstatistikler güncellendi! (Sol panele bakınız)", icon="🎉")
                    
                else:
                    st.error(f"Hata: {response.text}")

            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")
                st.caption(f"Denenen Adres: {API_URL}")