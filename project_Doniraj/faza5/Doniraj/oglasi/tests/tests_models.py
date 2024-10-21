from django.test import TestCase
from oglasi.models import Tag, Oglas, Sadrzi
from users.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(tag="TestTag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.tag, "TestTag")

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), "TestTag")


class OglasModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password")
        self.tag1 = Tag.objects.create(tag="Tag1")
        self.tag2 = Tag.objects.create(tag="Tag2")
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
        self.oglas.tagovi.add(self.tag1, self.tag2)

    def test_oglas_creation(self):
        self.assertEqual(self.oglas.naziv, "Test Oglas")
        self.assertEqual(self.oglas.stanje, 1)
        self.assertEqual(self.oglas.opis, "Test opis")
        self.assertEqual(self.oglas.korisnik, self.user)
        self.assertEqual(self.oglas.pol, 'musko')
        self.assertEqual(self.oglas.velicina, 'M')
        self.assertTrue(self.oglas.vreme)
        self.assertTrue(self.oglas.slika)

    def test_oglas_str_method(self):
        self.assertEqual(str(self.oglas), "Test Oglas")

    def test_oglas_tags(self):
        self.assertEqual(self.oglas.tagovi.count(), 2)
        self.assertIn(self.tag1, self.oglas.tagovi.all())
        self.assertIn(self.tag2, self.oglas.tagovi.all())


class SadrziModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password")
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
        self.sadrzi = Sadrzi.objects.create(oglas=self.oglas, tag=self.tag)

    def test_sadrzi_creation(self):
        self.assertEqual(self.sadrzi.oglas, self.oglas)
        self.assertEqual(self.sadrzi.tag, self.tag)

    def test_sadrzi_str_method(self):
        self.assertEqual(str(self.sadrzi), "Test Oglas - TestTag")
