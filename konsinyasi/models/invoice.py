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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.multi
    @api.depends('discount_total')
    def _get_amount_bfr_discount(self):
        for order in self:
            order.amount_bfr_discount = order.amount_untaxed + order.discount_total 
        
    @api.multi
    @api.depends('invoice_line.discount')
    def _get_discount_total(self):
        """
        Compute the total discount of the SO.
        """
        for order in self:
            amount_discount = 0.0
            for line in order.invoice_line:
                base_price = line.price_unit * line.quantity
                amount_discount += base_price * line.discount / 100
            order.discount_total = amount_discount
    
    amount_bfr_discount = fields.Float(string='Before Discount', readonly=True, store=True,
        digits=dp.get_precision('Product Price'), compute='_get_amount_bfr_discount')
    discount_total = fields.Float(string='Total Discount', readonly=True, store=True,
        digits=dp.get_precision('Product Price'), compute='_get_discount_total')