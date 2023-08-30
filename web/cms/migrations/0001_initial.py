# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2020-06-10 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomHTMLContent',
            fields=[
                ('token', models.CharField(help_text='Format: Page HTML - Bloc', max_length=50, primary_key=True, serialize=False, unique=True, verbose_name="Token d'identification")),
            ],
            options={
                'verbose_name': 'Contenu HTML',
                'verbose_name_plural': 'Contenus HTML',
                'permissions': [('edit', 'Can edit content')],
            },
        ),
    ]
