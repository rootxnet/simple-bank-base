from django.contrib.auth.models import AbstractUser

from contrib.models import BaseModel


class User(AbstractUser, BaseModel):
    pass
