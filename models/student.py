# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
_logger = logging.getLogger(__name__)

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
        'in_project' : fields.boolean(
            string = 'in_project'
        )
    }

    _defaults = {
        'in_project': 0,
    }

    def create(self,cr, uid, value, context=None):
        value.update({
            'name':value['first_name'] +' '+ value['last_name']
        })
        res = super(InputStudent, self).create(cr, uid, value, context=context)
        vals = ({
            'name':res
        })
        self.pool.get('score.summary').create(cr, uid, vals, context=context)
        return res


