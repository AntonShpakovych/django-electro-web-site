# Generated by Django 3.2.7 on 2021-10-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0004_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]