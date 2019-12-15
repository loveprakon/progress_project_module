from report import report_sxw
import logging
_logger = logging.getLogger(__name__)
import time

class ReportProtectExams(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ReportProtectExams, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'proj_obj':self.proj_obj,
            'format_date':self.format_date,
        })

    def proj_obj(self,pro_ids):
        rec = self.pool.get('protect.exams.line')
        rec = rec.browse(self.cr, self.uid, self.pool['protect.exams.line']
                                    .search(self.cr, self.uid, [('name','in',pro_ids)]))
        return rec

    def format_date(self,date):
        if date:
            format_date = date.split('-')
            date = format_date[2]+'/'+format_date[1]+'/'+format_date[0]
            return date
        return '-'

report_sxw.report_sxw('report.protect_exams_report', 'protect.exams.wizard',
                      'protect_project_module/report/protect_exams_report.rml'
                      , parser=ReportProtectExams,
                      header='')
