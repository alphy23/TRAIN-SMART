# Generated by Django 4.2.6 on 2023-11-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_bmidata_bmi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('profile_pic', models.ImageField(default='', upload_to='main/uploads')),
            ],
        ),
    ]
