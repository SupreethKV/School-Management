# -*- coding: utf-8 -*-
{
    'name': "Mass Attendance",
    'summary': """
        Mass Attendance for employees""",
    'description': """
        Takes Mass Attendance for all Employess listed in HR Module. 
        Once validated, present employess will be listed in Attendance menu and Absent 
        Employees will be listed in HR Leaves.
    """,
    'author': "Supreeth",
    'website': "http://www.autochip.in",
    'category': 'Attendance',
    'version': '11.0.1.0.0',
    'depends': ['hr', 'hr_attendance', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/mass_attendance_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}