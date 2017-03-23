from django.forms.fields import MultiValueField
from django.forms.fields import DateField as DjangoDateField
from django.forms.fields import TimeField as DjangoTimeField
from .widgets import *


__all__ = ('TimeField', 'DateField', 'DateRangeField')


class TimeField(DjangoTimeField):
    widget = TimeWidget


class DateField(DjangoDateField):
    widget = DateWidget


class DateRangeField(MultiValueField):
    widget = DateRangeWidget

    def __init__(self, *args, require_start=True, require_end=True, **kwargs):
        kwargs['require_all_fields'] = False
        super().__init__(fields=(
            DateField(required=require_start),
            DateField(required=require_end)
        ), *args, **kwargs)

    def compress(self, data_list):
        return data_list
