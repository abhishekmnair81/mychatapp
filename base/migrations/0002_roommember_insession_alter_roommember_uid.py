# Generated by Django 5.1.2 on 2024-12-04 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommember',
            name='insession',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='uid',
            field=models.CharField(max_length=1000),
        ),
    ]