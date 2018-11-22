# Generated by Django 2.1.1 on 2018-11-22 15:19

from django.db import migrations, models
import django.utils.timezone
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20181109_2135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalstay',
            options={'ordering': ('date_from',)},
        ),
        migrations.AlterModelOptions(
            name='cleaning',
            options={'ordering': ('date',)},
        ),
        migrations.AlterModelOptions(
            name='feeding',
            options={'ordering': ('date',)},
        ),
        migrations.AlterModelOptions(
            name='feedinganimal',
            options={'ordering': ('feeding__date',)},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('type_role__order', 'last_name', 'first_name'), 'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AddField(
            model_name='cleaning',
            name='x_created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cleaning',
            name='x_modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='cleaning',
            name='id',
        ),
        migrations.AddField(
            model_name='cleaning',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_animals',
            field=models.ManyToManyField(blank=True, help_text='Type animals that is qualified to feed.', through='core.PersonTypeAnimal', to='core.TypeAnimal'),
        ),
        migrations.AlterField(
            model_name='person',
            name='trained_type_enclosures',
            field=models.ManyToManyField(blank=True, help_text='Type enclosures that is qualified to clean.', through='core.PersonTypeEnclosure', to='core.TypeEnclosure'),
        ),
    ]