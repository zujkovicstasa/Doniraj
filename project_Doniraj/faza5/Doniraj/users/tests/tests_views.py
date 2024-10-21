from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone
from users.models import User, Organization, Zahtev
from users.views import admin_required, anonymous_required, login_required
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser

class ViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password',
            is_staff=True
        )
        self.non_admin_user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='password',
            is_staff=False
        )
        self.normal_non_admin_user = User.objects.create_user(
            email='normaluser@example.com',
            username='normaluser',
            password='normalpassword',
            is_staff=False
        )
        self.organization = Organization.objects.create(
            name="Test Org",
            address="123 Street",
            pib="123456",
            website="http://example.com",
            description="Test Description",
            needs_description="Test Needs",
            user=self.non_admin_user,
        )
        self.zahtev = Zahtev.objects.create(
            organization=self.organization,
            time=timezone.now()
        )

    def test_admin_required_decorator(self):
        request = self.factory.get('/some-url/')
        request.user = self.admin_user
        response = admin_required(lambda req: HttpResponse("OK"))(request)
        self.assertEqual(response.status_code, 200)

        request.user = self.non_admin_user
        response = admin_required(lambda req: HttpResponse("OK"))(request)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_required_decorator(self):
        request = self.factory.get('/some-url/')
        request.user = self.non_admin_user
        response = anonymous_required(lambda req: HttpResponse("OK"))(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("You are already authenticated as", response.content.decode())

    def test_login_required_decorator(self):
        request = self.factory.get('/some-url/')
        request.user = self.non_admin_user
        response = login_required(lambda req: HttpResponse("OK"))(request)
        self.assertEqual(response.status_code, 200)

        request.user = AnonymousUser()
        response = login_required(lambda req: HttpResponse("OK"))(request)
        self.assertEqual(response.status_code, 403)

    def test_registracija_view(self):
        response = self.client.post(reverse('users:registracija'), {'username': 'testuser', 'password1': 'testpass', 'password2': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registracija.html')

        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'password',
            'password2': 'password',
        }
        response = self.client.post(reverse('users:registracija'), data)
        self.assertEqual(response.status_code, 200)

    def test_logovanje_view(self):
        
        user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        
        response = self.client.post(reverse('users:logovanje'), {'email': 'user2@example.com', 'password': 'password2'})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('oglasi:home'))

    def test_zahtevi_view(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('users:zahtevi'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/zahtevi.html')

    def test_zahtev_view(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('users:zahtev', args=[self.zahtev.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/zahtev.html')

    def test_nalozi_view(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('users:nalozi'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/nalozi.html')

    def test_logout_view(self):
        self.client.login(email='user@example.com', password='password')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('oglasi:home'))

    def test_approve_zahtev_view(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.post(reverse('users:approve_zahtev', args=[self.zahtev.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:zahtevi'))

    def test_reject_zahtev_view(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.post(reverse('users:reject_zahtev', args=[self.zahtev.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:zahtevi'))

    def test_promenaLozinke_view(self):
        self.client.login(email='user@example.com', password='password')
        response = self.client.get(reverse('users:promenaLozinke'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/promenaLozinke.html')

    def test_zaboravljenaLozinka_view(self):
        response = self.client.get(reverse('users:zaboravljenaLozinka'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/zaboravljenaLozinka.html')

        data = {'email': self.non_admin_user.email}
        response = self.client.post(reverse('users:zaboravljenaLozinka'), data)
        self.assertEqual(response.status_code, 302)

    def test_codeVerify_view(self):
        session = self.client.session
        session['password_reset_code'] = 'test-code'
        session.save()

        response = self.client.get(reverse('users:code_verify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/zaboravljenaLozinka.html')

        data = {'code': 'test-code'}
        response = self.client.post(reverse('users:code_verify'), data)
        self.assertEqual(response.status_code, 302)

    def test_passwordReset_view(self):
        session = self.client.session
        session['password_reset_email'] = self.non_admin_user.email
        session['password_reset_code'] = 'test-code'
        session.save()

        response = self.client.get(reverse('users:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/zaboravljenaLozinka.html')

        data = {
            'new_password': 'newpassword',
            'confirm_password': 'newpassword',
        }
        response = self.client.post(reverse('users:password_reset'), data)
        self.assertEqual(response.status_code, 302)

    def test_promenaSlike_view(self):
        self.client.login(email='user@example.com', password='password')
        response = self.client.get(reverse('users:promenaSlike'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/promenaSlike.html')

    def test_delete_account_view(self):
        self.client.login(email='admin@example.com', password='password',)
        response = self.client.post(reverse('users:delete_account',kwargs={'user_id': self.normal_non_admin_user.id}))
        self.assertEqual(response.status_code, 200)

    def test_milica_view(self):
        response = self.client.get(reverse('users:milica', args=[self.non_admin_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/milica.html')
