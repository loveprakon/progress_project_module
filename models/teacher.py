# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
_logger = logging.getLogger(__name__)

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
        'email': fields.char(
            string='อีเมลล์',
        ),

    }

    def create(self, cr, uid, value, context=None):
        res = super(InputTeacher, self).create(cr, uid, value, context=context)
        vals = ({
            'name':res
        })
        self.pool.get('project.summary').create(cr, uid, vals, context=context)
        self.pool.get('progress.exams').create(cr, uid, vals, context=context)
        return res


