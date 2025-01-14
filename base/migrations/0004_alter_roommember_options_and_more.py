# Generated by Django 5.1.2 on 2024-12-04 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_roommember_options_alter_roommember_insession_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roommember',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='roommember',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='insession',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='room_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='uid',
            field=models.CharField(max_length=1000),
        ),
    ]
