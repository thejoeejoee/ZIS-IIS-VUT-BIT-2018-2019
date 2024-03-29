# Generated by Django 2.1.1 on 2018-11-25 11:36

import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20181122_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalregion',
            options={'verbose_name': 'Animal region', 'verbose_name_plural': 'Animal regions'},
        ),
        migrations.AlterModelOptions(
            name='animalstay',
            options={'ordering': ('date_from',), 'verbose_name': 'Animal stay', 'verbose_name_plural': 'Animal stays'},
        ),
        migrations.AlterModelOptions(
            name='cleaning',
            options={'ordering': ('date',), 'permissions': (('mark_as_done', 'Mark as done'),)},
        ),
        migrations.AlterModelOptions(
            name='feeding',
            options={'ordering': ('date',), 'permissions': (('mark_as_done', 'Mark as done'),)},
        ),
        migrations.AlterModelOptions(
            name='persontypeanimal',
            options={'verbose_name': 'Person trained on animal'},
        ),
        migrations.AlterModelOptions(
            name='typeanimal',
            options={'ordering': ('order',), 'verbose_name': 'Animal type', 'verbose_name_plural': 'Animal types'},
        ),
        migrations.AlterField(
            model_name='animal',
            name='death_date',
            field=models.DateField(blank=True, null=True, verbose_name='Death date'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='origin_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animal_origin_country', to='core.TypeCountry', verbose_name='Origin country'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='parent1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animal_parent1', to='core.Animal', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='parent2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animal_parent2', to='core.Animal', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='type_animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='animal_type_animal', to='core.TypeAnimal', verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='color',
            field=colorful.fields.RGBColorField(blank=True, help_text='Describing color used in system UI as helper, black is default.', null=True, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='min_cleaners_count',
            field=models.PositiveIntegerField(verbose_name='Minimum cleaners count'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='min_cleaning_duration',
            field=models.DurationField(verbose_name='Minimum cleaning duration'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='type_enclosure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enclosure_type_enclosure', to='core.TypeEnclosure', verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='feeding',
            name='date',
            field=models.DateTimeField(help_text='Planned start of cleaning.'),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(verbose_name='Birth date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='education',
            field=models.TextField(blank=True, null=True, verbose_name='Education'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_animals',
            field=models.ManyToManyField(blank=True, help_text='Type animals that person is qualified for to feed.', through='core.PersonTypeAnimal', to='core.TypeAnimal', verbose_name='Animal types qualification'),
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_enclosures',
            field=models.ManyToManyField(blank=True, help_text='Type enclosures that is qualified to clean.', through='core.PersonTypeEnclosure', to='core.TypeEnclosure', verbose_name='Enclosure types qualification'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
