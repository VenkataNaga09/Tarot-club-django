from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
#from subjects.serializers import TAROT_CARDS

# Create your models here.

class SubjectProfileManager(BaseUserManager):
    """Manager for subject profiles"""

    def create_subject(self, email, name, password=None):
        """Create a new subject profile"""
        if not email:
            raise ValueError('Subjects must have an email address')
        email = self.normalize_email(email)
        subject = self.model(email=email, name=name)

        subject.set_password(password)
        subject.save(using=self._db)

        return subject

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        subject = self.create_subject(email, name, password)

        subject.is_superuser = True
        subject.is_staff = True
        subject.save(using=self._db)

        return subject

class SubjectProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for subjects in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    tarot_card_name = models.CharField(max_length=255,unique=True, default='The Fool')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SubjectProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of subject"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of subject"""
        return self.name

    def __str__(self):
        """Return string representation of the subject"""
        return f"{self.email} - {self.tarot_card_name}"


class ProfileFeedItem(models.Model):
     """Profile status update"""
     subject_profile = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE
     )
     content = models.CharField(max_length=255)
     created_on = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         """Return the model as a string"""
         return self.content