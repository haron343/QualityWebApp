# Generated by Django 4.2.1 on 2023-06-29 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-date'], 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
    ]