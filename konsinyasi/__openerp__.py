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
    "name": "Konsinyasi Sales",
    'version': '0.4',
    'category': 'Sale',
    'sequence': 14,
    'author':  'sincpayou.com',
    'website': 'www.sincpayou.com',
    'license': 'AGPL-3',
    'summary': '',
    "description": """
* Penyesuaian Form SO untuk konsep penjualan konsinyasi, penjualan cash, dan penjualan kredit
* Print Out Custom untuk konsinyasi
* Tambah total diskon dan total sebelum diskon pada form invoice
* Discount otomatis terisi ketika add product di Sales Order jika pada partnernya field Default Discount diisi

    """,
    "depends": [
        "sale",
    ],
    "data": [
        "views/sale_order.xml",
        "views/journal.xml",
        "views/invoice.xml",
        "views/partner.xml",
        "views/menu.xml",
        "reports/invoice_konsinyasi.xml",
        "data/data.xml"
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
