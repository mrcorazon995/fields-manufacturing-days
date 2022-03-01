# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil import rrule


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    # def getDifferenceDays(self, dt1, dt2):
    #     monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    #     n1 = dt1.year * 365 + dt1.day
    #     for i in range(0, dt1.month - 1):
    #         n1 += monthDays[i]
    #     y = dt1.year
    #     if (dt1.month <= 2):
    #         y -= 1
    #     n1 += int(y / 4) - int(y / 100) + int(y / 400)
    #     n2 = dt2.year * 365 + dt2.day
    #     for i in range(0, dt2.month - 1):
    #         n2 += monthDays[i]
    #     y2 = dt2.year
    #     if (dt2.month <= 2):
    #         y2 -= 1
    #     n2 += int(y2 / 4) - int(y2 / 100) + int(y2 / 400)
    #     return (n2 - n1 +1)

    @api.model
    def _automated_days_manufacturing(self):
        to_process = self.env['mrp.production'].search([('state', '=','done')])
        to_process.automated_days_manufacturing()

    def automated_days_manufacturing(self):
    	for rec in self:
	        dt1 = rec.create_date.date()
	        dt2 = rec.date_finished or datetime.now()
	        ddif = dt2.date() - dt1
	        rec.natural_days = ddif.days + 1


	        days_off = 5, 6
	        workdays = [x for x in range(7) if x not in days_off]
	        days = rrule.rrule(rrule.DAILY, dtstart=dt1, until=dt2.date(), byweekday=workdays)
	        rec.business_days = days.count()

	        rec.entry_week = dt1.isocalendar()[1]

	        rec.departure_week = dt2.date().isocalendar()[1]

    natural_days = fields.Char(string="Dias Naturales")
    business_days = fields.Char(string="Dias Habiles")
    entry_week = fields.Char(string="Semana de entrada")
    departure_week = fields.Char(string="Semena de salida")