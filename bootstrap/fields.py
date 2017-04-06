from django.forms.fields import MultiValueField
from django.forms.fields import DateField as DjangoDateField
from django.forms.fields import TimeField as DjangoTimeField
from django.utils.encoding import force_text
from .widgets import *


__all__ = ('TimeField', 'DateField', 'DateRangeField')


class TimeField(DjangoTimeField):
    widget = TimeWidget


class DateField(DjangoDateField):
    widget = DateWidget


class DateRangeField(MultiValueField):
    widget = DateRangeWidget

    def __init__(self, *args, require_end=True, **kwargs):
        kwargs['require_all_fields'] = False
        super().__init__(fields=(
            DateField(required=True),
            DateField(required=require_end)
        ), *args, **kwargs)

    def prepare_value(self, data_list):
        if data_list and any(data_list):
            separator = force_text(self.widget.get_options()['separator'])
            formatted = [self.widget.format_value(data_list[0])]
            if data_list[1]:
                formatted.append(self.widget.format_value(data_list[1]))
            return separator.join(formatted)
        return ''

    def compress(self, data_list):
        if data_list:
            return tuple(data_list)
        return None, None
