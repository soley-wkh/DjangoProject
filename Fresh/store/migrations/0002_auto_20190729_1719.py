# Generated by Django 2.2 on 2019-07-29 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='store_id',
            new_name='store',
        ),
    ]