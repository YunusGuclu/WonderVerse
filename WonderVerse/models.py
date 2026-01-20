from django.db import models

# 1. 🧬 POKEMON
class Pokemon(models.Model):
    isim = models.CharField(max_length=100)
    resim = models.URLField()
    tur = models.CharField(max_length=50)
    guc = models.IntegerField()
    can = models.IntegerField(default=50)
    boy = models.FloatField(help_text="Metre cinsinden")
    kilo = models.FloatField(help_text="Kilogram cinsinden")
    yetenekler = models.CharField(max_length=255, help_text="Özel yetenekleri")
    ses_dosyasi = models.URLField(blank=True, null=True, help_text="Pokemon sesi")

# 2. 🚀 UZAY (SPACEX & GEZEGENLER)
class UzayGorevi(models.Model): # SpaceX
    gorev_adi = models.CharField(max_length=200)
    detay = models.TextField(default="Gizli Görev")
    roket_adi = models.CharField(max_length=100)
    firlatma_tarihi = models.CharField(max_length=100)
    resim = models.URLField(blank=True, null=True)
    basari_durumu = models.BooleanField(default=True)
    youtube_link = models.URLField(blank=True, null=True)
    wikipedia_link = models.URLField(blank=True, null=True)
    firlatma_yeri = models.CharField(max_length=200, default="Bilinmiyor")

class Gezegen(models.Model): # Yeni Sınırsız Sistem
    isim = models.CharField(max_length=100)
    tur = models.CharField(max_length=100)
    resim = models.URLField()
    sicaklik = models.CharField(max_length=100, default="Bilinmiyor")
    yercekimi = models.CharField(max_length=100, default="Normal")
    ozellik = models.TextField(default="Çok gizemli bir gökcismi.")
    
    def __str__(self):
        return self.isim

# 3. ✂️ YARATICI ATÖLYE
class ElSanati(models.Model):
    isim = models.CharField(max_length=100)
    aciklama = models.TextField(help_text="Sanatın kısa tanımı")
    resim = models.URLField()
    malzemeler = models.CharField(max_length=200, default="Kağıt, Makas")
    zorluk = models.CharField(max_length=50, default="Kolay")

# 4. 🎨 SANAT
class SanatEseri(models.Model):
    baslik = models.CharField(max_length=200)
    sanatci = models.CharField(max_length=200)
    resim = models.URLField()
    tarih = models.CharField(max_length=100, blank=True)
    muze_linki = models.URLField(blank=True)

# 5. EĞLENCE & HAYVANLAR
class Hayvan(models.Model):
    TURLER = (('kedi', 'Kedi'), ('kopek', 'Köpek'))
    resim = models.URLField()
    tur = models.CharField(max_length=10, choices=TURLER)
    sevimli_puan = models.IntegerField(default=100)

class Saka(models.Model):
    soru = models.TextField()
    cevap = models.TextField()
    kategori = models.CharField(max_length=50, default="Genel")

class BilgiSorusu(models.Model):
    kategori = models.CharField(max_length=100)
    soru = models.TextField()
    dogru_cevap = models.CharField(max_length=200)
    zorluk = models.CharField(max_length=20)
    tip = models.CharField(max_length=20)

class Aktivite(models.Model):
    baslik = models.CharField(max_length=255)
    tur = models.CharField(max_length=50)
    katilimci_sayisi = models.IntegerField(default=1)
    fiyat_seviyesi = models.FloatField(default=0.0)

# 6. 🥣 LEZZETLİ MUTFAK
class YemekTarifi(models.Model):
    isim = models.CharField(max_length=200)
    resim = models.URLField()
    ozet = models.TextField(help_text="Kısa açıklama")
    malzemeler = models.TextField(default="Malzeme bilgisi yok.", help_text="Virgülle ayrılmış malzemeler")
    tarif_detay = models.TextField(default="Tarif hazırlanıyor...", help_text="Adım adım yapılışı")
    hazirlama_suresi = models.IntegerField(default=30)
    saglik_puani = models.IntegerField(default=80)
    kalori = models.FloatField(default=0)
    protein = models.CharField(max_length=50, default="0g")
    yag = models.CharField(max_length=50, default="0g")
    karbonhidrat = models.CharField(max_length=50, default="0g")
    seker = models.CharField(max_length=50, default="0g")

class Oyun(models.Model):
    baslik = models.CharField(max_length=200)
    resim = models.URLField(help_text="Kapak resmi")
    iframe_url = models.URLField(help_text="Oyunun çalışacağı link")
    kategori = models.CharField(max_length=50, default="Macera")
    
    def __str__(self):
        return self.baslik