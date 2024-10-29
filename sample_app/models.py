from django.db import models
from django.utils import timezone

class NonoData(models.Model):
    data_key = models.CharField('data_key', max_length=255)
    data_value = models.CharField('data_value', max_length=255)
    update_date = models.DateTimeField('update_date', auto_now=True)

    def __str__(self):
        return '<id:' + str(self.id) + ',' + self.data_key + ',' + self.data_value + '>'
