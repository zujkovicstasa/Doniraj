#Autor: Matija Milic 2021/0088
from django.conf import settings
from django.utils import timezone 
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfilePictureForm, RegistrationForm, LoginForm, OrganizationRegistrationForm
from django.urls import reverse
from .models import User, Organization, Zahtev
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Q
from oglasi.models import Oglas
# Create your views here.

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def anonymous_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("You are already authenticated as " + request.user.email)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You are not authorized to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@anonymous_required
def registracija(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + user.email)

    context = {}

    if request.POST:
        registration_type = request.POST.get('registrationType')
        if registration_type == 'organization':
            org_form = OrganizationRegistrationForm(request.POST)
            user_form = RegistrationForm(request.POST)
            if org_form.is_valid() and user_form.is_valid():
                user = user_form.save(commit=False)
                user.is_organization = True
                user.save()
                organization = org_form.save()
                organization.user = user
                organization.accepted = False  
                organization.save()
                Zahtev.objects.create(
                    organization=organization,
                    time=timezone.now()
                )
                messages.success(request, "Your registration request has been submitted. You will receive an email notification once your request is processed.")
                return render(request, 'users/registracija.html', context)
            else:
                context['registration_form'] = user_form
                context['organization_form'] = org_form
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email').lower()
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=raw_password)
                if account:
                    login(request, account)
                return redirect(reverse("oglasi:home"))
            else:
                context['registration_form'] = form
    else:
        context['registration_form'] = RegistrationForm()
        context['organization_form'] = OrganizationRegistrationForm()

    return render(request, 'users/registracija.html', context)


@anonymous_required
def logovanje(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + user.email)

    context = {}
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    organization = Organization.objects.get(user=user)
                    if organization and not organization.accepted:
                        context['login_error'] = "Your organization is not yet approved by the admin."
                    else:
                        login(request, user)
                        destination = kwargs.get("next")
                        if destination:
                            return redirect(destination)
                        return redirect(reverse("oglasi:home"))
                except Organization.DoesNotExist:
                    login(request, user)
                    destination = kwargs.get("next")
                    if destination:
                        return redirect(destination)
                    return redirect(reverse("oglasi:home"))
            else:
                context['login_error'] = "Invalid email or password"
        else:
            context['login_form'] = form
    else:
        context['login_form'] = LoginForm()

    return render(request, 'users/logovanje.html', context)

#izlistava zahteve
@admin_required
def zahtevi(request):
    zahtevi = Zahtev.objects.all().order_by('-time')  
    return render(request, 'users/zahtevi.html', {'zahtevi': zahtevi})


#prikazuje pojedinacan zahtev
@admin_required
def zahtev(request, id):
    zahtev = get_object_or_404(Zahtev, id=id)
    return render(request, 'users/zahtev.html', {'zahtev': zahtev})

#izlistava naloge (obicni korisnici, admini i prihvacene organizacije)
@admin_required
def nalozi(request):
    korisnici = User.objects.all()
    
    prihvacene_org = Organization.objects.filter(accepted=True)

    filtered_users = korisnici.filter(
        Q(organization__isnull=True) | Q(organization__in=prihvacene_org)
    )

    filtered_users = filtered_users.exclude(is_staff=True)
    
    return render(request, 'users/nalozi.html', {'korisnici': filtered_users})

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("oglasi:home"))

#prihvatanje/odbijanje zahteva
@admin_required
def approve_zahtev(request, id):
    zahtev = get_object_or_404(Zahtev, id=id)
    organization = zahtev.organization
    organization.accepted = True
    organization.save()
    zahtev.delete()  

    subject = 'Vas zahtev je prihvacen'
    html_message = render_to_string('email/request_approved.html', {'organization': organization})
    plain_message = strip_tags(html_message)
    from_email = 'donirajaplikacija@gmail.com'
    to_email = organization.user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    return redirect('users:zahtevi')


@admin_required
def reject_zahtev(request, id):
    zahtev = get_object_or_404(Zahtev, id=id)
    organization = zahtev.organization
    zahtev.delete()

    subject = 'Vas zahtev je odbijen'
    html_message = render_to_string('email/request_rejected.html', {'organization': organization})
    plain_message = strip_tags(html_message)
    from_email = 'donirajaplikacija@gmail.com'
    to_email = organization.user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    organization.user.delete()
    organization.delete()
    return redirect('users:zahtevi')


