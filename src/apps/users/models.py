from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, username: str, password: str | None = None, **other_fields
    ):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        return user

    def create_superuser(
        self, email: str, username: str, password: str, **other_fields
    ):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True"))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be assigned to is_superuser=True"))

        self.create_user(email, username, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ORGANIZER = "organizer", _("Organizer")
        GUIDE = "guide", _("Guide")
        ATTENDEE = "attendee", _("Attendee")

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    role = models.CharField(max_length=40, choices=Role.choices, default=Role.ATTENDEE)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return str(self.username)
