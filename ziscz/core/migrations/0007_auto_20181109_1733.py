# Generated by Django 2.1.1 on 2018-11-09 16:33

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20181106_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonTypeAnimal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('x_created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('x_modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_type_animal_person', to='core.Person')),
                ('type_animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_type_animal_type_animal', to='core.TypeAnimal')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='animalperson',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='animalperson',
            name='animal',
        ),
        migrations.RemoveField(
            model_name='animalperson',
            name='person',
        ),
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ('-death_date', 'type_animal', 'name'), 'verbose_name': 'Animal', 'verbose_name_plural': 'Animals'},
        ),
        migrations.RemoveField(
            model_name='animal',
            name='trained_person',
        ),
        migrations.AlterField(
            model_name='animalstay',
            name='animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='animal_stay_animal', to='core.Animal'),
        ),
        migrations.AlterField(
            model_name='animalstay',
            name='enclosure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='animal_stay_enclosure', to='core.Enclosure'),
        ),
        migrations.DeleteModel(
            name='AnimalPerson',
        ),
        migrations.AddField(
            model_name='typeanimal',
            name='trained_persons',
            field=models.ManyToManyField(through='core.PersonTypeAnimal', to='core.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='persontypeanimal',
            unique_together={('type_animal', 'person')},
        ),
    ]
