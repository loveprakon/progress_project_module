# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputSubject(osv.Model):
    'model for put subjectname'
    _name = "input.subject"

    _columns = {
        'name': fields.char(
         string = 'ชื่อวิชา',
         required = True,
        ),
    }