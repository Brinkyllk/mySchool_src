import xlwt
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
import logging

_ir_translation_name = 'op.crm.employee.performance.analysis.xls'

# ... Get current date .... s#
printed_date = datetime.today().now()
printed_date = printed_date.strftime('%Y-%m-%d')


class op_crm_employee_performance_analysis_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(op_crm_employee_performance_analysis_parser, self).__init__(
            cr, uid, name, context=context)

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        return translate(self.cr, _ir_translation_name, 'report', lang, src) or src


class op_crm_employee_performance_analysis_xls(report_xls):
    def __init__(self, name, table, rml=False, parser=False, header=False,
                 store=False):
        super(op_crm_employee_performance_analysis_xls, self).__init__(
            name, table, rml, parser, header, store)

        # Cell Styles
        _xs = self.xls_styles
        # header
        rh_cell_format = _xs['bold'] + _xs['fill_grey'] + _xs['borders_all']
        self.rh_cell_style = xlwt.easyxf(rh_cell_format)
        self.rh_cell_style_left = xlwt.easyxf(rh_cell_format + _xs['left'])
        self.rh_cell_style_center = xlwt.easyxf(rh_cell_format + _xs['center'])
        self.rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['right'])
        # lines
        aml_cell_format = _xs['borders_all']
        self.aml_cell_style = xlwt.easyxf(aml_cell_format)
        self.aml_cell_style_center = xlwt.easyxf(
            aml_cell_format + _xs['center'])
        self.aml_cell_style_date = xlwt.easyxf(
            aml_cell_format + _xs['left'],
            num_format_str=report_xls.date_format)
        self.aml_cell_style_decimal = xlwt.easyxf(
            aml_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # totals
        rt_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rt_cell_style = xlwt.easyxf(rt_cell_format)
        self.rt_cell_style_right = xlwt.easyxf(rt_cell_format + _xs['right'])
        self.rt_cell_style_decimal = xlwt.easyxf(
            rt_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)

        # Column Spec
        self.col_specs_template = {
            'id': {
                'header': [1, 8, 'text', _render("'ID'")],
                'lines': [1, 0, 'number', _render("(line['id'] )")],
                'totals': [1, 0, 'text', None]},
            'code': {
                'header': [2, 8, 'text', _render("'Code'")],
                'lines': [2, 0, 'text', _render("(str(line['code']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'name': {
                'header': [2, 8, 'text', _render("'Name'")],
                'lines': [2, 0, 'text', _render("(str(line['name']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'leads': {
                'header': [2, 8, 'text', _render("'No.Of Inquiries'")],
                'lines': [2, 0, 'number', _render("(line['leads'])")],
                'totals': [2, 0, 'text', None]},
            'enrollments': {
                'header': [2, 8, 'text', _render("'No.Of Enrolled'")],
                'lines': [2, 0, 'number', _render("(line['enrollments'] )")],
                'totals': [2, 0, 'text', None]},

        }

        self.wanted_list = ['id', 'code', 'name', 'leads', 'enrollments'
        ]

    def get_data(self, params):
        st = params['start_date']
        end = params['end_date']
        usr_id = params['user_id']

        if usr_id != False:
            sql ="""
            SELECT
              DISTINCT
              stpr.id,
              stpr.code,
              stpr.name,

                (select count(cl.id) from crm_lead as cl,op_study_programme_lead_rel as splr
                where
                  (cl.user_id = '%(usr_id)d') and (cl.id = splr.lead_id) and (splr.study_programme_id = stpr.id)) as leads,

                (select count(cl.id) from crm_lead as cl,op_study_programme_lead_rel as splr
                where
                (cl.user_id = '%(usr_id)d')and (cl.id = splr.lead_id) and (cl.stage_id = 6) and (splr.study_programme_id = stpr.id)) as enrollments

            FROM op_study_programme as stpr, crm_lead as lead, op_study_programme_lead_rel as splr
            WHERE (splr.lead_id = lead.id) AND (lead.user_id = '%(usr_id)d') AND (splr.study_programme_id = stpr.id)
            AND ((lead.inquiry_date) BETWEEN ('%(st)s')AND( '%(end)s'))
            """% ({'usr_id': usr_id, 'st':st, 'end':end})
        else:
            sql="""
            SELECT
              DISTINCT
              stpr.id,
              stpr.code,
              stpr.name,

                (select count(cl.id) from crm_lead as cl,op_study_programme_lead_rel as splr
                where
                (cl.user_id = users.id) and (cl.id = splr.lead_id) and (splr.study_programme_id = stpr.id)) as leads,

                (select count(cl.id) from crm_lead as cl,op_study_programme_lead_rel as splr
                where
                (cl.user_id = users.id)and (cl.id = splr.lead_id) and (cl.stage_id = 6) and (splr.study_programme_id = stpr.id)) as enrollments

            FROM op_study_programme as stpr, crm_lead as lead, res_users as users, op_study_programme_lead_rel as splr
            WHERE (splr.lead_id = lead.id) AND (lead.user_id = users.id) AND (splr.study_programme_id = stpr.id)
            AND ((lead.inquiry_date) BETWEEN ('%(st)s')AND( '%(end)s'))
            """% ({'st': st, 'end': end})
        self.cr.execute(sql)
        val = self.cr.dictfetchall()
        return val

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        new = data['user_name']
        if new == False:
            new = 'All'

        # Initialize workbook 1
        report_name = _("Employee Performance Analysis Report")
        ws = wb.add_sheet(report_name[18:])
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0

        # set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']

        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'] + _xs['center'])
        c_specs = [
            ('re_name', 2, 0, 'text', "Report", None, self.rh_cell_style_left),
            ('report_name', 5, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, ['re_name', 'report_name'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

        # Employee Name
        cell_style = xlwt.easyxf(_xs['xls_title'] + _xs['center'])
        c_specs = [
            ('st_pr', 2, 0, 'text', "Employee Name", None, self.rh_cell_style_left),
            ('stpr_nm', 3, 0, 'text', new),
        ]
        row_data = self.xls_row_template(c_specs, ['st_pr', 'stpr_nm'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

        # Report Info
        c_specs = [
            ('from', 2, 0, 'text', "From", None, self.rh_cell_style_left),
            ('st_dt', 3, 0, 'text', (data['start_date'])),
            ('to', 2, 0, 'text', "To", None, self.rh_cell_style_left),
            ('end_dt', 3, 0, 'text', (data['end_date'])),
            ]
        row_data = self.xls_row_template(c_specs, ['from', 'st_dt', 'to', 'end_dt'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.aml_cell_style_center)
        row_pos += 3

        # Column headers
        report_info_cell_style = xlwt.easyxf(_xs['borders_all'] + _xs['center'] + _xs['fill_grey'])
        c_specs = map(lambda x: self.render(
            x, self.col_specs_template, 'header',),self.wanted_list)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=report_info_cell_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)

        # Lines
        lines = self.get_data(params=data)
        for line in lines:
            c_specs = map(
                lambda x: self.render(x, self.col_specs_template,
                                      'lines'), self.wanted_list)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=self.aml_cell_style)
        row_pos += 1

        # Report Creator
        cell_style = xlwt.easyxf(_xs['left'])
        c_specs = [
            ('user', 5, 0, 'text', ("Generated By " + data['uname'] + ' on ' + printed_date))
        ]
        row_data = self.xls_row_template(c_specs, ['user'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

op_crm_employee_performance_analysis_xls('report.op.crm.employee.performance.analysis.xls', 'crm.lead',
                         parser=op_crm_employee_performance_analysis_parser)