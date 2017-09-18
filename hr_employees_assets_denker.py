# -*- coding: utf-8 -*-

from openerp import addons
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
#from dateutil.relativedelta import relativedelta
#from datetime import timedelta
from datetime import datetime
from datetime import date
#import time

class denker_hr_employees_assets(models.Model):
    #_name = 'hr.employees.assets'
    _inherit = 'account.asset.asset'

    estatus = fields.Selection([
                ('0','Disponible'),
                ('1','En uso'),
                ], 'Asignado', readonly=True, help="Estado del Activo", invisible=True, default='0')

    @api.multi
    def set_estatus(self, id, estatus):
        #print 'denker_hr_employees_assets SET_ESTATUS'
        #print 'id ', id
        #print 'estatus ', estatus
        self.env.cr.execute(
            """
            UPDATE account_asset_asset SET estatus = %s WHERE id=%s 
            """,
            ( str(estatus),str(id),)
            )

        #print 'entro al query'
        return True
        #self.write({'estatus': '1'})

    # def write(self, vals):
    #     print '2 ENTRO AL METODO WRITE'
    #     print 'VALS: ', vals

    #     asset = self.env['account.asset.asset']
    #     asset.write({'estatus': '1'})
    #     return super(denker_hr_employees_assets, self).write(vals)
    
    
class denker_hr_employees(models.Model):
    _inherit = 'hr.employee'

    employee_ids = fields.One2many('hr.employee.asset.assignment', 'name', 'Lineas', track_visibility='always',)

    @api.model   
    def create(self, vals):
        #print 'denker_hr_employees CREATE'
        result = super(denker_hr_employees, self).create(vals)
        #print vals['employee_ids']
        for record in vals['employee_ids']:
            self.env['account.asset.asset'].set_estatus(record[2]['asset_id'],'1')
        
        return result

    def write(self, vals):
        #print 'denker_hr_employees WRITE'
        result = super(denker_hr_employees, self).write(vals)
        #print vals
        #print self.employee_ids.id
        for record in self.employee_ids:
            #print 'ASSET: ', record.asset_id.id
            self.env['account.asset.asset'].set_estatus(record.asset_id.id,'1')

        return result



class denker_hr_employee_asset_assignment(models.Model):
    _name = 'hr.employee.asset.assignment'

    name = fields.Integer('Nombre', size=64)
    asset_id = fields.Many2one('account.asset.asset','Activo', ondelete='cascade', required=True, domain="[('estatus', '=', '0')]")
    assigned_by = fields.Many2one('hr.employee', 'Responsable de asignacion', ondelete='cascade', required=True)

    employee = fields.Char('Empleado')#,  compute='get_employee_name'

    @api.multi
    def unlink(self):
        #print 'denker_hr_employee_asset_assignment UNLINK'
        for record in self.asset_id:
            #print 'ASSET: ', record.id
            self.env['account.asset.asset'].set_estatus(record.id,'0')

        return super(denker_hr_employee_asset_assignment, self).unlink()

    @api.model
    def get_employee_name(self):
        employee = ''
        self.env.cr.execute(
            """
            SELECT name_related FROM hr_employee WHERE id=%s 
            """,
            (self.name,))

        res = self.env.cr.fetchall()

        for rec in res:
            employee = rec[0]

        print 'NOMBRE EMPLEADO: ', employee
        return employee

    @api.multi
    def asset_print(self):
        #self.ensure_one()
        self.employee = self.get_employee_name()
        print 'ACTIVO: ',self.asset_id.name, ' ASIGNADO POR:', self.assigned_by.name, ' ASIGNA A:', self.employee
        return self.env['report'].get_action(self, 'hr_employees_assets_denker.template_hr_assigned_assets2')
