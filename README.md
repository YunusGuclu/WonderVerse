# 🌌 WONDERVERSE - Çocuk Portalı — API Tabanlı Eğlence & Keşif Platformu

> ** "Sadece bir web sitesi değil; 9 farklı API ile beslenen, arka planda sürekli yaşayan ve kendini güncelleyen bir dijital evren."**

---

# 🚀 Çocuk Macera Portalı (Django) — API Tabanlı Dinamik İçerik Platformu

Çocuklara yönelik eğlenceli ve öğretici içerikleri tek bir çatı altında sunan **Django tabanlı bir web platformu**.  
Bu projede içerikler **harici API’lerden otomatik olarak çekilir**, veritabanına kaydedilir ve **APScheduler + django-apscheduler** ile zamanlanmış görevler sayesinde **anlık/güncel şekilde kullanıcılara sunulur**.

> ✅ Pokemon, Uzay/gezegenler, SpaceX görevleri, kahramanlar, sanat eserleri, şakalar, bilgi soruları, hayvan görselleri, yemek tarifleri ve HTML5 oyunlar tek projede!

---

## ✨ Öne Çıkan Özellikler

- **Tamamen API tabanlı dinamik içerik** (manuel içerik girme yok)
- **Zamanlayıcı ile otomatik güncelleme (Scheduler)**
  - İçerikler belirli aralıklarla çekilir ve her sayfada “güncel veri” gösterilir
- **Çocuk dostu kategori yapısı**
  - Uzay, oyun, hayvanlar, mutfak, keşif/sanat , kahramanlar gibi sayfalar
- **Türkçe içerik desteği**
  - API’den gelen İngilizce metinler `deep-translator (GoogleTranslator)` ile TR’ye çevrilir
- **Veri şişmesini engelleyen limitli kayıt sistemi**
  - Her model için maksimum kayıt sayısı korunur (ör. Pokemon 12, Şaka 10 vb.)
- **Basit ve hızlı arayüz mantığı**
  - Sayfalarda “son eklenen” veya “rastgele seçilen” içerikler gösterilir
- **Pagination (sayfalama)**
  - Sanat eserleri listesi sayfalı şekilde sunulur

---

## 🧠 Proje Mimarisi (Kısa)

**Akış:**
Kullanıcı siteye girdiğinde sistem dış API servislere istek atmaz. Bunun yerine:
* **Django APScheduler** entegrasyonu ile arka plan görevleri (`tasks.py`) oluşturulmuştur.
* Görevler belirli aralıklarla (45 saniye, 1 saat, 4 saat vb.) tetiklenir.
* Veriler çekilir, **Deep Translator** ile anlık olarak Türkçe'ye çevrilir ve normalize edilir.
* İşlenmiş veri **SQLite** veritabanına kaydedilir.
* **Sonuç:** Frontend, veriyi doğrudan yerel veritabanından çeker. Sayfa yüklenme hızları milisaniyeler seviyesindedir.

---

## 🔌 Entegre Edilen Servisler (Teknoloji Yığını)

Proje, toplamda **9 farklı dış servis** ile haberleşmektedir:

| Servis | Modül / Kullanım | Güncelleme Sıklığı |
| :--- | :--- | :--- |
| **The Solar System OpenData** | Uzay / Gezegenlerin anlık sıcaklık verileri | 1 Saat |
| **SpaceX API** | Uzay / Gelecek roket fırlatmaları ve görselleri | 1 Saat |
| **PokeAPI** | Oyunlar / Pokemon yetenekleri, gücü ve türleri | 45 Saniye |
| **TheMealDB** | Mutfak / Detaylı yemek tarifleri ve malzemeler | 4 Saat |
| **Met Museum Art API** | Keşif / Rastgele sanat eserleri ve tarihçesi | 3 Dakika |
| **Superhero API** | Keşif / Süper kahraman güç istatistikleri | 2 Dakika |
| **TheCatAPI** | Hayvanlar / Rastgele kedi görselleri | 50 Saniye |
| **DogCEO API** | Hayvanlar / Rastgele köpek görselleri | 50 Saniye |
| **Official Joke & OpenTDB** | Eğlence / Şakalar ve Bilgi Yarışması | 50 Saniye |

---
## 🗃️ Veritabanı Tasarımı (Modeller)

Projede içerikler aşağıdaki modellerle tutulur:

- `Pokemon` → isim, resim, tür, güç, can, boy, kilo, yetenekler, ses
- `Gezegen` → isim, tür, resim, sıcaklık, yerçekimi, özellik
- `UzayGorevi` → görev adı, detay, fırlatma tarihi, görsel vb.
- `ElSanati` → isim, açıklama, resim, malzemeler, zorluk
- `SanatEseri` → başlık, sanatçı, resim, tarih, müze linki
- `Hayvan` → resim, tür(kedi/köpek), sevimli puan
- `Saka` → soru, cevap, kategori
- `BilgiSorusu` → kategori, soru, doğru cevap, zorluk, tip
- `YemekTarifi` → isim, görsel, özet, malzemeler, detay, besin değerleri
- `Oyun` → başlık, resim, iframe_url, kategori
- `Aktivite` → (hazır alan) aktivite önerileri için
  
**Ayrıca her model için veritabanı kayıtları sınırsız büyümesin diye “limit temizliği” uygulanır.
---
## 📂 Modüller ve Özellikler

