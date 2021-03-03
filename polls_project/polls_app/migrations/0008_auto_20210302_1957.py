# Generated by Django 2.2.10 on 2021-03-02 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0007_auto_20210302_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollmodel',
            name='questions',
        ),
        migrations.AddField(
            model_name='pollmodel',
            name='questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls_app.QuestionModel'),
        ),
    ]
