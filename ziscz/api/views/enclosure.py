# coding=utf-8
from __future__ import unicode_literals

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.translation import ungettext
from django.views import View
from rest_framework.generics import get_object_or_404

from ziscz.core.models import Enclosure, Animal, AnimalStay


class EnclosureAnimalsSetup(CsrfExemptMixin, PermissionRequiredMixin, JsonRequestResponseMixin, View):
    require_json = True
    permission_required = 'core.change_animal'

    def post(self, request: WSGIRequest, *args, **kwargs):
        enclosures = self.request_json.get('enclosures')
        moved = []

        for enclosure_data in enclosures:
            enclosure = get_object_or_404(Enclosure, pk=enclosure_data.get('id'))
            animals = Animal.live_animals.filter(
                pk__in=enclosure_data.get('animals')
            )

            for animal in animals:
                if animal.actual_enclosure != enclosure:
                    AnimalStay.objects.move_animal(
                        animal=animal,
                        new_enclosure=enclosure,
                    )
                    moved.append(animal)

        return JsonResponse(dict(
            success=True,
            msg=ungettext(
                'Animal {} was moved.',
                'Animals {} were moved.',
                len(moved)).format(''.join(map(str, moved)))
        ))
