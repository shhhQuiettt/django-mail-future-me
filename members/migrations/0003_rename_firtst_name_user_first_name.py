# Generated by Django 4.1 on 2022-08-10 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firtst_name',
            new_name='first_name',
        ),
    ]