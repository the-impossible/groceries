# My Django imports
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# My app imports

# Create your models here.
class AccountsManager(BaseUserManager):
    def create_user(self, email, fullname, phone, password=None):

        #creates a user with the parameters
        if not email:
            raise ValueError('Email Address required!')

        if fullname is None:
            raise ValueError('Fullname is required!')

        if not phone:
            raise ValueError('Phone Number is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname.title().strip(),
            phone = phone.strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, fullname, phone, password):
        # create a superuser with the above parameters
        if not email:
            raise ValueError('Email Address is required!')

        if fullname is None:
            raise ValueError('Fullname is required!')

        if phone is None:
            raise ValueError('Phone number is required!')

        if password is None:
            raise ValueError('Password should not be empty')

        user = self.create_user(
            email=self.normalize_email(email),
            fullname=fullname.title().strip(),
            phone = phone.strip(),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class Accounts(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=30, db_index=True)
    email = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='email address', blank=True)
    phone = models.CharField(max_length=14, db_index=True, unique=True, blank=True)
    picture = models.ImageField(default='user.png', upload_to='uploads/', null=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['fullname', 'phone']

    objects = AccountsManager()

    def get_name(self):
        return self.fullname

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

    class Meta:
        db_table = 'Accounts'
        verbose_name_plural = 'Accounts'