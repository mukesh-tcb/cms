# -*- coding: utf-8 -*-

{
    'name': "Clinic Management System(Base)",
    'summary': """
    This module is for Clinic  """,

    'description': """ """,
    'author': "Mukesh Kumar",
    'website': "",

    'category': 'education',
    'version': '0.1',

    'depends': ['base','mail','hr','product','account'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
            'views/patient_view.xml',
            'views/physician_view.xml',
            'views/appointment_view.xml',
            'reports/report_actions.xml',
            'reports/appointment_report.xml',
            'reports/header_footer.xml',
            ],
    
    'assets': {
        'web.assets_backend': [],
    },
    
    'installable': True,
    'application': True,
    }