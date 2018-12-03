from django.contrib import admin

# Register your models here.
from ziscz.core.models import (
    Animal, TypeAnimal, Person, TypeRole,
    PersonTypeAnimal, TypeCountry, Enclosure,
    TypeEnclosure, TypeFeed, TypeRegion,
    TypeCleaningAccessory, TypeEnclosureTypeCleaningAccessory)


class BaseTypeModelAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'identifier',
        'description',
        'order',
    ]


admin.register(TypeAnimal)(BaseTypeModelAdmin)
admin.register(TypeRole)(BaseTypeModelAdmin)
admin.register(TypeRegion)(BaseTypeModelAdmin)
admin.register(TypeCountry)(BaseTypeModelAdmin)
admin.register(TypeEnclosure)(BaseTypeModelAdmin)
admin.register(TypeFeed)(BaseTypeModelAdmin)
admin.register(TypeCleaningAccessory)(BaseTypeModelAdmin)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type_animal',
    ]


@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type_enclosure',
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
    ]


@admin.register(PersonTypeAnimal)
class AnimalPersonAdmin(admin.ModelAdmin):
    list_display = [
        'person',
        'type_animal',
    ]


@admin.register(TypeEnclosureTypeCleaningAccessory)
class TypeEnclosureTypeCleaningAccessoryAdmin(admin.ModelAdmin):
    list_display = [
        'type_enclosure',
        'type_cleaning_accessory',
    ]
