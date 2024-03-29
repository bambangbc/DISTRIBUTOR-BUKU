# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  widianajuniar@gmail.com
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Sales Report Wizard",
    'version': '0.1',
    'category': 'Sale',
    'sequence': 14,
    'author':  'sincpayou.com',
    'website': 'www.sincpayou.com',
    'license': 'AGPL-3',
    'summary': '',
    "description": """
* Report list penjualan dalam satu tempat (wizard)

    """,
    "depends": [
        "sale",
    ],
    "data": [
        "wizard/sales_report_wizard.xml",
        "views/sales_report.xml",
        "security/ir.model.access.csv",
        "views/donesm.xml"
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
