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
    _name = "sales.report.wizard"

    date_start = fields.Date(string='Date From', required=True, default=time.strftime('%Y-%m-01'))
    date_end = fields.Date(string='Date To', required=True, default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])

    @api.multi
    def query_transactions(self, date_start, date_end):
        self._cr.execute("SELECT aj.type_penjualan,ai.number,rp.name,ai.date_invoice,pp.default_code,pt.name,ail.price_unit,ail.quantity, "\
                            "(ail.quantity*ail.price_unit) AS gross, "\
                            "ail.discount, "\
                            "(ail.quantity*ail.price_unit)*(ail.discount/100) AS discount_value,"\
                            "(ail.quantity*ail.price_unit)-((ail.quantity*ail.price_unit)*(ail.discount/100)) AS nett "\
                            "FROM account_invoice_line ail "\
                            "LEFT JOIN account_invoice ai ON ail.invoice_id = ai.id "\
                            "LEFT JOIN res_partner rp ON ai.partner_id = rp.id "\
                            "LEFT JOIN product_product pp ON ail.product_id = pp.id "\
                            "LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id "\
                            "LEFT JOIN account_journal aj ON ai.journal_id = aj.id "\
                            "WHERE ai.state='open' "\
                            "AND rp.customer = True "\
                            "AND (ai.date_invoice BETWEEN %s AND %s)" , ( date_start , date_end,))

        inv_line      = self._cr.fetchall()
        return inv_line

    @api.multi
    def compute_report_sales(self):
        inv_obj = self.env['account.invoice']
        sql = "delete from sales_report"
        self._cr.execute(sql)
        #import pdb;pdb.set_trace()
        invoice_line = self.query_transactions(self.date_start, self.date_end)
        if not invoice_line  :
            raise osv.except_osv(_('Null Query!'), _('Tidak ada data untuk ditampilkan !'))
        for line in invoice_line :
            if line[0] == 'putus':
                jual = 'Cash'
            elif line[0] == 'showroom' :
                jual = 'Kredit'
            elif line[0] == 'konsinyasi' :
                jual = 'Konsinyasi'
            else :
                jual = 'Cash'
            type_jual   = jual
            inv         = line[1]
            cust        = line[2]
            tgl_inv     = line[3]
            prod_id     = line[4]
            jdl         = "["+line[4]+"] "+line[5]
            unit_price  = line[6] or 0.0
            qty         = line[7] or 0.0
            gross       = line[8] or 0.0
            disc        = line[9] or 0.0
            disc_value  = line[10] or 0.0
            net         = line[11] or 0.0

            sql = """INSERT INTO sales_report( 
                        type_jual,
                        no_inv,
                        customer,
                        tgl_inv,
                        kode_buku,
                        judul,
                        harga_satuan,
                        qty,
                        bruto,
                        disc,
                        disc_nominal,
                        nett) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               
                        """ % ( "'"+str(type_jual)+"'",
                                "'"+str(inv)+"'",
                                "'"+str(cust)+"'",
                                "'"+str(tgl_inv)+"'",
                                "'"+str(prod_id)+"'",
                                "'"+str(jdl)+"'",
                                unit_price,
                                qty,
                                gross,
                                disc,
                                disc_value,
                                net)

            self._cr.execute(sql)

        view_ref = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'sales_report', 'view_sales_report_tree')
        view_id = view_ref and view_ref[1] or False,     
        return {
            'name' : _('Laporan Penjualan '+jual+' Periode '+str(self.date_start)+' - '+str(self.date_end)),
            'view_type': 'form',
            'view_mode': 'tree',            
            'res_model': 'sales.report',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'target': 'current',
            'domain' : "[]",
            'views': [(view_id, 'tree')],
            'context': '{"search_default_type_jual":1}',
            'nodestroy': True,
            }
