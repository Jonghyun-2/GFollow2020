from django import template

register = template.Library()


@register.filter(name='addslash')
def addslash(value):
    val_split = value.split("\\")
    res = ""
    for i in range(len(val_split)):
        if i != len(val_split)-1:
            res = res + val_split[i] + '//'
        else:
            res = res + val_split[i]
    return res
