from django.test import TestCase
from users.models import User
from users.models import Organization, Zahtev
from datetime import datetime

class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_organization)
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpassword')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)
        self.assertFalse(admin_user.is_organization)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='admin@example.com', password='adminpassword', is_superuser=False)

class OrganizationModelTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Test Organization', address='Test Address', pib='123456789', description='Test Description', needs_description='Test Needs Description')

    def test_organization_creation(self):
        self.assertEqual(self.organization.name, 'Test Organization')
        self.assertEqual(self.organization.address, 'Test Address')
        self.assertEqual(self.organization.pib, '123456789')
        self.assertEqual(self.organization.description, 'Test Description')
        self.assertEqual(self.organization.needs_description, 'Test Needs Description')

class ZahtevModelTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name='Test Organization', address='Test Address', pib='123456789', description='Test Description', needs_description='Test Needs Description')
        self.zahtev = Zahtev.objects.create(organization=self.organization, time=datetime.now())

    def test_zahtev_creation(self):
        self.assertEqual(self.zahtev.organization, self.organization)
