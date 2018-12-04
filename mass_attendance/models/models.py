# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import datetime, timedelta
import time
from odoo.exceptions import ValidationError
import math

class DailyAttendance(models.Model):
    _name = 'daily.attendance'
    _description = 'Daily Attendance'
    _rec_name = 'date'

    @api.multi
    @api.depends('employee_ids')
    def _compute_total(self):
        for rec in self:
            rec.total_student = len(rec.employee_ids)

    @api.multi
    @api.depends('employee_ids')
    def _compute_present(self):
        for rec in self:
            count = 0
            if rec.employee_ids:
                for att in rec.employee_ids:
                    if att.is_present:
                        count += 1
                rec.total_presence = count

    @api.multi
    @api.depends('employee_ids')
    def _compute_absent(self):
        for rec in self:
            count_fail = 0
            if rec.employee_ids:
                for att in rec.employee_ids:
                    if att.is_absent:
                        count_fail += 1
                rec.total_absent = count_fail

    user_id = fields.Boolean('List all Students', required=True)
    date = fields.Date("Date", help="Current Date", default=lambda *a: time.strftime('%Y-%m-%d'))
    state = fields.Selection([('draft', 'Draft'), ('validate', 'Validate')], 'Status', readonly=True, default='draft')
    employee_ids = fields.One2many('daily.attendance.line', 'emp_id','Employee')
    total_student = fields.Integer(compute="_compute_total", store=True, help="Total Students", string='Total Students')
    total_presence = fields.Integer(compute="_compute_present", store=True, string='Present Students', help="Present Students")
    total_absent = fields.Integer(compute="_compute_absent", store=True, string='Absent Students', help="Absent Students")
    date_time_from = fields.Datetime(string='Check In', default=datetime.now().replace(hour=2, minute=30, second=00))
    date_time_to = fields.Datetime(string='Check Out', default=datetime.now().replace(hour=14, minute=30, second=00))
    present_all = fields.Boolean()
    absent_all = fields.Boolean()

    @api.model
    def create(self, vals):
        curr = datetime.now()
        new_date = datetime.strftime(curr, '%Y-%m-%d')
        cal_obj = self.env['daily.attendance'].search([])
        if cal_obj:
            for co in cal_obj:
                co.date
            if co.date == new_date:
                raise ValidationError(_('''Current Date Attendance Already Exist!'''))
        return super(DailyAttendance, self).create(vals)

    @api.multi
    @api.onchange('user_id')
    def onchange_department(self):
        if self.user_id == True:
            emps = self.env['student.student'].search([])
            emp_attd = []
            check_in = (datetime.strptime(self.date, '%Y-%m-%d') + timedelta(hours=5,minutes=30))
            check_in_from = check_in.strftime("%Y-%m-%d 03:30:00")
            check_out = (datetime.strptime(self.date, '%Y-%m-%d') + timedelta(hours=5, minutes=30))
            check_out_from = check_out.strftime("%Y-%m-%d 12:30:00")
            for emp in emps:
                vals = {
                    'employe_id':emp.id,
                    'check_in': check_in_from,
                    'check_out': check_out_from,
                    'is_present': True
                }
                emp_attd.append([0, 0, vals])
            self.update({
                'employee_ids': emp_attd,
            })
        else:
            self.employee_ids = False
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def attendance_validate(self):
        for emp in self.employee_ids:
            if emp.is_present == True:
                attd = self.env['hr.attendance']
                attd_crete_id = attd.create({'employee_id': emp.employe_id.id,
                                               'check_in': emp.check_in,
                                               'check_out': emp.check_out,
                                            })
                self.write({
                    'state': 'validate',
                })

            elif emp.is_absent == True:
                if emp.is_absent == True:
                    attd = self.env['hr.holidays']
                    from_dt = fields.Datetime.from_string(emp.check_in)
                    to_dt = fields.Datetime.from_string(emp.check_out)
                    d1 = datetime.strptime(str(emp.check_in), '%Y-%m-%d %H:%M:%S')
                    d2 = datetime.strptime(str(emp.check_out), '%Y-%m-%d %H:%M:%S')
                    timedelta = to_dt - from_dt
                    d3 = math.ceil(timedelta.days + float(timedelta.seconds) / 86400)
                    # self.total_days = str(d3.days)
                    attd_crete_id = attd.create({'employee_id': emp.employe_id.id,
                                                  'date_from': emp.check_in,
                                                  'date_to': emp.check_out,
                                                  'number_of_days_temp': d3
                                                })
                    self.write({
                        'state': 'validate',
                    })
            else:
                attd_crete_id = None
        return attd_crete_id


class DailyAttendanceLine(models.Model):
    _description = 'Daily Attendance Line'
    _name = 'daily.attendance.line'

    emp_id = fields.Many2one('daily.attendance', 'Students')
    is_present = fields.Boolean('Present', help="Check if student is present", default=True)
    is_absent = fields.Boolean('Absent', help="Check if student is absent")
    employe_id = fields.Many2one('student.student', 'Student Name')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')

    @api.onchange('is_present')
    def onchange_attendance(self):
        '''Method to make absent false when student is present'''
        if self.is_present:
            self.is_absent = False

    @api.onchange('is_absent')
    def onchange_absent(self):
        '''Method to make present false when student is absent'''
        if self.is_absent:
            self.is_present = False

    @api.constrains('is_present', 'is_absent')
    def check_present_absent(self):
        if not self.is_present and not self.is_absent:
            raise ValidationError(_('Check Present or Absent for all Employees!!'))


class HRHolidays(models.Model):
    _description = 'HR Holidays'
    _inherit = 'hr.holidays'

    holiday_status_id = fields.Many2one("hr.holidays.status", string="Leave Type", required=True, readonly=True,
                                        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                        default=lambda self: self.env['hr.holidays.status'].search([('name', '=', 'Unpaid')]))
