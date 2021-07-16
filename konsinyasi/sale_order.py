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
import openerp
from openerp.osv import fields, osv
from openerp import api, fields, models, _, SUPERUSER_ID


class SaleOrder(models.Model):
    _inherit = "sale.order"

    areahead_id = fields.Many2one('hr.employee','Area Head',readonly=True, states={'draft': [('readonly', False)]})
    spg_id = fields.Many2one('hr.employee','SPG',readonly=True, states={'draft': [('readonly', False)]})
    is_konsinyasi = fields.Boolean('Konsinyasi')
    type_penjualan = fields.Selection([('konsinyasi','Konsinyasi'),('showroom','Showroom'),('putus','Putus')],'Type Penjualan')

SaleOrder()

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bon_date = fields.Date('Bon Date',default=fields.Datetime.now)
    bon_number = fields.Char('Bon Number',default='-')

SaleOrderLine()