# Generated by Django 2.0.4 on 2018-04-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='postal_code',
            field=models.TextField(),
        ),
    ]
