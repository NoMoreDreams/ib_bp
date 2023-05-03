from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    return value.as_widget(attrs={'class': f'{css_classes} {arg}'})


@register.filter
def attr(value, arg):
    """
    Returns the value of the attribute with the given name on the given object.
    """
    try:
        return getattr(value, arg)
    except AttributeError:
        return None
