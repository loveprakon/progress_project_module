# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
from datetime import datetime,date
_logger = logging.getLogger(__name__)


class ScoreSummary(osv.Model):
    'model for show point and grade each student'
    _name = 'score.summary'

    _columns = {
        'name': fields.many2one(
            'input.student',
            string='ชื่อนักศึกษา',
            ondelete='cascade',
        ),
        'student_code': fields.related(
            'name',
            'student_code',
            type = 'char',
            relation='input.student',
            string='รหัสนักศึกษา',
            store = True
        ),
        'major': fields.related(
            'name',
            'major',
            type = 'char',
            relation='input.student',
            string='สาขา',
            store = True
        ),
        'point': fields.integer(
            string='คะแนน',
        ),
        'grade': fields.char(
            string='เกรด',
        ),

    }

    def send_email(self, cr, uid,ids,*args):
        _logger.info('cron job send_email ids {}'.format(ids))
        """notifications about grade that has null to teacher and will set grade"""

        cr.execute(''' select name,
                        (nextcall + interval '7 hour')::date as dead_date_line,
                        (nextcall + interval '7 hour')::time as dead_time_line,
                        (now())::date as now_time
                        from ir_cron 
                        where function = 'give_grade_i'
                        and active = True
                     ''')
        time_items = cr.dictfetchall()
        if len(time_items) > 0:
            time_items = time_items[0]
            dead_date_line = time_items.get('dead_date_line').split('-')
            now_time = time_items.get('now_time').split('-')
            t1 = datetime(year = int(dead_date_line[0]), month = int(dead_date_line[1]), day = int(dead_date_line[2]))
            t2 = datetime(year=int(now_time[0]), month=int(now_time[1]), day=int(now_time[2]))
            deadline = t1 - t2
            for day in args: #day before deadline
                if int(day) == deadline.days:
                    cr.execute('''
                        select ss.student_code,
                                ss.name,
                                coalesce(da_p.name,'-') as project_name,
                                coalesce(advisor.name,'-') as advisor
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
                    query_results = cr.dictfetchall()
                    if query_results:  #if query_results have data
                        self.send_email_action(cr,uid,query_results=query_results,deadline= dead_date_line)

        return True

    def send_email_action(self, cr, uid, query_results,deadline,context=None,):
        email_template_obj = self.pool.get('email.template')
        score_summary_obj = self.pool.get('score.summary').search(cr, uid, [], context=context)
        template_ids = email_template_obj.search(cr, uid, [('model_id.model', '=', 'score.summary')], context=context)
        if template_ids and score_summary_obj:
            values = email_template_obj.generate_email(cr, uid, template_ids[0], score_summary_obj[0], context=context)
            subject = ''
            subject_str = values.get('subject',False)
            if subject_str:
                rec = self.pool.get('input.subject')
                rec = rec.browse(cr,uid,self.pool['input.subject']
                                 .search(cr,uid, []))
                deadline = deadline[2] + ' ' + deadline[1] + ' ' + deadline[0]
                subject = subject_str +' '+rec[0].name + '\n' + u'ตัดเกรดวันที่ ' + u'%s'%(deadline)
                values.update({
                    'subject':subject
                })

            student = ''
            mail = []
            for query_result in query_results:
                student += '<tr><td>%s</td><td>%s' \
                          '</td><td>%s</td><td>%s</td>'%(query_result.get('student_code'),
                                                                query_result.get('name'),
                                                                query_result.get('project_name'),
                                                                query_result.get('advisor')
                                                                )
            cr.execute('''select email
                         from input_teacher
                          where email is not null

            ''')
            query_results = cr.dictfetchall()
            for query_result in query_results:
                mail.append(query_result.get('email'))
            # body = u'<table><tbody>{}</tbody></table>'.format(student)
            body = u"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    .table_log {
                        border: 1px solid black;
                        }
                    .table_log tr{
                        border: 1px solid black;
                        }
                    .table_log td{
                        border: 1px solid black;
                        }
                    .table_log th{
                        border: 1px solid black;
                        }
                </style>
                </head>
                <body>
                <table class="table_log">
                <tr>
                    <th>รหัสนักศึกษา</th>
                    <th>ชื่อ-นามสกุล</th>
                    <th>โปรเจค</th>
                    <th>อาจารย์ที่ปรึกษา</th>
                </tr>
                  %s
                </table>
                </body>
                </html>
                """%(student,)

            values.update({'body_html':body})
            values.update({'email_recipients': mail})
            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)
            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)
        return True

    def give_grade_i(self, cr, uid, ids=None, context=None):
        """ give grade i for student that doesn't grade"""
        cr.execute('''
                update score_summary
                set	write_uid = %s,
                    write_date = current_timestamp::timestamp,
                    grade = 'I'
                Where grade is null
                ''',(uid, ))
        return True

    def open_wizard(self,cr, uid, *args, **kw):

        return {'type': 'ir.actions.act_window',
                'res_model': 'progress.exams.wizard',
                'view_mode': 'form',
                'res_id': 0,
                'target': 'new'}
