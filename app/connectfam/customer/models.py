from django.db import models

from oscar.apps.customer.models import *  # noqa isort:skip
from oscar.apps.customer.abstract_models import AbstractUser


class User(AbstractUser):
    first_name_kana = models.CharField('First name katakana', max_length=255, blank=True)
    last_name_kana = models.CharField('Last name katakana', max_length=255, blank=True)

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()
