from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Session(models.Model):

    _name = 'openacademy.session'
    _description = 'Session'

    # If you want to add chatter
    #_inherit = ['crm.team', 'mail.thread']
    _inherit = ['mail.thread']
    name = fields.Char(required=True)
    start_date = fields.Date("Start Date", default=fields.Date.today)
    duration = fields.Float()
    description = fields.Text()
    course_description = fields.Text()
    seats = fields.Integer("Number of Seats")
    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], required=True, default='draft')
    instructor_id = fields.Many2one('res.partner')
    course_id = fields.Many2one('openacademy.course')
    attendee_ids = fields.Many2many('res.partner')
    course_description = fields.Text(related="course_id.description")
    color = fields.Integer()
    date = fields.Date(string="Session Date")
    attendee_count = fields.Integer(compute='calculate_occupation', store=True)
    occupation = fields.Float(compute='calculate_occupation')

    # you can use onchange when you want to updates in form view live
    @api.onchange('course_id')
    def onchange_course(self):
        if not self.name:
            if self.course_id:
                self.name = "Session for " + self.course_id.name
            else:
                self.name = ""

    @api.model
    def create(self, values):  # override
        # other code
        return super(Session, self).create(values)

    @api.multi
    def write(self, values):
        # other code
        return super(Session, self).write(values)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        return super(Session, self).copy(default=default)

    @api.multi
    def unlink(self):
        if self.name == "test":
            raise ValidationError(
                "Recrod name having test not deletable")
        return super(Session, self).unlink()

    def do_confirm(self):
        self.state = 'confirmed'

    def do_done(self):
        self.state = 'done'

    # constrains are only checked at the time of save
    @api.constrains('attendee_ids', 'instructor_id')
    def attendee_const(self):
        if self.instructor_id.id in self.attendee_ids.ids:
            raise ValidationError('You can not add instructor in attendee')

    @api.depends('attendee_ids', 'seats')
    def calculate_occupation(self):
        for session in self:
            session.attendee_count = len(session.attendee_ids)
            if session.seats:
                session.occupation = len(
                    session.attendee_ids) * 100 / session.seats
            else:
                session.occupations = 0.0
