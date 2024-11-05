
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Appointment(models.Model):
    _inherit = 'hms.appointment'


    def action_refer_ophthalmology(self):
        pass
        # return self.env.ref('tcb_ophthalmology.ophthalmology_action')