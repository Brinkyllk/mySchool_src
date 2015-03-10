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
    'depends': ['product', 'web'],
    'data': [
        'op_standard/op_standard_view.xml',
        'op_subject/op_subject_view.xml',
        'op_course/op_course_view.xml',
        'op_batch/op_batch_view.xml',
        'op_student/op_student_view.xml',
        'myschool_view.xml'

    ],
    'js': ['static/src/js/resource.js'],
    'qweb': ['static/src/xml/resource.xml'],

    'installable': True,
    'auto_install': False,
    'application': True,
}