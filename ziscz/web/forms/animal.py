# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row
from django.forms import ModelChoiceField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.forms.widgets.select2 import AnimalSelectWidget
from ziscz.core.models import Animal, AnimalRegion, Enclosure, AnimalStay, TypeRegion
from ziscz.core.utils.m2m import update_m2m


class AnimalForm(BaseModelForm):
    animal_stay = ModelChoiceField(
        queryset=Enclosure.objects.all(),
        required=False,
        label=_('Animal stay'),
    )

    class Meta:
        model = Animal
        fields = (
            'name',
            'type_animal',
            'birth_date',
            'origin_country',
            'occurrence_region',
            'death_date',

            'parent1',
            'parent2',
        )

        widgets = {
            'death_date': DatePickerInput(
                options=dict(
                    maxDate='now',
                )
            ),
            'birth_date': DatePickerInput(
                options=dict(
                    maxDate='now',
                )
            ),
            'occurrence_region': Select2MultipleWidget,
            'parent1': AnimalSelectWidget(dependent_fields={
                'type_animal': 'type_animal'
            }),
            'parent2': AnimalSelectWidget(dependent_fields={
                'type_animal': 'type_animal'
            })
        }

    DISABLED_ON_DEATH = (
        'name',
        'type_animal',
        'birth_date',
        'occurrence_region',
        'origin_country',
        'animal_stay',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['occurrence_region'].required = False
        self.fields['animal_stay'].initial = self.instance.actual_enclosure.pk if self.instance.actual_enclosure else None

        self.helper.layout = Layout(
            'name',
            'type_animal',
            Row(
                Col('birth_date'),
                Col('death_date'),
            ),
            Row(
                Col('origin_country'),
                Col('occurrence_region'),
            ),
            Row(
                Col('parent1'),
                Col('parent2'),
            ),
            'animal_stay',
        )

        if self.updating:
            self.fields['parent1'].queryset = self.fields['parent2'].queryset = self.fields['parent1'].queryset.filter(
                type_animal=self.instance.type_animal
            ).exclude(pk=self.instance.pk)
            if self.instance.death_date and self.instance.death_date <= timezone.now().date():
                for f in self.DISABLED_ON_DEATH:
                    self.fields[f].disabled = True
        else:
            self.fields['birth_date'].initial = timezone.localdate()

    def _save_m2m(self):
        update_m2m(
            actual_objects=TypeRegion.objects.filter(animal_region_region__animal=self.instance),
            new_objects=self.cleaned_data.get('occurrence_region'),
            relation_model=AnimalRegion,
            static_field='animal',
            static_object=self.instance,
            dynamic_field='region',
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if 'animal_stay' in self.changed_data:
            AnimalStay.objects.move_animal(
                animal=self.instance,
                new_enclosure=self.cleaned_data.get('animal_stay'),
            )
        return instance

    def clean(self):
        data = super().clean()
        parent1 = data.get('parent1')
        if parent1 and parent1.type_animal != data.get('type_animal'):
            self.add_error('parent1', _('Animal {} cannot have parent type of {}.').format(
                data.get('type_animal'),
                parent1.type_animal,
            ))

        parent2 = data.get('parent2')
        if parent2 and parent2.type_animal != data.get('type_animal'):
            self.add_error('parent2', _('Animal {} cannot have parent type of {}.').format(
                data.get('type_animal'),
                parent2.type_animal,
            ))

        if parent1 and parent1 == parent2:
            self.add_error('parent2', _('Animal cannot have one parent two times {}.').format(
                parent1,
            ))

        death_date = data.get('death_date')
        if death_date and death_date > timezone.localdate():
            self.add_error('death_date', _('Cannot set death date in future.'))

        return super().clean()
