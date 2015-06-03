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
    'depends': ['product', 'web', 'base','account'],
    'data': [
        'op_standard/op_standard_view.xml',
        '   /op_subject_view.xml',
        'op_course/op_course_view.xml',
        'op_batch/op_batch_view.xml',
        'op_lecturer/op_lecturer_view.xml',
        'op_student/op_student_view.xml',
        'op_student/op_student_sequence.xml',
        'op_payment_schedule/op_payment_schedule_view.xml',
        'op_student/op_student_batch_mapping_view.xml',
        'op_timetable/op_timetable_view.xml',
        'op_timetable/op_timetable_workflow.xml',
        'op_timetable/timetable_postponed_view.xml',
        'op_classroom/op_classroom_view.xml',
        'wizard/generate_time_table_view.xml',
        'op_payment_schedule_line/op_payment_schedule_line_view.xml',
        'myschool_view.xml'

    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}