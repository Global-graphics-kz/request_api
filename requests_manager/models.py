import os
import datetime

from django.db import models
from django.conf import settings
from users_manager.models import User

# Create your models here.

def file_upload_path(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, f'{instance.user.id}/{filename}')

class Request(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Не подписан"),
        ("ACTIVE", "Подписан"),
        ("CANCELLED", "Расторгнут"),
    ]

    PRIORITY_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3")
    ]

    id = models.AutoField(primary_key=True, editable=False, help_text="", verbose_name="Номер заявки")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests", help_text="", verbose_name="Пользователь")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="DRAFT", help_text="", verbose_name="Статус")
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=3, verbose_name="Приоритет")
    file = models.FileField(upload_to=file_upload_path, null=True, blank=True, help_text="", verbose_name="Файлы заявки")
    start_date = models.DateField(help_text="", default=datetime.date.today, verbose_name="Дата вступления в силу")
    end_date = models.DateField(help_text="", blank=True, null=True, verbose_name="Дата расторжения")
    created_at = models.DateTimeField(auto_now_add=True, help_text="", verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="", verbose_name="Дата изменения")

    class Meta:
        db_table = "requests"
        constraints = []
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        
    def __str__(self):
        return 'Заявка под номером %s у %s' % (self.id, self.user)
    
class RequestComment(models.Model):
    id = models.AutoField(primary_key=True, editable=False, help_text="", verbose_name="Номер заявки")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_comments", help_text="", verbose_name="Заявка")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", help_text="", verbose_name="Пользователь")
    content = models.CharField(max_length=256, blank=False, verbose_name="Комментарий")
    start_date = models.DateField(help_text="", default=datetime.date.today, verbose_name="Дата вступления в силу")
    end_date = models.DateField(help_text="", blank=True, null=True, verbose_name="Дата расторжения")
    created_at = models.DateTimeField(auto_now_add=True, help_text="", verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="", verbose_name="Дата изменения")

    class Meta:
        db_table = "request_comments"
        constraints = []
        verbose_name = "Коментарий к заявке"
        verbose_name_plural = "Коментарии к заявке"
        
    def __str__(self):
        return 'Комментарий для %s под номером %s' % (self.request, self.id)
    