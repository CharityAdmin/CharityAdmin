from django.forms import widgets
from timeslots.models import days_of_week_list

class SplitDateTimeFieldWithLabels(widgets.SplitDateTimeWidget):
	def format_output(self, rendered_widgets):
		return u'<div class="widget-wrapper widget-wrapper-date">%s</div><div class="widget-wrapper widget-wrapper-time hidden"><label>Time</label> %s</div>' % (rendered_widgets[0], rendered_widgets[1])
		# show time field, labels
		# return u'<div class="widget-wrapper widget-wrapper-date"><label>Date</label> %s</div><div class="widget-wrapper widget-wrapper-time"><label>Time</label> %s</div>' % (rendered_widgets[0], rendered_widgets[1])


# class OpeningMetadataWidget(widgets.MultiWidget):
# 	def __init__(self, attrs=None):
# 		# include each of the widget types:
# 		# TextInput for selecting day of month or specific date
# 		# CheckboxSelectMultiple for selecting days of week or alternating days of week

# 		_widgets = (
# 			widgets.Select(attrs={'class':hidden}, choices=['days_of_week', 'date']),
# 			widgets.CheckboxSelectMultiple(attrs=attrs, choices=days_of_week_list),
# 			widgets.DateInput(attrs=attrs),
# 		)
# 		super(OpeningMetadataWidget, self).__init__(_widgets, attrs)

# 	def decompress(self, value):
#