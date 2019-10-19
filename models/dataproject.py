# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class DataProject(osv.model):
    'model for put data like projectname advisor student blahhh'
    _name = "data.project"

    _columns = {
        'name': fields.char('ชื่อโปรเจค', required=True, ),
        'project_code': fields.char('รหัส', size=50, ),
        'course': fields.many2one('progress.subject', 'รหัสวิชา'),
        'teacher': fields.many2one('progress.input.teacher', 'อาจารย์ที่ปรึกษา'),
        'president': fields.many2one('progress.input.teacher', 'ประธาน'),
        'commitee': fields.many2one('progress.input.teacher', 'กรรมการ'),
        'co_teacher': fields.many2one('progress.input.teacher', 'อาจารย์ที่ปรึกษาร่วม'),
        'approval_date': fields.date('วันที่หัวหน้าภาคอนุมัติ'),
        'student_menu_ids': fields.one2many('progress.show.student', 'student_menu_id',
                                            string="รายชื่อนักศึกษาที่ทำโปรเจค", ondelete='cascade'),
        'total_name': fields.char('ชื่อนักศึกษาที่ทำโปรเจค', size=250, ),
        'total_id_student': fields.char('รหัสประจำตัวนักศีกษา', size=250, ),
        'total_major': fields.char('สาขา', size=250, ),
        }
