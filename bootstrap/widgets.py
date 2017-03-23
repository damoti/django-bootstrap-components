import re
import json
from django.forms.widgets import TimeInput, DateInput, Media
from django.utils.formats import get_format, localize_input
from django.utils.translation import get_language, ugettext_lazy as _
from django.utils.functional import Promise
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text


__all__ = (
    'TimeWidget', 'DateWidget', 'DateRangeWidget',
)


class LocalizedJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super().default(obj)


class LocalizedWidgetMixin:
    PY_TO_JS = {}
    PY_TO_JS_RE = None
    default_options = {}

    def __init__(self, options=None, attrs=None, format=None, input_formats=None, input_formats_index=0):
        super().__init__(attrs)
        assert not all((format, input_formats)), \
            "Only format or input_formats may be passed, but not both."
        self.format = format
        self.input_formats = input_formats
        self.input_formats_index = input_formats_index
        self.options = options or {}

    def get_format(self):
        if self.input_formats:
            return self.input_formats[self.input_formats_index]
        if self.format:
            return self.format
        return get_format(self.format_key)[self.input_formats_index]

    def format_value(self, value):
        return localize_input(value, self.get_format())

    def get_options(self):
        options = self.default_options.copy()
        options.update(self.options)
        return options

    def get_json_options(self):
        return json.dumps(self.get_options(), cls=LocalizedJSONEncoder)


class TimeWidget(LocalizedWidgetMixin, TimeInput):
    template_name = 'bootstrap/time.html'
    default_options = {
        'autoclose': True,
        'donetext': _('Done'),
        'twelvehour': False,
        'vibrate': True,
    }

    class Media:
        css = {
            'all': ('css/bootstrap-clockpicker.min.css',)
        }
        js = (
            'js/bootstrap-clockpicker.min.js',
        )

    def javascript_init(self, bound):
        return "$('input[name=\"{}\"]').parent().clockpicker({});" \
            .format(bound.html_name, self.get_json_options())


class DateWidget(LocalizedWidgetMixin, DateInput):

    template_name = 'bootstrap/date.html'

    PY_TO_JS = {
        '%d': 'dd',
        '%m': 'mm',
        '%y': 'yy',
        '%Y': 'yyyy',
        '%M': 'ii',
        '%I': 'HH',
        '%H': 'hh',
        '%S': 'ss',
        '%p': 'P',
    }

    PY_TO_JS_RE = re.compile(r'(?<!\w)(' + '|'.join(PY_TO_JS.keys()) + r')\b')

    _js_format_cache = {}

    def get_javascript_format(self, python_format):
        js_format = self._js_format_cache.get(python_format)
        if not js_format:
            js_format = self._js_format_cache[python_format] = \
                self.PY_TO_JS_RE.sub(lambda x: self.PY_TO_JS[x.group()], python_format)
        return js_format

    def _media(self):
        language = get_language()
        return Media(
            css={'all': ('css/bootstrap-datepicker3.min.css',)},
            js=['js/bootstrap-datepicker.min.js'] + (
               ['js/locales/bootstrap-datepicker.%s.min.js' % language] if language != 'en' else []
            )
        )
    media = property(_media)

    def get_options(self):
        options = super().get_options()
        options['language'] = get_language()
        options['format'] = self.get_javascript_format(self.get_format())
        return options

    def javascript_init(self, bound):
        return "$('input[name=\"{}\"]').datepicker({});" \
            .format(bound.html_name, self.get_json_options())


class DateRangeWidget(LocalizedWidgetMixin, DateInput):

    template_name = 'bootstrap/date.html'

    default_options = {
        'autoClose': True,
        'separator': ' ~ ',
    }

    PY_TO_JS = {
        '%d': 'D',
        '%m': 'M',
        '%y': 'YY',
        '%Y': 'YYYY',
        '%M': 'mm',
        '%I': 'hh',
        '%H': 'HH',
        '%S': 'ss',
        '%p': 'a',
    }

    PY_TO_JS_RE = re.compile(r'(?<!\w)(' + '|'.join(PY_TO_JS.keys()) + r')\b')

    _js_format_cache = {}

    def get_javascript_format(self, python_format):
        js_format = self._js_format_cache.get(python_format)
        if not js_format:
            js_format = self._js_format_cache[python_format] = \
                self.PY_TO_JS_RE.sub(lambda x: self.PY_TO_JS[x.group()], python_format)
        return js_format

    class Media:
        css = {
            'all': ('css/daterangepicker.min.css',)
        }
        js = (
            'js/moment-with-locales.min.js',
            'js/jquery.daterangepicker.min.js',
        )

    def get_options(self):
        options = super().get_options()
        options['language'] = get_language()
        options['format'] = self.get_javascript_format(self.get_format())
        return options

    def javascript_init(self, bound):
        return "$('input[name=\"{}\"]').dateRangePicker({});" \
            .format(bound.html_name, self.get_json_options())

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            separator = force_text(self.get_options()['separator'])
            dates = value.split(separator)
            return (value, None) if len(dates) == 1 else dates
        return None, None
