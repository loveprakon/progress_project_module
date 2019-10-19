# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputSubject(osv.model):
    'model for put subjectname'
    _name = "input.subject"

    _columns = {
        'name': fields.char('ชื่อวิชา', size=40),
    }