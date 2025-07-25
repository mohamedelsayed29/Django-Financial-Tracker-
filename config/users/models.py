from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import identify_hasher , make_password
from polymorphic.models import PolymorphicModel



class CustomUserManager(BaseUserManager):
    USERNAME_REQUIRED_FIELDS = "The username field is required."
    STAFF_REQUIRED_FIELDS = "The staff field is required."
    SUPERUSER_REQUIRED_FIELDS = "The superuser field is required."

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(self.USERNAME_REQUIRED_FIELDS)
        
        user = self.model(username=username, **extra_fields )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self , username, password=None, **extra_fields ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(self.STAFF_REQUIRED_FIELDS)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(self.SUPERUSER_REQUIRED_FIELDS) 
        
        return self.create_user(username, password, **extra_fields)
    


class User(PolymorphicModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username' 
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if self.password:
            try:
              identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    

class CustomUser(User):
    email = models.EmailField(unique=True, blank=True, null=True)    
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]  # Set username from email
        super().save(*args, **kwargs)   

    def __str__(self):
        return self.username
     


class Otp(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='otp') 
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=4)

    class Meta: 
        indexes = [
            models.Index(fields=['customer', 'created_at']),
        ]


    def mark_otp_as_verified(self):
        self.is_verified = True
        self.expired_at = timezone.now()
        self.save(update_fields=['is_verified', 'expired_at'])     