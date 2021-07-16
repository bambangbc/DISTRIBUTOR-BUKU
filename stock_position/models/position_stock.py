# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016  widianajuniar@gmail.com
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


from openerp import api, fields, models, _, SUPERUSER_ID
import openerp.addons.decimal_precision as dp


class PositionStock(models.Model):
    _name = "position.stock"

    customer = fields.Char(string='Customer', size=100)
    warehouse = fields.Char(string='Warehouse', size=100)
    kode_buku = fields.Char(string='Kode Buku', size=25)
    judul = fields.Char(string='Judul', size=182)
    harga_satuan = fields.Float(string='Hrg Satuan', digits= dp.get_precision('Product Price'))
    awal = fields.Float(string='Awal', digits= dp.get_precision('Product UoS'), group_operator="sum")
    jual = fields.Float(string='Jual', digits= dp.get_precision('Product Price'), group_operator="sum")
    retur = fields.Float(string='Retur', digits= dp.get_precision('Discount'), group_operator="sum")
    akhir = fields.Float(string='Akhir', digits= dp.get_precision('Product Price'), group_operator="sum")

PositionStock()