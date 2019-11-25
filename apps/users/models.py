from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="NickName", default="")
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("male","male"),("femaile", "female")), default="femaile")
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username

    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="VerifyCode")
    email = models.EmailField(max_length=50, verbose_name="Email")
    send_type = models.CharField(choices=(("r", "register"), ("f", "forgot"), ("update_email", "modify")), verbose_name="SendType", max_length=30)
    send_time = models.DateTimeField(verbose_name="SendTime", default=datetime.now)

    class Meta:
        verbose_name = "VerifyCode"
        verbose_name_plural = "VerifyCodes"

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="Banner", max_length=100)
    url = models.URLField(max_length=200, verbose_name="URL")
    index = models.IntegerField(default=100, verbose_name="Index")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="Addtime")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"