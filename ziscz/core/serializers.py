# coding=utf-8
from __future__ import unicode_literals

from typing import Optional

from django.utils.datetime_safe import datetime
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from ziscz.core.models import Animal, Enclosure


class AnimalSerializer(ModelSerializer):
    type_animal = StringRelatedField()
    type_animal_icon = StringRelatedField(source='type_animal.icon')

    class Meta:
        model = Animal
        fields = (
            'id',
            'name',
            'type_animal',
            'type_animal_icon',
        )


class EnclosureSerializer(ModelSerializer):
    type_enclosure = StringRelatedField()
    last_cleaning_date = SerializerMethodField()
    animals = AnimalSerializer(source='current_animals', many=True)

    @staticmethod
    def get_last_cleaning_date(obj: Enclosure) -> Optional[datetime]:
        last_cleaning = obj.last_cleaning
        return last_cleaning.date if last_cleaning else None

    class Meta:
        model = Enclosure
        fields = (
            'id',
            'name',
            'type_enclosure',
            'enclosure_color',
            'animals',
            'last_cleaning_date',
        )
