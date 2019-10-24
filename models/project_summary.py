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
        'data_project_ids': fields.one2many(
            'data.project',
            'advisor',
            string = "โปรเจค",
        ),

    }

    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        print('pass')
        print((self._columns.get('name')))
        return True
