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
                        with tb_point as (    
                                        select pline.point as point,
                                                dp.id as p_id,
                                                pp.name as student_id
                                        from protect_exams_line pline 
                                        inner join (select id
                                                    from data_project
                                                    ) dp on pline.name = dp.id
                                        inner join (select name,
                                                            data_project_id
                                                    from provider_in_project
                                                    ) pp on pp.data_project_id = dp.id
                                        where pline.id = %s
                        )
                        update score_summary ss
                        set point = tb_point.point
                        from tb_point 
                        where  ss.id = tb_point.student_id            
                    ''',(ids[0],))
        return res