import requests
import random
from datetime import datetime
from .models import *
from deep_translator import GoogleTranslator

# --- YARDIMCI FONKSİYONLAR ---
def cevir(metin):
    if not metin or metin == "": return ""
    try:
        metin_str = str(metin)
        if len(metin_str) > 4500: metin_str = metin_str[:4500]
        cevrilmis = GoogleTranslator(source='auto', target='tr').translate(metin_str)
        return cevrilmis
    except: return metin

def temizle(ModelClass, limit=20):
    if ModelClass.objects.count() > limit:
        ModelClass.objects.order_by('id').first().delete()

# 1. ⚡ POKEMON GÖREVİ
def gorev_pokemon_avla():
    print("⚡ Pokemon Aranıyor...")
    try:
        pid = random.randint(1, 151)
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pid}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            orijinal_isim = d['name'].capitalize()
            ing_tur = d['types'][0]['type']['name']
            tr_tur = cevir(ing_tur).capitalize()
            
            # Yetenekler
            abilities = [a['ability']['name'].replace('-', ' ') for a in d['abilities']]
            tr_yetenekler = cevir(", ".join(abilities)).title()

            Pokemon.objects.create(
                isim=orijinal_isim, 
                resim=d['sprites']['other']['official-artwork']['front_default'],
                tur=tr_tur,
                guc=d['base_experience'],
                can=d['stats'][0]['base_stat'],
                boy=d['height'] / 10,
                kilo=d['weight'] / 10,
                yetenekler=tr_yetenekler,
                ses_dosyasi=d.get('cries', {}).get('latest', None)
            )
            temizle(Pokemon, 12)
            print(f"✅ Pokemon: {orijinal_isim}")
    except Exception as e: print(f"Pokemon Hatası: {e}")

