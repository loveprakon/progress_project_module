# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import datetime


class ScoreSummary(osv.Model):
    'model for show point and grade each student'
    _name = 'score.summary'

    _columns = {
        'name': fields.char(
            string='ชื่อนักศึกษา',
        ),
        'student_code': fields.char(
            string='รหัสนักศึกษา',
        ),
        'major': fields.char(
            string='สาขา',
        ),
        'point': fields.char(
            string='คะแนน',
        ),
        'grade': fields.char(
            string='เกรด',
        ),

    }