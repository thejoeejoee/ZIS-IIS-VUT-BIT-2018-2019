# Generated by Django 2.1.1 on 2018-11-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20181109_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeding',
            name='amount',
            field=models.CharField(default='', help_text='Amount of feed, etc. 1 kg, 1 l or 20 pieces.', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_animals',
            field=models.ManyToManyField(help_text='Type animals that is qualified to feed.', through='core.PersonTypeAnimal', to='core.TypeAnimal'),
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_enclosures',
            field=models.ManyToManyField(help_text='Type enclosures that is qualified to clean.', through='core.PersonTypeEnclosure', to='core.TypeEnclosure'),
        ),
    ]
