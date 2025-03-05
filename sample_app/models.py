from django.db import models
from django.utils import timezone

class NonoData(models.Model):
    data_key = models.CharField('キー', max_length=255, help_text='データのキーを入力してください')
    data_value = models.CharField('値', max_length=255, help_text='データの値を入力してください')
    date = models.DateField('日付', null=True, blank=True, default=timezone.now, help_text='このデータに関連付ける日付')
    update_date = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'Nonoデータ'
        verbose_name_plural = 'Nonoデータ'

    def __str__(self):
        return f'<id:{self.id}, key:{self.data_key}, value:{self.data_value}, date:{self.date}>'