# 2. 🚀 UZAY İSTASYONU (KIRILMAZ VERSİYON)
def gorev_uzay_istasyonu():
    print("🚀 Uzay İstasyonu Taranıyor...")
    
    # SABİT KATALOG (Asla Bozulmaz)
    gezegen_katalogu = {
        "Sun": {"tr": "Güneş", "tur": "Yıldız", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg/600px-The_Sun_by_the_Atmospheric_Imaging_Assembly_of_NASA%27s_Solar_Dynamics_Observatory_-_20100819.jpg", "ozellik": "Isı ve ışık kaynağımız.", "sicaklik": "Çok Sıcak (5500°C)", "cekim": "Çok Güçlü"},
        "Mercury": {"tr": "Merkür", "tur": "Gezegen", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Mercury_in_true_color.jpg/600px-Mercury_in_true_color.jpg", "ozellik": "Güneş'e en yakın gezegen.", "sicaklik": "Gündüz 430°C", "cekim": "Hafif"},
        "Venus": {"tr": "Venüs", "tur": "Gezegen", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Venus-real_color.jpg/600px-Venus-real_color.jpg", "ozellik": "En parlak ve sıcak gezegen.", "sicaklik": "462°C", "cekim": "Dünya Gibi"},
        "Earth": {"tr": "Dünya", "tur": "Gezegen", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/600px-The_Earth_seen_from_Apollo_17.jpg", "ozellik": "Bizim evimiz!", "sicaklik": "Ortalama 15°C", "cekim": "Normal (1G)"},
        "Mars": {"tr": "Mars", "tur": "Gezegen", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/OSIRIS_Mars_true_color.jpg/600px-OSIRIS_Mars_true_color.jpg", "ozellik": "Kızıl Gezegen.", "sicaklik": "Soğuk (-60°C)", "cekim": "Hafif"},
        "Jupiter": {"tr": "Jüpiter", "tur": "Dev Gaz", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Jupiter_and_its_shrunken_Great_Red_Spot.jpg/600px-Jupiter_and_its_shrunken_Great_Red_Spot.jpg", "ozellik": "En büyük gezegen!", "sicaklik": "Soğuk (-145°C)", "cekim": "Çok Güçlü"},
        "Saturn": {"tr": "Satürn", "tur": "Dev Gaz", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Saturn_during_Equinox.jpg/800px-Saturn_during_Equinox.jpg", "ozellik": "Halkaların Efendisi.", "sicaklik": "Soğuk (-178°C)", "cekim": "Güçlü"},
        "Uranus": {"tr": "Uranüs", "tur": "Buz Dev", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Uranus2.jpg/600px-Uranus2.jpg", "ozellik": "Yan yatmış gezegen.", "sicaklik": "Buz Gibi (-224°C)", "cekim": "Dünya Gibi"},
        "Neptune": {"tr": "Neptün", "tur": "Buz Dev", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Neptune_-_Voyager_2_%2829347980845%29_flatten_crop.jpg/600px-Neptune_-_Voyager_2_%2829347980845%29_flatten_crop.jpg", "ozellik": "En uzak ve rüzgarlı.", "sicaklik": "Dondurucu (-214°C)", "cekim": "Güçlü"}
    }

    # API İLE GÜNCELLEME
    try:
        r = requests.get("https://api.le-systeme-solaire.net/rest/bodies/", timeout=10)
        if r.status_code == 200:
            bodies = r.json()['bodies']
            for item in bodies:
                eng_name = item['englishName']
                if eng_name in gezegen_katalogu:
                    try:
                        temp_k = item.get('avgTemp', 0)
                        if temp_k > 0:
                            gezegen_katalogu[eng_name]['sicaklik'] = f"{int(temp_k - 273.15)}°C"
                    except: pass
    except: pass

    for key, val in gezegen_katalogu.items():
        Gezegen.objects.update_or_create(
            isim=val['tr'],
            defaults={'tur': val['tur'], 'resim': val['resim'], 'sicaklik': val['sicaklik'], 'yercekimi': val['cekim'], 'ozellik': val['ozellik']}
        )
    print("✅ Gezegenler Hazır.")

    # SPACEX
    try:
        r = requests.get("https://api.spacexdata.com/v4/launches/upcoming", timeout=10)
        if r.status_code == 200:
            launches = r.json()[:4]
            for l in launches:
                links = l.get('links') or {}
                patch = links.get('patch') or {}
                resim = patch.get('small') or "https://images.unsplash.com/photo-1517976487492-5750f3195933?w=500"
                detay = l.get('details') or "Detay bekleniyor."

                if not UzayGorevi.objects.filter(gorev_adi=l['name']).exists():
                    UzayGorevi.objects.create(
                        gorev_adi=l['name'],
                        detay=cevir(detay[:200]),
                        firlatma_tarihi=l.get('date_utc', 'Tarih Yok')[:10],
                        resim=resim
                    )
            temizle(UzayGorevi, 5)
            print("✅ SpaceX Hazır.")
    except Exception as e: print(f"SpaceX Hatası: {e}")

# 3. 🦸‍♂️ KAHRAMANLAR
def gorev_heroes(): 
    try:
        r = requests.get("https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json", timeout=10)
        if r.status_code == 200:
            for k in random.sample(r.json(), 5):
                tam_isim = f"{k['name']} ({k.get('biography', {}).get('publisher', 'Bilinmiyor')})"
                if not ElSanati.objects.filter(isim=tam_isim).exists():
                    ElSanati.objects.create(
                        isim=tam_isim,
                        resim=k['images']['lg'],
                        aciklama=str(k.get('powerstats', {}).get('intelligence') or 50),
                        malzemeler=str(k.get('powerstats', {}).get('strength') or 50),
                        zorluk=str(k.get('powerstats', {}).get('speed') or 50)
                    )
            temizle(ElSanati, 8)
            print("✅ Kahramanlar Hazır.")
    except: pass

# 4. 🎨 SANAT
def gorev_sanat():
    konu = random.choice(['cat', 'dog', 'sunflowers', 'birds', 'toys', 'music'])
    try:
        r = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={konu}&hasImages=true", timeout=10)
        if r.status_code == 200:
            ids = r.json().get('objectIDs', [])
            if ids:
                art = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{random.choice(ids[:50])}", timeout=5).json()
                if art.get('primaryImageSmall'):
                    SanatEseri.objects.create(
                        baslik=cevir(art.get('title', 'Sanat Eseri')),
                        sanatci=art.get('artistDisplayName', 'Bilinmeyen Sanatçı'),
                        resim=art.get('primaryImageSmall'),
                        tarih=art.get('objectDate', 'Tarih Yok'),
                        muze_linki=art.get('objectURL', '')
                    )
                    temizle(SanatEseri, 9)
                    print("✅ Sanat Eseri Hazır.")
    except: pass

# 5. 😂 ŞAKALAR & HAYVANLAR
def gorev_hayvan_saka():
    try:
        r = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        Saka.objects.create(soru=cevir(r['setup']), cevap=cevir(r['punchline']), kategori=r['type'])
        temizle(Saka, 10)
    except: pass
    
    try:
        r = requests.get("https://opentdb.com/api.php?amount=1&type=multiple").json()['results'][0]
        BilgiSorusu.objects.create(
            kategori=cevir(r['category']), soru=cevir(r['question']), 
            dogru_cevap=cevir(r['correct_answer']), zorluk=r['difficulty'], tip=r['type']
        )
        temizle(BilgiSorusu, 5)
    except: pass

    try:
        r = requests.get("https://api.thecatapi.com/v1/images/search").json()
        Hayvan.objects.create(resim=r[0]['url'], tur='kedi', sevimli_puan=random.randint(80,100))
    except: pass
    try:
        r = requests.get("https://dog.ceo/api/breeds/image/random").json()
        Hayvan.objects.create(resim=r['message'], tur='kopek', sevimli_puan=random.randint(80,100))
    except: pass
    temizle(Hayvan, 20)

# 6. 🥣 LEZZETLİ MUTFAK
def gorev_minik_sef():
    print("🥣 Tarif Hazırlanıyor...")
    try:
        r = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
        if r.status_code == 200:
            d = r.json()['meals'][0]
            malzemeler = [f"{d.get(f'strMeasure{i}')} {d.get(f'strIngredient{i}')}".strip() for i in range(1, 21) if d.get(f'strIngredient{i}')]
            
            tr_isim = cevir(d['strMeal'])
            tr_tarif = cevir(d['strInstructions'])
            
            YemekTarifi.objects.create(
                isim=tr_isim, resim=d['strMealThumb'], ozet=tr_tarif[:150] + "...",
                malzemeler=cevir(", ".join(malzemeler)), tarif_detay=tr_tarif,
                hazirlama_suresi=random.choice([20, 30, 45, 60]), saglik_puani=random.randint(75, 100),
                kalori=random.randint(200, 600), protein=f"{random.randint(5,30)}g",
                yag=f"{random.randint(5,20)}g", karbonhidrat=f"{random.randint(20,80)}g", seker=f"{random.randint(2,20)}g"
            )
            temizle(YemekTarifi, 6)
            print(f"✅ Tarif: {tr_isim}")
    except Exception as e: print(f"Mutfak Hatası: {e}")

# 7. 🎮 OYUN KUTUSU (SENİN SEÇTİĞİN 20 OYUN)
def gorev_oyunlari_yukle():
    print("🎮 Oyun Kutusu Yükleniyor...")
    garanti_oyunlar = [
        {"isim": "Minecraft Classic", "resim": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png", "url": "https://classic.minecraft.net/", "kat": "Yaratıcılık"},
        {"isim": "2048", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/2048_logo.svg/1200px-2048_logo.svg.png", "url": "https://play2048.co/", "kat": "Zeka"},
        {"isim": "Dinozor Oyunu", "resim": "https://i.imgur.com/8X8v3bZ.png", "url": "https://chromedino.com/", "kat": "Macera"},
        {"isim": "Flappy Bird", "resim": "https://upload.wikimedia.org/wikipedia/en/0/0a/Flappy_Bird_icon.png", "url": "https://flappybird.io/", "kat": "Beceri"},
        {"isim": "Pac-Man", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Pacman.svg/1200px-Pacman.svg.png", "url": "https://freepacman.org/", "kat": "Klasik"},
        {"isim": "Hextris", "resim": "https://raw.githubusercontent.com/Hextris/hextris/gh-pages/images/icons/apple-touch-120.png", "url": "https://hextris.io/", "kat": "Zeka"},
        {"isim": "Tetris", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Tetris_logo.svg/1200px-Tetris_logo.svg.png", "url": "https://chvin.github.io/react-tetris/", "kat": "Klasik"},
        {"isim": "Sudoku", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Sudoku-by-L2G-20050714.svg/1200px-Sudoku-by-L2G-20050714.svg.png", "url": "https://zhang-suen.github.io/sudoku/", "kat": "Zeka"},
        {"isim": "Mayın Tarlası", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Minesweeper_flag.svg/1200px-Minesweeper_flag.svg.png", "url": "https://muan.github.io/mk-minesweeper/", "kat": "Zeka"},
        {"isim": "2048 Cupcakes", "resim": "https://img.poki.com/cdn-cgi/image/quality=78,width=600,height=600,fit=cover,f=auto/937805177583626786a34937740e53a2.png", "url": "https://0x0800.github.io/2048-CUPCAKES/", "kat": "Zeka"},
        {"isim": "Space Invaders", "resim": "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/SpaceInvaders-Arcade-1978.png/220px-SpaceInvaders-Arcade-1978.png", "url": "https://freeinvaders.org/", "kat": "Klasik"},
        {"isim": "Pong", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Pong.png/1200px-Pong.png", "url": "https://pong-2.com/", "kat": "Spor"},
        {"isim": "Yılan Oyunu", "resim": "https://i.imgur.com/3f3gT8q.png", "url": "https://patorjk.com/games/snake/", "kat": "Klasik"},
        {"isim": "Tic Tac Toe", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/1200px-Tic_tac_toe.svg.png", "url": "https://tictactoegame.net/", "kat": "Zeka"},
        {"isim": "Connect 4", "resim": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Connect_Four.gif", "url": "https://kevinshannon.com/connect4/", "kat": "Zeka"},
        {"isim": "Quick Draw", "resim": "https://upload.wikimedia.org/wikipedia/en/9/97/Quick_Draw_Logo.png", "url": "https://quickdraw.withgoogle.com/", "kat": "Eğlence"},
        {"isim": "Song Maker", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/G_Clef.svg/800px-G_Clef.svg.png", "url": "https://musiclab.chromeexperiments.com/Song-Maker/", "kat": "Müzik"},
        {"isim": "Hafıza Oyunu", "resim": "https://i.imgur.com/eB4yq9X.png", "url": "https://marina-ferreira.github.io/memory-game/", "kat": "Zeka"},
        {"isim": "Little Alchemy 2", "resim": "https://littlealchemy2.com/static/img/share.png", "url": "https://littlealchemy2.com/", "kat": "Bilim"},
        {"isim": "Satranç", "resim": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Chessboard480.svg/1200px-Chessboard480.svg.png", "url": "https://rviscarra.github.io/simple-chess/", "kat": "Zeka"}
    ]

    for oyun in garanti_oyunlar:
        if not Oyun.objects.filter(baslik=oyun["isim"]).exists():
            Oyun.objects.create(
                baslik=oyun["isim"], resim=oyun["resim"], iframe_url=oyun["url"], kategori=oyun["kat"]
            )
            print(f"✅ Oyun Eklendi: {oyun['isim']}")
    print("🚀 Oyunlar Hazır!")