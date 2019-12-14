# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class ProtectExamsWizard(osv.TransientModel):
    _name = 'protect.exams.wizard'
    _columns = {
        'head':  fields.text(
            string = 'Head',
            required=True,
        ),
        'project_ids':fields.many2many(
            'data.project',
            'data_project_protect_rel',
            string = 'โปรเจค',
            required=True,
        )
    }
    _defaults = {
        'head': 'สอบป้องกัน',
    }


    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'protect.exams.wizard',
            'form': data
        }
        _logger.info('data {}'.format(datas))
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'protect_exams_report',
            'datas': datas,
        }

ProtectExamsWizard()
