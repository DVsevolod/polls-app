# Generated by Django 2.2.10 on 2021-03-02 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0004_auto_20210302_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollmodel',
            name='questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls_app.QuestionModel'),
        ),
    ]