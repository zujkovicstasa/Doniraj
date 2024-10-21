from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from oglasi.models import Oglas, Tag, Sadrzi
from oglasi.forms import OglasForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from PIL import Image
import io

class OglasViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user.save()
        self.tag = Tag.objects.create(tag="TestTag")
        self.oglas = Oglas.objects.create(
            naziv="Test Oglas",
            stanje=1,
            opis="Test opis",
            korisnik=self.user,
            pol='musko',
            velicina='M',
            vreme=timezone.now(),
            slika=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.oglas.tagovi.add(self.tag)

    def test_pocetna_view(self):
        response = self.client.get(reverse('oglasi:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oglasi/pocetna.html')
        self.assertContains(response, 'Test Oglas')

    def test_oglas_view(self):
        response = self.client.get(reverse('oglasi:oglas', args=[self.oglas.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oglasi/oglas.html')
        self.assertContains(response, 'Test opis')

    def test_postaviOglas_view_get(self):
        self.client.login(email='user1@example.com', password='password1')
        response = self.client.get(reverse('oglasi:postaviOglas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oglasi/postaviOglas.html')

    def test_postaviOglas_view_post(self):
        self.client.login(email='user1@example.com', password='password1')

        
        # Create a valid in-memory image
        image = io.BytesIO()
        Image.new('RGB', (100, 100)).save(image, format='JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('test_image.jpg', image.read(), content_type='image/jpeg')

        response = self.client.post(reverse('oglasi:postaviOglas'), {
            'naziv': 'New Oglas',
            'stanje': 2,
            'opis': 'New opis',
            'pol': 'zensko',
            'velicina': 's',
            'slika': image_file,
            'tagovi': 'newtag'
        })

        # Debug: Print form errors if the response code is not 302
        if response.status_code != 302:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(Oglas.objects.filter(naziv='New Oglas').exists())
        self.assertTrue(Tag.objects.filter(tag='newtag').exists())

    def test_search_view(self):
        response = self.client.get(reverse('oglasi:search'), {'q': 'Test', 'velicina': 'M', 'pol': 'musko'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['oglasi'][0]['naziv'], 'Test Oglas')

    def test_deleteOglas_view_post(self):
        self.client.login(email='user1@example.com', password='password1')
        response = self.client.post(reverse('oglasi:deleteOglas', args=[self.oglas.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertFalse(Oglas.objects.filter(id=self.oglas.id).exists())

    def test_deleteOglas_view_invalid_method(self):
        response = self.client.get(reverse('oglasi:deleteOglas', args=[self.oglas.id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

   