# coding: utf-8

from odoo import models, api, fields
from datetime import date, datetime, timedelta


class AcsRescheduleAppointments(models.TransientModel):
    _name = 'tcb.reschedule.appointments'
    _description = "Reschedule Appointments"

    tcb_reschedule_time = fields.Float(string="Reschedule Selected Appointments by (Hours)", required=True)

    def tcb_reschedule_appointments(self):
        appointments = self.env['hms.appointment'].search([('id','in',self.env.context.get('active_ids'))])
        #TCB: do it in method only to use that method for notifications.
        appointments.tcb_reschedule_appointments(self.tcb_reschedule_time)
