# Generated by Django 5.1.1 on 2025-01-10 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonodata',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='date'),
        ),
    ]
