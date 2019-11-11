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

    def send_email(self, cr, uid, ids=None, context=None):
        """notifications about grade that has null to teacher and will set grade"""
        _logger.info('send_email')
        cr.execute(''' 
        
        
        ''')


        cr.execute('''
                    select ss.student_code,
                            ss.name,
                            coalesce(da_p.name,'') as project_name,
                            coalesce(advisor.name,'') as advisor
                    from ( select student_code,name
                            from score_summary
                            where grade = 'I'
                        ) ss
                    left join (select student_code as student_code_in_project,
                                data_project_id
                                from provider_in_project) pip on ss.student_code = pip.student_code_in_project
                    left join (select advisor,name,id
                                from data_project 
                                )da_p on pip.data_project_id = da_p.id
                    left join (select id,name 
                                from input_teacher
                                ) advisor  on advisor.id =  da_p.advisor        
                    ''')

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
