# Generated by Django 3.0.3 on 2020-03-22 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_remove_profile_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='users', verbose_name='Аватарка'),
        ),
    ]