# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import datetime


class ScoreSummary(osv.Model):
    'model for show point and grade each student'
    _name = 'score.summary'

    _columns = {
        'name': fields.char(
            string='ชื่อโปรเจค',
            required=True,
        ),
        'major': fields.char(
            string='',
            required=True,
        ),
        'point': fields.char(
            string='ชื่อโปรเจค',
            required=True,
        ),
        'grade': fields.char(
            string='ชื่อโปรเจค',
            required=True,
        ),

    }