import io
from django import template, forms
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag('bootstrap/bootstrap.html')
def bootstrap(element, layout='default'):
    return {'element': element, 'layout': layout}


@register.filter
def bootstrapwidget(field, css_class='form-control'):
    return field.as_widget(attrs={'class': css_class})


@register.simple_tag
def fieldinit(element):
    s = io.StringIO()
    s.write('<script>\n')
    if isinstance(element, forms.BoundField):
        element = [element]
    elif not isinstance(element, forms.BaseForm):
        raise TypeError
    for bound in element:
        if hasattr(bound.field.widget, 'javascript_init'):
            s.write(bound.field.widget.javascript_init(bound))
            s.write('\n')
    s.write('</script>')
    return mark_safe(s.getvalue())


@register.filter
def is_form(element):
    return isinstance(element, forms.BaseForm)


@register.filter
def is_formset(element):
    return isinstance(element, forms.BaseFormSet)


@register.filter
def is_field(element):
    return isinstance(element, forms.BoundField)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)
