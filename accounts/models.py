from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Creating Custom user model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



# Custom user Manager
class UserManager(BaseUserManager):
    """
    In charge of managing the custom user model
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Args:
            - email : user login email
            - password : user password
            - **extra_fields: dictionnary containing extrafields ('is_staff', 'is_active'..)
        Returns:
            created user
        """
        if not email:
            raise ValueError(_('Email is compulsory'))
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Args:
            - extra_fields: the additionnal fields ('is_superuser'..)
        Returns :
            - Created user
        """
        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('\'is_staff\' must be = True'))

        if not extra_fields.get('is_superuser'):
            raise ValueError(_('\'is_superuser\' must be = True'))
        
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    """
    The custom user model.
    - Defines email as USERNAME_FIELD
    """

    email = models.EmailField(_('Email'), unique=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    first_name = models.CharField(_('First name'), max_length=255, blank=True)

    is_active = models.BooleanField(_('Account activated'), default=True, help_text=_("" \
    "Defines wether the user's accounts can be use or not (a temporal delection control)"))

    is_staff = models.BooleanField(_('Member of the staff'), default=False)
    
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Profile(models.Model):
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    bio = models.TextField(_('Bio'), max_length=600, blank=True)
    picture = models.ImageField(_('Profile'), upload_to='media/profiles', blank=True)


    def __str__(self):
        return self.user.email
