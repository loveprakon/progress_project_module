# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from bs4 import BeautifulSoup
from openerp.tools.translate import _
import logging,requests,pandas
_logger = logging.getLogger(__name__)

class GetTeacherFromWebWizard(osv.TransientModel):
    _name = 'get.teacher.from.web.wizard'

    def _get_teacher(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        re_obj = requests.get('http://elec.cit.kmutnb.ac.th/?p=2400')
        bea_obj = BeautifulSoup(re_obj.text,'lxml')
        tag_figure = bea_obj.find_all('figure',{'class':'aligncenter'})

        teacher_list = []
        for i in range((len(tag_figure))):
            _logger.info(i)
            tag_a = tag_figure[i].find_all('a')
            if tag_a == []:
                continue

            re_obj = requests.get('{}'.format(tag_a[0]['href']))
            bea_obj = BeautifulSoup(re_obj.text,'lxml')
            tag_class = bea_obj.find_all('div',{'class':'profile-info'})
            tag_h4 = tag_class[0].find_all('h4')
            tag_ul_mail = tag_class[0].find_all('ul',{'class':'list-unstyled disp_group_commu'})
            tag_li_mail = tag_ul_mail[0].find_all('li')
            tag_a_mail =  tag_li_mail[0].find_all('a')
            if tag_a_mail == []:
                mail = None
            else:
                mail = tag_a_mail[0].text
            new_line = { 'name': tag_h4[0].text,
                         'department':'EnET',
                         'email':mail,
                        }
            teacher_list.append((0,0,new_line))
        return teacher_list

    def get_teacher_to_db(self, cr, uid, ids, context=None):
        for teacher_id in self.read(cr, uid, ids):
            cr.execute("""
                select name,monogram,department,email
                from get_teacher_from_web_line
                where id in %s
            """,(tuple(teacher_id['teacher_line']), ))
        teacher_items = cr.dictfetchall()
        for teacher in teacher_items:
            teacher_obj = self.pool.get('input.teacher')
            teacher_obj.create(cr, uid, teacher, context=context)



        return True


    _columns = {
        'name':  fields.char(
            string = 'name',
        ),
        'teacher_line': fields.one2many(
            'get.teacher.from.web.line',
            'order_id',
            string='TeacherLine',

        )

    }
    _defaults = {
        'teacher_line': _get_teacher,
    }





class GetTeacherFromWebLine(osv.osv_memory):
    _name = 'get.teacher.from.web.line'
    _columns = {

        'name': fields.char(
            string = 'ชื่อ-นามสกุล',
        ),
        'monogram': fields.char(
            string = 'ชื่อย่อ',
        ),
        'department': fields.char(
            string = 'แผนก',
        ),
        'email': fields.char(
            string='อีเมลล์',
        ),
        'order_id': fields.many2one(
            'get.teacher.from.web.wizard'
        ),

    }
