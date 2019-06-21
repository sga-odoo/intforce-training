# -*- coding: utf-8 -*-

from odoo import models, fields


class Wizard_Course(models.TransientModel):
    _name = 'wiz.openacademy.course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    def add_session(self):
        for course_id in self._context.get('active_ids', []):
            self.env['openacademy.session'].create({
                'name': self.name,
                'description': self.description,
                'course_id': course_id
            })
