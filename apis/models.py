#from asyncio.windows_events import NULL
from email.policy import default
from django.db.models.deletion import CASCADE
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User ,AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class User(AbstractUser) :
    username = None
    is_Patient = models.BooleanField(default = False)
    is_Nurse = models.BooleanField(default = False)
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    otp = models.CharField(max_length=200 , null=True , blank=True)
    is_verified = models.BooleanField(default=False)
   # iiiii = models.CharField(max_length= 555)

    objects = CustomUserManager() 


    def __str__(self):
        return self.email



class Patient(models.Model):
    user = models.OneToOneField(User , related_name ="Patient", on_delete = models.CASCADE)

    name = models.CharField(max_length=100)
    mobile = models.IntegerField (default = 0)
    city = models.CharField(max_length =100)
    birthdate = models.DateField(null = True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES  ,null= True)
    def __str__(self):
        return self.user.email



class Nurse(models.Model):
    #name = models.CharField(max_length=100)
    user = models.OneToOneField(User , related_name ="Nurse" , on_delete = models.CASCADE,default=None)
    mobile = models.IntegerField(default = 0)
    city = models.CharField(max_length =100)
    birthdate = models.DateTimeField(null = True)

    def __str__(self):
        return self.user.username


class Reservation(models.Model):
    patient = models.ForeignKey(Patient,  on_delete=models.CASCADE)
    nurse =  models.ForeignKey (Nurse,  on_delete=models.CASCADE)
    date = models.DateField(auto_now=True,blank=True)

    def __str__(self):
        return str(self.date)

'''
@receiver(post_save , sender = settings.AUTH_USER_MODEL)
def create_token(sender ,instance = None , created = False ,  **kwargs ):
    if created :
        Token.objects.create(user = instance)
'''

# def create_object(sender , **kwargs ):
#     if kwargs['created'] and kwargs['instance'].is_Nurse :
#         nurse = Nurse.objects.create(user = kwargs['instance'])

#     elif kwargs['created'] and kwargs['instance'].is_Patient :
#         patient = Patient.objects.create(user = kwargs['instance'])


# post_save.connect(create_object , sender = User)



