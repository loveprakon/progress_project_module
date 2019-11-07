# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)


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

    def test_scheduler(self, cr, uid, ids=None, context=None):
        _logger.info("Scheduler Testing" + str(datetime.today()))
        return True

    def give_grade_i(self, cr, uid, ids=None, context=None):
        """ give grade i for student that doesn't grade"""
        _logger.info("Scheduler Testing Grade" + str(datetime.today()))
        cr.execute('''
                update score_summary
                set	write_uid = %s,
                    write_date = current_timestamp::timestamp,
                    grade = 'I'
                Where grade is null
                ''',(uid, ))
        return True



    def send_email(self, cr, uid, ids, cron_mode=True, context=None):
        """notifications about grade that has null to teacher and will set grade"""
        cr.execute('''
                 
        
        ''')
        return True