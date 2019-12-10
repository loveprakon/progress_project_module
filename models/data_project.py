# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import datetime


class DataProject(osv.Model):
    'model for put data like projectname advisor student blahhh'
    _name = 'data.project'

    _columns = {
        'name': fields.char(
            string='ชื่อโปรเจค',
            required=True,
        ),

        'project_code': fields.char(
            string='รหัส',
        ),

        'course': fields.many2one(
            'input.subject',
            string='รหัสวิชา',
        ),

        'advisor': fields.many2one(
            'input.teacher',
            string='อาจารย์ที่ปรึกษา',
        ),

        'president': fields.many2one(
            'input.teacher',
            string='ประธาน',
        ),

        'commitee': fields.many2one(
            'input.teacher',
            string='กรรมการ',
        ),

        'co_teacher': fields.many2one(
            'input.teacher',
            string='อาจารย์ที่ปรึกษาร่วม',
        ),

        'approval_date': fields.date(
            string='วันที่หัวหน้าภาคอนุมัติ',
        ),

        'student_ids': fields.one2many(
            'provider.in.project',
            'data_project_id',
            string="รายชื่อนักศึกษาที่ทำโปรเจค",
        ),

        'total_name': fields.text(
            string='ชื่อนักศึกษาที่ทำโปรเจค',
        ),

        'total_student_code': fields.text(
            string='รหัสประจำตัวนักศีกษา',
        ),

        'total_major': fields.text(
            string='สาขา',
        ),

        'grade': fields.text(
            string='เกรด',
        ),

    }

    def create(self, cr, uid, value, context=None):
        cr.execute('''
                    SELECT    id
                    FROM      data_project
                    ORDER BY  id DESC LIMIT 1
                ''')
        id_data_project = cr.fetchall()
        years = (datetime.datetime.now()).strftime("%Y")
        if id_data_project:
            number_project = int(id_data_project[0][0]) + 1
        else:
            number_project = 1
        total_name = ''
        total_student_code = ''
        total_major = ''
        id_student = []
        for data_student in value.get('student_ids'):
            cr.execute('''
                        SELECT    name
                        FROM      input_student
                        WHERE     id = %s
                    ''', (data_student[2].get('name'),))
            rec = cr.dictfetchall()[0]
            total_name += rec.get('name') + '\n'
            total_student_code += data_student[2].get('student_code') + '\n'
            total_major += data_student[2].get('major') + '\n'
            id_student.append(data_student[2].get('name'))
        #chaenge fields in_project
        self.change_status_student(cr,state=True,stu_id=id_student)


        value.update({
            'project_code': 'PJ-%s-%s' % (years, number_project),
            'total_name': total_name,
            'total_student_code': total_student_code,
            'total_major': total_major,
        })

        res = super(DataProject, self).create(cr, uid, value, context=context)
        vals = ({
            'name':res
        })
        self.pool.get('progress.exams.line').create(cr, uid, vals, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('grade',False): #update grade to model provider.in.project
            score_obj = self.pool['provider.in.project'].browse(cr, uid, self.pool['provider.in.project']
                                                                .search(cr, uid, [('data_project_id','=',ids[0])]))
            grades = vals.get('grade').split('\n')
            if len(score_obj) != len(grades):
                raise osv.except_osv(('Warning!'), (u"ใส่เกรด นักศึกษา ไม่ครบ"))

            for score_index in range(len(score_obj)):
                score_obj[score_index].write({'grade':grades[score_index]})
        id_student_true = []
        id_student_false = []
        if vals.get('student_ids', False):
            total_name = ''
            total_student_code = ''
            total_major = ''
            for data_student in vals.get('student_ids'):
                if data_student[0] == 4: #replace
                    cr.execute('''
                            select in_s.id,pip.name,in_s.name,in_s.student_code,in_s.major
                            from (select name 
                                  from provider_in_project
                                  where id = %s
                                    ) pip 
                            inner join ( select id,name,student_code,major
                                        from input_student
                                    ) in_s on pip.name = in_s.id
                        ''', (data_student[1], ))
                    rec = cr.dictfetchall()[0]
                    total_name += rec.get('name') + '\n'
                    total_student_code += rec.get('student_code') + '\n'
                    total_major += rec.get('major') + '\n'
                    id_student_true.append(rec.get('id'))


                if  data_student[0] == 0: #update
                    cr.execute('''
                                    SELECT    name
                                    FROM      input_student
                                    WHERE     id = %s
                                ''', (data_student[2].get('name'),))
                    rec = cr.dictfetchall()[0]
                    total_name += rec.get('name') + '\n'
                    total_student_code += data_student[2].get('student_code') + '\n'
                    total_major += data_student[2].get('major') + '\n'
                    id_student_true.append(data_student[2].get('name'))

                if data_student[0] == 2: #delete
                    cr.execute('''
                            select in_s.id,pip.name,in_s.name,in_s.student_code,in_s.major
                            from (select name 
                                  from provider_in_project
                                  where id = %s
                                    ) pip 
                            inner join ( select id,name,student_code,major
                                        from input_student
                                    ) in_s on pip.name = in_s.id
                        ''', (data_student[1], ))
                    rec = cr.dictfetchall()[0]
                    id_student_false.append(rec.get('id'))


                if len(total_name)>1:
                    vals.update({
                    'total_name': total_name,
                    'total_student_code': total_student_code,
                    'total_major': total_major,
                    })

                if id_student_true:
                    self.change_status_student(cr, state=True, stu_id=id_student_true)
                if id_student_false:
                    self.change_status_student(cr, state=False, stu_id=id_student_false)


        return super(DataProject, self).write(cr, uid, ids, vals, context=context)

    def change_status_student(self,cr,stu_id,state):
        'change status student this fuction is called from def create def write'
        cr.execute('''
            UPDATE  input_student
            SET     in_project = %s
            where   id in %s
        ''',(state,tuple(stu_id), ))

    def print_report(self, cr, uid, ids, context=None):
        datas = {
            'model': 'data.project',
            'ids': ids,
            'form': self.pool.get('data.project').read(cr, uid, ids, context=context),
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'data_project_report',
            'datas': datas,
            'nodestroy': True
        }


class ProviderInProject(osv.Model):
    'model for input student to project'
    _name = "provider.in.project"

    _columns = {
        'sequence': fields.integer(
            string='Sequence',
        ),
        'data_project_id': fields.many2one(
            'data.project',
        ),
        'name': fields.many2one(
            'input.student',
            string='ชื่อนักศึกษา',
            required=True),
        'student_code': fields.char(
            string='รหัสนักศึกษา',
        ),
        'major': fields.char(
            string='ห้อง',
        ),
        'grade': fields.char(
            string='ห้อง',
        ),
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ProviderInProject, self).write(cr, uid, ids, vals, context=context)
        print('vals {}'.format(vals))
        if vals.get('grade',False): #recieve grade from project.summary
            cr.execute('''
            with with_score_summary as (
                            select id,student_code,grade,name
                            from provider_in_project
                            where id = %s
                        ),
            with_update as (
                            update score_summary
                            set	write_uid = %s,
                                write_date = current_timestamp::timestamp,
                                grade = wss.grade
                            from with_score_summary as wss
                            where score_summary.name = wss.name
                            returning score_summary.id  as id_update
                    )
            select
                (select max(student_code) from with_score_summary) as amount_write
            ''',(ids[0],uid))
        return res

    def onchange_data_student(self, cr, uid, ids, name, context=None):
        cr.execute('''
            SELECT   name,student_code,major
            FROM     input_student
            WHERE    id = %s
        ''', (name,))
        student_item = cr.dictfetchall()[0]
        return {'value': {'student_code': student_item['student_code'], 'major': student_item['major'], }}
