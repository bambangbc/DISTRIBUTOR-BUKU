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

from datetime import datetime, timedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            flag = vals.get('type_penjualan')
            if flag == 'konsinyasi':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order.konsinyasi') or '/'
            elif flag == 'showroom':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order.credit') or '/'
            else:
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order') or '/'
        if vals.get('partner_id') and any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id', 'fiscal_position']):
            defaults = self.onchange_partner_id(cr, uid, [], vals['partner_id'], context=context)['value']
            if not vals.get('fiscal_position') and vals.get('partner_shipping_id'):
                delivery_onchange = self.onchange_delivery_id(cr, uid, [], vals.get('company_id'), None, vals['partner_id'], vals.get('partner_shipping_id'), context=context)
                defaults.update(delivery_onchange['value'])
            vals = dict(defaults, **vals)
        ctx = dict(context or {}, mail_create_nolog=True)
        new_id = super(SaleOrder, self).create(cr, uid, vals, context=ctx)
        self.message_post(cr, uid, [new_id], body=_("Quotation created"), context=ctx)
        return new_id


    @api.multi
    @api.depends('discount_total')
    def _get_amount_bfr_discount(self):
        for order in self:
            order.amount_bfr_discount = order.amount_untaxed + order.discount_total 
        
    @api.multi
    @api.depends('order_line.discount')
    def _get_discount_total(self):
        """
        Compute the total discount of the SO.
        """
        for order in self:
            amount_discount = 0.0
            for line in order.order_line:
                base_price = line.price_unit * line.product_uom_qty
                amount_discount += base_price * line.discount / 100
            order.discount_total = amount_discount
    
    amount_bfr_discount = fields.Float(string='Before Discount', readonly=True, store=True,
        digits=dp.get_precision('Product Price'), compute='_get_amount_bfr_discount')
    discount_total = fields.Float(string='Total Discount', readonly=True, store=True,
        digits=dp.get_precision('Product Price'), compute='_get_discount_total')
    areahead_id = fields.Many2one('hr.employee','Area Head',readonly=True, states={'draft': [('readonly', False)]})
    spg_id = fields.Many2one('hr.employee','SPG',readonly=True, states={'draft': [('readonly', False)]})
    is_konsinyasi = fields.Boolean('Konsinyasi')
    type_penjualan = fields.Selection([('konsinyasi','Konsinyasi'),('showroom','Kredit'),('putus','Cash')],'Type Penjualan')

SaleOrder()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bon_date = fields.Date('Bon Date',default=fields.Datetime.now)
    bon_number = fields.Char('Bon Number',default='-')

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang', False)
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
        warning = False
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        partner = partner_obj.browse(cr, uid, partner_id)
        lang = partner.lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False

        fpos = False
        if not fiscal_position:
            fpos = partner.property_account_position or False
        else:
            fpos = self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position)
        if update_tax: #The quantity only have changed
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += '\n'+product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}
        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {
                        'uom': uom or result.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error!'),
                       'message' : warning_msgs
                    }
        #import pdb;pdb.set_trace()
        disc_partner = partner.default_discount
        if disc_partner > 0.0 and disc_partner <= 100:
            result.update({'discount': disc_partner})

        return {'value': result, 'domain': domain, 'warning': warning}

SaleOrderLine()

class SaleOrderCredit(models.Model):
    _name = 'sale.order.credit'
    # tabel bayangan untuk so credit

    name = fields.Char(string='Name')

SaleOrderCredit()

class SaleOrderKonsinyasi(models.Model):
    _name = 'sale.order.konsinyasi'
    # tabel bayangan untuk so konsinyasi
    name = fields.Char(string='Name')
    
SaleOrderKonsinyasi()