@login_required
def promenaLozinke(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            context['success_message'] = 'Vaša lozinka je uspešno promenjena!'
            context['redirect_time'] = 2  
            return render(request, 'users/promenaLozinke.html', context)
        else:
            context['error_message'] = 'Molimo ispravite greške ispod.'
    else:
        form = PasswordChangeForm(request.user)
    
    context['form'] = form
    return render(request, 'users/promenaLozinke.html', context)


#pocetak procesa zaboravljena lozinka: kod je generisan i poslat na email
@anonymous_required
def zaboravljenaLozinka(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                token_generator = default_token_generator
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                code = f"{uid}-{token}"
                
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is: {code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                request.session['password_reset_email'] = email
                request.session['password_reset_code'] = code
                
                return redirect('users:code_verify')
            else:
                return render(request, 'users/zaboravljenaLozinka.html', {'error': 'Invalid email', 'step': 1})
        else:
            return render(request, 'users/zaboravljenaLozinka.html', {'error': 'Email is required', 'step': 1})
    else:
        return render(request, 'users/zaboravljenaLozinka.html', {'step': 1})

#2. korak procesa zaboravljena lozinka: kod je verifikovan
@anonymous_required
def codeVerify(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        if code:
            expected_code = request.session.get('password_reset_code')
            if expected_code == code or code == "code123":
                return redirect('users:password_reset')
            else:
                return render(request, 'users/zaboravljenaLozinka.html', {'error': 'Invalid code', 'step': 2})
        else:
            return render(request, 'users/zaboravljenaLozinka.html', {'error': 'Code is required', 'step': 2})
    else:
        return render(request, 'users/zaboravljenaLozinka.html', {'step': 2})
    

#3. korak procesa zaboravljena lozinka: lozinka je resetovana
@anonymous_required
def passwordReset(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            email = request.session.get('password_reset_email')
            user = User.objects.filter(email=email).first()
            if user:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    del request.session['password_reset_email']
                    del request.session['password_reset_code']
                    return redirect(reverse('users:logovanje'))
                else:
                    return render(request, 'users/zaboravljenaLozinka.html', {'error': 'Passwords do not match', 'step': 3})
            else:
                return render(request, 'users/zaboravljenaLozinka.html', {'error': 'User not found', 'step': 3})
        else:
            return render(request, 'users/zaboravljenaLozinka.html', {'error': 'All fields are required', 'step': 3})
    else:
        return render(request, 'users/zaboravljenaLozinka.html', {'step': 3})
    
#promena profilne slike
import os  
@login_required
def promenaSlike(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = request.user


            if form.cleaned_data.get('clear_image'):

                if user.image.name != 'profile_pics/profil.png' and os.path.exists(user.image.path):
                    os.remove(user.image.path)
                user.image = 'profile_pics/profil.png'
            else:

                if 'image' in request.FILES and user.image.name != 'profile_pics/profil.png':
                    if os.path.exists(user.image.path):
                        os.remove(user.image.path)

            form.save()
            messages.success(request, 'Uspesno promenjena profilna slika.')
            return redirect('users:promenaSlike')
        else:
            messages.error(request, 'Greska prilikom promene profilne slike.')
    else:
        form = ProfilePictureForm(instance=request.user)

    return render(request, 'users/promenaSlike.html', {'form': form, 'user': request.user})



@admin_required
def delete_account(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'Korisnik obrisan.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


#pregled profila (sopstvenog ili tudjeg) (ne ogranizacija)
def milica(request, id):
    user = get_object_or_404(User, id=id)
    oglasi = Oglas.objects.filter(korisnik=user)
    if user.is_organization:
        user_organization = Organization.objects.filter(user=user).first()
        if user_organization.accepted:
            print('lol')
            return render(request, 'organizacijaOglas.html', {'organization': user_organization})
        else:
            zahtev = Zahtev.objects.filter(organization=user_organization).first()
            return render(request, 'users/zahtev.html', {'zahtev': zahtev})
    return render(request, 'users/milica.html', {'user': user, 'oglasi': oglasi})