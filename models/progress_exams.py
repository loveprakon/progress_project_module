# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
from datetime import datetime,date
_logger = logging.getLogger(__name__)

class ProgressExam(osv.Model):
    _name = 'progress.exams'

    _columns = {
        'name': fields.many2one(
            'input.teacher',
            string='อาจารย์ที่ปรึกษา',
            ondelete='cascade',
            readonly=True,
        ),

        'project_ids': fields.one2many(
            'progress.exams.line',
            'advisor',
            string="รายชื่อนักศึกษาที่ทำโปรเจค",
            required=True,
        ),
    }

    def open_wizard(self,cr, uid, *args, **kw):

        return {'type': 'ir.actions.act_window',
                'res_model': 'progress.exams.wizard',
                'view_mode': 'form',
                'res_id': 0,
                'target': 'new'}

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        """ Check advisor false and update"""
        cr.execute("""
                     with tb_advisor_false as (
                             select pr_line.name,
                                     pr_line.advisor as advisor_line,
                                     dp.id,
                                     dp.advisor as advisor_dp
                             from progress_exams_line pr_line
                             inner join (select id,advisor
                                         from data_project
                                         ) dp on pr_line.name =  dp.id
                     )
                     update progress_exams_line
                     set advisor = tb_advisor_false.advisor_dp
                     from tb_advisor_false 
                     where progress_exams_line.name = tb_advisor_false.name
                     and tb_advisor_false.advisor_line != tb_advisor_false.advisor_dp
         """)
        res = super(ProgressExam, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu=submenu)
        return res

class ProgressExamLine(osv.Model):
    _name = 'progress.exams.line'

    _columns = {
        'name': fields.many2one(
            'data.project',
            string='ชื่อโปรเจค',
            ondelete='cascade',
            readonly=True,
        ),

        'advisor': fields.related(
            'name',
            'advisor',
            type="many2one",
            relation="input.teacher",
            string='ที่ปรึกษา',
            readonly=True,
            store=True,
        ),

        'project_code': fields.related(
            'name',
            'project_code',
            type='char',
            string='รหัสโปรเจค',
            readonly=True,
            store=True,
        ),

        'state': fields.related(
            'name',
            'state',
            type='selection',
            string='สถานะ',
            readonly=True,
            store=False,
        ),

        'approval_date':fields.related(
            'name',
            'approval_date',
            type='date',
            string='วันที่หัวหน้าภาคอนุมัติ',
            readonly=True,
            store=False,
        ),

        'total_name': fields.related(
            'name',
            'total_name',
            type='text',
            string='นักศึกษา',
            readonly=True,
            store=True,
        ),

        'total_major': fields.related(
            'name',
            'total_major',
            type='text',
            string='สาขา',
            readonly=True,
            store=True,
        ),

        'room': fields.char(
            string='ห้อง',
        ),

        'date_exam': fields.date(
            string='วันสอบ',
        ),

        'time_exam': fields.char(
            string='เวลาสอบ',
        ),

        'point': fields.integer(
            string='คะแนน',
        ),
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ProgressExamLine, self).write(cr, uid, ids, vals, context=context)
        if vals.get('point', False):
            _logger.info('va {}'.format(type(ids[0])))
            cr.execute(''' 
                        with tb_score as (
                                    select  coalesce(pline.point,0) + coalesce(protect.point,0) as point_sum,	
                                            pp.name as student_id
                                    from progress_exams_line pline 
                                    inner join (select  COALESCE(point,0) as point,
                                                        project_code
                                                from protect_exams_line
                                                ) protect on  pline.project_code = protect.project_code
                                    inner join (select id
                                                from data_project
                                                ) dp on pline.name = dp.id
                                    inner join (select name,
                                                        data_project_id
                                                from provider_in_project
                                                ) pp on pp.data_project_id = dp.id
                        )
                        update score_summary
                        set point = point_sum
                        from tb_score 
                        where score_summary.name = tb_score.student_id
                        and point_sum != 0           
                    ''')

        line_obj = self.browse(cr, uid, ids, context=context)
        pj_obj = self.pool['data.project'].browse(cr, uid, self.pool['data.project']
                                                            .search(cr, uid, [('id','=',line_obj[0].name.id)]))
        pj_obj[0].write({'state':'progress'})
        return res

    def alert_progress_exam(self, cr, uid, ids=None, context=None):
        if context == None:
            context = {}
        context.update({'model':'progress.exams','name':'alert_progress'})
        _logger.info('>>> Alert Progress Exam <<<')
        self.create_email_template(cr, uid,context)
        progress_exams_obj = self.pool.get('progress.exams').search(cr, uid, [], context=context)
        email_template_obj = self.pool.get('email.template')
        template_ids = email_template_obj.search(cr, uid, [('model_id.model', '=', 'progress.exams')], context=context)
        values = email_template_obj.generate_email(cr, uid, template_ids[0], progress_exams_obj[0], context=context)
        cr.execute(''' 
            select dp.name ,
                    pxl.date_exam,
                    pxl.time_exam,
                    pxl.room,
                    it.name,
                    it.email
            from progress_exams_line pxl 
            inner join data_project dp  on pxl.name = dp.id
            inner join input_teacher it on pxl.advisor = it.id 
            where dp.state   = 'progress' 
            and  (pxl.date_exam - interval '1 days')::date = now()::date
        ''')
        for line in  cr.dictfetchall():
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
                        <th>ชื่อโปรเจค</th>
                        <th>วัน</th>
                        <th>เวลา</th>
                        <th>ห้อง</th>
                        <th>อาจารย์</th>
                    </tr>
                    <tr>
                        <th>%s</th>
                        <th>%s</th>
                        <th>%s</th>
                        <th>%s</th>
                        <th>%s</th>
                    </tr>
                    </table>
                    </body>
                    </html>
            
            """%(line.get('project_name','-'),
                 line.get('date_exam','-'),
                 line.get('time_exam','-'),
                 line.get('room','-'),
                 line.get('name','-'))
            values.update({'body_html':body})

            mail = "[%s,]"%(line.get('email',False))
            values.update({'email_to':mail})
            mail_mail_obj = self.pool.get('mail.mail')
            msg_id = mail_mail_obj.create(cr, uid, values, context=context)
            if msg_id:
                mail_mail_obj.send(cr, uid, [msg_id], context=context)
        return True


    def create_email_template(self,cr, uid,context=None):
        email_template_obj = self.pool.get('email.template').search(cr, uid, [('model_id.model', '=', context.get('model'))], context=context)
        if not email_template_obj :
            ir_obj = self.pool.get('ir.model').search(cr, uid, [('model', '=', 'progress.exams')], context=context)
            vals = {'name': context.get('name'),
                    'model_id':ir_obj[0],
                    }
            self.pool.get('email.template').create(cr, uid,vals)






