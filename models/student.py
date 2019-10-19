# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputStudent(osv.Model):
    'Model for input detail of student'
    _name = 'input.student'
    _columns = {
        'student_code': fields.char('รหัสนักศึกษา', size=40, ),
        'name': fields.char('ชื่อจริง-นามสกุล', size=80, ),
        'first_name': fields.char('ชื่อจริง', size=40, ),
        'last_name': fields.char('นามสกุล', size=40, ),
        'major': fields.char('ชื่อย่อสาขา', size=40, ),
    }