from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator

def index(request):
    # Ana sayfa (Dashboard)
    context = {
        # Artık Gezegen modelini kullanıyoruz (NASA yok)
        'son_uzay': Gezegen.objects.order_by('?').first(),
        'son_hayvan': Hayvan.objects.order_by('?').first(),
        'son_poke': Pokemon.objects.order_by('?').first(),
        'son_kahraman': ElSanati.objects.order_by('?').first(),
        'son_yemek': YemekTarifi.objects.order_by('?').first(),
        'son_saka': Saka.objects.order_by('?').first(),
    }
    return render(request, 'macera/index.html', context)

def uzay_sayfasi(request):
    context = {
        'gunun_gokcismi': Gezegen.objects.order_by('?').first(), 
        'gezegenler': Gezegen.objects.all(),
        'spacex_list': UzayGorevi.objects.order_by('firlatma_tarihi')[:4], 
    }
    return render(request, 'macera/uzay.html', context)

def hayvanlar_sayfasi(request):
    context = {
        'kediler': Hayvan.objects.filter(tur='kedi').order_by('-id')[:12],
        'kopekler': Hayvan.objects.filter(tur='kopek').order_by('-id')[:12],
    }
    return render(request, 'macera/hayvanlar.html', context)

def oyun_eglence_sayfasi(request):
    context = {
        'html5_oyunlar': Oyun.objects.all(),
        'pokemonlar': Pokemon.objects.order_by('-id')[:12],
        'sakalar': Saka.objects.order_by('-id')[:6],
        'sorular': BilgiSorusu.objects.order_by('-id')[:5],
        'aktiviteler': Aktivite.objects.order_by('-id')[:5],
    }
    return render(request, 'macera/oyunlar.html', context)

def kesif_sanat_sayfasi(request):
    elsanatlari = ElSanati.objects.order_by('-id')[:8]
    sanat_listesi = SanatEseri.objects.order_by('-id')
    paginator = Paginator(sanat_listesi, 9) 
    sayfa_numarasi = request.GET.get('page')
    sayfa_objesi = paginator.get_page(sayfa_numarasi)

    context = {
        'elsanatlari': elsanatlari,
        'page_obj': sayfa_objesi,
    }
    return render(request, 'macera/kesif.html', context)

def mutfak_sayfasi(request):
    context = {
        'yemekler': YemekTarifi.objects.order_by('-id')[:9]
    }
    return render(request, 'macera/mutfak.html', context)

def mutfak_detay(request, id):
    yemek = get_object_or_404(YemekTarifi, id=id)
    return render(request, 'macera/mutfak_detay.html', {'yemek': yemek})