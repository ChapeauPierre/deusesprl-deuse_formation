# Generated by Django 3.2.5 on 2023-08-28 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20230825_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=10),
        ),
    ]
