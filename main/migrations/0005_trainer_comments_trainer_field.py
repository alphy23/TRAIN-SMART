# Generated by Django 4.2.6 on 2023-11-04 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='comments',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='trainer',
            name='field',
            field=models.CharField(default='', max_length=200),
        ),
    ]
