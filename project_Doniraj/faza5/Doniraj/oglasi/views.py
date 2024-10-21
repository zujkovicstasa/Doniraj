from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OglasForm
from .models import Oglas, Tag, Sadrzi
from django.contrib.auth.decorators import login_required
# Create your views here.
#Autor: Matija Milic 2021/0088 ,Lazar Krpovic 2021/0633

def fetch_oglases(request):
    if request.method == 'GET':
        oglasi = Oglas.objects.all()
        oglasi_list = [
            {
                'id': oglas.id,
                'naziv': oglas.naziv,
                'opis': oglas.opis,
                'slika_url': request.build_absolute_uri(oglas.slika.url)  # Construct the full URL for the image
            } for oglas in oglasi
        ]
        return JsonResponse({'oglasi': oglasi_list})


def pocetna(request):
    oglasi = Oglas.objects.all()
    return render(request, 'oglasi/pocetna.html', {'oglasi': oglasi})

def oglas(request, oglas_id):
    oglas = get_object_or_404(Oglas, pk=oglas_id)
    return render(request, 'oglasi/oglas.html', {'oglas': oglas})


def postaviOglas(request):
    if request.method == "POST":
        form = OglasForm(request.POST, request.FILES)
        if form.is_valid():
            oglas = form.save(commit=False)
            oglas.korisnik = request.user  
            oglas.save()
            
            tags_str = form.cleaned_data['tagovi']
            tags_list = [tag.strip() for tag in tags_str.split(' ')]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(tag=tag_name)
                Sadrzi.objects.create(oglas=oglas, tag=tag)
            
            return redirect('oglasi:home')  
    else:
        form = OglasForm()
    
    return render(request, 'oglasi/postaviOglas.html', {'form': form})

#AJAX poziv za pretragu kada se submituje search forma
def search(request):
    query = request.GET.get('q', '')
    words = query.split()
    velicina = request.GET.get('velicina', '')
    pol = request.GET.get('pol', '')

    oglasi = Oglas.objects.all()

    if velicina != 'null':
        oglasi = oglasi.filter(velicina=velicina)
    if pol != 'null':
        oglasi = oglasi.filter(pol=pol)

    if query:
        for word in words:
            oglasi_by_name = oglasi.filter(naziv__icontains=word)
            oglasi_by_tag = oglasi.filter(tagovi__tag__icontains=word)
            oglasi = (oglasi_by_name | oglasi_by_tag).distinct()

    oglasi_list = [
        {
            'id': oglas.id,
            'naziv': oglas.naziv,
            'opis': oglas.opis,
            'slika_url': oglas.slika.url
        }
        for oglas in oglasi
    ]
    return JsonResponse({'oglasi': oglasi_list})


def deleteOglas(request, oglas_id):
    if request.method == 'POST':
        oglas = get_object_or_404(Oglas, id=oglas_id)
        nizSadrzi = Sadrzi.objects.filter(oglas = oglas)
        tagovi = [sadrzi.tag for sadrzi in nizSadrzi]
        oglas.delete()
       
        for tag in tagovi:
            SadrziNiz = Sadrzi.objects.filter(tag = tag)
            if not SadrziNiz:
                tag.delete()


        return JsonResponse({'status': 'success', 'message': 'Oglas obrisan.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

    