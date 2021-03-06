{
    'name': 'OpenArc My School',
    'version': '0.0.1',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Students, Faculties and Education Institute',
    'description': """
            This module provide overall education management system over OpenERP
            Features includes managing
                * Student
                * Lectures


    """,
    'author': 'OpenArc System Management Pvt. Ltd.',
    'website': 'http://www.openarc.lk',
    'depends': ['product', 'web', 'base', 'crm', 'marketing_crm'],
    'data': [
        'op_subject/op_subject_view.xml',
        'op_course/op_course_view.xml',
        'op_batch/op_batch_view.xml',
        'op_lecturer/op_lecturer_view.xml',
        'op_student/op_student_view.xml',
        'op_student/op_student_sequence.xml',
        'op_payment_schedule/op_payment_schedule_view.xml',
        'op_student/op_student_batch_mapping_view.xml',
        'op_timetable/timetable_postponed_view.xml',
        'op_timetable/op_timetable_view.xml',
        'op_timetable/op_timetable_workflow.xml',
        'op_classroom/op_classroom_view.xml',
        'wizard/generate_time_table_view.xml',
        'wizard/op_crm_employee_performance_analysis.xml',
        'wizard/op_crm_lead_analysis.xml',
        'wizard/op_enrollment_analysis.xml',
        'wizard/op_promotional_activity_analysis.xml',
        'wizard/op_followup_actions_detail_analysis.xml',
        'wizard/op_inquiry_modes_analysis.xml',
        'op_payment_schedule_line/op_payment_schedule_line_view.xml',
        'op_registration/op_registration_view.xml',
        'op_registration/op_registration_sequence.xml',
        'op_study_programme/op_study_programme_view.xml',
        'op_enrollment/op_enrollment_view.xml',
        'crm_lead/crm_lead_view.xml',
        'myschool_view.xml',
        'views/op_crm_lead_analysis_report_generate.xml',

    ],
    # 'test': [
    #          'test/new_admission.yml',
    # ],
    # 'images': ['images/Admission_Process.png','images/Student_Information.png'],
    'test': 'static/files/csv_template.csv',
    'installable': True,
    'auto_install': False,
    'application': True,
}