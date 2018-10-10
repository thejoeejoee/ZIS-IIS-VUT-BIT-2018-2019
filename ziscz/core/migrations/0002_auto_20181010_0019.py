# Generated by Django 2.1.1 on 2018-10-10 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='animalperson',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='animalregion',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='animalstay',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='cleaningperson',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='enclosure',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='enclosureperson',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='feeding',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='feedinganimal',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typeanimal',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typecleaningaccessory',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typecountry',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typeenclosure',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typeenclosuretypecleaningaccessory',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typefeed',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typeregion',
            old_name='x_updated',
            new_name='x_modified',
        ),
        migrations.RenameField(
            model_name='typerole',
            old_name='x_updated',
            new_name='x_modified',
        ),
    ]