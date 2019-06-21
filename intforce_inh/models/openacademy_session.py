from odoo import models, fields, api


class Session(models.Model):
    #traditional type 1
    _inherit = 'openacademy.session'
    test = fields.Char(string="Test")
    full_name = fields.Char(string="Full name")
    cc_name = fields.Char(string="CC name")


class Session2(models.Model):

    #traditional type 2
    _name = 'openacademy.dup'
    _inherit = ['openacademy.session', 'mail.thread']

    test = fields.Char(string="Test")
