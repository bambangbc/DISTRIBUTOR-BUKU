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
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 widianajuniar@gmail.com
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


class SalesReport(models.Model):
    _name = "sales.report"

    no_inv = fields.Char(string='No Bukti', size=25)
    tgl_inv = fields.Char(string='Tanggal Inv', size=25)
    customer = fields.Char(string='Customer', size=100)
    kode_buku = fields.Char(string='Kode Buku', size=25)
    judul = fields.Char(string='Judul', size=182)
    harga_satuan = fields.Float(string='Hrg Satuan', digits= dp.get_precision('Product Price'), group_operator="avg")
    qty = fields.Float(string='Quantity', digits= dp.get_precision('Product UoS'), group_operator="sum")
    bruto = fields.Float(string='Bruto', digits= dp.get_precision('Product Price'), group_operator="sum")
    disc = fields.Float(string='Disc %', digits= dp.get_precision('Discount'), group_operator="avg")
    disc_nominal = fields.Float(string='Disc Rp', digits= dp.get_precision('Product Price'), group_operator="sum")
    nett = fields.Float(string='Nett', digits= dp.get_precision('Product Price'), group_operator="sum")
    type_jual = fields.Char(string='Type Penjualan', size=25)

SalesReport()

class StockReport(models.Model):
    _name = "stock.report"

    name = fields.Char('Des')
    location = fields.Many2one('stock.location', string='location')
    product = fields.Many2one('product.product', string='product', size=100)
    quantity = fields.Float(string='quantity')

StockReport()

class StockReport(models.Model):
    _name = "stock.report2"

    name = fields.Char('Des')
    location = fields.Many2one('stock.location', string='location')
    product = fields.Many2one('product.product', string='product', size=100)
    quantity = fields.Float(string='quantity')

StockReport()

class StockReportLost(models.Model):
    _name = "stock.report.masuk"

    location = fields.Many2one('stock.location', string='location')
    product = fields.Many2one('product.product', string='product', size=100)
    quantity = fields.Float(string='quantity')
    date = fields.Datetime('Dtae')

StockReport()

class StockReportFinal(models.Model):
    _name = "stock.report.keluar"

    location = fields.Many2one('stock.location', string='location')
    product = fields.Many2one('product.product', string='product', size=100)
    quantity = fields.Float(string='quantity')
    date = fields.Datetime('date')

StockReportFinal()

class StockReportFinals(models.Model):
    _name = "stock.report.final"

    location = fields.Many2one('stock.location', string='location')
    product = fields.Many2one('product.product', string='product', size=100)
    quantity = fields.Float(string='quantity')

StockReportFinals()