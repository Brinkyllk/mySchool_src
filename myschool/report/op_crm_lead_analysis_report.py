import xlwt
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
import logging

_ir_translation_name = 'op.crm.lead.analysis.xls'


class op_crm_lead_analysis_parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(op_crm_lead_analysis_parser, self).__init__(
            cr, uid, name, context=context)

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        return translate(self.cr, _ir_translation_name, 'report', lang, src) or src


class op_crm_lead_analysis_xls(report_xls):
    def __init__(self, name, table, rml=False, parser=False, header=False,
                 store=False):
        super(op_crm_lead_analysis_xls, self).__init__(
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
            'code': {
                'header': [1, 8, 'text', _render("'CODE'")],
                'lines': [1, 0, 'text', _render("(str(line['code']) or '-')")],
                'totals': [1, 0, 'text', None]},
            'name': {
                'header': [1, 8, 'text', _render("'NAME'")],
                'lines': [1, 0, 'text', _render("(str(line['name']) or '-')")],
                'totals': [1, 0, 'text', None]},
            'sat_any': {
                'header': [1, 8, 'text', _render("'SAT_ANY'")],
                'lines': [1, 0, 'number', _render("(line['sat_any'])")],
                'totals': [1, 0, 'text', None]},
            'sun_any': {
                'header': [1, 8, 'text', _render("'SUN_ANY'")],
                'lines': [1, 0, 'number', _render("(line['sun_any'] )")],
                'totals': [1, 0, 'text', None]},
            'wkd_any': {
                'header': [1, 8, 'text', _render("'WKD_ANY'")],
                'lines': [1, 0, 'number', _render("(line['wkd_any'])")],
                'totals': [1, 0, 'text', None]},
            'sat_mor': {
                'header': [1, 8, 'text', _render("'SAT_MOR'")],
                'lines': [1, 0, 'number', _render("(line['sat_mor'])")],
                'totals': [1, 0, 'text', None]},
            'sun_mor': {
                'header': [1, 8, 'text', _render("'SUN_MOR'")],
                'lines': [1, 0, 'number', _render("(line['sun_mor'])")],
                'totals': [1, 0, 'text', None]},
            'wkd_mor': {
                'header': [1, 8, 'text', _render("'WKD_MOR'")],
                'lines': [1, 0, 'number', _render("(line['wkd_mor'])")],
                'totals': [1, 0, 'text', None]},
            'sat_aft': {
                'header': [1, 8, 'text', _render("'SAT_AFT'")],
                'lines': [1, 0, 'number', _render("(line['sat_aft'])")],
                'totals': [1, 0, 'text', None]},
            'sun_aft': {
                'header': [1, 8, 'text', _render("'SUN_AFT'")],
                'lines': [1, 0, 'number', _render("(line['sun_aft'])")],
                'totals': [1, 0, 'text', None]},
            'wkd_aft': {
                'header': [1, 8, 'text', _render("'WKD_AFT'")],
                'lines': [1, 0, 'number', _render("(line['wkd_aft'])")],
                'totals': [1, 0, 'text', None]},
            'sat_eve': {
                'header': [1, 8, 'text', _render("'SAT_EVE'")],
                'lines': [1, 0, 'number', _render("(line['sat_eve'])")],
                'totals': [1, 0, 'text', None]},
            'sun_eve': {
                'header': [1, 8, 'text', _render("'SUN_EVE'")],
                'lines': [1, 0, 'number', _render("(line['sun_eve'])")],
                'totals': [1, 0, 'text', None]},
            'wkd_eve': {
                'header': [1, 8, 'text', _render("'WKD_EVE'")],
                'lines': [1, 0, 'number', _render("(line['wkd_eve'])")],
                'totals': [1, 0, 'text', None]},
            'total': {
                'header': [1, 8, 'text', _render("'TOTAL'")],
                'lines': [1, 0, 'number', _render("(line['total'])")],
                'totals': [1, 0, 'text', None]},
            'follow_ups': {
                'header': [1, 8, 'text', _render("'NO.OF FOLLOW-UPS'")],
                'lines': [1, 0, 'number', _render("(line['follow_ups'])")],
                'totals': [1, 0, 'text', None]},
            'enrollments': {
                'header': [1, 8, 'text', _render("'ENROLLMENTS'")],
                'lines': [1, 0, 'number', _render("(line['enrollments'])")],
                'totals': [1, 0, 'text', None]},
        }

        self.wanted_list = ['id','code', 'name', 'sat_any', 'sun_any', 'wkd_any', 'sat_mor', 'sun_mor',
                            'wkd_mor', 'sat_aft',
                            'sun_aft', 'wkd_aft', 'sat_eve', 'sun_eve', 'wkd_eve',
                            'total', 'follow_ups', 'enrollments'
        ]

    def get_data(self, params):
        # st = params['start_date']
        # end = params['end_date']
        # stpr = params['study_programme_id']
        #

        sql = """
        SELECT
                        stpr.id,
                        stpr.code,
                        stpr.name,

-- AnyTime Time Frames

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (1 = attf.time_frame_id)) as sat_any,

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (2 = attf.time_frame_id)) as sun_any,

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (3= attf.time_frame_id)) as wkd_any,

-- Morning Time Frames

                (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (1= mtf.time_frame_id)) as sat_mor,

                    (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (2= mtf.time_frame_id)) as sun_mor,

                    (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (3= mtf.time_frame_id)) as wkd_mor,

-- Afternoon Time Frames

                    (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (1= atf.time_frame_id)) as sat_aft,

                (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (2= atf.time_frame_id)) as sun_aft,

                (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (3= atf.time_frame_id)) as wkd_aft,

-- Evening Time Frames
                (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (1= etf.time_frame_id)) as sat_eve,

                (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (2= etf.time_frame_id)) as sun_eve,

                (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (3= etf.time_frame_id)) as wkd_eve,

                (select count(cl.id) from crm_lead as cl, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND (cl.id = splr.lead_id)) as total,

                (select sum (cl.meeting_count) from crm_lead as cl, op_study_programme_lead_rel as splr
                where
                (splr.lead_id = cl.id) and (splr.study_programme_id = stpr.id)) as follow_ups,

                (select count(cl.id) from crm_lead as cl,op_study_programme_lead_rel as splr
                where
                (cl.id = splr.lead_id) and (cl.stage_id = 6) and (splr.study_programme_id = stpr.id)) as enrollments

                FROM op_study_programme as stpr
        """

        #       # % ({'st': st, 'end': end, 'stpr': stpr})
        self.cr.execute(sql)
        val = self.cr.dictfetchall()
        return val

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        # Initialize workbook 1
        report_name = _("Lead Analysis Report")
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

        lines = self.get_data(params=data)

        for line in lines:
            c_specs = map(
                lambda x: self.render(x, self.col_specs_template,
                                      'lines'), self.wanted_list)
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=self.aml_cell_style)


op_crm_lead_analysis_xls('report.op.crm.lead.analysis.xls', 'crm.lead',
                         parser=op_crm_lead_analysis_parser)
