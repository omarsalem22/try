# Generated by Django 4.1 on 2022-09-12 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_forbiddenwords_delete_badword'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
    ]
