from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    """Custom User Manager Definition"""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given email, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_admin_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, type="관리자", **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            username, password, status=User.UserStatusChoice.admin, **extra_fields
        )

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    """Custom User Model Definition"""

    class UserStatusChoice(models.TextChoices):
        active = ("활성유저", "활성유저")  # 정상
        admin = ("관리자", "관리자")  # 관리자
        withdraw = ("탈퇴유저", "탈퇴유저")  # 탈퇴

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="아이디",
    )
    email = models.EmailField(
        max_length=50,
        null=True,
        blank=True,
        help_text="이메일",
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # change this related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # change this related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    status = models.CharField(
        max_length=10,
        choices=UserStatusChoice.choices,
        default=UserStatusChoice.active,
        help_text="회원 유형",
    )


class Jwt(models.Model):
    user = models.OneToOneField(
        User, related_name="login_user", on_delete=models.CASCADE, help_text="회원"
    )
    access = models.TextField(help_text="Access Token")
    refresh = models.TextField(help_text="Refresh Token")
