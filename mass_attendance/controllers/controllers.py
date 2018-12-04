# -*- coding: utf-8 -*-
from odoo import http

# class MassAttendance(http.Controller):
#     @http.route('/mass_attendance/mass_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mass_attendance/mass_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mass_attendance.listing', {
#             'root': '/mass_attendance/mass_attendance',
#             'objects': http.request.env['mass_attendance.mass_attendance'].search([]),
#         })

#     @http.route('/mass_attendance/mass_attendance/objects/<model("mass_attendance.mass_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mass_attendance.object', {
#             'object': obj
#         })