# Generated by Django 3.0.8 on 2021-02-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210219_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=models.FileField(blank=True, default='default.png', upload_to='docter_finder/images/'),
        ),
    ]
