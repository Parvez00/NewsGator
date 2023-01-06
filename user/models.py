from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users Must have an email address.")
        if not username:
            raise ValueError("Users Must have an username.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class NewsPreference(models.Model):
    user_id = models.IntegerField(null=False)
    news_preference = models.TextField(null=False, max_length=1000)
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(verbose_name="added at",auto_now_add=True)

    REQUIRED_FIELDS = ['user_id','news_preference']

    def __str__(self):
        return self.user_id


class NewsDomain(models.Model):
    domain_name = models.CharField(null=False, max_length=255)
    domain_source = models.TextField(null=False, max_length=1000)
    domain_link = models.TextField(null=False, max_length=1000)
    domain_image = models.TextField(null=False, max_length=1000)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['domain_name','domain_source','domain_link']

    def __str__(self):
        return self.domain_name