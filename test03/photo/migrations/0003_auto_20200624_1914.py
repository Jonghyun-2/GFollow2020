# Generated by Django 3.0.3 on 2020-06-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20200623_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(default='photos/no_image.png', upload_to='./photos'),
        ),
    ]
