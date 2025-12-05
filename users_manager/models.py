from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', "ADMIN")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Основной пользователь системы.
    Расширяет стандартного пользователя Django (email, пароль, и т.п.)
    """
    ROLE_CHOISES = [
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("USER", "User")
    ]

    id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(
        max_length=50,
        unique=True,
        help_text="Обязательное поле. До 50 символов. Буквы, цифры и @/./+/-/_ символы.",
        error_messages={
            "unique": "Заданное имя пользователя уже существует.",
        },
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOISES,
        blank=False,
        default="USER"
    )
    
    is_staff = models.BooleanField("Сотрудник", default=False)
    is_superuser = models.BooleanField("Администратор", default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
