# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputTeacher(osv.Model):
    'model for put Teacher name'
    _name = 'input.teacher'

    _columns = {
        'name': fields.char(
            string = 'ชื่อ-นามสกุล',
            required=True,
        ),
        'monogram': fields.char(
            string = 'ชื่อย่อ',
            required=True,
        ),
        'department': fields.char(
            string = 'แผนก',
            required=True,
        ),
    }

    def create(self, cr, uid, value, context=None):
        res = super(InputTeacher, self).create(cr, uid, value, context=context)
        cr.execute('''
                    INSERT INTO project_summary
                    (name) 
                    values      (%s)
                    
                ''',(value.get('name'), ))

        return res


