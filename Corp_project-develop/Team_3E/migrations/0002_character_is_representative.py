# Generated by Django 5.1 on 2024-09-27 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team_3E', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='is_representative',
            field=models.BooleanField(default=False),
        ),
    ]
