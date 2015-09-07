import xlwt
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
import logging

_ir_translation_name = 'op.followup.actions.detail.analysis.xls'


class op_followup_actions_detail_analysis_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(op_followup_actions_detail_analysis_parser, self).__init__(
            cr, uid, name, context=context)

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        return translate(self.cr, _ir_translation_name, 'report', lang, src) or src


class op_followup_actions_detail_analysis_xls(report_xls):
    def __init__(self, name, table, rml=False, parser=False, header=False,
                 store=False):
        super(op_followup_actions_detail_analysis_xls, self).__init__(
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

        # Column Spec
        self.col_specs_template = {
            'id': {
                'header': [1, 8, 'text', _render("'ID'")],
                'lines': [1, 0, 'number', _render("(line['id'] )")],
                'totals': [1, 0, 'text', None]},
            'first_name': {
                'header': [2, 10, 'text', _render("'First Name'")],
                'lines': [2, 0, 'text', _render("(str(line['first_name']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'last_name': {
                'header': [2, 10, 'text', _render("'Last Name'")],
                'lines': [2, 0, 'text', _render("(str(line['last_name']) or '-')")],
                'totals': [2, 0, 'text', None]},
            'studypro_code': {
                'header': [2, 8, 'text', _render("'Study Programme Code'")],
                'lines': [2, 0, 'number', _render("(line['studypro_code'])")],
                'totals': [2, 0, 'text', None]},
            'studypro_name': {
                'header': [2, 8, 'text', _render("'Study Programme Name'")],
                'lines': [2, 0, 'number', _render("(line['studypro_name'] )")],
                'totals': [2, 0, 'text', None]},
            'status': {
                'header': [2, 8, 'text', _render("'Status'")],
                'lines': [2, 0, 'number', _render("(line['status'])")],
                'totals': [2, 0, 'text', None]},

        }

        self.wanted_list = ['id', 'first_name', 'last_name', 'studypro_code', 'studypro_name','status']

    def get_data(self, params):
        st = params['start_date']
        end = params['end_date']
        stpr_id = params['study_programme_id']

        if stpr_id != False:
            sql = """
                select
                 distinct
                 cl.id,
                 cl.first_name,
                 cl.last_name,

                    (select distinct stpr.code
                        from op_study_programme as stpr
                        where (stpr.id = stprl.study_programme_id)
                        ) as studypro_code,

                    (select distinct stpr.name
                        from op_study_programme as stpr
                        where (stpr.id = stprl.study_programme_id)
                        ) as studypro_name,

                    (select stg.name from crm_case_stage as stg
                        where (cl.stage_id = stg.id)) as status

                from crm_lead as cl, op_study_programme as stpr, op_study_programme_lead_rel as stprl
                where (cl.id = stprl.lead_id) and ('%(stpr_id)d' = stprl.study_programme_id)
                AND ((cl.inquiry_date) BETWEEN ('%(st)s')AND( '%(end)s'))
                """% ({'stpr_id': stpr_id, 'st': st, 'end': end})
        else:
            sql = """
                select
                 distinct
                 cl.id,
                 cl.first_name,
                 cl.last_name,

                    (select distinct stpr.code
                        from op_study_programme as stpr
                        where (stpr.id = stprl.study_programme_id)
                        ) as studypro_code,

                    (select distinct stpr.name
                        from op_study_programme as stpr
                        where (stpr.id = stprl.study_programme_id)
                        ) as studypro_name,

                    (select stg.name from crm_case_stage as stg
                        where (cl.stage_id = stg.id)) as status

                from crm_lead as cl, op_study_programme as stpr, op_study_programme_lead_rel as stprl
                where (cl.id = stprl.lead_id) and (stpr.id = stprl.study_programme_id)
                AND ((cl.inquiry_date) BETWEEN ('%(st)s')AND( '%(end)s'))
                """% ({'st': st, 'end': end})

        self.cr.execute(sql)
        val = self.cr.dictfetchall()
        return val

    def generate_xls_report(self, _p, _xs, data, objects, wb):

        # Initialize workbook 1
        report_name = _("Follow-up Actions Detail Analysis Report")
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
            ('report_name', 1, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, ['report_name'])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        row_pos += 1

        #Report Info
        c_specs = [
            ('st_pr', 2, 0, 'text', "Study Programme", None, self.rh_cell_style_right),
            ('stpr_nm', 3, 0, 'text', (data['study_programme_name'])),
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

op_followup_actions_detail_analysis_xls('report.op.followup.actions.detail.analysis.xls', 'crm.lead',
                         parser=op_followup_actions_detail_analysis_parser)