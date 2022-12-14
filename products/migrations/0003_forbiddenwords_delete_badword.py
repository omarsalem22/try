# Generated by Django 4.1 on 2022-09-11 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_badword_catecory_comment_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForbiddenWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forbidden_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='BadWord',
        ),
    ]
