
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class AppointmentPurpose(models.Model):
    _name = 'appointment.purpose'
    _description = "Appointment Purpose"

    name = fields.Char(string='Appointment Purpose', required=True, translate=True)


class AppointmentCabin(models.Model):
    _name = 'appointment.cabin'
    _description = "Appointment Cabin"

    name = fields.Char(string='Appointment Cabin', required=True, translate=True)


class TcbCancelReason(models.Model):
    _name = 'tcb.cancel.reason'
    _description = "Cancel Reason"

    name = fields.Char('Reason')

    
class Appointment(models.Model):
    _name = 'hms.appointment'
    _description = "Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    
    name = fields.Char(string='Appointment Id', readonly=True, copy=False, tracking=True)
    patient_id = fields.Many2one('hms.patient', ondelete='restrict', string='Patient',
        required=True, index=True, help='Patient Name', tracking=True)
    physician_id = fields.Many2one('hms.physician', ondelete='restrict', string='Physician',
        index=True, help='Physician\'s Name', tracking=True)
    department_id = fields.Many2one('hr.department', ondelete='restrict', string='Department', tracking=True, domain=[('patient_department', '=', True)])
    
    care_of = fields.Char(string='Care of', tracking=True, related = "patient_id.care_of")
    # relation = fields.Char(string='Relation', tracking=True, related = "patient_id.relation")
    birthday = fields.Date(string='Date of Birth', tracking=True, related = "patient_id.birthday")
    
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', related = "patient_id.gender")
    age = fields.Integer(string='Age', related = "patient_id.age")
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Group', related = "patient_id.blood_group")
    mobile = fields.Char(string='Mobile', tracking=True, related = "patient_id.mobile")
    phone = fields.Char(string='Phone', tracking=True, related = "patient_id.phone")
    email = fields.Char(string='Email', tracking=True, related = "patient_id.email")
    city = fields.Char(string='City', tracking=True, related = "patient_id.city")
    street = fields.Char(string='Address line1', tracking=True, related = "patient_id.street")
    street2 = fields.Char(string='Address line2', tracking=True, related = "patient_id.street2")
    state_id = fields.Many2one('res.country.state', string='State', tracking=True, related = "patient_id.state_id")
    country_id = fields.Many2one('res.country', string='Country', tracking=True, related = "patient_id.country_id")
    zip = fields.Char(string='Zip', tracking=True, related = "patient_id.zip")
    
    aadhar = fields.Char(string='Aadhar', tracking=True, related = "patient_id.aadhar")
    pan = fields.Char(string='PAN', tracking=True, related = "patient_id.pan")
    occupation = fields.Char(string='Occupation', tracking=True, related = "patient_id.occupation")
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status', default="single", tracking=True, related = "patient_id.marital_status")
    education = fields.Char("Patient Education", related = "patient_id.education")
    occupation = fields.Char("Occupation", related = "patient_id.occupation")   
    # company = fields.Char("Company")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    amount_total = fields.Float(string='Total Amount')
    
    partner_id = fields.Many2one('res.partner', string='Partner', related = "patient_id.partner_id")
    
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)
    duration = fields.Float(string='Duration (Minutes)', default=15.0)
    notes = fields.Text(string='Notes')
    
    # Existing fields...
    
    def action_confirm(self):
        self.state = 'confirmed'
    
    def action_start(self):
        self.state = 'in_progress'
    
    def action_complete(self):
        self.state = 'completed'
    
    def action_cancel(self):
        self.state = 'cancelled'
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_create_invoice(self):
        if self.invoice_id:
            raise UserError(_("Invoice already created for this appointment."))
        
        invoice_vals = {
            'partner_id': self.patient_id.partner_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': f"Appointment - {self.name}",
                'quantity': 1,
                'price_unit': self.amount_total,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        return {
            'name': _('Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
        }
    
    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hms.appointment') or '/'
        return super(Appointment, self).create(vals)        
    def action_report_hms_appointment(self):
        return self.env.ref('tcb_hms_base.action_report_hms_appointment').report_action(self)
    
    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hms.appointment') or '/'
        return super(Appointment, self).create(vals)
