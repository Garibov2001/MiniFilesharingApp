# Generated by Django 3.1.3 on 2021-02-04 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_sharing', '0003_filesharing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filesharing',
            name='date_posted',
        ),
        migrations.AlterField(
            model_name='filesharing',
            name='permission',
            field=models.IntegerField(choices=[(0, 'Read Only'), (1, 'Read and Comment')], default=1),
        ),
    ]
