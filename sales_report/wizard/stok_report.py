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
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning as UserError
from openerp.osv import osv
import openerp.addons.decimal_precision as dp


class SalesReportWizard(models.TransientModel):
	_name = "stock.report.wizard"

	date_start = fields.Date(string='Date From')
	date_end = fields.Date(string='Date To')

	@api.multi
	def fill_table_so(self):
		st = False
		self._cr.execute("delete from stock_report")
		obj = self.env['stock.inventory']
		src = obj.search([('name','=','PALAPA STOCK MARET')])
		for stock in src:
			for stock_real in stock.line_ids:
				#import pdb;pdb.set_trace()
				st = self.env['stock.report'].create({'name':stock.name,
														'location':stock_real.location_id.id,
														'product':stock_real.product_id.id,
														'quantity':stock_real.product_qty})
		return True

	@api.multi
	def fill_table_so2(self):
		st = False
		self._cr.execute("delete from stock_report")
		obj = self.env['stock.inventory']
		src = obj.search([('name','=','Februari')])
		for stock in src:
			for stock_real in stock.line_ids:
				#import pdb;pdb.set_trace()
				st = self.env['stock.report2'].create({'name':stock.name,
														'location':stock_real.location_id.id,
														'product':stock_real.product_id.id,
														'quantity':stock_real.product_qty})
		return True

	@api.multi
	def fill_table_2(self,date_start, date_end):
		self._cr.execute("SELECT product_id,location_dest_id, SUM(product_uom_qty) FROM stock_move WHERE state='done' and location_dest_id=12 GROUP BY product_id, location_dest_id ORDER BY product_id")
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table_masuk(self):
		self._cr.execute("delete from stock_report_masuk")
		#import pdb;pdb.set_trace()
		stock_masuk = self.fill_table_2(self.date_start, self.date_end)
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_report_masuk(
							product,
							location,
							quantity)
							VALUES (%s, %s, %s)

							""" % (product,
								   location,
								   quantity)
			self._cr.execute(sql)
		return True

	@api.multi
	def fill_table_3(self,date_start, date_end):
		self._cr.execute("SELECT product_id,location_id, SUM(product_uom_qty) FROM stock_move WHERE state='done' and location_id=12 GROUP BY product_id, location_id ORDER BY product_id")
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table_keluar(self):
		self._cr.execute("delete from stock_report_keluar")
		#import pdb;pdb.set_trace()
		stock_masuk = self.fill_table_3(self.date_start, self.date_end)
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_report_keluar(
							product,
							location,
							quantity)
							VALUES (%s, %s, %s)

							""" % (product,
								   location,
								   quantity)
			self._cr.execute(sql)
		return True

	@api.multi
	def fill_table_change(self):
		self._cr.execute("delete from stock_report_final")
		obj_so1 = self.env['stock.report']
		obj_move = self.env['stock.move']
		src = obj_so1.search([])
		for stock in src:
			qty_masuk = 0
			qty_keluar = 0
			qty_total = 0
			prod = stock.product
			qty_inv = stock.quantity
			for stock_masuk in obj_move.search([('product_id','=',stock.product.id),('location_dest_id','=',stock.location.id),('create_date','>=','2017-03-18 06:00:00'),('state','=','done'),('name','!=','INV:PALAPA STOCK MARET')]):
				qty_masuk += stock_masuk.product_uom_qty
			for stock_keluar in obj_move.search([('product_id','=',stock.product.id),('location_id','=',stock.location.id),('create_date','>=','2017-03-18 06:00:00'),('state','=','done'),('name','!=','INV:PALAPA STOCK MARET')]):
				qty_keluar += stock_keluar.product_uom_qty
			qty_total = qty_inv + qty_masuk - qty_keluar
			st = self.env['stock.report.final'].create({'location':stock.location.id,
														'product':stock.product.id,
														'quantity':qty_total})
		return True