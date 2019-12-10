from report import report_sxw
import logging
_logger = logging.getLogger(__name__)
import time

class ReportProgressExams(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ReportProgressExams, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'proj_obj':self.proj_obj,
            'format_date':self.format_date,
        })

    def proj_obj(self,pro_ids):
        rec = self.pool.get('progress.exams.line')
        rec = rec.browse(self.cr, self.uid, self.pool['progress.exams.line']
                                    .search(self.cr, self.uid, [('name','in',pro_ids)]))
        return rec

    def format_date(self,date):
        if date:
            format_date = date.split('-')
            date = format_date[2]+'/'+format_date[1]+'/'+format_date[0]
            return date
        return '-'

report_sxw.report_sxw('report.progress_exams_report', 'progress.exams.wizard',
                      'progress_project_module/report/progress_exams_report.rml'
                      , parser=ReportProgressExams,
                      header='')
