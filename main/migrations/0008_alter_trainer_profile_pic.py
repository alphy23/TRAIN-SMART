# Generated by Django 4.2.6 on 2023-11-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_persontotrainer_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='static/img'),
        ),
    ]
