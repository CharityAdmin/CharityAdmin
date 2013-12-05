from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag()
def commitment_instance_url(instance):
    return reverse('timeslots_commitment_instance_view', kwargs={'clientid': instance['client'].user.id, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.simple_tag()
def opening_instance_url(instance):
    return reverse('timeslots_opening_instance_view', kwargs={'clientid': instance['client'].user.id, 'year': instance['date'].year, 'month': instance['date'].month, 'day': instance['date'].day, 'time': instance['date'].strftime('%H%M')})


@register.inclusion_tag('timeslots/partials/display_address.html')
def display_address(client):
	return {'client': client}