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
	def fill_table_1(self,date_start, date_end):
		self._cr.execute("SELECT product_id,location_dest_id, SUM(product_uom_qty) FROM stock_move WHERE state='done' GROUP BY product_id, location_dest_id ORDER BY product_id")
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table(self):
		self._cr.execute("delete from stock_report")
		stock_masuk = self.fill_table_1(self.date_start, self.date_end)
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_report(
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
	def fill_table_2(self,date_start, date_end):
		self._cr.execute("SELECT product_id,location_id, SUM(product_uom_qty) FROM stock_move WHERE state='done' GROUP BY product_id, location_id ORDER BY product_id")
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table_lost(self):
		self._cr.execute("delete from stock_report_lost")
		stock_masuk = self.fill_table_2(self.date_start, self.date_end)
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_report_lost(
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
		self._cr.execute("SELECT A.product,A.location,(A.quantity - T.quantity) AS total FROM stock_report AS A INNER JOIN stock_report_lost AS T ON T.product = A.product AND T.location = A.location")
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table_final(self):
		self._cr.execute("delete from stock_report_final")
		stock_masuk = self.fill_table_3(self.date_start, self.date_end)
		#import pdb;pdb.set_trace()
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_report_final(
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
	def fill_table_4(self,date_start, date_end):
		self._cr.execute("SELECT product,location,quantity FROM stock_report_final") 
		stock = self._cr.fetchall()
		return stock

	@api.multi
	def fill_table_change(self):
		self._cr.execute("delete from stock_move")
		stock_masuk = self.fill_table_4(self.date_start, self.date_end)
		#import pdb;pdb.set_trace()
		for line in stock_masuk :
			product = line[0]
			location = line[1]
			quantity = line[2]
			sql = """INSERT INTO stock_move(
							product_id,
							location_dest_id,
							location_id,
							name,
							product_uom_qty,)
							VALUES (%s, %s, %s)

							""" % (product,
								   location,
								   5,
								   "Update",
								   quantity)
			self._cr.execute(sql)
		return True
	
	