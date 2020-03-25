# Generated by Django 3.0.3 on 2020-03-20 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_profile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='username',
        ),
        migrations.AddField(
            model_name='profile',
            name='posts',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='User.posts'),
        ),
    ]