# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputTeacher(osv.model):
    'model for put Teacher name'
    _name = "input.teacher"

    class progress_input_teacher(osv.Model):
        'Model for input detail of teacher'
        _name = 'progress.input.teacher'

        _columns = {
            'name': fields.char('ชื่อ-นามสกุล', size=200, required=True, ),
            'monogram': fields.char('ชื่อย่อ', size=100, required=True, ),
            'department': fields.char('แผนก', size=200, required=True, ),
        }