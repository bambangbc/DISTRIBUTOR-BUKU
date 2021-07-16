# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 - widianajuniar@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import openerp
from openerp import api, fields, models, _, SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp import tools

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def search_invoices(self):
        for pick in self :
            if pick.state == 'done' :
            	inv_obj = self.env['account.invoice']
                inv_id = inv_obj.sudo().search([('origin','=',pick.name)],limit=1)
                if inv_id :
                	pick.invoice_id = inv_id.id

    def search_so(self):
        for pick in self :
            if pick.state not in ('draft','cancel') :
                so_obj = self.env['sale.order']
                so_id = so_obj.sudo().search([('name','=',pick.origin)],limit=1)
                if so_id :
                    pick.so_id = so_id.id

    def search_manager(self):
        for pick in self :
            manager_obj = self.env['res.partner']
            manager_id = manager_obj.sudo().search([('manager','=',True)],limit=1)
            if manager_id :
                pick.manager = manager_id.id

    @api.multi
    @api.depends('move_lines.gross','move_lines.disc','move_lines.nett')
    def _get_total_picking(self):
        for pick in self:
            gross = 0
            disc = 0
            nett = 0
            for move in pick.move_lines:
                gross += move.gross
                disc += move.disc
                nett += move.nett
            pick.gross = gross
            pick.disc = disc
            pick.nett = nett
    
    gross = fields.Float(string='Total Gross', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total_picking')
    disc = fields.Float(string='Total Discount', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total_picking')
    nett = fields.Float(string='Total Nett', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total_picking')
    invoice_id = fields.Many2one('account.invoice',string='Invoice',compute='search_invoices') 
    so_id = fields.Many2one('sale.order',string='SO',compute='search_so') 
    manager = fields.Many2one('res.partner',string="Manager Pemasaran", compute='search_manager')
StockPicking()

class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _get_total(self):
        gross = 0
        disc = 0
        nett = 0
        for move in self:
            gross = move.product_id.lst_price * move.product_uom_qty
            if move.picking_id.id and move.picking_id.partner_id.id :
                disc = gross * move.picking_id.partner_id.default_discount / 100
            nett = gross - disc
            move.gross = gross
            move.disc = disc
            move.nett = nett
            move.price = move.product_id.lst_price
            move.discount = move.picking_id.partner_id.default_discount

    gross = fields.Float(string='Total Gross', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total')
    disc = fields.Float(string='Total Discount', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total')
    nett = fields.Float(string='Total Nett', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total')
    price = fields.Float(string='Unit Price', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total')
    discount = fields.Float(string='Discount (%)', readonly=True,digits=dp.get_precision('Product Price'), compute='_get_total')
StockMove()

class res_partner(models.Model):
    _inherit = "res.partner"

    manager = fields.Boolean('Is Manager')
res_partner()