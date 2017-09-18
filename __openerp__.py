# -*- coding: utf-8 -*-
{
    'name': 'Pestaña de activos',
    'version': '1.1',
    'summary': 'Modulo de RRHH que agrega la pestaña de activos al módulo de empleados.',
    'category': 'Denker',
    'description': """
    Modulo que crea una pestaña en Empleados con la informacion necesaria para la asignacion de activos. Integra el catalogo de activos de contabilidad.
    """,
    'author': 'Humanytek',
    'website': 'http://www.humanytek.com',
    'depends': ['hr','hr_contract','account_asset'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'hr_employees_assets_denker.xml',
        'report/assigned_assets.xml',
        'report/assigned_assets2.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
