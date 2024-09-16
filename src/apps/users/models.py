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


class UserRoles(models.Model):
    organizer = "organizer"
    guide = "guide"
    attendee = "attendee"

    ROLE_CHOICE = (
        (organizer, _("Organizer")),
        (guide, _("Guide")),
        (attendee, _("Attendee")),
    )


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ORGANIZER = "organizer", _("Organizer")
        GUIDE = "guide", _("Guide")
        ATTENDEE = "attendee", _("Attendee")

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.ManyToManyField(UserRoles)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    base_role = Role.ORGANIZER

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.role = self.base_role

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.username)


class OrganizerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(role=User.Role.ORGANIZER)


class Organizer(User):
    base_role = User.Role.ORGANIZER

    objects = OrganizerManager()

    class Meta:
        proxy = True


class GuideManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(role=User.Role.GUIDE)


class Guide(User):
    base_role = User.Role.GUIDE

    objects = GuideManager()

    class Meta:
        proxy = True


class AttendeeManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(role=User.Role.ATTENDEE)


class Attendee(User):
    base_role = User.Role.ATTENDEE

    objects = AttendeeManager()

    class Meta:
        proxy = True
