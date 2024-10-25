# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import format_datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF, DEFAULT_SERVER_DATETIME_FORMAT as DTF, format_datetime as tool_format_datetime
import pprint

class ResPartner(models.Model):
    _inherit= "res.partner"

    is_referring_doctor = fields.Boolean(string="Is Refereinng Physician")
    is_referering_patient = fields.Boolean(string="Is Referering Patient")

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Master'
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']
    # _inherits = {
    #     'res.partner': 'partner_id',
    # }
    name = fields.Char(string='Name', required=True, tracking=True)
    
    code = fields.Char(string='Patient Code', readonly=True, copy=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', default="male")
    birthday = fields.Date(string='Date of Birth' , store= True)
    date_of_death= fields.Date(string='Date of Birth')
    care_of = fields.Char(string='Care of')
    relation = fields.Many2one('tcb.family.relation', string='Relation')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Group')

    # ref_doctor_ids = fields.Many2many('res.partner', 'rel_doc_pat', 'doc_id', 
    #     'patient_id', 'Referring Doctors',domain=[('is_referring_doctor','=',True)])

    title = fields.Many2one('res.partner.title')

    gov_code = fields.Char(string='Government Identity', copy=False, tracking=True)
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status', default="single")
    spouse_name = fields.Char("Spouse's Name")
    spouse_edu = fields.Char("Spouse's Education")
    spouse_business = fields.Char("Spouse's Business")
    education = fields.Char("Patient Education")
    occupation = fields.Char("Occupation")
    religion = fields.Char("Religion")
    date_of_death = fields.Date("Date of Death")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict' , default=lambda self: self.env.user.company_id.country_id)

    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    aadhar = fields.Char(string="Aadhar Number")
    pan = fields.Char(string="PAN Number")
    
    primary_physician_id = fields.Many2one('hms.physician' , 'Primary Care Doctor')

    active = fields.Boolean(string="Active", default=True)
    
    partner_id = fields.Many2one('res.partner', string='Res Partner')
    
    is_patient = fields.Boolean(string="Is Patient", default=True)
    
    
    @api.model
    def create(self, vals):
        # Generate patient code if not provided
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('hms.patient') or '/'
        
        # Create a partner record first
        partner_vals = {
            'name': vals.get('name'),
            'is_referering_patient': True,
        }
        partner = self.env['res.partner'].create(partner_vals)
        
        # Add the partner_id to vals
        vals['partner_id'] = partner.id
        
        # Create the patient record
        patient = super(HmsPatient, self).create(vals)
        
        return patient

    def write(self, vals):
        res = super(HmsPatient, self).write(vals)
        print("---------------WRITE VALS",vals)
        # Update the partner name if the patient name has changed
        if 'name' in vals:
            for record in self:
                if record.partner_id:
                    record.partner_id.name = vals['name']
                    print ("yessssssssssss")
                else:
                    # Create a new partner if it doesn't exist
                    partner = self.env['res.partner'].create({
                        'name': vals['name'],
                        'is_referering_patient': True,
                    })
                    record.partner_id = partner.id
                    print ("nooooooooooooooo")
                    
        print("---------------WRITE RES  /n ",self.partner_id.name,"---------------partnerid - ",self.partner_id)
        return res
    
    
    @api.onchange('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _onchange_address(self):
        print('-------------------yeaay')

        records = self.env['res.partner'].search([])
        for record in records:
            print(record.name, record.is_referering_patient) 
            
    # @api.onchange('name','care_of','partner_id')
    # def get_partner_id (self):
    #     if self.name:
    #         self.partner_id.name = self.name
    #         print("============yessssssssss- ", self.partner_id.name)
    #     else :
    #         self.partner_id = ""
    #         print("============nooooooooooooo- ", self.partner_id)
            
    # @api.model
    # def write(self, vals):
    #     if vals.get('patient_id'):
    #         partner_vals = {
    #             'name': vals['patient_id'],
    #             'is_patient': True,
    #         }
    #         partner_id = self.env['res.partner'].write(partner_vals)
    #         vals['patient_id'] =self.partner_id.name
    #         vals['partner_id'] = partner_id.id
    #     return super(HmsPatient, self).write(vals)
    
    
    
# , compute='_compute_invoicing_stats',, compute='_compute_invoicing_stats',
    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                record.age = (datetime.now().date() - record.birthday).days // 365
            else:
                record.age = 0
    

    # @api.model
    # def create(self, vals):
        
    #     return super(HmsPatient, self).create(vals)



    def view_invoices(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('partner_id', '=', self.partner_id.id), ('move_type', '=', 'out_invoice')]
        return action

    def action_view_attachments(self):
        self.ensure_one()
        action = self.env.ref('base.action_attachment').read()[0]
        action['domain'] = [('res_model', '=', 'hms.patient'), ('res_id', '=', self.id)]
        action['context'] = {'default_res_model': 'hms.patient', 'default_res_id': self.id}
        return action
        
    

    @api.depends('birthday')
    def _compute_today_is_birthday(self):
        today = fields.Date.today()
        for patient in self:
            patient.today_is_birthday = patient.birthday and patient.birthday.day == today.day and patient.birthday.month == today.month

    today_is_birthday = fields.Boolean(string="Is Birthday Today" )
    
    
    # # THese are more fields from inherited moudels
    
