import requests
from datetime import datetime
import json
import random
from .models import *
import time

def get_api_data(endpoint):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(endpoint, headers=headers)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"API Hatası: {e}")
        return None

def yemek_tarifi_guncelle():
    # TheMealDB - Ücretsiz API
    api_url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        tarifler = []
        for _ in range(5):  # 5 rastgele tarif al
            data = get_api_data(api_url)
            if data and data['meals']:
                meal = data['meals'][0]
                tarifler.append({
                    "isim": meal['strMeal'],
                    "malzemeler": "\n".join([meal[f'strIngredient{i}'] for i in range(1, 21) if meal[f'strIngredient{i}']]),
                    "yapilis": meal['strInstructions'],
                    "zorluk": "Orta",
                    "hazirlama_suresi": "30 dakika",
                    "pisirme_suresi": "20 dakika",
                    "resim_url": meal['strMealThumb']
                })
            time.sleep(1)  # API limit aşımını önlemek için
        
        if tarifler:
            YemekTarifi.objects.all().delete()
            for tarif in tarifler:
                YemekTarifi.objects.create(**tarif)
                print(f"Yeni tarif eklendi: {tarif['isim']}")
                
    except Exception as e:
        print(f"Yemek tarifi güncelleme hatası: {e}")

def hikaye_guncelle():
    # Türkçe Wikipedia API'si - Çocuk Hikayeleri kategorisi
    api_url = "https://tr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Kategori:Çocuk_edebiyatı",
        "cmlimit": "10"
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if 'query' in data and 'categorymembers' in data['query']:
            HikayeMasallar.objects.all().delete()
            for hikaye in data['query']['categorymembers'][:5]:
                # Her hikaye için detay bilgisi al
                detay_params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts|pageimages",
                    "titles": hikaye['title'],
                    "exintro": True,
                    "explaintext": True
                }
                detay = requests.get(api_url, params=detay_params).json()
                page = next(iter(detay['query']['pages'].values()))
                
                HikayeMasallar.objects.create(
                    baslik=hikaye['title'],
                    tur="hikaye",
                    icerik=page.get('extract', '')[:500],  # İlk 500 karakter
                    yazar="Halk Hikayesi",
                    okuma_suresi="10 dakika",
                    yas_grubu="6-12",
                    anahtar_kelimeler="çocuk, hikaye, masal"
                )
                time.sleep(1)
    except Exception as e:
        print(f"Hikaye güncelleme hatası: {e}")


def bilmece_guncelle():
    # Türkçe Wikipedia API'si - Bilmeceler kategorisi
    api_url = "https://tr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Kategori:Bilmeceler",
        "cmlimit": "10"
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if 'query' in data and 'categorymembers' in data['query']:
            BilmeceBulmaca.objects.all().delete()
            for bilmece in data['query']['categorymembers'][:5]:
                detay_params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts",
                    "titles": bilmece['title'],
                    "exintro": True,
                    "explaintext": True
                }
                detay = requests.get(api_url, params=detay_params).json()
                page = next(iter(detay['query']['pages'].values()))
                icerik = page.get('extract', '').split('\n')
                
                BilmeceBulmaca.objects.create(
                    tur="Bilmece",
                    soru=icerik[0] if icerik else "Bilmece",
                    cevap=icerik[1] if len(icerik) > 1 else "Cevap",
                    zorluk="Kolay",
                    ipucu="Düşün bakalım!"
                )
                time.sleep(1)
    except Exception as e:
        print(f"Bilmece güncelleme hatası: {e}")


