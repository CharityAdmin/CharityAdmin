from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag()
def commitment_instance_url(instance):
    return reverse('timeslots_commitment_instance_view', kwargs={'clientid': instance['client'].user.id, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.simple_tag()
def opening_instance_url(instance):
    return reverse('timeslots_opening_instance_view', kwargs={'clientid': instance['client'].user.id, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})

@register.simple_tag()
def opening_exception_add_url(instance):
    return reverse('timeslots_opening_exception_view', kwargs={'openingid': instance['openingid'], 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.simple_tag()
def opening_exception_delete_url(instance):
    return reverse('timeslots_opening_exception_delete', kwargs={'openingid': instance['openingid'], 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.simple_tag()
def commitment_exception_add_url(commitmentid, instance):
    return reverse('timeslots_commitment_exception_view', kwargs={'commitmentid': commitmentid, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.simple_tag()
def commitment_exception_delete_url(commitmentid, instance):
    print "COMMITMENTID"
    print commitmentid
    return reverse('timeslots_commitment_exception_delete', kwargs={'commitmentid': commitmentid, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.inclusion_tag('timeslots/partials/display_address.html')
def display_address(client):
    return {'client': client}


@register.filter()
def field_class(formfield):
    fieldclass = formfield.field.widget.attrs['class'] if formfield.field.widget.attrs and 'class' in formfield.field.widget.attrs else ""
    return fieldclass

@register.filter()
def negate(value):
    return not value