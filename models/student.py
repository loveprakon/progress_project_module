# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputStudent(osv.Model):
    'Model for input detail of student'
    _name = 'input.student'
    _columns = {
        'student_code': fields.char(
            string = 'รหัสนักศึกษา',
            required = True),
        'name': fields.char(
            string = 'ชื่อจริง-นามสกุล',
            ),
        'first_name': fields.char(
            string = 'ชื่อจริง',
            required = True),
        'last_name': fields.char(
            string = 'นามสกุล',
            required = True),
        'major': fields.char(
            string = 'ชื่อย่อสาขา',
            required = True),
    }

    def create(self,cr, uid, value, context=None):
        value.update({
            'name':value['first_name'] +' '+ value['last_name']
        })
        return super(InputStudent, self).create(cr, uid, value, context=context)