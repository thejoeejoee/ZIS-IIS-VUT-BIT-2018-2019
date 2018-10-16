# coding=utf-8
from __future__ import unicode_literals

from operator import attrgetter


def update_m2m(actual_objects, new_objects, relation_model, static_field, static_object, dynamic_field,
               filters=None, extra_relation_values=None):
    """
    For general usage of saving ModelMultipleChoiceField values.

    :param actual_objects: objects that are already saved in m2m table
    :param new_objects: all objects send with post, including already saved
    :param relation_model: eg HorseSubjectBreeder - m2m table
    :param static_field: eg for 1 horse is more subject breeders - so its 'horse'
    :param static_object: eg instance of Horse
    :param dynamic_field: second joining value in m2m table eg 'subject'
    :param filters: additional filters to delete unused relation - must be type of dict
    :param extra_relation_values - dict of extra values to set, key is field name, value is a value
    """
    actual_objects = set(actual_objects or ())
    new_objects = set(new_objects or ())  # set does not respect order

    if actual_objects == new_objects:
        return
    if isinstance(filters, dict):
        filters.update({static_field: static_object})
    else:
        filters = {static_field: static_object}

    to_delete = actual_objects - new_objects
    to_insert = new_objects - actual_objects

    relation_model.objects.filter(**{
        static_field: static_object,
        '{}_id__in'.format(dynamic_field): map(attrgetter('id'), to_delete)
    }).filter(**filters).delete()

    for order, target_object in enumerate(to_insert, start=1):
        relation_object = relation_model()
        setattr(relation_object, dynamic_field, target_object)
        setattr(relation_object, static_field, static_object)

        if extra_relation_values:
            for field, value in extra_relation_values.items():
                setattr(relation_object, field, value)
        relation_object.save()
