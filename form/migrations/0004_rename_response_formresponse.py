# Generated by Django 5.1.4 on 2024-12-16 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_rename_answer_response'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='FormResponse',
        ),
    ]
