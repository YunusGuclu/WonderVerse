import requests
import random
from .models import Pokemon, UzayBilgisi, Animal, Country, FunItem, Fruit, ArtPiece


def fetch_all_data():
    print("--- Veri Çekme İşlemi Başladı ---")
    get_pokemon()
    get_nasa()
    get_spacex()
    get_animals()
    get_countries()
    get_jokes()
    get_trivia()
    get_bored_activity()
    get_fruits()
    get_art()
    print("--- Veri Çekme İşlemi Tamamlandı ---")

def get_pokemon():
    try:
        pid = random.randint(1, 151)
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pid}").json()
        name = data['name'].capitalize()
        if not Pokemon.objects.filter(name=name).exists():
            Pokemon.objects.create(
                name=name,
                image_url=data['sprites']['other']['official-artwork']['front_default'],
                types=", ".join([t['type']['name'] for t in data['types']]),
                abilities=", ".join([a['ability']['name'] for a in data['abilities']])
            )
    except: pass

def get_nasa():
    try:
        data = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY").json()
        if not SpaceFact.objects.filter(title=data['title']).exists():
            SpaceFact.objects.create(
                source="NASA", title=data['title'], 
                description=data.get('explanation', '')[:500], image_url=data.get('url')
            )
    except: pass

def get_spacex():
    try:
        data = requests.get("https://api.spacexdata.com/v4/launches/latest").json()
        patch = data['links']['patch']['small']
        if patch and not SpaceFact.objects.filter(title=data['name']).exists():
            SpaceFact.objects.create(
                source="SpaceX", title=f"Roket: {data['name']}",
                description=data.get('details', 'Görev Başarılı!'), image_url=patch
            )
    except: pass

def get_animals():
    # Köpek
    try:
        url = requests.get("https://dog.ceo/api/breeds/image/random").json()['message']
        if not Animal.objects.filter(image_url=url).exists():
            Animal.objects.create(species="Köpek", image_url=url)
    except: pass
    # Kedi
    try:
        url = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url']
        if not Animal.objects.filter(image_url=url).exists():
            Animal.objects.create(species="Kedi", image_url=url)
    except: pass

def get_countries():
    try:
        all_c = requests.get("https://restcountries.com/v3.1/all").json()
        c = random.choice(all_c)
        name = c['name']['common']
        if not Country.objects.filter(name=name).exists():
            Country.objects.create(
                name=name, capital=c.get('capital', ['Yok'])[0],
                flag_url=c['flags']['svg'], population=c.get('population', 0),
                region=c.get('region', 'Dünya')
            )
    except: pass

def get_jokes():
    try:
        joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        if not FunItem.objects.filter(question=joke['setup']).exists():
            FunItem.objects.create(category="Şaka", question=joke['setup'], answer=joke['punchline'])
    except: pass

def get_trivia():
    try:
        triv = requests.get("https://opentdb.com/api.php?amount=1&type=boolean").json()['results'][0]
        if not FunItem.objects.filter(question=triv['question']).exists():
            FunItem.objects.create(category="Bilgi", question=triv['question'], answer=triv['correct_answer'])
    except: pass

def get_bored_activity():
    try:
        act = requests.get("https://bored-api.appbrewery.com/random").json()
        if not FunItem.objects.filter(question=act['activity']).exists():
            FunItem.objects.create(category="Aktivite", question=act['activity'], answer=f"Tür: {act['type']}")
    except: pass

def get_fruits():
    try:
        fruits = requests.get("https://www.fruityvice.com/api/fruit/all").json()
        f = random.choice(fruits)
        if not Fruit.objects.filter(name=f['name']).exists():
            Fruit.objects.create(
                name=f['name'], calories=f['nutritions']['calories'], sugar=f['nutritions']['sugar']
            )
    except: pass

def get_art():
    try:
        # Met Museum'da 'Toys' araması
        search = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=toys&hasImages=true").json()
        if search['total'] > 0:
            obj_id = random.choice(search['objectIDs'][:30])
            art = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}").json()
            if art.get('primaryImageSmall') and not ArtPiece.objects.filter(title=art['title']).exists():
                ArtPiece.objects.create(
                    title=art['title'], artist=art.get('artistDisplayName', 'Bilinmiyor'),
                    image_url=art['primaryImageSmall']
                )
    except: pass