# Generated by Django 4.1 on 2022-08-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]