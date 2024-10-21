#Autor: Lazar Krpovic 2021/0633
from django import forms
from .models import Oglas

class OglasForm(forms.ModelForm):

    VELICINA_CHOICES = [
        ('bebe', 'Bebe'),
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL')
    ]
    
    POL_CHOICES = [
        ('musko', 'Muškarci'),
        ('zensko', 'Žene'),
        ('decije', 'Deca')
    ]
    
    velicina = forms.ChoiceField(
        choices= VELICINA_CHOICES,
        widget=forms.Select(attrs={'id': 'velicina'})
    )

    pol = forms.ChoiceField(
        choices= POL_CHOICES,
        widget=forms.Select(attrs={'id': 'pol'})
    )
    tagovi = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Unesite tagove odvojene razmakom', 'style': 'width: 400px;'}))

    class Meta:
        model = Oglas
        fields = ['naziv', 'stanje', 'opis', 'pol', 'velicina', 'slika', 'tagovi']
        widgets = {
            
            'naziv': forms.TextInput(attrs={'id': 'naziv'}),
            'stanje': forms.NumberInput(attrs={'id': 'stanje', 'min': 1, 'max': 5}),
            
            'opis': forms.Textarea(attrs={'id': 'opis', 'rows': 4, 'cols': 50}),
            'slika': forms.ClearableFileInput(attrs={'id': 'slika'}),
        }
