# 1. temel base katmanı hangi işletim sistemi hangi dil

FROM python:3.12

#2. konteynerin içinde nerede çalışacağız 
WORKDIR /app


#3. bagımlılıkları yönetme
#bilgisayarda reuqirement dosyasını workdir/app'e kopyala
COPY requirements.txt .

#pip install calıstır ve kütüphaneleri kur
# no cache dir: docker image şişirmemek için önbellek dosyalarını tutma
RUN pip install --no-cache-dir -r requirements.txt

#4 kodları taşıma kısmı

COPY . . 
 
#hangi port kapı numarası içerdkei konteyner icindeki numara kapı zili gibi 
EXPOSE 8000

#  BAŞLATMA KOMUTU (CMD): Konteyner çalışınca ilk ne yapsın?
# "Python'ı değil, uvicorn'u çağır ve server'ı başlat."
# 0.0.0.0 çok önemli: Dışarıdan erişime izin verir.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


