# Generated by Django 3.2.5 on 2022-04-25 18:28

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=user.models.LowercaseEmailField(max_length=254, unique=True, verbose_name='Adresse email'),
        ),
    ]
