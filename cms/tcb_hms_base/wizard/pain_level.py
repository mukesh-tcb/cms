# coding: utf-8

from odoo import models, api, fields

class AcsPainLevel(models.TransientModel):
    _name = 'tcb.pain.level'
    _description = "Pain Level Diagram"

    name = fields.Char()