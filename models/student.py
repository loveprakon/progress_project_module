# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class InputStudent(osv.Model):
    'Model for input detail of student'
    _name = 'input.student'
    _columns = {
        'student_code': fields.char(
            string = 'รหัสนักศึกษา',
            required = True),
        'name': fields.char(
            string = 'ชื่อจริง-นามสกุล',
            ),
        'first_name': fields.char(
            string = 'ชื่อจริง',
            required = True),
        'last_name': fields.char(
            string = 'นามสกุล',
            required = True),
        'major': fields.char(
            string = 'ชื่อย่อสาขา',
            required = True),
        'in_project' : fields.boolean(
            string = 'in_project'
        )
    }

    _defaults = {
        'in_project': 0,
    }

    def create(self,cr, uid, value, context=None):
        value.update({
            'name':value['first_name'] +' '+ value['last_name']
        })
        res = super(InputStudent, self).create(cr, uid, value, context=context)
        cr.execute('''
                    INSERT INTO score_summary
                    (name,major) 
                    values      (%s,%s)
                ''', (value.get('name'),value.get('major')))

        return res


    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('first_name',False) or vals.get('last_name',False):
            inputstudent_obj = self.browse(cr, uid, ids, context=context)
            vals.update({'name':vals.get('first_name',inputstudent_obj[0].first_name)+' '
                                +vals.get('last_name',inputstudent_obj[0].last_name),
            })
        res = super(InputStudent, self).write(cr, uid, ids, vals, context=context)
        cr.execute('''
                    with with_score_summary as (
                            select id,name,major,student_code
                            from input_student
                            where id in %s
                        ),
                    with_update as (
                            update score_summary
                            set	write_uid = %s,
                            write_date = current_timestamp::timestamp,
                            major = wss.major,
                            name = wss.name,
                            student_code = wss.student_code
                    from with_score_summary as wss
                    where score_summary.id = wss.id
                    returning score_summary.id  as id_update
                    )
                    select 
                    (select max(name) from with_score_summary) as amount_create
            ''',(tuple(ids),uid))
        return res


