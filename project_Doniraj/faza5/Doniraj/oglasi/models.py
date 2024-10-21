from django.db import models

# Create your models here.

from users.models import User
#Autor: Lazar Krpovic 2021/0633

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Oglas(models.Model):
    POL_CHOICES = (
        ('musko' , 'musko'),
        ('zensko' , 'zensko'),
        ('decije', 'decije'),
    )
    VELICINA_CHOICES = (
        ('bebe' , 'bebe'),
        ('xs' , 'XS'),
        ('s' , 'S'),
        ('m' , 'M'),
        ('l' , 'L'),
        ('xl' , 'XL'),
        ('xxl' , 'XXL'),

    )
    

    naziv = models.CharField(max_length=255)
    stanje = models.IntegerField()
    opis = models.TextField()
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    pol = models.CharField(max_length=6, choices=POL_CHOICES)
    velicina = models.CharField(max_length=5, choices = VELICINA_CHOICES)
    vreme = models.DateTimeField(auto_now_add=True)
    slika = models.ImageField(upload_to='oglasi/')
    tagovi = models.ManyToManyField(Tag, through='Sadrzi')

    def __str__(self):
        return self.naziv

class Sadrzi(models.Model):
    oglas = models.ForeignKey(Oglas, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.oglas.naziv} - {self.tag.tag}"