#Ref was taken form GNU HEALTH ophthalmology module

from odoo import api, fields, models ,_
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class ACSOphthalmologyEvaluation(models.Model):
    _name = "acs.ophthalmology.evaluation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ophthalmology Evaluation"

    STATES = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}

    name = fields.Char(string='Name', default='/', copy=False, tracking=True)
    patient_id = fields.Many2one('hms.patient', 'Patient', required=True, states=STATES, tracking=True)
    date = fields.Datetime('Date', default=fields.Datetime.now, help="Date of Consultation", states=STATES, tracking=True)
    age = fields.Char(compute="get_patient_age", string='Age', store=True,
            help="Computed patient age at the moment of the evaluation")
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Physician', 
        index=True, help='Physician\'s Name', states=STATES)
    appointment_id = fields.Many2one('hms.appointment', ondelete="restrict", 
        string='Appointment', states=STATES)
    diseases_ids = fields.Many2many("hms.diseases", 'hms_diseases_ophthalmology_rel', 'evaluation_id', 'diseases_id', "Disease", states=STATES)
