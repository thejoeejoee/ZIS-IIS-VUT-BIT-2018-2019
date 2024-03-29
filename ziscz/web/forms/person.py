# coding=utf-8
from __future__ import unicode_literals

from crispy_forms.layout import Layout, Row, HTML, Fieldset
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, User
from django.db.transaction import atomic
from django.forms import Textarea, CharField, PasswordInput
from django.utils.text import slugify
from django.utils.timezone import localdate
from django.utils.translation import ugettext_lazy as _, ugettext

from ziscz.core.forms.base import BaseModelForm
from ziscz.core.forms.crispy import Col
from ziscz.core.forms.fields import BooleanSwitchField
from ziscz.core.forms.widgets.datepicker import DatePickerInput
from ziscz.core.forms.widgets.select2 import TypeAnimalMultipleSelectWidget, TypeEnclosureMultipleSelectWidget
from ziscz.core.models import Person, PersonTypeEnclosure, TypeEnclosure, TypeAnimal, PersonTypeAnimal, TypeRole
from ziscz.core.utils.m2m import update_m2m


class PersonForm(BaseModelForm):
    is_active = BooleanSwitchField(label=_('Is active'), help_text=_('Can user log in?'), required=False, initial=True)

    password1 = CharField(
        label=_('Password'),
        widget=PasswordInput,
        required=False
    )
    password2 = CharField(
        label=_('Password second'),
        widget=PasswordInput,
        required=False
    )

    class Meta:
        model = Person
        fields = (
            'type_role',
            'first_name',
            'last_name',
            'birth_date',
            'education',
            'note',
            'trained_type_animals',
            'trained_type_enclosures',
        )

        widgets = {
            'birth_date': DatePickerInput(),
            'trained_type_animals': TypeAnimalMultipleSelectWidget(),
            'trained_type_enclosures': TypeEnclosureMultipleSelectWidget(),
            'education': Textarea(attrs=dict(rows=3)),
            'note': Textarea(attrs=dict(rows=3)),
        }

    def __init__(self, user=None, *args, **kwargs):
        self._user = user  # type: User
        super().__init__(*args, **kwargs)

        self.fields['trained_type_enclosures'].initial = TypeEnclosure.objects.filter(
            person_type_enclosure_type_enclosure__person=self.instance
        )

        self.fields['trained_type_animals'].initial = TypeAnimal.objects.filter(
            person_type_animal_type_animal__person=self.instance
        )

        self.fields['is_active'].initial = self.instance.user.is_active if self.instance.user else True

        self.helper.layout = Layout(
            Row(
                Col('first_name'),
                Col('last_name'),
            ),
            'type_role',
            Row(
                Col('birth_date'),
                Col('is_active'),
            ),
            'trained_type_animals',
            'trained_type_enclosures',
            Row(
                Col('education'),
                Col('note'),
            ),
            Fieldset(
                _('Password change'),
                Row(
                    Col('password1'),
                    Col('password2'),
                )
            ) if self._user.has_perm('auth.change_user') and not self.updating else None,
            Row(
                Col(HTML(
                    ': '.join(
                        map(
                            str,
                            (
                                ugettext('User'),
                                self.instance.user
                            )
                        )
                    )
                )) if self.instance.user else None,
                Col(HTML(
                    ': '.join((
                        ugettext('Groups'),
                        ', '.join(map(str, self.instance.user.groups.all()))
                    ))
                )) if self.instance.user else None,
            ),

        )

    def _save_m2m(self):
        update_m2m(
            actual_objects=self.fields['trained_type_enclosures'].initial,
            new_objects=self.cleaned_data.get('trained_type_enclosures'),
            relation_model=PersonTypeEnclosure,
            static_field='person',
            static_object=self.instance,
            dynamic_field='type_enclosure',
        )
        update_m2m(
            actual_objects=self.fields['trained_type_animals'].initial,
            new_objects=self.cleaned_data.get('trained_type_animals'),
            relation_model=PersonTypeAnimal,
            static_field='person',
            static_object=self.instance,
            dynamic_field='type_animal',
        )

    @atomic
    def save(self, commit=True):
        instance = super().save(commit=commit)  # type: Person
        if not self.updating:
            user_model = get_user_model()  # type: AbstractUser
            base_username = slugify('.'.join(map(str, (
                instance.last_name,
                instance.first_name,
            ))))
            username = base_username
            i = 1
            while user_model.objects.filter(username=username).exists():
                username = '{}.{}'.format(base_username, i)
                i += 1

            user = user_model.objects.create_user(
                username=username,
                last_name=instance.last_name,
                first_name=instance.first_name,
            )
            instance.user = user
            instance.save(update_fields=['user'])
        else:
            user = self.instance.user  # type: AbstractUser

        if user:
            # remove all type roles groups
            for g in Group.objects.filter(name__in=TypeRole.objects.values_list('name', flat=True)):
                user.groups.remove(g)
            # assign all roles with higher order than selected
            for tr in TypeRole.objects.filter(order__gte=self.instance.type_role.order):
                user.groups.add(Group.objects.get_or_create(name=tr.name)[0])

            user.is_active = self.cleaned_data.get('is_active')
            user.save(update_fields=['is_active'])

        password = self.cleaned_data.get('password1')
        if self._user.has_perm('auth.change_user') and password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return instance

    def clean(self):
        data = super().clean()

        birth = data.get('birth_date')
        if birth and birth > localdate():
            self.add_error('birth_date', _('Cannot set birth date to future.'))

        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', _('Password does not match the first one.'))

        return data
