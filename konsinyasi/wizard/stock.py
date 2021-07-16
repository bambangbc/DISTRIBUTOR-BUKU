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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

class stock_invoice_onshipping(osv.osv_memory):
    _inherit = "stock.invoice.onshipping"
    
    def _get_journal_by_type_penjualan(self, cr, uid, context=None):
        #import pdb;pdb.set_trace()
        journal_obj = self.pool.get('account.journal')
        journal_type = self._get_journal_type(cr, uid, context=context)
        journals = journal_obj.search(cr, uid, [('type', '=', journal_type)])

        # custom type penjualan
        pick_obj = self.pool.get('stock.picking')
        sale_obj = self.pool.get('sale.order')
        origin = pick_obj.browse(cr,SUPERUSER_ID,context.get('active_id')).origin
        # konsinyasi
        sale_exist = sale_obj.search(cr, SUPERUSER_ID, [('name', '=', origin)],limit=1)
        if sale_exist :
            type_penjualan = sale_obj.browse(cr,SUPERUSER_ID,sale_exist[0]).type_penjualan

            if type_penjualan == 'konsinyasi' :        
                journals_kons = journal_obj.search(cr, uid, [('type', '=', journal_type),('type_penjualan', '=', 'konsinyasi')],limit=1)
                if journals_kons :
                    journals = journals_kons
            elif type_penjualan == 'showroom' :
                journals_cred = journal_obj.search(cr, SUPERUSER_ID, [('type', '=', journal_type),('type_penjualan', '=', 'showroom')])
                if journals_cred :    
                    journals = journals_cred
            elif type_penjualan == 'putus' :
                journals_cash = journal_obj.search(cr, SUPERUSER_ID, [('type', '=', journal_type),('type_penjualan', '=', 'putus')])
                if journals_cash :    
                    journals = journals_cash        

        return journals and journals[0] or False

    _defaults = {
        'journal_id' : _get_journal_by_type_penjualan,
    }