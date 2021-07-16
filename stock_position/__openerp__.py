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
    "name": "Stock Position Report Wizard",
    'version': '0.2',
    'category': 'Stock',
    'sequence': 14,
    'author':  'sincpayou.com',
    'website': 'www.sincpayou.com',
    'license': 'AGPL-3',
    'summary': '',
    "description": """
* Report product per gudang konsinyasi (wizard)

    """,
    "depends": [
        "sale",
        "sales_report"
    ],
    "data": [
        "wizard/position_stock_wizard.xml",
        "views/position_stock.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
