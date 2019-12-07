# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class ProgressExamsWizard(osv.TransientModel):
    _name = 'progress.exams.wizard'
    _columns = {
        'head':  fields.text('Head', required=True),
    }
    _defaults = {
        'head': 'สอบก้าวหน้า',
    }


    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'progress.exams.wizard',
            'form': data
        }
        _logger.info('data {}'.format(datas))
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'progress_exams_report',
            'datas': datas,
        }

ProgressExamsWizard()
