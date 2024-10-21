#Autor: Matija Milic 2021/0088
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen
from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Organization

#Forma za registraciju obicnog korisnika
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
#Forma za registraciju ogranizacije
class OrganizationRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name',  'address', 'pib', 'website', 'description', 'needs_description']
    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website:
            parsed_url = urlparse(website)
            if not (parsed_url.scheme and parsed_url.netloc):
                raise forms.ValidationError("Enter a valid URL.")

            if not parsed_url.scheme:
                website = 'http://' + website

            try:
                
                with urlopen(website) as response:
                    pass  
            except URLError:
                raise forms.ValidationError("The URL does not seem to point to a valid website.")
        return website
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

#Forma za prijavu
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')
    email = forms.EmailField(label="Email", max_length=255, help_text='Required. Add a valid email address.')
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        fields = ['email', 'password'] 

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data
    

#Forma za promenu profilne slike
class ProfilePictureForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, initial=False, label='Clear current image')

    class Meta:
        model = User
        fields = ['image']

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        if self.cleaned_data.get('clear_image'):
            user.image = 'profile_pics/profil.png'
        user.save()
        return user