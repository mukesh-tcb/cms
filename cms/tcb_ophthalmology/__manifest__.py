# -*- coding: utf-8 -*-

{
    'name': "Ophthalmology(CMS)",
    'summary': """
    This module is for Ophthalmology.
        """,

    'description': """ """,
    'author': "Mukesh Kumar",
    'website': "",

    'category': 'Medical',
    'version': '0.1',

    'depends': ['base','tcb_hms_base','mail','tcb_hms_base'],

    'data': [
        'security/ir.model.access.csv',
        'views/ophthalmology_view.xml',
        'views/presenting_complaints_page_ophthalmology.xml'
        # 'views/appointment_view_inherit.xml'
        
            ],
    
    'assets': {
        'web.assets_backend': [
                    # 'tcb_ophthalmology/static/src/js/ophthalmology_custom.js',
                    'tcb_ophthalmology/static/src/css/ophthalmology.css',
                    
            ],
    },
    
    'installable': True,
    'application': True,
    }