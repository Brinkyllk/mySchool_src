import xlwt
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
import logging

_ir_translation_name = 'op.enrollment.analysis.xls'


class op_enrollment_analysis_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(op_enrollment_analysis_parser, self).__init__(
            cr, uid, name, context=context)

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        return translate(self.cr, _ir_translation_name, 'report', lang, src) or src


class op_enrollment_analysis_xls(report_xls):
    def __init__(self, name, table, rml=False, parser=False, header=False,
                 store=False):
        super(op_enrollment_analysis_xls, self).__init__(
            name, table, rml, parser, header, store)

        # Cell Styles
        _xs = self.xls_styles
        # header
        rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        self.rh_cell_style = xlwt.easyxf(rh_cell_format)
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

        #  Column Spec
        self.col_specs_template = {
            'batch_code': {
                'header': [2, 8, 'text', _render("'Batch CODE'")],
                'lines': [2, 0, 'text', _render("(str(line['batch_code']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'name': {
                'header': [2, 8, 'text', _render("'Batch NAME'")],
                'lines': [2, 0, 'text', _render("(str(line['name']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'std_code': {
                'header': [3, 8, 'text', _render("'Study Programme CODE'")],
                'lines': [3, 0, 'text', _render("(str(line['std_code']) or '-')")],
                'totals': [3, 0, 'text', None]},
            'std_name': {
                'header': [3, 8, 'text', _render("'Study Programme NAME'")],
                'lines': [3, 0, 'text', _render("(str(line['std_name']) or '-')")],
                'totals': [3, 0, 'text', None]},
            'enrollments': {
                'header': [2, 8, 'text', _render("'Enrollments'")],
                'lines': [2, 0, 'number', _render("(line['enrollments'])")],
                'totals': [2, 0, 'text', None]},
        }

        self.wanted_list = ['batch_code', 'name', 'std_code', 'std_name', 'enrollments']

    def get_data(self, params):

        sql = """
        SELECT DISTINCT ba.batch_code, ba.name,

        (SELECT stpr.code FROM  op_study_programme as stpr
        WHERE (ba.study_prog_code = stpr.id)) as std_code,

        (SELECT stpr.name FROM  op_study_programme as stpr
        WHERE (ba.study_prog_code = stpr.id)) as std_name,

        (SELECT count(en.id) FROM op_enrollment as en
        WHERE (en.batch_code = ba.id))as enrollments

        FROM op_batch as ba,op_enrollment as en  WHERE (ba.id = en.batch_code)
        """

        self.cr.execute(sql)
        val = self.cr.dictfetchall()
        return val

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        # Initialize workbook 1
        report_name = _("Enrollment Analysis Report")
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
        cell_style = xlwt.easyxf(_xs['xls_title'])
        c_specs = [
            ('report_name', 5, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, ['report_name'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

        # Report Info
        c_specs = [
            ('dt', 2, 0, 'text', "Date Range", None, self.rh_cell_style_right),
            ('st_dt', 4, 0, 'text', (' From ' + data['start_date'] + ' To ' + data['end_date'])),
        ]
        row_data = self.xls_row_template(c_specs, ['st_pr', 'stpr_nm', 'dt', 'st_dt'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.aml_cell_style)
        row_pos += 1

        # Column headers
        c_specs = map(lambda x: self.render(
            x, self.col_specs_template, 'header',),self.wanted_list)
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=self.rh_cell_style,
            set_column_size=True)
        ws.set_horz_split_pos(row_pos)

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


op_enrollment_analysis_xls('report.op.enrollment.analysis.xls', 'crm.lead',
                         parser=op_enrollment_analysis_parser)