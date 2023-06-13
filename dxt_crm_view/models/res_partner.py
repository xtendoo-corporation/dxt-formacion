from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Alumno")
    ref_alexia = fields.Char('Id Alexia')
    date_birth = fields.Date('Date of Birth')
    tutor = fields.Char('Tutor')
    bank = fields.Char('Bank')
    bank_account = fields.Char('Bank account')


