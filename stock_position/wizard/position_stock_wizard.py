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
from openerp import models, fields, api, _, SUPERUSER_ID
from openerp.exceptions import except_orm, Warning as UserError
from openerp.osv import osv
import openerp.addons.decimal_precision as dp


class PositionStockWizard(models.TransientModel):
    _name = "position.stock.wizard"

    date_start = fields.Date(string='Date From', required=True, default=time.strftime('%Y-%m-01'))
    date_end = fields.Date(string='Date To', required=True, default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    
    @api.multi
    def query_awal_by_loction_id(self, location_id, product_id, date_start):
        self._cr.execute("SELECT SUM(sm.product_uom_qty) AS total FROM stock_move sm "\
                            "LEFT JOIN product_product pp on pp.id = sm.product_id "\
                            "LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id "\
                            "LEFT JOIN stock_picking sp ON sp.id = sm.picking_id "\
                            "LEFT JOIN res_partner rp ON rp.id = sp.partner_id "\
                            "LEFT JOIN stock_warehouse sw ON sw.id = sm.location_dest_id "\
                            "LEFT JOIN stock_location sl ON sl.id = sw.lot_stock_id "\
                            "WHERE sm.location_id = %s "\
                            "AND sm.product_id = %s "\
                            "AND sm.state = 'done' "\
                            "AND sm.date < %s " , ( location_id ,product_id, date_start,))
        move      = self._cr.fetchone()
        return move

    @api.multi
    def query_awal_by_loction_dest_id(self, location_dest_id, date_start):
        self._cr.execute("SELECT rp.name,sw.name,pp.id,pp.default_code,pt.name,pt.list_price,SUM(sm.product_uom_qty) AS total FROM stock_move sm "\
                            "LEFT JOIN product_product pp on pp.id = sm.product_id "\
                            "LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id "\
                            "LEFT JOIN stock_picking sp ON sp.id = sm.picking_id "\
                            "LEFT JOIN res_partner rp ON rp.id = sp.partner_id "\
                            "LEFT JOIN stock_warehouse sw ON sw.id = sm.location_dest_id "\
                            "LEFT JOIN stock_location sl ON sl.id = sw.lot_stock_id "\
                            "WHERE sm.location_dest_id = %s "\
                            "AND sm.state = 'done' "\
                            "AND sm.date < %s "\
                            "GROUP BY rp.name,sw.name,pp.id,pp.default_code,pt.name,pt.list_price" , ( location_dest_id ,date_start,))
        move      = self._cr.fetchall()
        return move

    @api.multi
    def query_jual(self, location_dest_ids, location_id, product_id, date_start, date_end):
        self._cr.execute("SELECT SUM(sm.product_uom_qty) AS total FROM stock_move sm "\
                            "LEFT JOIN product_product pp on pp.id = sm.product_id "\
                            "LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id "\
                            "LEFT JOIN stock_picking sp ON sp.id = sm.picking_id "\
                            "LEFT JOIN res_partner rp ON rp.id = sp.partner_id "\
                            "LEFT JOIN stock_warehouse sw ON sw.id = sm.location_dest_id "\
                            "LEFT JOIN stock_location sl ON sl.id = sw.lot_stock_id "\
                            "WHERE sm.location_dest_id in %s "\
                            "AND sm.location_id = %s "\
                            "AND sm.product_id = %s "\
                            "AND sm.state = 'done' "\
                            "AND (sm.date BETWEEN %s AND %s ) " , ( location_dest_ids , location_id, product_id, date_start, date_end))
        move      = self._cr.fetchone()
        return move

    @api.multi
    def query_retur(self, location_id, location_dest_ids, product_id, date_start, date_end):
        self._cr.execute("SELECT SUM(sm.product_uom_qty) AS total FROM stock_move sm "\
                            "LEFT JOIN product_product pp on pp.id = sm.product_id "\
                            "LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id "\
                            "LEFT JOIN stock_picking sp ON sp.id = sm.picking_id "\
                            "LEFT JOIN res_partner rp ON rp.id = sp.partner_id "\
                            "LEFT JOIN stock_warehouse sw ON sw.id = sm.location_dest_id "\
                            "LEFT JOIN stock_location sl ON sl.id = sw.lot_stock_id "\
                            "WHERE sm.location_id = %s "\
                            "AND sm.location_dest_id not in %s "\
                            "AND sm.product_id = %s "\
                            "AND sm.state = 'done' "\
                            "AND (sm.date BETWEEN %s AND %s ) " , ( location_id, location_dest_ids, product_id, date_start, date_end))
        move      = self._cr.fetchone()
        return move

    @api.multi
    def compute_position_stock(self):
        move_obj = self.env['account.move']
        sql = "delete from position_stock"
        self._cr.execute(sql)
         # customer location
        loc_obj = self.pool.get('stock.location')
        location_dest_ids = loc_obj.search(self._cr,SUPERUSER_ID,[('usage','=','customer')])
        
        location_id = self.warehouse_id.lot_stock_id.id
        move_in = self.query_awal_by_loction_dest_id(location_id, self.date_start)
        if not move_in  :
            raise osv.except_osv(_('Null Query!'), _('Tidak ada data awal untuk ditampilkan !'))
        for line in move_in :
            cust         = line[0]
            warehouse    = line[1]
            prod_id      = line[2]
            kode_brg     = line[3]
            nama_brg     = line[4]
            harga_brg    = line[5]
            ttl_brg      = line[6] or 0.0

            out = 0.0
            move_out = self.query_awal_by_loction_id(location_id, prod_id, self.date_start)
            if move_out :
                out = move_out[0] or 0.0
            ttl_brg = ttl_brg-out
            # Jual
            jual  = 0.0
            jual_exist = self.query_jual(tuple(location_dest_ids), location_id, prod_id, self.date_start, self.date_end)
            if jual_exist :
                jual = jual_exist[0] or 0.0
            # Retur
            retur = 0.0
            retur_exist = self.query_retur(location_id, tuple(location_dest_ids), prod_id, self.date_start, self.date_end)
            if retur_exist :
                retur = retur_exist[0] or 0.0
            # akhir
            akhir = ttl_brg-jual-retur


            sql = """INSERT INTO position_stock(
                        customer,
                        warehouse,
                        kode_buku,
                        judul,
                        harga_satuan,
                        awal,
                        jual,
                        retur,
                        akhir) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               
                        """ % ( "'"+str(cust)+"'",
                                "'"+str(self.warehouse_id.name)+"'",
                                "'"+str(kode_brg)+"'",
                                "'"+str(nama_brg)+"'",
                                "'"+str(harga_brg)+"'",
                                ttl_brg,
                                jual,
                                retur,
                                akhir)

            self._cr.execute(sql)

        view_ref = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'stock_position', 'view_position_stock_tree')
        view_id = view_ref and view_ref[1] or False,     
        return {
            'name' : _('Laporan Sisa Stock Periode '+str(self.date_start)+' - '+str(self.date_end)),
            'view_type': 'form',
            'view_mode': 'tree',            
            'res_model': 'position.stock',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'target': 'current',
            'domain' : "[]",
            'views': [(view_id, 'tree')],
            'context': '{"search_default_warehouse":1}',
            'nodestroy': True,
            }