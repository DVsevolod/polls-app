# Generated by Django 2.2.10 on 2021-03-02 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0005_auto_20210302_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollmodel',
            name='date_start',
            field=models.DateField(auto_now_add=True),
        ),
    ]
