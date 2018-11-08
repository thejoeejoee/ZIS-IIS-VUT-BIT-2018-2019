# coding=utf-8
from __future__ import unicode_literals

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
    animals = AnimalSerializer(source='current_animals', many=True)

    class Meta:
        model = Enclosure
        fields = (
            'id',
            'name',
            'type_enclosure',
            'enclosure_color',
            'animals',
        )
