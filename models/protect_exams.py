# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import logging
from datetime import datetime,date
_logger = logging.getLogger(__name__)

class ProtectExams(osv.Model):
    _name = 'protect.exams'

    _columns = {
        'name': fields.many2one(
            'input.teacher',
            string='อาจารย์ที่ปรึกษา',
            ondelete='cascade',
            readonly=True,
        ),

        'project_ids': fields.one2many(
            'protect.exams.line',
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
        res = super(ProtectExams, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu=submenu)
        return res

class ProtectExamsLine(osv.Model):
    _name = 'protect.exams.line'

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

        'approval_date':fields.related(
            'name',
            'approval_date',
            type='date',
            string='วันที่หัวหน้าภาคอนุมัติ',
            readonly=True,
            store=True,
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
        res = super(ProtectExamsLine, self).write(cr, uid, ids, vals, context=context)
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
        return res