### 🪐 1. Uzay Üssü (Space Module)
* **Hibrit Gezegen Sistemi:** Sabit veri ile canlı API verisinin birleşimi.
* **SpaceX Launch Tracker:** Fırlatma tarihi, roket adı ve görev detayları.

### 🐾 2. Dijital Hayvanat Bahçesi (Animals Module)
* **Çoklu API Yönetimi:** Hem `TheCatAPI` hem de `DogCEO` servislerinden aynı anda veri çekilir.
* **Rastgele İçerik:** Her döngüde farklı eğlenceli kedi ve köpek türleri listelenir.
* **Gamification:** Her hayvana arka planda rastgele bir "Sevimli Puan" (Cute Score) atanarak etkileşim artırılır.

### 🎮 3. Oyun & Eğlence Kutusu
* **Pokedex Kartları:** `Pokemon` modeli üzerinden XP, HP, Boy/Kilo verilerinin analizi.
* **HTML5 Oyun Kutusu:** FlapyBird, Pac-Man, 2048 gibi oyunların iframe entegrasyonu.
* **Mikro İçerikler:** `Official Joke API` ile İngilizce şakaların Türkçeleştirilmesi ve `OpenTDB` ile bilgi yarışması soruları.
* **Şakalar** Eğlenceli şakalar.
* **Bilgi soruları** Bilgilendirici soru ve cevaplar.

### 🥣 4. Minik Şef (Culinary AI)
* **Tarif Motoru:** İngilizce gelen karmaşık tarif metinlerini ve malzeme listelerini parse edip Türkçe'ye çevirir.
* **Besin Simülasyonu:** Tarifler için rastgele kalori ve besin değeri ataması yapar.

### 🌍 5. Keşif & Sanat
* **Sanal Müze:** Met Museum API ile rastgele sanat eserlerini veritabanına kaydeder.
* **Kahraman Analizi:** Süper kahraman dünyasının tanıtılması Zeka, Güç ve Hız vb. puanların karşılaştırılması.

---
## 🌌Arayüzler

### Anasayfa

<img width="1638" height="907" alt="image" src="https://github.com/user-attachments/assets/12ce982f-3498-4bb7-a7d8-3b6fcca41c83" />

---
### Uzay

<img width="1632" height="906" alt="image" src="https://github.com/user-attachments/assets/1eebef6b-0ed5-4bdf-ba99-57285d742b3e" />

---
### Hayvanlar

<img width="1638" height="906" alt="image" src="https://github.com/user-attachments/assets/df9d5a12-de07-486d-8a61-4ddcb509fe35" />

---
### Oyunlar

<img width="1638" height="906" alt="image" src="https://github.com/user-attachments/assets/5cc37241-1421-4f70-bf0d-5b9d9b6a5cb1" />
<img width="1650" height="906" alt="image" src="https://github.com/user-attachments/assets/53b0f5e8-ddc2-461b-874e-0bf8d8849477" />
<img width="1635" height="907" alt="image" src="https://github.com/user-attachments/assets/d51753a2-c922-495f-b901-fd60d7a1c808" />

---
### Keşif

<img width="1642" height="907" alt="image" src="https://github.com/user-attachments/assets/57dd4848-5251-4fa8-b189-20408364e067" />
<img width="1631" height="906" alt="image" src="https://github.com/user-attachments/assets/03afd2de-ce49-4b52-8b10-feeb4c455180" />

---
### Mutfak

<img width="1633" height="902" alt="image" src="https://github.com/user-attachments/assets/eae7c3c1-5875-435c-97be-4151e8a8ecaf" />
<img width="1631" height="902" alt="image" src="https://github.com/user-attachments/assets/9c8f68fb-906d-48d3-b451-80acadeb4eca" />

---

## 🧰 Kullanılan Teknolojiler & Kütüphaneler

- **Python / Django**
- **requests** → API istekleri
- **APScheduler** → zamanlanmış görevler
- **django-apscheduler** → scheduler job store (DB tabanlı)
- **deep-translator** → otomatik çeviri
- **SQLite (dev ortamı)** → hızlı kurulum ve demo
---

### Adım 1: Repoyu Klonlayın
```
git clone [https://github.com/KULLANICI_ADINIZ/WonderVerse.git](https://github.com/KULLANICI_ADINIZ/WonderVerse.git)
cd WonderVerse
```
### Adım 2: Sanal Ortam Oluşturun
```
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
### Adım 3: Bağımlılıkları Yükleyin
```
pip install django requests apscheduler deep-translator django-apscheduler
```
### Adım 4: Veritabanını Hazırlayın
```
python manage.py makemigrations
python manage.py migrate
```
### Adım 5: Veri Motorunu Başlatın (ÖNEMLİ ⚠️)
Scheduler çalışmaya başlamadan önce, veritabanını ilk verilerle doldurmak için shell komutlarını kullanın:
```
python manage.py shell
```
```
from WonderVerse.tasks import *
print("Veri motoru manuel tetikleniyor...")
gorev_uzay_istasyonu()  # Gezegenler ve SpaceX
gorev_oyunlari_yukle()  # HTML5 Oyunları
gorev_pokemon_avla()    # İlk Pokemon
gorev_minik_sef()       # İlk Tarif
gorev_heroes()          # Kahramanlar
gorev_hayvan_saka()     # Kedi, Köpek, Şaka ve Trivia Verileri
gorev_sanat()           # Sanat
exit()
```
### Adım 6: Sunucuyu Başlatın
```
python manage.py runserver
```
