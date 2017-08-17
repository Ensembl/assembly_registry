from django import template

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    class_old = field.field.widget.attrs.get('class', None)
    class_new = class_old + ' ' + css if class_old else css
    return field.as_widget(attrs={"class": class_new})


@register.filter
def html_placeholder(field, placeholder):
    return field.as_widget(attrs={"placeholder": placeholder})
