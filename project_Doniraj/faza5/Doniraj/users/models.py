#Autor: Matija Milic 2021/0088
from django.conf import settings
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError('Niste uneli email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pib = models.CharField(max_length=50)
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    needs_description = models.TextField()
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Zahtev(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()

    def __str__(self):
        return self.organization.name

class User (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True , default='')
    username = models.CharField(blank=True,default='',unique=True, max_length=50)
    image = models.ImageField(blank=True, default='profile_pics/profil.png', upload_to='profile_pics')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        try:
            this = User.objects.get(id=self.id)
            if this.image and self.image and this.image != self.image and this.image.name != 'profile_pics/profil.png':
                this.image.delete(save=False)
        except User.DoesNotExist:
            pass

        if not self.image:
            self.image = 'profile_pics/profil.png'
        
        super(User, self).save(*args, **kwargs)