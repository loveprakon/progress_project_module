from report import report_sxw
import logging
_logger = logging.getLogger(__name__)
import time

class ReportDataProject(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ReportDataProject, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'detail_pro':self.detail_pro,
            'format_date':self.format_date,
            'teacher': self.teacher
        })
    def detail_pro(self):
        rec = self.pool.get('data.project')
        rec = rec.browse(self.cr, self.uid, self.pool['data.project']
                                    .search(self.cr, self.uid, []))
        return rec

    def format_date(self,date):
        if date:
            format_date = date.split('-')
            date = format_date[2]+'/'+format_date[1]+'/'+format_date[0]
            return date
        return '-'

    def teacher(self):
        rec = self.pool.get('input.teacher')
        rec = rec.browse(self.cr, self.uid, self.pool['input.teacher']
                         .search(self.cr, self.uid, []))
        return rec

report_sxw.report_sxw('report.data_project_report', 'data.project',
                      'progress_project_module/report/data_project_report.rml'
                      , parser=ReportDataProject,
                      header='')
