from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db.models import EmailField, CharField, BooleanField, DateTimeField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, name=None, fullname=None, is_active=True, is_stuff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("User must has email")
        if not password:
            raise ValueError("User must enter password")
        email = self.normalize_email(email)

        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_stuff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self._create_user(email, name=name, password=password, is_stuff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self._create_user(email, name=name, password=password, is_stuff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    name = CharField(max_length=255, blank=True, null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        return self.email

    def get_full_name(self):
        if self.name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        print(self.password)
        if not all((self.id, self.staff, self.admin)):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

