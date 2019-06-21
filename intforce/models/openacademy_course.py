from odoo import models, fields, api
# models : for get models features in your class
# fields: for declare fields
# api: for accessing decorators
# _ : translation


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', help="this is test", required=True)
    description = fields.Text()
    session_ids = fields.One2many('openacademy.session', 'course_id')
    html = fields.Html()
    upper = fields.Char(compute='_compute_upper', inverse='_inverse_upper', readonly=False)
    responsible = fields.Many2one('res.users')
    image = fields.Binary()

    @api.depends('name')
    def _compute_upper(self):
        for rec in self:
            rec.upper = rec.name.upper() if rec.name else False

    def _inverse_upper(self):
        for rec in self:
            rec.name = rec.upper.lower() if rec.upper else False
