# Generated by Django 2.1.5 on 2019-04-07 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zwitter', '0002_tweet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]