# Generated by Django 4.1.4 on 2022-12-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_banner_clothsize_clothattribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(null=True, upload_to='category_imgs/'),
        ),
    ]
