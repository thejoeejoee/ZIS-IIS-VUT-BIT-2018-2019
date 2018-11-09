# Generated by Django 2.1.1 on 2018-11-06 17:29

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20181030_1653'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('last_name', 'first_name'), 'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AddField(
            model_name='typeanimal',
            name='icon',
            field=models.FilePathField(blank=True, null=True, path='/home/thejoeejoee/projects/ZIS-IIS-VUT-BIT-2017-2018/ziscz/web/static/img/icons/animals/'),
        ),
        migrations.AlterField(
            model_name='cleaning',
            name='date',
            field=models.DateTimeField(help_text='Planned start of cleaning.'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='color',
            field=colorful.fields.RGBColorField(blank=True, help_text='Describing color used in system UI as helper, black is default.', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='typeenclosure',
            name='color',
            field=colorful.fields.RGBColorField(blank=True, help_text='Describing color used for type of enclosure in system UI as helper, black is default.', null=True),
        ),
    ]
