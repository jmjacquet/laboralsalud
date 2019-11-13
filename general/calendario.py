# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import turnos
from django.core.urlresolvers import reverse

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(fecha__day=day)
		d = ''
		for event in events_per_day:
			d += '<li> <a href="{}" class="modal-detail" data-modal-head="DETALLE TURNO">{}</a></li>'.format(reverse('turnos_detalles', kwargs={'id':event.pk}),unicode(event.get_turno()))			
		if day != 0:
			return u"<td><span class='date'>{}</span><ul> {} </ul></td>".format(day,d)
		return u'<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return u'<tr> {} </tr>'.format(week)

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = turnos.objects.filter(fecha__year=self.year, fecha__month=self.month)

		cal = u'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += u'{}\n'.format(self.formatmonthname(self.year, self.month, withyear=withyear))
		cal += u'{}\n'.format(self.formatweekheader())
		for week in self.monthdays2calendar(self.year, self.month):
			cal += '{}\n'.format(self.formatweek(week, events))
		return cal