def doga_bilgisi_guncelle():
    print("Çocuklar için doğa bilgisi güncelleme başladı...")
    
    # Çocuklara uygun doğa kategorileri
    cocuk_kategorileri = {
        "Evcil_hayvanlar": ["Kedi", "Köpek", "Hamster", "Muhabbet kuşu", "Tavşan"],
        "Vahşi_hayvanlar": ["Aslan", "Fil", "Zürafa", "Penguen", "Panda"],
        "Deniz_canlıları": ["Yunus", "Balina", "Deniz yıldızı", "Denizkaplumbağası"],
        "Böcekler": ["Kelebek", "Uğur böceği", "Arı", "Karınca"],
        "Kuşlar": ["Papağan", "Baykuş", "Kartal", "Flamingo", "Leylek"],
        "Bitkiler": ["Çiçekler", "Ağaçlar", "Meyveler", "Sebzeler"]
    }
    
    try:
        data_list = []
        
        for kategori, alt_konular in cocuk_kategorileri.items():
            print(f"{kategori} kategorisinden veriler çekiliyor...")
            
            for konu in alt_konular:
                # Makale API URL
                api_url = "https://tr.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts|pageimages",
                    "titles": konu,
                    "exintro": True,  # Sadece giriş paragrafını al
                    "explaintext": True,  # Düz metin olarak al
                    "pithumbsize": 500,  # Resim boyutu
                }
                
                try:
                    response = requests.get(api_url, params=params)
                    data = response.json()
                    
                    if 'query' in data and 'pages' in data['query']:
                        page = next(iter(data['query']['pages'].values()))
                        
                        # İçeriği çocuklar için düzenle
                        icerik = page.get('extract', '')
                        if icerik:
                            # İçeriği kısalt ve basitleştir
                            cumleler = icerik.split('.')
                            basit_icerik = '. '.join(cumleler[:3]) + '.'  # İlk 3 cümle
                            
                            # Resim URL'sini al
                            resim_url = page.get('thumbnail', {}).get('source', '')
                            
                            if resim_url and len(basit_icerik) > 50:  # Sadece resimli ve yeterli içeriği olanları al
                                ilginc_bilgi = random.choice([
                                    f"Biliyor muydun? {konu} hakkında ilginç bilgiler var!",
                                    f"Haydi {konu} hakkında daha fazla öğrenelim!",
                                    f"{konu} doğanın harika canlılarından biridir!",
                                    f"Doğadaki arkadaşımız {konu} ile tanışalım!"
                                ])
                                
                                data_list.append({
                                    "baslik": f"{konu} Hakkında",
                                    "kategori": kategori.replace("_", " "),
                                    "icerik": basit_icerik,
                                    "ilginc_bilgi": ilginc_bilgi,
                                    "resim_url": resim_url,
                                    "kaynak": "Wikipedia"
                                })
                                print(f"'{konu}' konusu eklendi.")
                
                    # API limitlerini aşmamak için kısa bekleme
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Konu çekme hatası ({konu}): {e}")
                    continue
        
        if data_list:
            # Mevcut verileri sil
            DogaBilgisi.objects.all().delete()
            print("Eski veriler silindi.")
            
            # Yeni verileri ekle
            for bilgi in data_list:
                DogaBilgisi.objects.create(**bilgi)
                print(f"Yeni bilgi eklendi: {bilgi['baslik']}")
            
            print(f"Toplam {len(data_list)} yeni doğa bilgisi eklendi.")
        else:
            print("Hiç veri çekilemedi!")
            
    except Exception as e:
        print(f"Genel güncelleme hatası: {e}")


def aktivite_guncelle():
    # Türkçe Wikipedia API'si - Çocuk Aktiviteleri
    api_url = "https://tr.wikipedia.org/w/api.php"
    aktivite_konulari = ["Oyun", "Spor", "Sanat", "Müzik", "Dans"]
    
    try:
        aktiviteler = []
        for konu in aktivite_konulari:
            params = {
                "action": "query",
                "format": "json",
                "prop": "extracts|pageimages",
                "titles": konu,
                "exintro": True,
                "explaintext": True,
                "pithumbsize": 500
            }
            
            response = requests.get(api_url, params=params)
            data = response.json()
            if 'query' in data and 'pages' in data['query']:
                page = next(iter(data['query']['pages'].values()))
                
                aktiviteler.append({
                    "baslik": f"Çocuklar için {konu}",
                    "aciklama": page.get('extract', '')[:300],
                    "kategori": konu,
                    "yas_grubu": "7-12",
                    "resim_url": page.get('thumbnail', {}).get('source', '')
                })
            time.sleep(1)
        
        if aktiviteler:
            Aktivite.objects.all().delete()
            for aktivite in aktiviteler:
                Aktivite.objects.create(**aktivite)
                print(f"Yeni aktivite eklendi: {aktivite['baslik']}")
                
    except Exception as e:
        print(f"Aktivite güncelleme hatası: {e}")

def el_sanatlari_guncelle():
    # Türkçe Wikipedia API'si - El Sanatları
    api_url = "https://tr.wikipedia.org/w/api.php"
    el_sanati_konulari = ["Origami", "Seramik", "Boyama", "El_işi", "Dokuma"]
    
    try:
        projeler = []
        for konu in el_sanati_konulari:
            params = {
                "action": "query",
                "format": "json",
                "prop": "extracts|pageimages",
                "titles": konu,
                "exintro": True,
                "explaintext": True,
                "pithumbsize": 500
            }
            
            response = requests.get(api_url, params=params)
            data = response.json()
            if 'query' in data and 'pages' in data['query']:
                page = next(iter(data['query']['pages'].values()))
                
                projeler.append({
                    "proje_adi": f"{konu} Projesi",
                    "malzemeler": "Gerekli malzemeler...",
                    "yapilis_adimlari": page.get('extract', '')[:300],
                    "zorluk": "Kolay",
                    "yas_grubu": "6+",
                    "resim_url": page.get('thumbnail', {}).get('source', '')
                })
            time.sleep(1)
        
        if projeler:
            ElSanatlari.objects.all().delete()
            for proje in projeler:
                ElSanatlari.objects.create(**proje)
                print(f"Yeni el sanatı projesi eklendi: {proje['proje_adi']}")
                
    except Exception as e:
        print(f"El sanatları güncelleme hatası: {e}")