from report import report_sxw
import logging
_logger = logging.getLogger(__name__)
import time

class ReportProgressExams(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ReportProgressExams, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'proj_obj':self.proj_obj,
        })

    def proj_obj(self,pro_ids):
        rec = self.pool.get('data.project')
        rec = rec.browse(self.cr, self.uid, self.pool['data.project']
                                    .search(self.cr, self.uid, [('id','in',pro_ids)]))
        return rec

report_sxw.report_sxw('report.progress_exams_report', 'progress.exams.wizard',
                      'progress_project_module/report/progress_exams_report.rml'
                      , parser=ReportProgressExams,
                      header='')
