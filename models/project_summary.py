# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class ProjectSummary(osv.Model):
    'Model for Summary Project'
    _name = 'project.summary'

    _columns = {
        'name': fields.char(
            string='อาจารย์ที่ปรึกษา',
            readonly=True,
        ),
        'project_qty': fields.integer(
            string='จำนวนโปรเจค',
            readonly=True,
        ),
        'monogram': fields.char(
            string='ชื่อย่อ',
            required=True,
        ),

        'data_project_ids': fields.one2many(
            'data.project',
            'advisor',
            string = "โปรเจค",
        ),


    }

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        if view_type == 'search':
            cr.execute('''
               WITH with_project_summary_qty as (
                        select count(dp.advisor) as qty ,dp.advisor,it.monogram
                        from data_project dp
                        inner join (select id,monogram
                                    from input_teacher ) it on dp.advisor = it.id
                        group by advisor,it.monogram
                        ),
                with_update_project_summary_qty as (
                        update project_summary
                        set	write_uid = %s,
                            write_date = current_timestamp::timestamp,
                            project_qty = wpsq.qty
                        from with_project_summary_qty as  wpsq
                        where project_summary.monogram = wpsq.monogram
                        returning project_summary.monogram as id_update
                        )
                select 
	                (select sum(qty) from with_project_summary_qty) as amount_create
            ''', (uid,))
            cr.commit()

        res = super(ProjectSummary, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar,
                                                    submenu=submenu)
        return res

