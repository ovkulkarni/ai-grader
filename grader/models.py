from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager


import os

# Create your models here.


class UserManager(DjangoUserManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Lab(models.Model):
    name = models.CharField(max_length=256)
    grader_filename = models.CharField(max_length=256)
    short_description = models.CharField(max_length=4096)
    detailed_description = models.TextField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.short_description)


def upload_directory(instance, filename=None):
    return os.path.join(settings.UPLOAD_DIRECTORY,
                        slugify(instance.lab.name),
                        "{}-{}.py".format(
                            instance.upload_time.strftime("%Y-%m-%d-%H-%M-%S"),
                            instance.user.username))


class Submission(models.Model):
    lab = models.ForeignKey('Lab', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    code = models.FileField(upload_to=upload_directory)
    output = models.CharField(max_length=4096 * 16)

    def __str__(self):
        return "Submission for {} at {} by {}".format(self.lab,
                                                      self.upload_time,
                                                      self.user)


@receiver(models.signals.post_delete, sender=Submission)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.code:
        if os.path.isfile(instance.code.path):
            os.remove(instance.code.path)
