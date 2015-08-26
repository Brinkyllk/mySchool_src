from openerp.addons.crm import crm
from openerp.osv import fields, osv
from openerp import tools


class op_crm_lead_analysis_report(osv.Model):
    """ CRM Opportunity Analysis """
    _name = "op.crm.lead.analysis.report"
    _auto = False
    _description = "CRM Lead Analysis"

    _columns = {
        'id': fields.integer('Id', readonly=True, ),
        'code': fields.char('Code', readonly=True),
        'name': fields.char('Name', readonly=True),
        'saturday_anytime': fields.integer('Saturday Anytime', readonly=True),
        'sunday_anytime': fields.integer('Sunday Anytime', readonly=True),
        'weekday_anytime': fields.integer('Weekday Anytime', readonly=True),
        'saturday_morning': fields.integer('Saturday Morning', readonly=True),
        'sunday_morning': fields.integer('Sunday Morning', readonly=True),
        'weekday_morning': fields.integer('Weekday Morning', readonly=True),
        'saturday_afternoon': fields.integer('Saturday Afternoon', readonly=True),
        'sunday_afternoon': fields.integer('Sunday Afternoon', readonly=True),
        'weekday_afternoon': fields.integer('Weekday Afternoon', readonly=True),
        'saturday_evening': fields.integer('Saturday Evening', readonly=True),
        'sunday_evening': fields.integer('Sunday Evening', readonly=True),
        'weekday_evening': fields.integer('Weekday Evening', readonly=True),
        'total': fields.integer("Total", readonly=True)
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'op_crm_lead_analysis_report')
        cr.execute("""
            CREATE OR REPLACE VIEW op_crm_lead_analysis_report AS (
                SELECT
                    stpr.id,
                    stpr.code,
                    stpr.name,

		            -- AnyTime Time Frames

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (1 = attf.time_frame_id)) as saturday_anytime,

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (2 = attf.time_frame_id)) as sunday_anytime,

                    (select count(cl.id) from crm_lead as cl, op_anytime_time_frame_rel as attf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = attf.lead_id) AND (3= attf.time_frame_id)) as weekday_anytime,

                    -- Morning Time Frames

		            (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (1= mtf.time_frame_id)) as saturday_morning,

                    (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (2= mtf.time_frame_id)) as sunday_morning,

                    (select count(cl.id) from crm_lead as cl, op_morning_time_frame_rel as mtf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = mtf.lead_id) AND (3= mtf.time_frame_id)) as weekday_morning,

                    -- Afternoon Time Frames

                    (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (1= atf.time_frame_id)) as saturday_afternoon,

		            (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (2= atf.time_frame_id)) as sunday_afternoon,

		            (select count(cl.id) from crm_lead as cl, op_afternoon_time_frame_rel as atf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = atf.lead_id)AND (3= atf.time_frame_id)) as weekday_afternoon,

		            -- Evening Time Frames
		            (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (1= etf.time_frame_id)) as saturday_evening,

		            (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (2= etf.time_frame_id)) as sunday_evening,

		            (select count(cl.id) from crm_lead as cl, op_evening_time_frame_rel as etf, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND
                    (cl.id = splr.lead_id) AND (cl.id = etf.lead_id) AND (3= etf.time_frame_id)) as weekday_evening,

                    (select count(cl.id) from crm_lead as cl, op_study_programme_lead_rel as splr
                    where
                    (splr.study_programme_id = stpr.id) AND (cl.id = splr.lead_id)) as total

                FROM op_study_programme as stpr
            )""")


class op_crm_lead_analysis_report_generate(osv.AbstractModel):
    _name = 'myschool.report.op_crm_lead_analysis_report_generate'
    _inherit = 'report.abstract_report'
    _template = 'myschool.op_crm_lead_analysis_report_generate'
    _wrapped_report_class = op_crm_lead_analysis_report
